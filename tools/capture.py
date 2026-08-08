#!/usr/bin/env python3
"""Capture pipeline for the project SECTION CARDS (Client feedback round 6).

Build-time tool only. This script ships nothing to the page: it records / screenshots
the three live demo sites with headed, GPU-backed Chromium, then post-processes each
take into the media that index.html references from media/.

ROUND 6 (owner-directed structural redesign). The single per-project "tour" webm is
retired. Each project now shows a scrollable stack of SECTION CARDS, so this script
captures 3 to 5 sections per project as either:

  - STATIC images (non-animated sections): a DPR-2 screenshot of a 16:9 window over
    the section, downscaled to ~1600 wide, jpg quality tuned well under 300KB.
  - SHORT LOOPS (animated sections): a fixed-position CDP-screencast recording with
    a natural or scripted cycle, post-processed into a seamless VP9 loop (the same
    hardened encode as round 5: VP9 Profile 0 / yuv420p, 30fps, SAR 1:1, tv/bt709,
    tail->head crossfade) plus a poster jpg from frame 0.

Section plan (chosen after inspecting each live site; see PROGRESS.md round 6):
  Blackthorn: cover, price menu, barbers, in-their-words, booking form (all STATIC:
    none of these sections cycles at rest; the reviews carousel is manual).
  Barker & Bloom: the welcome (STATIC: the paw trail draws once, no rest cycle),
    price menu (STATIC), before-and-after (LOOP: the compare slider is scripted to
    sweep), booking form (STATIC).
  Until the Last Star: the first star, the cosmic web, the last star (all LOOP: the
    WebGL scene animates continuously; parked at three bright epochs, black-hole
    finale included as one card among bright ones).

Shared plumbing kept from the round-5 tour pipeline (they share the encode path):
  assemble_raw, vfilter, vp9_args, encode_crossfade, choose_head_ss,
  seam_first_last_diff, make_poster, the CDP screencast capture and the GPU launch.

Usage (run from anywhere; paths resolve from this file):
  python tools/capture.py                       # everything
  python tools/capture.py --only star           # one project's sections
  python tools/capture.py --section star-darkages  # a single section
  python tools/capture.py --skip-capture        # re-process loops from raws
  python tools/capture.py --skip-process        # record raws only

House rules: UK English, no em dashes. Vanilla toolchain, no runtime deps.
"""

import argparse
import glob
import os
import subprocess
import tempfile
import time

TOOLS_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.dirname(TOOLS_DIR)
MEDIA_DIR = os.path.join(REPO_ROOT, "media")
RAW_DIR = os.path.join(TOOLS_DIR, "_raw")

# 16:9 recording viewport (the section card box is a fixed 16:9). CDP screencast
# returns CSS-pixel frames (verified 2026-08-08: at DPR 2 a 1280x720 context still
# yields 1280x720 screencast frames, maxWidth is only a downscale cap), so a loop
# raw is only as wide as the CSS viewport. page.screenshot (statics) DOES honour
# deviceScaleFactor, so statics come out at DPR-2 and downscale crisply regardless.
# Default recording viewport (blackthorn, barker). Per project via PROJECT_CFG.
REC_W, REC_H = 1280, 720
DPR = 2

# Loop output default. 16:9, mod-16 (1280 = 80*16, 720 = 45*16) so VP9 macroblocks
# align and hardware decode is efficient. Same profile-0 / SAR / colour hardening as
# round 5. Per-section `out_w` / `out_h` override this (star loops run 1600x900,
# captured from a 1600-wide CSS viewport so the source is genuinely 1600 px wide, not
# upscaled). 1600x900: width is mod-16 (100*16), height even (yuv420p safe); 900 is
# not a multiple of 16, which VP9 pads internally, the closest 16:9 gets above 720.
OUT_W, OUT_H = 1280, 720
FPS = 30

# Static output. DPR-2 capture downscaled to 1600 wide (cards render ~682 CSS px, so
# DPR-2 needs ~1364 device px; 1600 clears that with margin). jpg quality is picked
# highest-first: the best quality that fits STATIC_SOFT_KB, but never degraded past
# STATIC_Q_FLOOR, so a busy frame keeps its detail and simply runs larger (noted).
STATIC_W, STATIC_H = 1600, 900
STATIC_SOFT_KB = 300     # aim under this where achievable
STATIC_Q_FLOOR = 5       # never step jpg quality worse (higher -q:v) than this

