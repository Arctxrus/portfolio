#!/usr/bin/env python3
"""Capture pipeline for the three project preview clips (CONCEPT.md section 5).

Build-time tool only. This script ships nothing to the page: it records the
three live demo sites with headed, GPU-backed Chromium (Playwright), then
post-processes each raw take with ffmpeg into the muted, looping VP9 webm plus
poster jpg that index.html already references from media/.

Two stages, either of which can run alone:
  1. capture  - scripted, headed recording of each site to tools/_raw/
  2. process  - ffmpeg into a SEAMLESS LOOP via a tail->head xfade crossfade
                (all three are one continuous slow scroll that returns to its
                start; the closing hold dissolves into the opening hold), native
                1280x720, strip audio, VP9 CRF, a 1280-wide poster jpg from
                frame 0, and a printed loop-seam pixel-diff verification

Usage (run from anywhere, paths are resolved from this file):
  python tools/capture.py                 # capture then process, all three
  python tools/capture.py --only star     # just Until the Last Star
  python tools/capture.py --skip-capture  # re-encode from existing raw takes
  python tools/capture.py --skip-process  # record raw takes only

House rules: UK English, no em dashes. Vanilla toolchain, no runtime deps.
"""

import argparse
import glob
import os
import subprocess
import tempfile
import time

# Resolve repo paths from this file so the script is location independent.
TOOLS_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.dirname(TOOLS_DIR)
MEDIA_DIR = os.path.join(REPO_ROOT, "media")
RAW_DIR = os.path.join(TOOLS_DIR, "_raw")

# Recorded viewport. Client feedback round 1 (change 7, 2026-07-27): record at a
# NATIVE 16:9 viewport (1280x720) so there is no vertical crop. The previous
# 1280x800 take was centre-cropped to 16:9, which dropped 40px off the top and
# chopped the Blackthorn nav pill. At 1280x720 the top of each page is captured
# in full.
REC_W, REC_H = 1280, 720

# Output resolution. Client feedback round 2 (item 3, 2026-07-27): the previous
# 800x450 output looked soft when the panel is shown at ~680px+ and on larger
# screens. The clips are now exported at NATIVE 1280x720 (no downscale from the
# 1280x720 take) and quality-tuned so they stay crisp at full panel size.
OUT_W, OUT_H = 1280, 720

# ANGLE D3D11 on the discrete GPU, so the WebGL demo records its real visuals
# rather than a software fallback. Confirmed renderer: ANGLE NVIDIA RTX 3060.
GPU_ARGS = [
    "--use-angle=d3d11",
    "--enable-gpu-rasterization",
    "--enable-zero-copy",
    "--ignore-gpu-blocklist",
    "--disable-features=CalculateNativeWinOcclusion",
]

# Size budget. Client feedback round 2 (item 3, owner direction): the 300 to
# 500KB per-clip budget is AMENDED. Quality wins: each clip is VP9 CRF quality
# mode (constant quality, not a bitrate target) and kept as small as possible
# while crisp at full panel size. The clips remain lazy-loaded, so the first-load
# budget is untouched. WEBM_*_KB below is informational only (no enforcement).
# Posters are re-exported at 1280 wide, target under ~80KB each (78 gives a
# little margin under the ~80KB budget so the busy star frame is clearly under).
WEBM_MIN_KB, WEBM_MAX_KB = 300, 500   # informational only, not enforced
POSTER_MAX_KB = 78

# VP9 constant-quality (CRF) per clip. Lower is crisper and larger. The brief
# asks for ~32 to 34, tuned by eye on extracted frames. Across 32/33/34 the size
# moved only ~10% (blackthorn 1504/1436/1364KB) and all three were crisp on
# decoded webm frames, so 34 (top of range, smallest) is used per the owner's
# "as small as possible while crisp" direction (see PROGRESS.md round 2).
DEFAULT_CRF = 34

