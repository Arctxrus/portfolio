# tools/ · build-only capture pipeline

Build-time tooling for the project preview clips. Nothing in this folder ships
to the page: the page only loads the processed files in `media/`. This folder
is safe to ignore in production and is not referenced by `index.html`,
`css/styles.css` or `js/main.js`.

`capture.py` records the three live demo sites with headed, GPU-backed Chromium
(Playwright driving a CDP `Page.startScreencast` at ~60 to 90 fps), then
post-processes each take with ffmpeg into the muted, looping VP9 webm plus poster
jpg that the panel's V2 views reference (CONCEPT.md section 5). Raw takes (a
60fps CFR intermediate rebuilt from the timestamped screencast frames) are
written to `tools/_raw/`, which is gitignored.

Client feedback round 5 (2026-07-27): the capture was moved off Playwright's
`recordVideo` (which delivered only ~15 to 25 UNIQUE fps under load, juddering on
slow pans) to CDP screencast (a true ~60 unique fps through motion). The
recording viewport is now SQUARE-ISH (1000x1040 at deviceScaleFactor 2) so the
near-square desktop preview box crops almost nothing, and the output is 1500x1560
so the box gets native-or-better pixels (no more upscale blur). See the block
comments at the top of `capture.py` for the measured diagnosis.

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
  through THE AFTERGLOW ("the fog lifts", timeline t 0.13 to 0.17): a warm
  plasma nebula, the brightest sustainable span in the scene, so the poster is a
  bright, structured frame (not the old near-black long-night shot). Recorded
  headed on the GPU (renderer confirmed NVIDIA). No camera parallax, no crop.

## Loop technique

- The crossfade folds the tail (closing hold) into the head (opening hold);
  output length = base clip minus `CROSSFADE_S` (0.8s). See `encode_crossfade`.
- The demo heros run scroll-reveal animations that re-fire when scrolled back
  into view, so the take warms the hero to its settled scroll-return base state
  before the keeper (`warmup: True`, then `warmup_settle_ms` lets the reveals
  settle) so the opening hold matches the scroll-return closing hold. The star
  (WebGL) skips the warmup.
- Round 5: the screencast only sends a frame on visual change, so a static hold
  is ONE frame held for its whole duration; the raw-assembly duration clamp is
  set above the hold length so those holds are preserved (else the crossfade
  loses its static window). `choose_head_ss` picks the crossfade head CONTENT-
  first but is BOUNDED to the opening hold, so the head shares the tail's scroll
  position (for the star, a diffuse plasma dissolve at the same position, not a
  roam to a mid-tour frame).

## Output shape and budget

- 1280x1344 (square-ish, ratio 0.952), VP9 PROFILE 0 (yuv420p), no audio, 30fps.
  Captured at a 1000x1040 viewport at deviceScaleFactor 2 (raw 2000x2080),
  downscaled to 1280 wide. Length roughly 15 to 17s.
- PLAYBACK SMOOTHNESS (2026-07-28): the first round-5 cut was 1500x1560 at 60fps
  and, being VP9 profile 1 (yuv444p, forced by the xfade filter), dropped 31 to
  45% of frames to SOFTWARE decode in-browser. Fixed by pinning yuv420p (profile
  0, hardware-decodable, half the chroma - the biggest win; see `vp9_args`),
  halving to 30fps, and using MOD-16 dimensions.
- HARDWARE DECODE (2026-07-28): that cut still hit MediaError code 3
  PIPELINE_ERROR_DECODE on the GPU path because scaling the 1000x1040 screencast
  raw to a non-matching 1280x1344 left a fractional SAR (323:320, videoWidth 1292)
  and the raw's full-range/bt470bg colour carried through - both rejected by
  hardware VP9. `vfilter` now forces `setsar=1:1` (square pixels, videoWidth 1280)
  and CONVERTS full-range/bt601 to tv-range/bt709 (`in_range/out_range` +
  `in/out_color_matrix`), and `encode_crossfade`/`vp9_args` stamp tv + bt709
  matrix/primaries/transfer so pixels and tags agree. Verified in headed GPU
  Chromium: no MediaError, 0% dropped in the steady-state window.
  NOTE: CDP screencast returns CSS-pixel frames, so the raw is 1000 wide (the
  deviceScaleFactor does not enlarge it) and the 1280-wide output is a mild upscale.
- VP9 CRF quality mode (`DEFAULT_CRF = 34`). The clips stay lazy-loaded, so the
  first-load budget is untouched. Poster jpgs are 1280 wide, under 100KB
  (`POSTER_MAX_KB = 98`).
- The scrollbar is suppressed before recording (`NO_SCROLLBAR_CSS`), so no frame
  shows the demo site's scrollbar.
- `object-fit: cover` handles the mobile 2/1 box (the square-ish source shows its
  middle band there; the hero still reads); the desktop project view shows the
  clip large with a bottom fade cue and now crops only ~8% top/bottom.

## Tuning knobs

All per-project settings live in the `PROJECTS` list in `capture.py`: the `tour`
(`from`/`to` as a pixel offset or a `{"t": frac}` cosmic-dawn timeline fraction,
`tour_dur_ms`, `return_dur_ms`, the open/close hold ms), `settle_ms`, `warmup`,
`warmup_settle_ms`, and `extra_load_wait_ms`. `REC_W`/`REC_H`, `DPR`,
`OUT_W`/`OUT_H`, `FPS`, `CROSSFADE_S`, `KEYFRAME_INTERVAL` and `DEFAULT_CRF` are
module constants.