GPU_ARGS = [
    "--use-angle=d3d11",
    "--enable-gpu-rasterization",
    "--enable-zero-copy",
    "--ignore-gpu-blocklist",
    "--disable-features=CalculateNativeWinOcclusion",
]

SCREENCAST_QUALITY = 92   # near-lossless jpeg frames; the VP9 CRF does the real work

POSTER_MAX_KB = 100       # owner: posters under ~100KB preferred, quality wins if needed
DEFAULT_CRF = 32          # 1280x720 is small, so 32 stays crisp and light
STAR_CRF = 31             # 1600x900 star loops: one notch richer for the extra pixels
VP9_CPU_USED = 2
KEYFRAME_INTERVAL = 60    # a keyframe every 2s at 30fps
CROSSFADE_S = 0.8         # seamless-loop tail->head dissolve
TAIL_MARGIN_S = 0.10

NO_SCROLLBAR_CSS = (
    "html { scrollbar-width: none !important; -ms-overflow-style: none !important; }"
    "::-webkit-scrollbar { display: none !important; width: 0 !important; height: 0 !important; }"
)

BT_URL = "https://blackthorn.pagefront.co.uk/"
# barkerbloom returned 502 from Cloudflare during this round; BK_URL_OVERRIDE lets the
# run point at a locally served copy of C:\Dev\barker-bloom-demo (same code) instead.
BK_URL = os.environ.get("BK_URL_OVERRIDE", "https://barkerbloom.pagefront.co.uk/")
STAR_URL = "https://star.pagefront.co.uk/?tier=2"

# Project-level session config (applied once after navigation). `viewport` is the CSS
# recording viewport: blackthorn / barker keep 1280x720 (proven framing, DPR-2
# statics are 2560-wide sources downscaled to 1600); star runs 1600x900 so its
# screencast loop source is genuinely 1600 px wide (full-bleed aspect-driven WebGL,
# same composition at either size, no container gutters).
PROJECT_CFG = {
    "blackthorn": {"url": BT_URL, "nvidia": False, "load_wait_ms": 0, "preloader": False,
                   "viewport": (1280, 720)},
    "barker": {"url": BK_URL, "nvidia": False, "load_wait_ms": 0, "preloader": False,
               "viewport": (1280, 720)},
    # The WebGL scene needs the discrete GPU (tier 2) and ~10s to fully initialise.
    "star": {"url": STAR_URL, "nvidia": True, "load_wait_ms": 10000, "preloader": True,
             "viewport": (1600, 900)},
}

# Before/after compare slider: sweep the reveal smoothly (sine, so it is periodic and
# the crossfade finds a matching phase). Drives every .ba__stage on the page: the
# clip-path inset on .ba__before-wrap and the .ba__handle left, exactly as the site's
# own drag does (verified live: both are settable inline).
BA_SWEEP_JS = """
() => {
  const stages = Array.from(document.querySelectorAll('.ba__stage'));
  if (!stages.length) return false;
  const start = performance.now();
  const period = 5200;              // ms per full sweep cycle
  function frame(now) {
    const P = 50 + 30 * Math.sin((now - start) / period * Math.PI * 2);  // 20..80
    const right = (100 - P).toFixed(2);
    const left = P.toFixed(2);
    for (const st of stages) {
      const wrap = st.querySelector('.ba__before-wrap');
      const handle = st.querySelector('.ba__handle');
      if (wrap) wrap.style.clipPath = 'inset(0px ' + right + '% 0px 0px)';
      if (handle) handle.style.left = left + '%';
    }
    requestAnimationFrame(frame);
  }
  requestAnimationFrame(frame);
  return true;
}
"""

