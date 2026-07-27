#!/usr/bin/env python3
"""Capture pipeline for the three project preview clips (CONCEPT.md section 5).

Build-time tool only. This script ships nothing to the page: it records the
three live demo sites with headed, GPU-backed Chromium (Playwright), then
post-processes each raw take with ffmpeg into the muted, looping VP9 webm plus
poster jpg that index.html already references from media/.

Two stages, either of which can run alone:
  1. capture  - scripted, headed recording of each site to tools/_raw/
  2. process  - ffmpeg trim to a loop window, native 1280x720, strip audio,
                VP9 CRF quality mode, and a 1280-wide poster jpg from frame 0

Usage (run from anywhere, paths are resolved from this file):
  python tools/capture.py                 # capture then process, all three
  python tools/capture.py --only star     # just Until the Last Star
  python tools/capture.py --skip-capture  # re-encode from existing raw takes
  python tools/capture.py --skip-process  # record raw takes only

House rules: UK English, no em dashes. Vanilla toolchain, no runtime deps.
"""

import argparse
import math
import os
import subprocess
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
# Posters are re-exported at 1280 wide, target under ~80KB each.
WEBM_MIN_KB, WEBM_MAX_KB = 300, 500   # informational only, not enforced
POSTER_MAX_KB = 80

# VP9 constant-quality (CRF) per clip. Lower is crisper and larger. The brief
# asks for ~32 to 34, tuned by eye on extracted frames. Across 32/33/34 the size
# moved only ~10% (blackthorn 1504/1436/1364KB) and all three were crisp on
# decoded webm frames, so 34 (top of range, smallest) is used per the owner's
# "as small as possible while crisp" direction (see PROGRESS.md round 2).
DEFAULT_CRF = 34

# Client feedback round 3 (item 2): dense keyframe interval so the scroll-scrubbed
# desktop preview seeks smoothly in both directions. -g 12 at 30fps is a keyframe
# every ~0.4s. See encode_webm_crf for the rationale.
KEYFRAME_INTERVAL = 12

# Scrollbar suppression (item 4). The owner dislikes the demo sites' scrollbar in
# the captures. This CSS is injected into each page BEFORE the keeper so the
# recorded frames carry no scrollbar. Note: hiding the scrollbar reclaims its
# gutter width; the star (cosmic-dawn) take is checked after injection in case
# the WebGL scene sizes anything off the scrollbar width.
NO_SCROLLBAR_CSS = (
    "html { scrollbar-width: none !important; -ms-overflow-style: none !important; }"
    "::-webkit-scrollbar { display: none !important; width: 0 !important; height: 0 !important; }"
)

# The clip is trimmed to the tail of the raw take: the scripted sequence ends on
# its closing hold, and any frames after it are static at the same scroll
# position, so anchoring the trim to the end reliably lands on the intended end
# frame. This is robust against Playwright recording a timeline shorter than
# wall-clock (its tail frames lag), which an absolute front offset would miss.
# A small tail margin drops any frozen final frame.
TAIL_MARGIN_S = 0.10

