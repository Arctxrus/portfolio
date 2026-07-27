# tools/ · build-only capture pipeline

Build-time tooling for the project preview clips. Nothing in this folder ships
to the page: the page only loads the processed files in `media/`. This folder
is safe to ignore in production and is not referenced by `index.html`,
`css/styles.css` or `js/main.js`.

`capture.py` records the three live demo sites with headed, GPU-backed Chromium
(Playwright), then post-processes each take with ffmpeg into the muted, looping
VP9 webm plus poster jpg that the panel's V2 views reference (CONCEPT.md
section 5). Raw recordings and ffmpeg pass logs are written to `tools/_raw/`,
which is gitignored.

## Prerequisites

- Python 3 with the `playwright` package, and the Chromium browser installed:
  `python -m playwright install chromium`
- `ffmpeg` and `ffprobe` on PATH.
- A real GPU for the WebGL take. The cosmic-dawn clip is refused unless the
  in-page WebGL renderer reports NVIDIA (guards against a software fallback).
  Confirmed here: `ANGLE (NVIDIA, NVIDIA GeForce RTX 3060 Laptop GPU ...
  Direct3D11)`.

## Re-record commands (demo push checklist)

Record these late, after the demo sites are final, and re-run on any demo push
that changes the visuals. Run from the repo root.

- Re-record and re-process all three:

      python tools/capture.py

- Re-record and re-process a single project:

      python tools/capture.py --only blackthorn
      python tools/capture.py --only barker
      python tools/capture.py --only star

- Re-encode only, reusing the existing raw takes in `tools/_raw/` (fast, no
  browser). Re-runs the crossfade, the head-anchor content scan and the poster;
  useful when tuning the loop or poster without re-recording:

      python tools/capture.py --skip-capture

- Record the raw takes only, skip ffmpeg:

      python tools/capture.py --skip-process

## What each take captures (owner amendment, round 4)

Every clip is now ONE continuous, even, SLOW scroll down the page, then a brisk
glide back to its start and a closing hold on the same opening composition. The
closing hold is crossfaded (0.8s) into the opening hold, so the loop is
seamless. Both endpoints are the same composition, so the dissolve is clean.

- `blackthorn` -> `media/blackthorn-preview.webm` + `blackthorn-poster.jpg`
  Slow scroll from the cover down the page, then back to the cover.
- `barker` -> `media/barker-bloom-preview.webm` + `barker-bloom-poster.jpg`
  Slow scroll from the hero through the pricing bento, then back to the hero.
- `star` -> `media/until-the-last-star-preview.webm` +
  `until-the-last-star-poster.jpg`
  Waits 10s after load for the WebGL scene to initialise, then a slow scroll
  through THE AFTERGLOW ("the fog lifts", timeline t 0.15 to 0.21): a warm
  plasma nebula, the brightest stable frame in the scene, so the poster is a
  bright, structured frame (not the old near-black long-night shot). Recorded
  headed on the GPU (renderer confirmed NVIDIA). No camera parallax, no crop.

## Loop technique

- The crossfade folds the tail (closing hold) into the head (opening hold);
  output length = base clip minus `CROSSFADE_S` (0.8s). See `encode_crossfade`.
- The demo heros play a one-time load-in animation, so the take waits it out
  (`settle_ms`) and warms the hero to its settled base state before the keeper
  (a scroll excursion and back; `warmup: True`). The star (WebGL) skips this.
- `choose_head_ss` picks the crossfade head CONTENT-first: it scans the start of
  the take for the window that best matches the settled closing hold. This does
  not trust the recorded video timeline to align with the wall-clock keeper
  offset (Playwright records a non-linear timeline), which is why a fixed-offset
  anchor failed and a content match is used instead.

## Output shape and budget

- Native 1280x720 (16:9), VP9, no audio, 30fps. Length amended to roughly 10 to
  20s (owner, round 4) to keep the scroll slow; the shipped clips run ~16 to 17s.
- VP9 CRF quality mode (`DEFAULT_CRF = 34`). Sizes grow with the longer, busier
  scrolls (accepted by owner direction); the clips stay lazy-loaded, so the
  first-load budget is untouched. Poster jpgs are 1280 wide, under about 80KB
  (`POSTER_MAX_KB`).
- The scrollbar is suppressed before recording (`NO_SCROLLBAR_CSS`), so no frame
  shows the demo site's scrollbar.
- `object-fit: cover` handles the mobile 2/1 box; the desktop project view shows
  the clip large with a bottom fade cue.

## Tuning knobs

All per-project settings live in the `PROJECTS` list in `capture.py`: the `tour`
(`from`/`to` as a pixel offset or a `{"t": frac}` cosmic-dawn timeline fraction,
`tour_dur_ms`, `return_dur_ms`, the open/close hold ms), `settle_ms`, `warmup`,
and `extra_load_wait_ms`. `CROSSFADE_S`, `KEYFRAME_INTERVAL` and `DEFAULT_CRF`
are module constants.