# Section plan. `pos` is either {"sel": "#id", "off": px} (scroll so the section top
# sits `off` px below the viewport top) or {"t": frac} (a cosmic-dawn timeline
# fraction). `kind` is 'static' or 'loop'. Loops carry `record_ms` and an optional
# `script` run in-page during the recording. `settle_ms` waits after positioning so
# scroll-reveal animations finish.
SECTIONS = [
    # ---- Blackthorn (all static) ----
    {"p": "blackthorn", "out": "blackthorn-cover", "kind": "static",
     "pos": {"sel": "#cover", "off": 0}, "settle_ms": 2200},
    {"p": "blackthorn", "out": "blackthorn-prices", "kind": "static",
     "pos": {"sel": "#services", "off": 0}, "settle_ms": 1800},
    {"p": "blackthorn", "out": "blackthorn-barbers", "kind": "static",
     "pos": {"sel": "#team", "off": 0}, "settle_ms": 1800},
    {"p": "blackthorn", "out": "blackthorn-reviews", "kind": "static",
     "pos": {"sel": "#reviews", "off": 0}, "settle_ms": 1800},
    {"p": "blackthorn", "out": "blackthorn-booking", "kind": "static",
     "pos": {"sel": "#booking", "off": 0}, "settle_ms": 1800},

    # ---- Barker & Bloom ----
    {"p": "barker", "out": "barker-hero", "kind": "static",
     "pos": {"sel": "#home", "off": 0}, "settle_ms": 2200},
    {"p": "barker", "out": "barker-prices", "kind": "static",
     "pos": {"sel": "#services", "off": 0}, "settle_ms": 1800},
    {"p": "barker", "out": "barker-beforeafter", "kind": "loop",
     "pos": {"sel": "#gallery", "off": 60}, "settle_ms": 1500,
     "record_ms": 6500, "script": BA_SWEEP_JS,
     "poster_out": "barker-beforeafter-poster"},
    {"p": "barker", "out": "barker-booking", "kind": "static",
     "pos": {"sel": "#book", "off": 0}, "settle_ms": 2000},

    # ---- Until the Last Star (all loops, WebGL continuous) ----
    # New owner-directed section list (2026-08-08), replacing first star / cosmic web /
    # last star. 1600x900 loops from the 1600 CSS viewport (see PROJECT_CFG). t values
    # chosen from a live luminance / structure sweep (PROGRESS "Media re-capture:
    # post-migration"): spark 0.08 (bright, well-formed inflation flash), afterglow
    # 0.13 (top of the proven bright plateau, warm plasma), dark-ages 0.275 (the most
    # structured window in the 0.21-0.29 span, hydrogen gathering reads).
    # loop_min_s bounds the head-anchor scan so each loop is >= 5s (restarts less,
    # keeps dropped frames low); the crossfade dissolves the seam either way.
    #
    # Resolution decision (measured 2026-08-08, PROGRESS): captured at the 1600x900 CSS
    # viewport but OUTPUT 1280x720. A genuine 1600x900 loop was built and measured; the
    # dense/animated WebGL content pushed clips to 2.25-13.7MB (7-37 Mbps), far over the
    # 300-500KB house budget (CONCEPT 5, mobile-first), for only a ~6% perceptual gain
    # at the card's ~682px render size. Downscaling the 1600 raw to 1280 supersamples
    # the starfield (crisper, smoother, cheaper to encode) and keeps clips near budget.
    #
    # THE SPARK carries `orbit`: a slow, GENTLE, small-amplitude scripted circular
    # pointer orbit driven as real (isTrusted) mouse.move during the take, so the site's
    # spring-smoothed camera parallax visibly responds. The amplitude is deliberately
    # small: a large orbit globally translates the dense starfield every frame and
    # defeats temporal compression (an amp-150 orbit ballooned the clip to 8-28MB), so a
    # small amp keeps both the motion gentle (owner's brief) and the file near budget.
    # The circle is periodic in position and velocity so the crossfade finds a matching
    # phase; the CDP screencast draws no OS cursor (verified) and cursor:none is injected
    # as belt-and-braces.
    # Spark size note: even a gentle orbit makes this the one heavy card (multi-layer
    # star parallax has no single motion vector and thousands of point-stars flip pixel
    # state, so VP9 cannot compress it the way the no-parallax epochs compressed to
    # ~300KB). Kept small: amp 30x20, a 6.2s record cut to a ~4.7s loop, crf 48 (which
    # stays clean at this small amplitude; the dark-region blocking ceiling is ~46 only
    # at the large amplitudes tested). This lands ~1.8MB, the accepted cost of the
    # owner-requested visible parallax on a dense starfield.
    {"p": "star", "out": "star-spark", "kind": "loop",
     "pos": {"t": 0.08}, "settle_ms": 2500, "record_ms": 6200, "loop_min_s": 4.5,
     "crf": 48,
     "orbit": {"amp_x": 30, "amp_y": 20, "period_ms": 6500, "hz": 50},
     "poster_out": "star-spark-poster"},
    # Afterglow is FULL-FRAME smooth plasma motion (every block has residual every
    # frame), which unlike the mostly-static spark / dark-ages the decoder cannot skip;
    # at 1280x720 it dropped ~15% of frames in-page (continuous, not at the loop seam).
    # Output at 1024x576 (mod-16, 16:9): 0.64x the pixels to decode + composite brings
    # it under the 5% bar, and the softening is invisible on smooth plasma at the card
    # size. crf 36 (a touch richer, the smaller frame keeps the file small anyway).
    {"p": "star", "out": "star-afterglow", "kind": "loop",
     "pos": {"t": 0.13}, "settle_ms": 2500, "record_ms": 7000, "loop_min_s": 5.0,
     "crf": 36, "out_w": 1024, "out_h": 576,
     "poster_out": "star-afterglow-poster"},
    {"p": "star", "out": "star-darkages", "kind": "loop",
     "pos": {"t": 0.275}, "settle_ms": 2500, "record_ms": 7000, "loop_min_s": 5.0,
     "crf": 34,
     "poster_out": "star-darkages-poster"},
]

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