# Client feedback round 4 (item 5): the scroll-scrub is retired, so the dense
# keyframe interval (round 3's -g 12, needed only for reverse seeking) is no
# longer required. Back to a normal GOP: -g 60 at 30fps is a keyframe every 2s,
# which keeps the muted autoplay loops small again. See vp9_args.
KEYFRAME_INTERVAL = 60

# Client feedback round 4 (item 3, owner amendment): every clip is a one-way slow
# scroll that returns to its start, so a hard loop cut would jump. Each is
# post-processed into a seamless loop by dissolving its tail (the closing hold)
# into its head (the opening hold) with an xfade crossfade of this length; the
# shipped clip then runs (base clip length minus CROSSFADE_S). Both endpoints are
# the same opening composition, so the dissolve is clean (see choose_head_ss).
CROSSFADE_S = 0.8
FPS = 30

# Scrollbar suppression (item 4). The owner dislikes the demo sites' scrollbar in
# the captures. This CSS is injected into each page BEFORE the keeper so the
# recorded frames carry no scrollbar. Note: hiding the scrollbar reclaims its
# gutter width; the star (cosmic-dawn) take is checked after injection in case
# the WebGL scene sizes anything off the scrollbar width.
NO_SCROLLBAR_CSS = (
    "html { scrollbar-width: none !important; -ms-overflow-style: none !important; }"
    "::-webkit-scrollbar { display: none !important; width: 0 !important; height: 0 !important; }"
)

# The base clip ends near the tail of the raw take (its closing hold at the tour
# start), less a small margin that drops any frozen final frame. Robust against
# Playwright recording a timeline shorter than wall-clock (its tail frames lag).
TAIL_MARGIN_S = 0.10

# Round 4 verifier FAIL fix. A crossfade only reads clean when the two blended
# endpoints match. The tours ended on the reviews/bento, so dissolving that into
# the opening cover/hero gave a legible double exposure (peak diffs 144 and 46).
# Fix: every tour now glides back to its START and holds a closing composition,
# and demo heros are warmed into their settled BASE state before the keeper (a
# scroll excursion and back; see capture_one), so the opening and closing frames
# match. These takes are HEAD-anchored: choose_head_ss scans the region around the
# keeper start for the CROSSFADE_S window that is most static and best matches the
# settled closing frame, and the base clip runs from there to the closing hold.

