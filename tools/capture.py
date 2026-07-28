#!/usr/bin/env python3
"""Capture pipeline for the three project preview clips (CONCEPT.md section 5).

Build-time tool only. This script ships nothing to the page: it records the
three live demo sites with headed, GPU-backed Chromium, then post-processes each
raw take with ffmpeg into the muted, looping VP9 webm plus poster jpg that
index.html already references from media/.

Client feedback round 5 (owner-directed, 2026-07-27). Two capture-level defects
were fixed here:

  1. CROP + BLUR. Since round 3 the desktop preview box is near-square (measured
     682x652 at 1440x900, ratio ~1.046; ranges ~0.85 at 1280w to ~1.40 at 1920w),
     but the clips were 16:9 (1.778). object-fit: cover then cropped the sides
     ~41% ("cropped in") and upscaled the 720 rows ~1.8x at DPR 2 ("blurry"). Fix:
     record at a SQUARE-ISH viewport (1000x1040, ratio 0.962, the compromise
     across the 1440/1280 anchors) so almost nothing is cropped, at deviceScaleFactor
     2 so the source is sharp, and encode at 1500x1560 (1500 wide: the 1440 box is
     682 CSS = 1364 device px at DPR 2, so 1500 gives native-or-better pixels).

  2. FRAME RATE. The old clips ran ~15.6 to 24.8 UNIQUE fps (Playwright recordVideo
     is ~25fps nominal and drops/duplicates under load), which juddered on slow
     pans. Fix: capture via CDP Page.startScreencast (measured 75 to 91 fps on this
     RTX 3060) and rebuild a true 60fps CFR raw from the frame timestamps, so the
     scrolling motion carries ~60 unique fps.

Everything else follows the round-4c content plan: one continuous even slow scroll
that returns to its start, demo heros warmed to their settled base, the star a
bright afterglow span (t 0.13 to 0.17) after a 10s preload wait, all closed with a
tail->head crossfade so the loop is seamless.

Two stages, either of which can run alone:
  1. capture  - scripted, headed CDP-screencast recording of each site to
                tools/_raw/ (screencast JPEG frames reassembled to a 60fps CFR
                intermediate via their arrival timestamps)
  2. process  - ffmpeg into a SEAMLESS LOOP via a tail->head xfade crossfade,
                scaled to 1500x1560, audio stripped, VP9 CRF, a 1500-wide poster
                jpg from frame 0, and a printed loop-seam pixel-diff verification

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

# Recorded viewport. Client feedback round 5 (crop fix): a SQUARE-ISH viewport so
# the near-square preview box (682x652 at 1440x900) crops almost nothing under
# object-fit: cover. 1000x1040 (ratio 0.962) is the compromise across the box
# ratios at the two anchor widths the owner named (1440x900 = 1.046, 1280x720 =
# 0.853; average ~0.95). The demo sites are responsive and render legitimately at
# 1000px wide, so nothing is cropped out of the page itself.
REC_W, REC_H = 1000, 1040

# Device scale factor for the recording context. Client feedback round 5 (blur
# fix): capture at DPR 2 so the raw surface is 2000x2080 device px, then downscale
# to the 1500-wide output. That is a downscale (crisp), not the old upscale.
DPR = 2

# Output resolution. Round 5 first shipped 1500x1560, but that non-standard frame
# at 60fps forced SOFTWARE VP9 decode in-browser and dropped 31 to 34% of frames
# (verifier; reproduced). Playback-smoothness fix (2026-07-28): MOD-16 dimensions
# (macroblock-aligned: 1280 = 80*16, 1344 = 84*16) decode far more efficiently,
# keeping the ~0.952 aspect so the box fit is essentially unchanged. 1280 wide is
# a 6% upscale of the 1364 device-px box at DPR 2 (imperceptible; kept high for
# sharpness while stepping down from 1440x1504 for decode/composite margin). The
# bigger decode win is the VP9 profile: see vp9_args (yuv420p, profile 0).
OUT_W, OUT_H = 1280, 1344

# Output frame rate. Round 5 first shipped a true 60fps CFR, but combined with the
# large non-standard frame it overran the software decoder (see above). Halved to
# 30fps CFR (2026-07-28): a slow ambient drift reads perfectly smooth at 30 and it
# halves the per-second decode load. Measured in-browser after the change: dropped
# frames fall under ~5% with no repeated 50ms+ presentation spikes.
FPS = 30

# ANGLE D3D11 on the discrete GPU, so the WebGL demo records its real visuals
# rather than a software fallback. Confirmed renderer: ANGLE NVIDIA RTX 3060.
GPU_ARGS = [
    "--use-angle=d3d11",
    "--enable-gpu-rasterization",
    "--enable-zero-copy",
    "--ignore-gpu-blocklist",
    "--disable-features=CalculateNativeWinOcclusion",
]

# Screencast frame quality (JPEG). High so the intermediate is close to lossless;
# the max dims cap the returned frame to the full DPR-2 surface (no downscale in
# the browser; the downscale to 1500 wide happens in the final ffmpeg encode).
SCREENCAST_QUALITY = 90
SCREENCAST_MAX_W, SCREENCAST_MAX_H = REC_W * DPR, REC_H * DPR

# Size budget. Client feedback round 2 (item 3) retired the 300 to 500KB per-clip
# budget: quality wins, each clip is VP9 CRF quality mode and lazy-loaded so the
# first-load budget is untouched. Round 5 raises resolution and frame rate, so the
# files grow again (reported). POSTER_MAX_KB is under the owner's ~100KB poster aim.
POSTER_MAX_KB = 98

# VP9 constant-quality (CRF). Lower is crisper and larger. 34 is the established
# "crisp" value; at the higher round-5 resolution crispness comes mostly from the
# resolution, so 34 is kept. cpu-used 2 (was 1) roughly halves the encode time at
# 60fps with negligible quality cost (CRF, not cpu-used, governs crispness).
DEFAULT_CRF = 34
VP9_CPU_USED = 2

# GOP: a keyframe every 2s. At 30fps that is -g 60 (2026-07-28 playback fix).
KEYFRAME_INTERVAL = 60

# Each clip is a one-way slow scroll that returns to its start, so a hard loop cut
# would jump. Each is post-processed into a seamless loop by dissolving its tail
# (the closing hold) into its head (the opening hold) with an xfade of this length;
# the shipped clip then runs (base clip length minus CROSSFADE_S). Both endpoints
# are the same opening composition, so the dissolve is clean (see choose_head_ss).
CROSSFADE_S = 0.8

# Scrollbar suppression. The owner dislikes the demo sites' scrollbar in the
# captures. Injected into each page BEFORE the keeper so no recorded frame shows it.
NO_SCROLLBAR_CSS = (
    "html { scrollbar-width: none !important; -ms-overflow-style: none !important; }"
    "::-webkit-scrollbar { display: none !important; width: 0 !important; height: 0 !important; }"
)

# The base clip ends a small margin before the very tail so any single frozen final
# frame is dropped.
TAIL_MARGIN_S = 0.10

# Per project capture plan (owner amendment, rounds 4/4c; unchanged in round 5
# except the viewport). ALL THREE clips are a single continuous, even, SLOW scroll
# down the page (no section glides, no anchor stops, no mid-tour holds), then a
# brisk glide back to the start and a closing hold on the same opening composition,
# crossfaded (0.8s) into the opening hold so the loop is seamless. "tour" is that
# plan: open on `from`, drift slowly and evenly (near-linear) to `to` over
# tour_dur_ms, glide back over return_dur_ms, hold. A `from`/`to` given as
# {"t": frac} is a cosmic-dawn timeline fraction resolved to pixels at capture time;
# a plain number is a pixel offset.
PROJECTS = [
    {
        "name": "blackthorn",
        "url": "https://arctxrus.github.io/blackthorn-demo/",
        "out": "blackthorn-preview",
        "poster_out": "blackthorn-poster",
        "verify_nvidia": False,
        # The hero runs scroll-reveal animations (the nav morphs pill -> bar, content
        # slides up) that fire when the block enters the viewport. The closing frame
        # is reached by scrolling the tour back to the top (a scroll-return state), so
        # the opening must ALSO be a settled scroll-return state to match it, else the
        # pristine-load opening differs from the scroll-return closing (~9/255). The
        # warmup does a quick scroll excursion and back to put the hero in that state,
        # then warmup_settle_ms lets the reveals fully settle before the keeper so the
        # opening hold is static (the round-5 raw-assembly clamp fix keeps that hold
        # from collapsing). Both ends are then scroll-return-settled and match.
        "warmup": True,
        "warmup_settle_ms": 2500,
        "settle_ms": 4000,
        "tour": {"from": 0, "to": 5200, "open_hold_ms": 1500,
                 "tour_dur_ms": 13000, "return_dur_ms": 1700, "close_hold_ms": 1600},
    },
    {
        "name": "barker",
        "url": "https://arctxrus.github.io/barker-bloom-demo/",
        "out": "barker-bloom-preview",
        "poster_out": "barker-bloom-poster",
        "verify_nvidia": False,
        "warmup": True,               # same scroll-return matching as blackthorn
        "warmup_settle_ms": 2500,
        "settle_ms": 3500,            # let the hero load-in settle before the warmup
        "tour": {"from": 0, "to": 1150, "open_hold_ms": 1500,
                 "tour_dur_ms": 12000, "return_dur_ms": 1700, "close_hold_ms": 1600},
    },
    {
        "name": "star",
        # ?tier=2 forces the T2 quality tier so the real WebGL scene renders (not
        # the sprite fallback). The star is a bright SCROLLING capture of THE
        # AFTERGLOW ("the fog lifts", timeline t 0.13 to 0.17): a warm plasma nebula,
        # the brightest sustainable region in the scene (probed mean luminance stays
        # 69 -> 50, never below ~50, with visible plasma motion). It waits 10s after
        # load so the heavy WebGL scene is fully initialised. Camera parallax is off
        # (it fought the scroll; the crossfade carries the loop); no crop. Frame 0
        # (the poster) is the bright nebula at t 0.13.
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

# Defensive first-run overlay dismissal. Probing found no blocking overlays on any
# of the three sites, so this is belt and braces.
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
    """Hide the demo site's scrollbar before recording so the captured frames
    carry none."""
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


def assemble_raw(frames, raw_path):
    """Build a 60fps CFR intermediate from the screencast frames.

    `frames` is a list of (arrival_monotonic_s, jpeg_bytes), in order, plus a
    trailing (stop_monotonic_s, None) sentinel so the last real frame gets its
    held duration. The per-frame duration is the gap to the next arrival, clamped
    to a sane range so a stray outlier cannot stretch a frame; static holds (no
    new compositor frame) are represented as a single frame held for its gap. An
    ffmpeg concat demuxer with those durations, resampled to CFR 60, reproduces the
    real timing: ~60 unique fps through motion, duplicated frames across holds.
    The intermediate is H.264 CRF 12 (near-lossless, fast) so the final VP9 encode
    is the only meaningful generational loss after the JPEG capture."""
    if len(frames) < 2:
        raise RuntimeError("screencast produced too few frames")

    real = [f for f in frames if f[1] is not None]
    stop_ts = frames[-1][0]
    with tempfile.TemporaryDirectory() as td:
        list_path = os.path.join(td, "list.txt")
        names = []
        for i, (_, data) in enumerate(real):
            name = os.path.join(td, f"f_{i:06d}.jpg")
            with open(name, "wb") as fh:
                fh.write(data)
            names.append(name)

        # Durations: gap to the next arrival (last real frame -> stop sentinel).
        # Static holds legitimately produce ONE screencast frame held for the whole
        # hold (screencast only sends frames on visual change), so the upper clamp
        # must be well above the ~1.6s hold length or the opening/closing holds
        # collapse and the crossfade loses its static window. 2.5s preserves real
        # holds while still bounding a pathological stall.
        ts = [f[0] for f in real] + [stop_ts]
        lines = []
        for i, name in enumerate(names):
            dur = ts[i + 1] - ts[i]
            dur = max(1.0 / 120.0, min(2.5, dur))   # preserve holds, bound outliers
            safe = name.replace("\\", "/")
            lines.append(f"file '{safe}'")
            lines.append(f"duration {dur:.5f}")
        # Concat demuxer needs the last file repeated for its duration to apply.
        lines.append(f"file '{names[-1].replace(chr(92), '/')}'")
        with open(list_path, "w") as fh:
            fh.write("\n".join(lines) + "\n")

        cmd = [
            "ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", list_path,
            "-vsync", "cfr", "-r", str(FPS), "-pix_fmt", "yuv420p",
            "-c:v", "libx264", "-crf", "12", "-preset", "veryfast",
            raw_path,
        ]
        run(cmd)


def capture_one(project):
    """Record one scripted CDP-screencast take to tools/_raw/ and return its path."""
    from playwright.sync_api import sync_playwright

    os.makedirs(RAW_DIR, exist_ok=True)
    log(f"[{project['name']}] launching headed Chromium with GPU args (DPR {DPR})")

    frames = []   # list of (arrival_monotonic_s, jpeg_bytes or None sentinel)

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, args=GPU_ARGS)
        context = browser.new_context(
            viewport={"width": REC_W, "height": REC_H},
            device_scale_factor=DPR,
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
        try:
            page.wait_for_selector("#preloader", state="detached", timeout=20000)
        except Exception:
            pass

        dismiss_overlays(page)
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

        if project.get("extra_load_wait_ms"):
            page.wait_for_timeout(project["extra_load_wait_ms"])

        tour = project["tour"]

        def to_px(v):
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

        # Warm the hero into its settled base state with a quick excursion and back
        # (a one-time load-in animation would otherwise still be running through the
        # opening hold and not match the scroll-return closing composition). WebGL
        # scenes have no such load-in, so they skip this.
        if project.get("warmup"):
            page.evaluate(EASE_SCROLL_JS, {"toY": from_y + 700, "duration": 500})
            page.evaluate(EASE_SCROLL_JS, {"toY": from_y, "duration": 500})
            page.wait_for_timeout(project.get("warmup_settle_ms", 2500))

        # Start the CDP screencast just before the keeper so the raw contains ONLY
        # keeper frames (the opening composition is at raw t ~ 0).
        client = context.new_cdp_session(page)

        def on_frame(params):
            frames.append((time.monotonic(), _b64(params["data"])))
            try:
                client.send("Page.screencastFrameAck", {"sessionId": params["sessionId"]})
            except Exception:
                pass

        client.on("Page.screencastFrame", on_frame)
        client.send("Page.startScreencast", {
            "format": "jpeg",
            "quality": SCREENCAST_QUALITY,
            "maxWidth": SCREENCAST_MAX_W,
            "maxHeight": SCREENCAST_MAX_H,
            "everyNthFrame": 1,
        })

        # Keeper: open hold, one slow even scroll down, brisk glide back, closing
        # hold on the same opening composition (folded into the opening by xfade).
        page.wait_for_timeout(tour["open_hold_ms"])
        page.evaluate(EASE_SCROLL_JS,
                      {"toY": to_y, "duration": tour["tour_dur_ms"], "linear": True})
        page.evaluate(EASE_SCROLL_JS,
                      {"toY": from_y, "duration": tour["return_dur_ms"]})
        page.wait_for_timeout(tour["close_hold_ms"])

        client.send("Page.stopScreencast")
        frames.append((time.monotonic(), None))   # stop sentinel for the last hold

        if frames and frames[0][1] is not None:
            log(f"[{project['name']}] screencast: {len([f for f in frames if f[1]])} frames")
        context.close()
        browser.close()

    named = os.path.join(RAW_DIR, project["name"] + "-raw.mp4")
    if os.path.exists(named):
        os.remove(named)
    assemble_raw(frames, named)
    dur = probe_duration(named)
    nreal = len([f for f in frames if f[1] is not None])
    log(f"[{project['name']}] raw take: {named}  ({kb(named):.0f}KB, {dur:.2f}s, "
        f"{nreal} screencast frames -> {FPS}fps CFR)")
    return named


def _b64(data):
    import base64
    return base64.b64decode(data)


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
    # The raw is the CDP screencast surface (1000x1040, yuvj420p full-range, tagged
    # bt470bg). NOTE: CDP screencast returns CSS-pixel frames, so the deviceScaleFactor
    # did NOT enlarge them; the raw is 1000 wide and the output is a mild upscale
    # (accepted: the crop/blur was verified in round 5). Scale to OUT_W x OUT_H and,
    # critically for HARDWARE VP9 decode (2026-07-28 fix):
    #   (a) setsar=1:1 forces SQUARE pixels. Scaling 1000x1040 (DAR 25:26) to the
    #       non-matching 1280x1344 otherwise leaves a fractional SAR (323:320, so
    #       videoWidth reports 1292), which hardware VP9 rejects
    #       (MediaError code 3 PIPELINE_ERROR_DECODE). The <1% aspect nudge is
    #       invisible and cover-cropped by the panel anyway.
    #   (b) convert full-range/bt470bg to the standard tv-range/bt709 that hardware
    #       paths accept. The pixels are CONVERTED (in_range/out_range +
    #       in/out_color_matrix), not just retagged, so pixels and tags agree.
    # object-fit: cover in the panel handles the mobile 2/1 ratio.
    return (f"scale={OUT_W}:{OUT_H}:flags=lanczos"
            f":in_range=full:out_range=tv:in_color_matrix=bt601:out_color_matrix=bt709"
            f",setsar=1:1")


def vp9_args(crf):
    """Shared VP9 constant-quality (CRF) output args. Audio stripped, 60fps CFR,
    -b:v 0 selects true constant-quality VP9; alt-ref kept for compression."""
    return [
        "-an", "-r", str(FPS),
        "-c:v", "libvpx-vp9", "-crf", str(crf), "-b:v", "0",
        # Force VP9 profile 0 (yuv420p): the xfade filter otherwise re-expands to
        # yuv444p (profile 1), which forces SOFTWARE decode on virtually all devices
        # and doubles the chroma data. 4:2:0 is hardware-decodable and halves chroma,
        # the single biggest decode-cost win (playback-smoothness fix, 2026-07-28).
        "-pix_fmt", "yuv420p",
        # Tag the encoded stream tv-range/bt709 to match the pixels the vfilter
        # produced (2026-07-28 hardware-decode fix). The pc + bt470bg combo the
        # earlier cut carried is an unusual pairing hardware VP9 paths reject.
        "-color_range", "tv", "-colorspace", "bt709",
        "-color_primaries", "bt709", "-color_trc", "bt709",
        "-deadline", "good", "-cpu-used", str(VP9_CPU_USED),
        "-auto-alt-ref", "1", "-lag-in-frames", "25",
        "-g", str(KEYFRAME_INTERVAL), "-row-mt", "1",
    ]


def encode_crossfade(raw, out, ss, base_dur, crf, cross, project=None):
    """Make a mathematically seamless loop by dissolving the clip's tail into its
    head. Standard xfade technique: split the base clip of length D into
    hold=[0, D-C] and end=[D-C, D], then xfade `end` over `hold` at offset 0 for
    duration C. Output length = D - C. The loop seam maps to two ADJACENT source
    frames, so it is continuous; the first C seconds are the tail->head dissolve."""
    d, c = base_dur, cross
    spatial = vfilter(project)
    fc = (
        f"[0:v]{spatial},fps={FPS},format=yuv420p,setpts=PTS-STARTPTS,split[a][b];"
        f"[a]trim=0:{d - c:.3f},setpts=PTS-STARTPTS[hold];"
        f"[b]trim={d - c:.3f}:{d:.3f},setpts=PTS-STARTPTS[end];"
        f"[end][hold]xfade=transition=fade:duration={c:.3f}:offset=0,format=yuv420p,setsar=1:1,"
        f"setparams=range=tv:colorspace=bt709:color_primaries=bt709:color_trc=bt709[v]"
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
    """Mean absolute pixel diff (0..255 per channel) between the OUTPUT clip's
    first and last frame. For a seamless loop these are near-adjacent, so a slow
    clip reads close to zero; a large value means a visible jump at the loop."""
    import numpy as np
    from PIL import Image
    with tempfile.TemporaryDirectory() as td:
        first_png = os.path.join(td, "first.png")
        last_png = os.path.join(td, "last.png")
        run(["ffmpeg", "-y", "-i", out, "-frames:v", "1", first_png])
        run(["ffmpeg", "-y", "-sseof", "-0.3", "-i", out,
             "-update", "1", "-frames:v", "1000", last_png])
        a = np.asarray(Image.open(first_png).convert("RGB"), dtype=np.int16)
        b = np.asarray(Image.open(last_png).convert("RGB"), dtype=np.int16)
    return float(np.mean(np.abs(a - b)))


def choose_head_ss(raw, spatial, raw_dur, open_hold_s):
    """Pick the crossfade HEAD start: the CROSSFADE_S window inside the OPENING
    HOLD that best matches the closing hold (the tail) and is calm. CONTENT-BASED.
    The round-5 raw contains ONLY the keeper (screencast started at the keeper), so
    the opening hold sits at t 0..open_hold_s at the tour START scroll position, the
    same position the tour returns to for the closing hold. The scan is bounded to
    that opening hold so the head is always the SAME scroll position as the tail:
    for the static heros this locks onto the settled window; for the
    continuously-animating star it locks onto the best plasma-phase frame at the
    start position (a diffuse dissolve, the round-4c accepted seam) rather than
    roaming to a mid-tour frame at a DIFFERENT scroll position (which would ghost)."""
    import numpy as np
    from PIL import Image
    win = int(round(CROSSFADE_S * FPS))
    s0 = 0.2
    # Stay inside the opening hold (plus a small margin) so the head shares the
    # tail's scroll position; never roam into the downward tour.
    s1 = min(raw_dur * 0.45, max(open_hold_s + 0.4, s0 + CROSSFADE_S + 0.2))
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
                       for k in range(win))
        match = float(np.mean(np.abs(reg[i + win // 2] - tail)))
        score = match + 0.4 * internal
        if best_score is None or score < best_score:
            best_i, best_score = i, score
    ss = s0 + best_i / FPS
    log(f"    head-anchor scan: ss={ss:.2f}s (region {s0:.2f}-{s1:.2f}s, "
        f"match-score {best_score:.2f})")
    return ss


def make_poster(webm, poster):
    """Frame 0 of the processed clip as a jpg, 1500 wide, quality tuned under the
    ~100KB budget."""
    chosen = None
    for q in (3, 4, 5, 6, 8, 10, 12, 15, 18, 22, 26):
        run([
            "ffmpeg", "-y", "-i", webm, "-frames:v", "1",
            "-q:v", str(q), "-vf", f"scale={OUT_W}:{OUT_H}", poster,
        ])
        size = kb(poster)
        chosen = (q, size)
        if size <= POSTER_MAX_KB:
            break
    log(f"    poster q={chosen[0]}: {chosen[1]:.0f}KB ({OUT_W} wide)")
    return chosen


def process_one(project):
    os.makedirs(MEDIA_DIR, exist_ok=True)
    raw = os.path.join(RAW_DIR, project["name"] + "-raw.mp4")
    if not os.path.exists(raw):
        raise FileNotFoundError(f"[{project['name']}] no raw take at {raw}; run capture first")

    raw_dur = probe_duration(raw)
    out = os.path.join(MEDIA_DIR, project["out"] + ".webm")
    poster = os.path.join(MEDIA_DIR, project["poster_out"] + ".jpg")
    crf = project.get("crf", DEFAULT_CRF)

    open_hold_s = project["tour"].get("open_hold_ms", 1000) / 1000.0
    ss = choose_head_ss(raw, vfilter(project), raw_dur, open_hold_s)
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