RENDERER_JS = """
() => {
  const c = document.createElement('canvas');
  const gl = c.getContext('webgl2') || c.getContext('webgl');
  if (!gl) return 'no-webgl';
  const dbg = gl.getExtension('WEBGL_debug_renderer_info');
  return dbg ? gl.getParameter(dbg.UNMASKED_RENDERER_WEBGL) : 'no-debug-ext';
}
"""

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


def run(cmd):
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def kb(path):
    return os.path.getsize(path) / 1024.0


def _b64(data):
    import base64
    return base64.b64decode(data)


def probe_duration(path):
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "default=noprint_wrappers=1:nokey=1", path],
        check=True, capture_output=True, text=True,
    )
    return float(out.stdout.strip())


def inject_no_scrollbar(page):
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


def scroll_to(page, pos):
    """Position the section: {'sel','off'} scrolls the section top to `off` px below
    the viewport top; {'t'} is a cosmic-dawn timeline fraction."""
    if "t" in pos:
        page.evaluate(
            "t => window.scrollTo(0, t * (document.documentElement.scrollHeight - window.innerHeight))",
            pos["t"],
        )
        return
    page.evaluate(
        """(a) => {
             const el = document.querySelector(a.sel);
             if (!el) { return; }
             const y = el.getBoundingClientRect().top + window.scrollY - a.off;
             window.scrollTo(0, Math.max(0, y));
           }""",
        {"sel": pos["sel"], "off": pos.get("off", 0)},
    )


# ---- static screenshot ----------------------------------------------------------

def capture_static(page, section):
    os.makedirs(MEDIA_DIR, exist_ok=True)
    scroll_to(page, section["pos"])
    page.wait_for_timeout(section.get("settle_ms", 1500))
    with tempfile.TemporaryDirectory() as td:
        shot = os.path.join(td, "shot.png")
        # Full 16:9 viewport at DPR 2. No clip needed: the viewport is 16:9.
        page.screenshot(path=shot, animations="disabled")
        jpg = os.path.join(MEDIA_DIR, section["out"] + ".jpg")
        # Highest quality first (lower -q:v is better). Step quality DOWN only until the
        # frame fits STATIC_SOFT_KB, and never past STATIC_Q_FLOOR: a busy frame keeps
        # its detail and simply runs larger (owner: highest quality, quality wins).
        chosen = None
        for q in (2, 3, 4, 5):
            run(["ffmpeg", "-y", "-i", shot, "-vf",
                 f"scale={STATIC_W}:{STATIC_H}:flags=lanczos", "-q:v", str(q), jpg])
            size = kb(jpg)
            chosen = (q, size)
            if size <= STATIC_SOFT_KB or q >= STATIC_Q_FLOOR:
                break
        flag = "" if chosen[1] <= STATIC_SOFT_KB else "  (over soft cap: quality kept)"
        log(f"[{section['out']}] static jpg q={chosen[0]}: {chosen[1]:.0f}KB "
            f"({STATIC_W}x{STATIC_H}){flag}")