# Per project capture plan (owner amendment, round 4). ALL THREE clips are now a
# single continuous, even, SLOW scroll down the page (no section glides, no anchor
# stops, no mid-tour holds), then a brisk glide back to the start and a closing
# hold on the same opening composition, crossfaded (0.8s) into the opening hold so
# the loop is seamless. "tour" is that plan: open on `from`, drift slowly and
# evenly (near-linear) to `to` over tour_dur_ms, glide back over return_dur_ms,
# hold. A `from`/`to` given as {"t": frac} is a cosmic-dawn timeline fraction
# resolved to pixels at capture time; a plain number is a pixel offset. All three
# are head-anchored crossfades (choose_head_ss) so both dissolve endpoints match.
PROJECTS = [
    {
        "name": "blackthorn",
        "url": "https://arctxrus.github.io/blackthorn-demo/",
        "out": "blackthorn-preview",
        "poster_out": "blackthorn-poster",
        "verify_nvidia": False,
        "warmup": True,        # hero has a one-time load-in animation; warm to base
        # The hero photo zooms in and the intro badges fade over several seconds on
        # first load; wait it out at the top so the opening matches the settled
        # closing (else the crossfade catches the load-in mid-animation).
        "settle_ms": 4000,
        # One slow even scroll cover -> down the page, then back to the cover.
        "tour": {"from": 0, "to": 5200, "open_hold_ms": 1000,
                 "tour_dur_ms": 13000, "return_dur_ms": 1700, "close_hold_ms": 1300},
    },
    {
        "name": "barker",
        "url": "https://arctxrus.github.io/barker-bloom-demo/",
        "out": "barker-bloom-preview",
        "poster_out": "barker-bloom-poster",
        "verify_nvidia": False,
        "warmup": True,
        "settle_ms": 3500,     # let the hero load-in settle before the take
        # One slow even scroll hero -> pricing bento, then back to the hero.
        "tour": {"from": 0, "to": 1150, "open_hold_ms": 1000,
                 "tour_dur_ms": 12000, "return_dur_ms": 1700, "close_hold_ms": 1300},
    },
    {
        "name": "star",
        # ?tier=2 forces the T2 quality tier so the real WebGL scene renders (not
        # the sprite fallback). Owner amendment (round 4): the star is a bright
        # SCROLLING capture, not the near-black fixed black-hole shot (poster
        # luminance ~35). It waits 10s after load, then scrolls slowly through a
        # NARROW window of THE AFTERGLOW ("the fog lifts", timeline t 0.13 to 0.17):
        # a warm plasma nebula that is the brightest region in the scene. Probed
        # (fine grid + a slow-scroll pass): mean luminance stays 69 -> 50 across the
        # whole span and NEVER drops below ~50, with visible plasma motion (frame
        # motion ~2.8 to 4.7, not a static hold). The wider t 0.15 to 0.21 window
        # used earlier scrolled on into a dark trough (~19 at t 0.19+) mid-clip, the
        # round-4b FAIL; this narrower window stays inside the bright material.
        # Frame 0 (the poster) is the bright nebula at t 0.13 (~69). Avoids the dark
        # ages (t 0.22+) and the near-black long night. Camera parallax DROPPED
        # (fought the scroll; the crossfade carries the loop); no crop. The cosmos is
        # inherently dark, so the mean caps below the ~80 aim; ~69 poster / ~50 floor
        # is the brightest sustainable span.
        "url": "https://arctxrus.github.io/cosmic-dawn/?tier=2",
        "out": "until-the-last-star-preview",
        "poster_out": "until-the-last-star-poster",
        "verify_nvidia": True,
        "warmup": False,               # WebGL scene, no load-in intro to warm off
        "extra_load_wait_ms": 10000,   # owner: 10s after load before the take
        "settle_ms": 2500,             # the afterglow brightens to ~69 over ~1.5s
        "tour": {"from": {"t": 0.13}, "to": {"t": 0.17}, "open_hold_ms": 1200,
                 "tour_dur_ms": 13000, "return_dur_ms": 1700, "close_hold_ms": 1500},
    },
]

# Scroll run inside the page via rAF (per-frame smooth, no manual driving, no
# mouse). The slow tour is near-linear (even, constant-ish speed, linear=true);
# the brisk return glide is easeInOutQuad so it does not jerk at the ends.
EASE_SCROLL_JS = """
async ({toY, duration, linear}) => {
  const startY = window.scrollY;
  const dist = toY - startY;
  const t0 = performance.now();
  const easeInOut = t => (t < 0.5 ? 2 * t * t : 1 - Math.pow(-2 * t + 2, 2) / 2);
  const ease = linear ? (t => t) : easeInOut;
  return new Promise(resolve => {
    function frame(now) {
      const t = Math.min(1, (now - t0) / duration);
      window.scrollTo(0, startY + dist * ease(t));
      if (t < 1) requestAnimationFrame(frame);
      else resolve();
    }
    requestAnimationFrame(frame);
  });
}
"""

# Read the unmasked WebGL renderer from inside the recording context.
RENDERER_JS = """
() => {
  const c = document.createElement('canvas');
  const gl = c.getContext('webgl2') || c.getContext('webgl');
  if (!gl) return 'no-webgl';
  const dbg = gl.getExtension('WEBGL_debug_renderer_info');
  return dbg ? gl.getParameter(dbg.UNMASKED_RENDERER_WEBGL) : 'no-debug-ext';
}
"""

# Defensive first-run overlay dismissal. Probing found no blocking overlays on
# any of the three sites, so this is belt and braces: press Escape, then click
# anything that looks like an accept or dismiss control if one appears.
DISMISS_SELECTORS = [
    "button[aria-label*='close' i]",
    "button[aria-label*='dismiss' i]",
    "[class*='overlay'] button",
    "[class*='intro'] button",
    "button:has-text('Accept')",
    "button:has-text('Got it')",
    "button:has-text('Enter')",
    "button:has-text('Begin')",
]


