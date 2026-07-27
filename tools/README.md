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
  browser, useful when only tuning bitrate, trim or poster quality):

      python tools/capture.py --skip-capture

- Record the raw takes only, skip ffmpeg:

      python tools/capture.py --skip-process

## What each take captures

- `blackthorn` -> `media/blackthorn-preview.webm` + `blackthorn-poster.jpg`
  Glide from the cover, through the price menu, to the rotating pull-quote.
- `barker` -> `media/barker-bloom-preview.webm` + `barker-bloom-poster.jpg`
  Hero, the paw-trail thread drawing on scroll, a peek at the pricing bento.
- `star` -> `media/until-the-last-star-preview.webm` +
  `until-the-last-star-poster.jpg`
  One epoch transition with lensing visible: First Light into The Web, the
  cosmic web of galaxies lensed along dark-matter filaments. Recorded headed
  with the GPU so the real visuals are captured.

## Output shape and budget

- Native 1280x720 (16:9), VP9, no audio, 30fps, 6 to 8 seconds.
- Client feedback round 2 (2026-07-27): the clips are exported at native
  1280x720 (no downscale) in VP9 CRF quality mode (`DEFAULT_CRF = 34`, within
  the sanctioned 32 to 34) so they stay crisp at full panel size. The 300 to
  500KB per-clip budget is AMENDED by owner direction: quality wins, each clip
  is kept as small as CRF makes it while crisp. Clips stay lazy-loaded, so the
  first-load budget is untouched. Poster jpgs are exported at 1280 wide, under
  about 80KB.
- The scrollbar is suppressed before recording (`NO_SCROLLBAR_CSS`, injected via
  `page.add_style_tag`), so no frame shows the demo site's scrollbar.
- `object-fit: cover` handles the mobile 2/1 box (trims the extra height); the
  desktop project view shows the clip large with a bottom fade cue.

## Tuning knobs

All per-project settings live in the `PROJECTS` list in `capture.py`: the
scroll `segments` (eased scrollTo targets and static holds), `clip_len_s`,
`bitrate`, and the `start_y` / `settle_ms` for scroll-driven scenes. The trim
is anchored to the end of each raw take (its closing hold), which is robust
against Playwright recording a timeline shorter than wall-clock.