# ---- loop recording -------------------------------------------------------------

def assemble_raw(frames, raw_path):
    """Build a CFR intermediate from the screencast frames (H.264 CRF 12, near
    lossless), preserving static holds. Same technique as the round-5 tour pipeline."""
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
        ts = [f[0] for f in real] + [stop_ts]
        lines = []
        for i, name in enumerate(names):
            dur = ts[i + 1] - ts[i]
            dur = max(1.0 / 120.0, min(2.5, dur))
            safe = name.replace("\\", "/")
            lines.append(f"file '{safe}'")
            lines.append(f"duration {dur:.5f}")
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


def drive_orbit(page, orbit, vp, record_ms):
    """Drive a slow circular REAL (isTrusted) mouse orbit for record_ms while the
    screencast records, so the star scene's spring-smoothed camera parallax responds.
    Interleaves mouse.move with tiny waits (~orbit['hz'] Hz); each call pumps the sync
    event loop so screencast frame acks keep flowing. Centred on the viewport, so the
    orbit is periodic in position and velocity (clean crossfade phase)."""
    import math
    cx, cy = vp[0] / 2.0, vp[1] / 2.0
    ax, ay = orbit["amp_x"], orbit["amp_y"]
    period = orbit["period_ms"]
    hz = orbit.get("hz", 50)
    step_ms = max(5, int(round(1000.0 / hz)))
    t0 = time.monotonic()
    while (time.monotonic() - t0) * 1000.0 < record_ms:
        el = (time.monotonic() - t0) * 1000.0
        ang = (el / period) * 2.0 * math.pi
        x = cx + ax * math.cos(ang)
        y = cy + ay * math.sin(ang)
        page.mouse.move(x, y)
        page.wait_for_timeout(step_ms)


def capture_loop(page, context, section, vp):
    """Record a fixed-position screencast take of an animated section to tools/_raw/."""
    os.makedirs(RAW_DIR, exist_ok=True)
    scroll_to(page, section["pos"])
    page.wait_for_timeout(section.get("settle_ms", 1500))

    # Start any in-page cycle script (e.g. the before/after sweep) before recording.
    if section.get("script"):
        ok = page.evaluate(section["script"])
        if ok is False:
            log(f"    warning: [{section['out']}] loop script found no targets")

    # Belt-and-braces: the CDP screencast does not draw the OS cursor (verified), but
    # hide any cursor for the pointer-orbit takes so no artefact can appear.
    orbit = section.get("orbit")
    if orbit:
        try:
            page.add_style_tag(content="*{cursor:none !important}")
        except Exception:
            pass
        # Seed the pointer at the orbit start so the parallax spring is already engaged
        # (not decaying to rest) when recording begins.
        page.mouse.move(vp[0] / 2.0 + orbit["amp_x"], vp[1] / 2.0)
        page.wait_for_timeout(400)

    frames = []

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
        "maxWidth": vp[0] * DPR,
        "maxHeight": vp[1] * DPR,
        "everyNthFrame": 1,
    })
    record_ms = section.get("record_ms", 6000)
    if orbit:
        drive_orbit(page, orbit, vp, record_ms)
    else:
        page.wait_for_timeout(record_ms)
    client.send("Page.stopScreencast")
    frames.append((time.monotonic(), None))

    raw = os.path.join(RAW_DIR, section["out"] + "-raw.mp4")
    if os.path.exists(raw):
        os.remove(raw)
    assemble_raw(frames, raw)
    dur = probe_duration(raw)
    nreal = len([f for f in frames if f[1] is not None])
    log(f"[{section['out']}] raw: {kb(raw):.0f}KB, {dur:.2f}s, {nreal} frames -> {FPS}fps CFR")
    return raw