def log(msg):
    print(msg, flush=True)


def inject_no_scrollbar(page):
    """Item 4: hide the demo site's scrollbar before recording so the captured
    frames carry none. Injected as a page style tag after load; belt and braces,
    also re-added on any same-document navigation via an init script is not
    needed here since the takes do not navigate."""
    try:
        page.add_style_tag(content=NO_SCROLLBAR_CSS)
    except Exception as exc:
        log(f"    warning: could not inject no-scrollbar CSS: {exc}")


def dismiss_overlays(page):
    try:
        page.keyboard.press("Escape")
    except Exception:
        pass
    for sel in DISMISS_SELECTORS:
        try:
            el = page.query_selector(sel)
            if el and el.is_visible():
                el.click(timeout=1000)
                page.wait_for_timeout(200)
        except Exception:
            pass


def capture_one(project):
    """Record one scripted take to tools/_raw/ and return its path."""
    from playwright.sync_api import sync_playwright

    os.makedirs(RAW_DIR, exist_ok=True)
    log(f"[{project['name']}] launching headed Chromium with GPU args")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, args=GPU_ARGS)
        t_ctx = time.monotonic()
        context = browser.new_context(
            viewport={"width": REC_W, "height": REC_H},
            record_video_dir=RAW_DIR,
            record_video_size={"width": REC_W, "height": REC_H},
        )
        page = context.new_page()
        page.goto(project["url"], wait_until="networkidle", timeout=90000)

        # Wait for fonts and a settled network before touching anything.
        try:
            page.evaluate("document.fonts && document.fonts.ready")
            page.wait_for_function("document.fonts ? document.fonts.status === 'loaded' : true", timeout=15000)
        except Exception:
            pass
        page.wait_for_load_state("networkidle", timeout=30000)

        # Cosmic-dawn shows a preloader that must clear before the scene renders.
        # For a site with no preloader, a detached-state wait resolves at once.
        try:
            page.wait_for_selector("#preloader", state="detached", timeout=20000)
        except Exception:
            pass

        dismiss_overlays(page)

        # Item 4: suppress the scrollbar before the keeper so no frame shows it.
        inject_no_scrollbar(page)

        if project["verify_nvidia"]:
            renderer = page.evaluate(RENDERER_JS)
            log(f"[{project['name']}] renderer: {renderer}")
            if "NVIDIA" not in renderer.upper():
                context.close()
                browser.close()
                raise RuntimeError(
                    f"[{project['name']}] renderer is not the NVIDIA GPU "
                    f"({renderer!r}); refusing the take (software fallback)."
                )

        # Owner amendment (round 4): wait extra after load so a heavy WebGL scene
        # is fully initialised before the take (the star waits 10s at the top).
        if project.get("extra_load_wait_ms"):
            page.wait_for_timeout(project["extra_load_wait_ms"])

        tour = project["tour"]

        def to_px(v):
            # Pixel offset, or a cosmic-dawn timeline fraction {"t": frac}.
            if isinstance(v, dict) and "t" in v:
                return page.evaluate(
                    "t => t * (document.documentElement.scrollHeight - window.innerHeight)",
                    v["t"],
                )
            return v

        from_y = to_px(tour["from"])
        to_y = to_px(tour["to"])

        # Open on the tour start and let it settle.
        page.evaluate("y => window.scrollTo(0, y)", from_y)
        page.wait_for_timeout(project["settle_ms"])

        # Round 4 verifier fix. Demo heros play a one-time load-in animation that is
        # still running through the opening hold, so the opening composition did not
        # match the closing one (reached via scroll-return, base state), giving a
        # legible crossfade double exposure. Warm the hero into its settled base
        # state with a quick scroll excursion and back before the keeper. WebGL
        # scenes have no such load-in, so they skip this.
        if project.get("warmup"):
            page.evaluate(EASE_SCROLL_JS, {"toY": from_y + 700, "duration": 500})
            page.evaluate(EASE_SCROLL_JS, {"toY": from_y, "duration": 500})
            page.wait_for_timeout(1200)

        # Keeper begins now. Persist the offset for head-anchored processing.
        keeper_offset_s = time.monotonic() - t_ctx
        log(f"[{project['name']}] keeper starts at ~{keeper_offset_s:.2f}s into the take")

        # ONE continuous, even, slow scroll down the page, then a brisk glide back
        # to the start and a closing hold on the same opening composition. The
        # crossfade folds that closing hold into the opening hold for a clean loop.
        page.wait_for_timeout(tour["open_hold_ms"])
        page.evaluate(EASE_SCROLL_JS,
                      {"toY": to_y, "duration": tour["tour_dur_ms"], "linear": True})
        page.evaluate(EASE_SCROLL_JS,
                      {"toY": from_y, "duration": tour["return_dur_ms"]})
        page.wait_for_timeout(tour["close_hold_ms"])

        page.wait_for_timeout(150)  # let the final frames flush
        video = page.video
        context.close()  # finalises the webm
        raw_path = video.path()
        browser.close()

    # Give the recording a stable, per-project name.
    named = os.path.join(RAW_DIR, project["name"] + "-raw.webm")
    if os.path.exists(named):
        os.remove(named)
    os.replace(raw_path, named)
    # Persist the keeper offset so head-anchored processing (return-to-top loops)
    # can start the base clip inside the opening settle at scroll 0 (static hero).
    with open(named + ".offset", "w") as fh:
        fh.write(f"{keeper_offset_s:.3f}")
    log(f"[{project['name']}] raw take: {named}  ({kb(named):.0f}KB, "
        f"keeper offset {keeper_offset_s:.2f}s)")
    return named


