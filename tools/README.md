# tools/ · build-only capture pipeline

Build-time tooling for the project SECTION CARDS. Nothing in this folder ships to
the page: the page only loads the processed files in `media/`. This folder is safe
to ignore in production and is not referenced by `index.html`, `css/styles.css` or
`js/main.js`.

Client feedback round 6 (2026-07-27): the single per-project "tour" webm is retired.
Each project now opens a DETAIL state with a scrollable stack of SECTION CARDS, so
`capture.py` captures 3 to 5 sections per project as either a STATIC image or a
SHORT LOOP. The old tour functions are gone; the hardened encode plumbing they
shared (CDP screencast capture, the tail->head crossfade, `choose_head_ss`, the
VP9 Profile-0 / SAR / bt709 args, poster export) is kept.

## Prerequisites

- Python 3 with the `playwright` package and Chromium:
  `python -m playwright install chromium`
- `ffmpeg` and `ffprobe` on PATH (Pillow + numpy for the loop-seam check).
- A real GPU for the WebGL takes. The cosmic-dawn sections are refused unless the
  in-page WebGL renderer reports NVIDIA (guards against a software fallback).
  Confirmed here: `ANGLE (NVIDIA, NVIDIA GeForce RTX 3060 Laptop GPU ... Direct3D11)`.

## Commands (demo push checklist)

Re-run on any demo push that changes the visuals. Run from the repo root.

- Everything (all sections, all projects):

      python tools/capture.py

- One project's sections:

      python tools/capture.py --only blackthorn
      python tools/capture.py --only barker
      python tools/capture.py --only star

- A single section by its out-name:

      python tools/capture.py --section star-last

- Re-process the loops only, reusing the raws in `tools/_raw/` (fast, no browser):

      python tools/capture.py --skip-capture

- Record raws only, skip ffmpeg:

      python tools/capture.py --skip-process

## Section plan

The plan lives in the `SECTIONS` list in `capture.py` (each entry: project, out
name, `kind`, a `pos` locator, `settle_ms`, and for loops `record_ms` + optional
`script`). It was chosen after inspecting each live site; loop vs static follows the
brief's rule (loop only for sections that genuinely cycle at rest).

- `blackthorn` (all STATIC: none of these sections cycles; the reviews carousel is
  manual): `blackthorn-cover`, `-prices`, `-barbers`, `-reviews`, `-booking`.
- `barker` : `barker-hero` (STATIC: the paw trail draws once, no rest loop),
  `barker-prices` (STATIC), `barker-beforeafter` (LOOP: the compare slider is
  scripted to sweep, `BA_SWEEP_JS`), `barker-booking` (STATIC).
- `star` (all LOOP: the WebGL scene animates continuously), parked at three bright
  epochs after a 10s load wait: `star-first` (t 0.40, "A star is lit"),
  `star-web` (t 0.52, "Structure, everywhere"), `star-last` (t 0.88, the lensed
  black hole finale). NVIDIA renderer re-confirmed in-context before each session.

## Output shape and budget

- STATIC: a DPR-2 screenshot of the 16:9 recording viewport (2560x1440) downscaled
  to `STATIC_W`x`STATIC_H` (1600x900), jpg quality stepped up until under
  `STATIC_MAX_KB` (290KB). All well under 300KB.
- LOOP: `OUT_W`x`OUT_H` (1280x720, 16:9, mod-16), VP9 Profile 0 (yuv420p), 30fps,
  SAR 1:1, tv-range/bt709, no audio - the same hardware-decodable hardening as
  round 5. A tail->head crossfade (`CROSSFADE_S` 0.8s) makes the loop seamless;
  `choose_head_ss` picks the crossfade head content-first near the start (a diffuse
  plasma dissolve for the continuously-animating WebGL, a near-exact match for the
  periodic before/after sweep). Poster jpg = frame 0, 1280 wide, under
  `POSTER_MAX_KB` (98KB).
- The scrollbar is suppressed before recording (`NO_SCROLLBAR_CSS`).
- All section media is 16:9 and `object-fit: cover` in the card, so nothing crops.
- CDP screencast returns CSS-pixel frames, so a loop raw is `REC_W` (1280) wide;
  statics use `page.screenshot`, which does honour `device_scale_factor` (DPR 2).

## Tuning knobs

Per-section settings live in `SECTIONS`. `REC_W`/`REC_H`, `DPR`, `OUT_W`/`OUT_H`,
`STATIC_W`/`STATIC_H`, `FPS`, `CROSSFADE_S`, `KEYFRAME_INTERVAL`, `DEFAULT_CRF`,
`POSTER_MAX_KB` and `STATIC_MAX_KB` are module constants. Loop raws (a 30fps CFR
H.264 intermediate rebuilt from the timestamped screencast frames) are written to
`tools/_raw/`, which is gitignored.