def vfilter(out_w=OUT_W, out_h=OUT_H):
    # scale to 16:9 output, square pixels, convert full-range/bt601 -> tv/bt709 so the
    # tags and pixels agree and hardware VP9 accepts it (round-5 hardening).
    return (f"scale={out_w}:{out_h}:flags=lanczos"
            f":in_range=full:out_range=tv:in_color_matrix=bt601:out_color_matrix=bt709"
            f",setsar=1:1")


def vp9_args(crf):
    return [
        "-an", "-r", str(FPS),
        "-c:v", "libvpx-vp9", "-crf", str(crf), "-b:v", "0",
        "-pix_fmt", "yuv420p",
        "-color_range", "tv", "-colorspace", "bt709",
        "-color_primaries", "bt709", "-color_trc", "bt709",
        "-deadline", "good", "-cpu-used", str(VP9_CPU_USED),
        "-auto-alt-ref", "1", "-lag-in-frames", "25",
        "-g", str(KEYFRAME_INTERVAL), "-row-mt", "1",
    ]


def encode_crossfade(raw, out, ss, base_dur, crf, cross, out_w=OUT_W, out_h=OUT_H):
    d, c = base_dur, cross
    spatial = vfilter(out_w, out_h)
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
        f"({out_w}x{out_h}, loop {d - c:.2f}s)")


def seam_first_last_diff(out):
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


def choose_head_ss(raw, spatial, raw_dur, ss_max=None):
    """Pick the crossfade HEAD start: the CROSSFADE_S window near the start that best
    matches the tail and is calm. Content-based. For a fixed-position take the whole
    clip is at one scroll position, so any early window shares the tail's framing; the
    scan finds the best-matching phase (the round-4c accepted diffuse dissolve for the
    continuously-animating WebGL scenes; a near-exact match for the periodic sweep).

    ss_max (round-6 FAIL 1) caps the head start so the resulting loop meets a
    minimum length: a later ss shortens the loop, so bounding it keeps the loop long
    enough to restart rarely."""
    import numpy as np
    from PIL import Image
    win = int(round(CROSSFADE_S * FPS))
    s0 = 0.2
    s1 = min(raw_dur * 0.5, s0 + max(2.5, CROSSFADE_S + 0.2))
    if ss_max is not None:
        # Cap the head start at ss_max so the loop meets its minimum length. Keep a
        # small non-empty scan window (>= s0 + 0.2s) so at least a few candidate
        # head phases are compared for the seam.
        s1 = min(s1, max(s0 + 0.2, ss_max))
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


def make_poster(webm, poster, out_w=OUT_W, out_h=OUT_H):
    chosen = None
    for q in (3, 4, 5, 6, 8, 10, 12, 15, 18, 22, 26):
        run(["ffmpeg", "-y", "-i", webm, "-frames:v", "1",
             "-q:v", str(q), "-vf", f"scale={out_w}:{out_h}", poster])
        size = kb(poster)
        chosen = (q, size)
        if size <= POSTER_MAX_KB:
            break
    log(f"    poster q={chosen[0]}: {chosen[1]:.0f}KB ({out_w} wide)")