def kb(path):
    return os.path.getsize(path) / 1024.0


def run(cmd):
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def probe_duration(path):
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "default=noprint_wrappers=1:nokey=1", path],
        check=True, capture_output=True, text=True,
    )
    return float(out.stdout.strip())


def vfilter(project=None):
    # The take is native 16:9 (1280x720) and the output is native 1280x720 (no
    # downscale), so the clip stays crisp at full panel size. A straight scale
    # keeps the full frame; object-fit: cover in the panel handles the mobile 2/1
    # ratio. (project is accepted for signature symmetry; no per-project crop.)
    return f"scale={OUT_W}:{OUT_H}"


def vp9_args(crf):
    """Shared VP9 constant-quality (CRF) output args. Client feedback round 4
    (item 5): the scroll-scrub is retired, so the GOP is back to normal (-g 60, a
    keyframe every 2s, KEYFRAME_INTERVAL), which keeps the muted autoplay loops
    small again. Audio stripped, 30fps, -b:v 0 selects true constant-quality VP9;
    alt-ref kept for compression."""
    return [
        "-an", "-r", str(FPS),
        "-c:v", "libvpx-vp9", "-crf", str(crf), "-b:v", "0",
        "-deadline", "good", "-cpu-used", "1",
        "-auto-alt-ref", "1", "-lag-in-frames", "25",
        "-g", str(KEYFRAME_INTERVAL), "-row-mt", "1",
    ]