# Per project capture plan. Scroll targets in CSS pixels came from probing each
# live site at 1280x800 (section anchors and epoch scroll map). "segments" is
# the scripted keeper motion: an eased scrollTo per {to, dur_ms} step and a
# static pause per {hold_ms}. The clip is trimmed to start inside the opening
# hold and end inside the closing hold, so the loop cut lands between two calm,
# near static frames.
PROJECTS = [
    {
        "name": "blackthorn",
        "url": "https://arctxrus.github.io/blackthorn-demo/",
        "out": "blackthorn-preview",
        "poster_out": "blackthorn-poster",
        # Glide from the cover, through the price menu, to the rotating reviews.
        "start_y": 0,
        "settle_ms": 1200,
        "segments": [
            {"hold_ms": 800},          # cover
            {"to": 1900, "dur_ms": 2200},   # arrive at the price menu (services)
            {"hold_ms": 800},          # let the menu read
            {"to": 5500, "dur_ms": 2600},   # down to the reviews pull-quote
            {"hold_ms": 1400},         # linger on a rotating quote
        ],
        "verify_nvidia": False,
        "clip_len_s": 7.0,
    },
    {
        "name": "barker",
        "url": "https://arctxrus.github.io/barker-bloom-demo/",
        "out": "barker-bloom-preview",
        "poster_out": "barker-bloom-poster",
        # Hero, the paw-trail thread drawing on scroll, a peek at the pricing bento.
        "start_y": 0,
        "settle_ms": 1200,
        "segments": [
            {"hold_ms": 800},          # hero
            {"to": 1150, "dur_ms": 3400},   # slow draw down into the pricing bento
            {"hold_ms": 2200},         # pricing bento settled
        ],
        "verify_nvidia": False,
        "clip_len_s": 6.0,
    },
    {
        "name": "star",
        # ?tier=2 forces the T2 quality tier, so the real screen-space
        # gravitational-lens pass (js/lensing.js) draws the black hole rather
        # than the flat sprite fallback. The scene sustains ~140fps on the RTX
        # 3060, well above the 55fps governor that would otherwise drop the lens.
        "url": "https://arctxrus.github.io/cosmic-dawn/?tier=2",
        "out": "until-the-last-star-preview",
        "poster_out": "until-the-last-star-poster",
        # THE LONG NIGHT (timeline t 0.79..0.90): the Gargantua black hole with
        # the lensed accretion disc and photon ring. Hold at peak lens (t 0.845)
        # and run a slow eased mouse-parallax orbit: cosmic-dawn's scene.js reads
        # the pointer into a spring-smoothed camera parallax orbit, and the
        # lensing answers the viewpoint, so the lensed arcs and ring shift. An
        # unmistakably 3D, reactive moment (decision 5h), not a starfield fade.
        "start_t": 0.845,           # scroll position derived from the timeline t
        "settle_ms": 2000,          # let the spring settle at t and the lens warm
        # Client feedback round 3 (item 1): the previous large vertical amplitude
        # (amp_y 150) swung the lensed accretion disc's lower arc down into the
        # bottom of the panel preview, where the bottom fade dissolved it into a
        # stray glowing "curve" (confirmed on extracted frames). The orbit is now
        # dominated by the horizontal sweep (which still shifts the lens and reads
        # as 3D) with only a small vertical component, so the disc stays centred
        # and the frame keeps clean dark space top and bottom throughout the clip.
        "parallax": {
            "amp_x": 150, "amp_y": 44,    # px around the viewport centre: a gentle orbit
            "period_s": 4.0,              # one camera orbit
            "keeper_s": 8.5,             # > clip_len_s; the last clip_len_s is trimmed out
            "step_ms": 20,               # ~50Hz pointer feed keeps the orbit from idling
        },
        "verify_nvidia": True,
        "clip_len_s": 7.0,
        # Client feedback round 3 (item 1): a gentle bottom-anchored reframe crop
        # on top of the reduced parallax. Drops the top 40px of dark sky and scales
        # back to native, nudging the whole lensed disc up by ~40px so its bright
        # lower arc stays clear of the panel preview's bottom fade across EVERY
        # scrub frame (measured: fade-band luminance a steady ~120 vs ~137 uncropped
        # and ~135 on the old clip). w,h,x,y for ffmpeg crop; scale restores 1280x720.
        "crop": (1280, 680, 0, 40),
    },
]