def process_loop(section):
    raw = os.path.join(RAW_DIR, section["out"] + "-raw.mp4")
    if not os.path.exists(raw):
        raise FileNotFoundError(f"[{section['out']}] no raw at {raw}; run capture first")
    raw_dur = probe_duration(raw)
    out = os.path.join(MEDIA_DIR, section["out"] + ".webm")
    poster = os.path.join(MEDIA_DIR, section["poster_out"] + ".jpg")
    crf = section.get("crf", DEFAULT_CRF)
    out_w = section.get("out_w", OUT_W)
    out_h = section.get("out_h", OUT_H)
    # If a minimum loop length is asked for, cap the head start so the loop is at
    # least that long (loop = raw_dur - ss - TAIL_MARGIN_S - CROSSFADE_S).
    ss_max = None
    if section.get("loop_min_s"):
        ss_max = raw_dur - TAIL_MARGIN_S - CROSSFADE_S - section["loop_min_s"]
    ss = choose_head_ss(raw, vfilter(out_w, out_h), raw_dur, ss_max)
    base = raw_dur - ss - TAIL_MARGIN_S
    log(f"[{section['out']}] loop (raw {raw_dur:.2f}s, ss={ss:.2f}s, base={base:.2f}s "
        f"-> {base - CROSSFADE_S:.2f}s, crf {crf})")
    encode_crossfade(raw, out, ss, base, crf, CROSSFADE_S, out_w, out_h)
    seam = seam_first_last_diff(out)
    make_poster(out, poster, out_w, out_h)
    log(f"[{section['out']}] done: {os.path.basename(out)} {kb(out):.0f}KB, "
        f"{os.path.basename(poster)} {kb(poster):.0f}KB, seam first-vs-last {seam:.2f}")


# ---- driver ---------------------------------------------------------------------

def run_project(pname, sections, do_capture, do_process):
    from playwright.sync_api import sync_playwright

    cfg = PROJECT_CFG[pname]
    loops = [s for s in sections if s["kind"] == "loop"]
    statics = [s for s in sections if s["kind"] == "static"]

    # Processing only (no browser needed for loops if raws exist; statics need capture).
    if not do_capture:
        if do_process:
            for s in loops:
                process_loop(s)
        return

    vp = cfg.get("viewport", (REC_W, REC_H))
    log(f"[{pname}] launching headed Chromium with GPU args "
        f"(viewport {vp[0]}x{vp[1]}, DPR {DPR})")
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, args=GPU_ARGS)
        context = browser.new_context(
            viewport={"width": vp[0], "height": vp[1]},
            device_scale_factor=DPR,
        )
        page = context.new_page()
        page.goto(cfg["url"], wait_until="networkidle", timeout=90000)
        try:
            page.evaluate("document.fonts && document.fonts.ready")
            page.wait_for_function(
                "document.fonts ? document.fonts.status === 'loaded' : true", timeout=15000)
        except Exception:
            pass
        page.wait_for_load_state("networkidle", timeout=30000)

        if cfg.get("preloader"):
            try:
                page.wait_for_selector("#preloader", state="detached", timeout=20000)
            except Exception:
                pass

        dismiss_overlays(page)
        inject_no_scrollbar(page)

        if cfg.get("nvidia"):
            renderer = page.evaluate(RENDERER_JS)
            log(f"[{pname}] renderer: {renderer}")
            if "NVIDIA" not in renderer.upper():
                context.close()
                browser.close()
                raise RuntimeError(
                    f"[{pname}] renderer is not the NVIDIA GPU ({renderer!r}); "
                    f"refusing (software fallback).")

        if cfg.get("load_wait_ms"):
            page.wait_for_timeout(cfg["load_wait_ms"])

        for s in sections:
            if s["kind"] == "static":
                capture_static(page, s)
            else:
                capture_loop(page, context, s, vp)

        context.close()
        browser.close()

    if do_process:
        for s in loops:
            process_loop(s)


def main():
    ap = argparse.ArgumentParser(description="Capture and process the section-card media.")
    ap.add_argument("--only", choices=list(PROJECT_CFG.keys()), help="one project")
    ap.add_argument("--section", help="a single section out-name (e.g. star-darkages)")
    ap.add_argument("--skip-capture", action="store_true", help="reuse existing raws")
    ap.add_argument("--skip-process", action="store_true", help="record raws only")
    args = ap.parse_args()

    sel = SECTIONS
    if args.section:
        sel = [s for s in SECTIONS if s["out"] == args.section]
    elif args.only:
        sel = [s for s in SECTIONS if s["p"] == args.only]

    # Group by project, preserving order.
    order = []
    for s in sel:
        if s["p"] not in order:
            order.append(s["p"])
    for pname in order:
        run_project(pname, [s for s in sel if s["p"] == pname],
                    not args.skip_capture, not args.skip_process)

    log("all done")


if __name__ == "__main__":
    main()