def encode_crossfade(raw, out, ss, base_dur, crf, cross, project=None):
    """Client feedback round 4 (item 3): make a mathematically seamless loop by
    dissolving the clip's tail into its head. Standard xfade technique: split the
    base clip of length D into hold=[0, D-C] and end=[D-C, D], then xfade `end`
    over `hold` at offset 0 for duration C. Output length = D - C. The loop seam
    (output last frame -> output first frame) maps to input[(D-C)-] -> input[D-C],
    two ADJACENT source frames, so it is continuous; the first C seconds are the
    intended tail->head dissolve. One VP9 encode straight from the raw take."""
    d, c = base_dur, cross
    spatial = vfilter(project)
    fc = (
        f"[0:v]{spatial},fps={FPS},format=yuv420p,setpts=PTS-STARTPTS,split[a][b];"
        f"[a]trim=0:{d - c:.3f},setpts=PTS-STARTPTS[hold];"
        f"[b]trim={d - c:.3f}:{d:.3f},setpts=PTS-STARTPTS[end];"
        f"[end][hold]xfade=transition=fade:duration={c:.3f}:offset=0[v]"
    )
    cmd = (
        ["ffmpeg", "-y", "-ss", f"{ss:.3f}", "-t", f"{d:.3f}", "-i", raw,
         "-filter_complex", fc, "-map", "[v]"]
        + vp9_args(crf) + [out]
    )
    run(cmd)
    log(f"    VP9 crf {crf} crossfade {c:.2f}s: {kb(out):.0f}KB "
        f"({OUT_W}x{OUT_H}, loop {d - c:.2f}s)")


def seam_first_last_diff(out):
    """Verification (items 3 and 6): mean absolute pixel diff (0..255 per channel)
    between the OUTPUT clip's first and last frame. For a seamless loop these are
    near-adjacent in the source, so a slow clip reads close to zero; a large value
    means a visible jump at the loop point."""
    import numpy as np
    from PIL import Image
    with tempfile.TemporaryDirectory() as td:
        first_png = os.path.join(td, "first.png")
        last_png = os.path.join(td, "last.png")
        run(["ffmpeg", "-y", "-i", out, "-frames:v", "1", first_png])
        # -update over the last 0.3s leaves the true final frame in last_png.
        run(["ffmpeg", "-y", "-sseof", "-0.3", "-i", out,
             "-update", "1", "-frames:v", "1000", last_png])
        a = np.asarray(Image.open(first_png).convert("RGB"), dtype=np.int16)
        b = np.asarray(Image.open(last_png).convert("RGB"), dtype=np.int16)
    return float(np.mean(np.abs(a - b)))