# Eased scroll run inside the page: easeInOutQuad over each segment via rAF, so
# the motion is per-frame smooth rather than stepped from Python. Resolves when
# the target is reached. No manual driving, no mouse.
EASE_SCROLL_JS = """
async ({toY, duration}) => {
  const startY = window.scrollY;
  const dist = toY - startY;
  const t0 = performance.now();
  const ease = t => (t < 0.5 ? 2 * t * t : 1 - Math.pow(-2 * t + 2, 2) / 2);
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


def run_parallax(page, cfg):
    """Drive a slow eased circular mouse orbit around the viewport centre for
    keeper_s seconds (decision 5h). cosmic-dawn's scene.js reads pointermove
    (mouse only) into a spring-smoothed camera parallax orbit, so the lensed arcs
    and photon ring shift with the viewpoint. Continuous ~50Hz moves keep the
    orbit alive (it decays to rest after 2.5s of pointer idle). The orbit is
    periodic in position and velocity, so the end-anchored trim (last clip_len_s)
    lands on a smooth, near-looping window with calm ends."""
    cx, cy = REC_W / 2.0, REC_H / 2.0
    ax, ay = cfg["amp_x"], cfg["amp_y"]
    period = cfg["period_s"]
    total = cfg["keeper_s"]
    step_ms = cfg.get("step_ms", 20)
    # settle the pointer onto the orbit start (phase 0: top of the ellipse)
    page.mouse.move(cx, cy - ay)
    page.wait_for_timeout(200)
    t0 = time.monotonic()
    while True:
        elapsed = time.monotonic() - t0
        if elapsed >= total:
            break
        phase = 2.0 * math.pi * elapsed / period
        page.mouse.move(cx + ax * math.sin(phase), cy - ay * math.cos(phase))
        page.wait_for_timeout(step_ms)


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

        # Move to the start scroll position and let a scroll-driven scene catch
        # up. Start can be given as an absolute pixel offset (start_y) or as a
        # timeline position (start_t, 0..1), resolved here to the scroll pixel.
        if "start_t" in project:
            start_y = page.evaluate(
                "t => t * (document.documentElement.scrollHeight - window.innerHeight)",
                project["start_t"],
            )
        else:
            start_y = project["start_y"]
        page.evaluate("y => window.scrollTo(0, y)", start_y)
        page.wait_for_timeout(project["settle_ms"])

        # Keeper begins now. Record the offset into the video so ffmpeg can trim
        # to the scripted window.
        keeper_offset_s = time.monotonic() - t_ctx
        log(f"[{project['name']}] keeper starts at ~{keeper_offset_s:.2f}s into the take")

        if "parallax" in project:
            # No scripted scroll: hold at the peak-lens position and orbit the
            # camera via the pointer (decision 5h).
            run_parallax(page, project["parallax"])
        else:
            for seg in project["segments"]:
                if "hold_ms" in seg:
                    page.wait_for_timeout(seg["hold_ms"])
                else:
                    page.evaluate(EASE_SCROLL_JS, {"toY": seg["to"], "duration": seg["dur_ms"]})

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
    log(f"[{project['name']}] raw take: {named}  ({kb(named):.0f}KB)")
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
    # Client feedback round 2 (item 3): the take is native 16:9 (1280x720) and
    # the output is native 1280x720 too (no downscale), so the clip stays crisp
    # at full panel size. A straight scale keeps the full frame including the top
    # nav pill; object-fit: cover in the panel handles the mobile 2/1 ratio.
    # Client feedback round 3 (item 1): a project may carry a "crop" (w,h,x,y) to
    # reframe before the scale (the star clip nudges the lensed disc up so the
    # bottom stays clean); everything scales back to OUT_W x OUT_H afterwards.
    crop = project.get("crop") if project else None
    if crop:
        w, h, x, y = crop
        return f"crop={w}:{h}:{x}:{y},scale={OUT_W}:{OUT_H}"
    return f"scale={OUT_W}:{OUT_H}"


def encode_webm_crf(raw, out, ss, dur, crf, project=None):
    """Single-pass VP9 constant-quality (CRF) encode. Client feedback round 2
    (item 3): quality mode, not a bitrate target, so the clip is as crisp as CRF
    dictates and as small as VP9 can make it at that quality. Audio stripped,
    30fps, keyframed. -b:v 0 selects true constant-quality VP9.

    Client feedback round 3 (item 2): the desktop preview is now scroll-scrubbed
    (video.currentTime driven by scroll), which seeks all over the timeline,
    including backwards. VP9 with sparse keyframes (-g 60, one every 2s) seeks
    badly: a reverse seek must decode from the previous keyframe, so the frame
    lags and stutters. The GOP is now DENSE (-g 12, a keyframe every ~0.4s at
    30fps) so any seek lands within ~12 frames of a keyframe and scrubbing, in
    either direction, resolves promptly. Sizes rise (accepted, quality wins);
    alt-ref is kept for compression, the dense keyframes carry the seek quality.
    KEYFRAME_INTERVAL is the single knob."""
    common = [
        "ffmpeg", "-y", "-ss", f"{ss:.3f}", "-t", f"{dur:.3f}", "-i", raw,
        "-an", "-vf", vfilter(project), "-r", "30",
        "-c:v", "libvpx-vp9", "-crf", str(crf), "-b:v", "0",
        "-deadline", "good", "-cpu-used", "1",
        "-auto-alt-ref", "1", "-lag-in-frames", "25",
        "-g", str(KEYFRAME_INTERVAL), "-row-mt", "1",
    ]
    run(common + [out])
    size = kb(out)
    log(f"    VP9 crf {crf}: {size:.0f}KB (1280x720, quality mode)")
    return crf, size


def make_poster(webm, poster):
    """Frame 0 of the processed clip as a jpg, 1280 wide, quality tuned under the
    ~80KB budget (item 3)."""
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

    # End-anchor the trim: take the last clip_len seconds of the raw take (less
    # a small tail margin), so the clip ends on the scripted closing hold and
    # runs the full requested length regardless of recorded-timeline drift.
    raw_dur = probe_duration(raw)
    dur = project["clip_len_s"]
    ss = max(0.0, raw_dur - dur - TAIL_MARGIN_S)
    out = os.path.join(MEDIA_DIR, project["out"] + ".webm")
    poster = os.path.join(MEDIA_DIR, project["poster_out"] + ".jpg")

    crf = project.get("crf", DEFAULT_CRF)
    log(f"[{project['name']}] encoding webm  (raw {raw_dur:.2f}s, ss={ss:.2f}s, len={dur:.1f}s, crf={crf})")
    encode_webm_crf(raw, out, ss, dur, crf, project)
    size = kb(out)
    make_poster(out, poster)
    log(f"[{project['name']}] done: {os.path.basename(out)} {size:.0f}KB, "
        f"{os.path.basename(poster)} {kb(poster):.0f}KB")


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
