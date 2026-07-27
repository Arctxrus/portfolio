#!/usr/bin/env python3
"""Capture pipeline for the three project preview clips (CONCEPT.md section 5).

Build-time tool only. This script ships nothing to the page: it records the
three live demo sites with headed, GPU-backed Chromium (Playwright), then
post-processes each raw take with ffmpeg into the muted, looping VP9 webm plus
poster jpg that index.html already references from media/.

Two stages, either of which can run alone:
  1. capture  - scripted, headed recording of each site to tools/_raw/
  2. process  - ffmpeg trim, crop to 16:9, scale to 800px, strip audio,
                VP9 to a size-tuned target, and a poster jpg from frame 0

Usage (run from anywhere, paths are resolved from this file):
  python tools/capture.py                 # capture then process, all three
  python tools/capture.py --only star     # just Until the Last Star
  python tools/capture.py --skip-capture  # re-encode from existing raw takes
  python tools/capture.py --skip-process  # record raw takes only

House rules: UK English, no em dashes. Vanilla toolchain, no runtime deps.
"""

import argparse
import os
import subprocess
import time

# Resolve repo paths from this file so the script is location independent.
TOOLS_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.dirname(TOOLS_DIR)
MEDIA_DIR = os.path.join(REPO_ROOT, "media")
RAW_DIR = os.path.join(TOOLS_DIR, "_raw")

# Recorded viewport (CONCEPT: about 1280x800). Output is cropped to 16:9 and
# scaled to 800px wide, matching the panel preview box aspect ratio so the
# clip fills the desktop 16/9 frame with no crop (object-fit: cover then only
# trims the small extra height at the mobile 2/1 ratio).
REC_W, REC_H = 1280, 800

# ANGLE D3D11 on the discrete GPU, so the WebGL demo records its real visuals
# rather than a software fallback. Confirmed renderer: ANGLE NVIDIA RTX 3060.
GPU_ARGS = [
    "--use-angle=d3d11",
    "--enable-gpu-rasterization",
    "--enable-zero-copy",
    "--ignore-gpu-blocklist",
    "--disable-features=CalculateNativeWinOcclusion",
]

# The size budget per clip (CONCEPT section 5): VP9, about 800px wide, 6 to 8
# seconds, loop friendly, 300 to 500KB. Posters must stay small (under ~40KB).
WEBM_MIN_KB, WEBM_MAX_KB = 300, 500
POSTER_MAX_KB = 40

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
        "bitrate": "430k",
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
        "bitrate": "470k",
    },
    {
        "name": "star",
        "url": "https://arctxrus.github.io/cosmic-dawn/",
        "out": "until-the-last-star-preview",
        "poster_out": "until-the-last-star-poster",
        # One epoch transition with lensing visible: First Light into The Web,
        # the cosmic web of galaxies lensed along dark-matter filaments.
        "start_y": 9600,
        "settle_ms": 1800,          # WebGL needs time to catch the jumped scroll
        "segments": [
            {"hold_ms": 800},          # First Light settled
            {"to": 12600, "dur_ms": 3600},  # transition into The Web (lensing)
            {"hold_ms": 1800},         # cosmic web held
        ],
        "verify_nvidia": True,
        "clip_len_s": 6.0,
        "bitrate": "520k",
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

        dismiss_overlays(page)

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

        # Move to the start scroll position and let a scroll-driven scene catch up.
        page.evaluate("y => window.scrollTo(0, y)", project["start_y"])
        page.wait_for_timeout(project["settle_ms"])

        # Keeper begins now. Record the offset into the video so ffmpeg can trim
        # to the scripted window.
        keeper_offset_s = time.monotonic() - t_ctx
        log(f"[{project['name']}] keeper starts at ~{keeper_offset_s:.2f}s into the take")

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


def vfilter():
    # Centre crop the 1280x800 take to 16:9 (drop 40px top and bottom), then
    # scale to 800x450. object-fit: cover in the panel handles the mobile 2/1.
    return f"crop={REC_W}:{int(REC_W * 9 / 16)}:0:{(REC_H - int(REC_W * 9 / 16)) // 2},scale=800:450"


def encode_webm(raw, out, ss, dur, bitrate):
    """Two-pass VP9 to a target bitrate. Audio stripped, 30fps, keyframed."""
    passlog = os.path.join(RAW_DIR, "vp9pass")
    common = [
        "ffmpeg", "-y", "-ss", f"{ss:.3f}", "-t", f"{dur:.3f}", "-i", raw,
        "-an", "-vf", vfilter(), "-r", "30",
        "-c:v", "libvpx-vp9", "-b:v", bitrate,
        "-deadline", "good", "-cpu-used", "1",
        "-auto-alt-ref", "1", "-lag-in-frames", "25",
        "-g", "60", "-row-mt", "1",
    ]
    run(common + ["-pass", "1", "-passlogfile", passlog, "-f", "null", os.devnull])
    run(common + ["-pass", "2", "-passlogfile", passlog, out])


def parse_bitrate(bitrate):
    return int(bitrate.rstrip("kK")) if bitrate.lower().endswith("k") else int(bitrate) // 1000


def encode_webm_tuned(raw, out, ss, dur, bitrate):
    """Encode, then nudge the bitrate once if the size misses the budget."""
    encode_webm(raw, out, ss, dur, bitrate)
    size = kb(out)
    log(f"    first VP9 pass at {bitrate}: {size:.0f}KB")
    if WEBM_MIN_KB <= size <= WEBM_MAX_KB:
        return bitrate, size
    # Scale the bitrate toward the middle of the budget and re-encode once.
    mid = (WEBM_MIN_KB + WEBM_MAX_KB) / 2.0
    br_kbps = parse_bitrate(bitrate)
    new_kbps = max(120, int(br_kbps * mid / max(size, 1)))
    new_br = f"{new_kbps}k"
    log(f"    out of budget, retuning bitrate {bitrate} -> {new_br}")
    encode_webm(raw, out, ss, dur, new_br)
    size = kb(out)
    log(f"    retuned VP9: {size:.0f}KB at {new_br}")
    return new_br, size


def make_poster(webm, poster):
    """Frame 0 of the processed clip as a jpg, quality tuned under the budget."""
    chosen = None
    for q in (3, 4, 5, 6, 8, 10, 12, 15):
        run([
            "ffmpeg", "-y", "-i", webm, "-frames:v", "1",
            "-q:v", str(q), "-vf", "scale=800:450", poster,
        ])
        size = kb(poster)
        chosen = (q, size)
        if size <= POSTER_MAX_KB:
            break
    log(f"    poster q={chosen[0]}: {chosen[1]:.0f}KB")
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

    log(f"[{project['name']}] encoding webm  (raw {raw_dur:.2f}s, ss={ss:.2f}s, len={dur:.1f}s)")
    br, size = encode_webm_tuned(raw, out, ss, dur, project["bitrate"])
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