def choose_head_ss(raw, keeper_offset, spatial, raw_dur):
    """Round 4 verifier fix. Pick the crossfade HEAD start: the CROSSFADE_S window
    in the FIRST part of the take that best matches the settled closing hold (the
    tail) and is calm. CONTENT-BASED, not reliant on the recorded video timeline
    aligning with the wall-clock keeper offset (it does not: Playwright records a
    non-linear timeline, so the offset only seeds a wide search). The settled
    opening composition matches the closing and is calm; load-in and tour frames do
    not match. Returns ss (seconds)."""
    import numpy as np
    from PIL import Image
    win = int(round(CROSSFADE_S * FPS))                       # 24 frames = 0.8s
    # Wide search over the first part of the take: load + settle + warmup + opening
    # hold + a little into the tour. Generous so it still contains the opening hold
    # even when the offset is off by a couple of seconds.
    s0 = 1.0
    s1 = min(raw_dur * 0.5, keeper_offset + 4.0)
    nreg = int(round((s1 - s0) * FPS)) + win + 2
    with tempfile.TemporaryDirectory() as td:
        patt = os.path.join(td, "h_%04d.png")
        run(["ffmpeg", "-y", "-ss", f"{s0:.3f}", "-i", raw,
             "-vf", f"{spatial},fps={FPS}", "-frames:v", str(nreg),
             "-start_number", "0", patt])
        files = sorted(glob.glob(os.path.join(td, "h_*.png")))
        reg = [np.asarray(Image.open(f).convert("RGB").resize((320, 180)), dtype=np.int16)
               for f in files]
        tref = os.path.join(td, "tail.png")
        run(["ffmpeg", "-y", "-ss", f"{raw_dur - TAIL_MARGIN_S - 0.4:.3f}", "-i", raw,
             "-vf", spatial, "-frames:v", "1", tref])
        tail = np.asarray(Image.open(tref).convert("RGB").resize((320, 180)), dtype=np.int16)
    best_i, best_score = 0, None
    for i in range(0, len(reg) - win):
        internal = max(float(np.mean(np.abs(reg[i + k] - reg[i + k + 1])))
                       for k in range(win))              # peak per-frame motion in window
        match = float(np.mean(np.abs(reg[i + win // 2] - tail)))   # match to closing
        # Match-dominant: locate the settled opening that looks like the closing,
        # with a light calmness tiebreaker.
        score = match + 0.4 * internal
        if best_score is None or score < best_score:
            best_i, best_score = i, score
    ss = s0 + best_i / FPS
    log(f"    head-anchor scan: ss={ss:.2f}s (region {s0:.2f}-{s1:.2f}s, "
        f"match-score {best_score:.2f})")
    return ss


def make_poster(webm, poster):
    """Frame 0 of the processed clip as a jpg, 1280 wide, quality tuned under the
    ~80KB budget (item 5)."""
    chosen = None
    for q in (3, 4, 5, 6, 8, 10, 12, 15):
        run([
            "ffmpeg", "-y", "-i", webm, "-frames:v", "1",
            "-q:v", str(q), "-vf", f"scale={OUT_W}:{OUT_H}", poster,
        ])
        size = kb(poster)
        chosen = (q, size)
        if size <= POSTER_MAX_KB:
            break
    log(f"    poster q={chosen[0]}: {chosen[1]:.0f}KB (1280 wide)")
    return chosen


def process_one(project):
    os.makedirs(MEDIA_DIR, exist_ok=True)
    raw = os.path.join(RAW_DIR, project["name"] + "-raw.webm")
    if not os.path.exists(raw):
        raise FileNotFoundError(f"[{project['name']}] no raw take at {raw}; run capture first")

    raw_dur = probe_duration(raw)
    out = os.path.join(MEDIA_DIR, project["out"] + ".webm")
    poster = os.path.join(MEDIA_DIR, project["poster_out"] + ".jpg")
    crf = project.get("crf", DEFAULT_CRF)

    # All three clips are head-anchored crossfade loops (owner amendment, round 4):
    # the base clip starts at the opening composition (choose_head_ss picks the
    # window best matching the settled closing hold using the persisted keeper
    # offset) and runs to the closing hold, so BOTH crossfade endpoints are the same
    # composition and the dissolve reads clean. Length is whatever the tour recorded
    # (kept inside ~10 to 20s by the scripted durations), not a fixed clip_len_s.
    off_file = raw + ".offset"
    if not os.path.exists(off_file):
        raise FileNotFoundError(
            f"[{project['name']}] no {off_file}; re-capture so the keeper offset "
            f"is persisted for head-anchored processing")
    with open(off_file) as fh:
        keeper_offset = float(fh.read().strip())
    ss = choose_head_ss(raw, keeper_offset, vfilter(project), raw_dur)
    base = raw_dur - ss - TAIL_MARGIN_S
    log(f"[{project['name']}] crossfade loop (raw {raw_dur:.2f}s, ss={ss:.2f}s, "
        f"base={base:.2f}s -> loop {base - CROSSFADE_S:.2f}s, "
        f"cross={CROSSFADE_S:.2f}s, crf {crf})")
    encode_crossfade(raw, out, ss, base, crf, CROSSFADE_S, project)
    seam = seam_first_last_diff(out)
    make_poster(out, poster)
    log(f"[{project['name']}] done: {os.path.basename(out)} {kb(out):.0f}KB, "
        f"{os.path.basename(poster)} {kb(poster):.0f}KB, "
        f"crossfade seam first-vs-last {seam:.2f}")


def main():
    ap = argparse.ArgumentParser(description="Capture and process the project preview clips.")
    ap.add_argument("--only", choices=[p["name"] for p in PROJECTS], help="single project")
    ap.add_argument("--skip-capture", action="store_true", help="reuse existing raw takes")
    ap.add_argument("--skip-process", action="store_true", help="record raw takes only")
    args = ap.parse_args()

    projects = [p for p in PROJECTS if not args.only or p["name"] == args.only]
    for project in projects:
        if not args.skip_capture:
            capture_one(project)
        if not args.skip_process:
            process_one(project)

    log("all done")


if __name__ == "__main__":
    main()
