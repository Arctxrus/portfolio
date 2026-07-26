# PROGRESS — Zayn Portfolio

Stage log, decisions and deviations for the build defined in CONCEPT.md.
House rules: UK English, no em dashes, instrument then fix, commit per stage.

## Open items

- [ ] Replace placeholder email. `hello@placeholder.invalid` is used everywhere the
      spec says REPLACE email. It lives in a single constant (`SITE_EMAIL` in
      js/main.js, mirrored once in index.html for the no-JS footer text). Swap
      before deploy.
- [ ] Panel sub lines for the three projects: drafted at stage 3, need approval.
- [ ] About and Pricing prose: drafted at stage 3, need approval.
- [ ] docs/de-vibe-audit.md: the agreed checklist was not supplied in this
      workspace. A draft checklist will be written at stage 8 and submitted for
      approval before the audit runs.
- [ ] Formspree endpoint ID: form is wired with a placeholder endpoint constant;
      real ID needed before deploy.
- [ ] Stage 6 video capture depends on the live demo sites and headed Chromium
      with GPU; may be marked blocked with exact local commands.
- [ ] Stage 10 waits on the confirmed deployed URL.

## Decisions and deviations

- 2026-07-26: Agent files requested with model "claude-opus-5" for the coder.
  No such model exists; the coder is set to `opus` (resolves to the latest
  Opus, currently 4.8). Verifier and triage use `sonnet` (Sonnet 5) as asked.
- 2026-07-26: Email placeholder `hello@placeholder.invalid` adopted per
  instruction, single-constant, listed above as an open item.

## Stage log

### Setup (2026-07-26)
- Repo initialised, GitHub repo Arctxrus/portfolio created, CONCEPT.md committed.
- PROGRESS.md, verify/, references/REFERENCES.md created.
- Agent team created in .claude/agents/ (coder, verifier, triage).

### Stage 1 — Scaffold
- Status: VERIFIED PASS (verifier run 2026-07-26, 0 FAILs, screenshots in
  verify/stage-1/). Carry-forward flag: --grey-label and --grey-soft text on
  --ground is below WCAG AA at desktop rest; CONCEPT section 10 scopes the
  remediation to mobile-at-rest and focus (stage 5), and the item must be
  re-checked at the de-vibe gate (stage 8).
- Files created: index.html, css/styles.css, js/main.js, media/.gitkeep,
  fonts/archivo-latin-var.woff2, fonts/martian-mono-latin-var.woff2. All asset
  references cache-busted ?v=1.
- Tokens: the full :root block from CONCEPT 3.1 is in styles.css verbatim.
- Fonts self-hosted (variable woff2, latin subset, font-display: swap). Source
  URLs recorded in a comment at the top of styles.css:
  - Archivo 400..600: gstatic archivo/v25/...sLydOxI.woff2 (34.9KB)
  - Martian Mono 300..500: gstatic martianmono/v6/...aTq9wQ.woff2 (23.6KB)
  Fetched via the Google Fonts CSS v2 API with a desktop Chrome user agent
  (PowerShell Invoke-WebRequest; git-bash curl failed TLS handshake, exit 35).
- Dot grid canvas: fixed, aria-hidden, DPR-aware, resize-safe (throttled, no
  layout shift). Per-dot exponential lerp toward --dot-warm within 100px,
  alpha 0.06 to 0.48 at ~12%/frame, rAF loop. Guards: under
  prefers-reduced-motion and touch-only ((hover: none) and (pointer: coarse))
  no mousemove listener is bound and the grid stays static.
- Static desktop layout per 3.1; left column flex with proof strip pinned via
  margin-top auto; panel V1 shown statically (header, giant ghost glyph,
  welcome line). Rows are real buttons at R1 rest with focus-visible accent
  ring. Testimonials slot present with `hidden` and real styles, no content.

Verified programmatically in-pane (no screenshot: browser pane tab stays
document.hidden, screenshots time out and rAF is paused there): DOM tree
correct; both fonts report document.fonts.check true; computed type specs
match (name 31px/600/-0.015em, positioning 16px/1.6, £300 mono accent, welcome
glyph 340px/lh 0.8); grid 460px/1fr, gap 80px, padding 76/76/56; canvas paints
dots at rest; testimonials display:none; footer mailto + year 2026 wired from
SITE_EMAIL; no console errors.

### Stage 1 deviations / judgement calls
- Expand glyph: chose a single "+" character in the system font stack, reused
  in rows, CTA and the welcome state (one consistent treatment per 3.2).
- CTA row 06 given a static --accent-fill-hover pill as its structural rest
  placeholder. Drift layers, white rim, edge lift, hover mist and press bloom
  are deferred to stage 2 exactly per this stage's brief.
- Copyright line included in the footer ("© <year> Zayn", year from JS) to
  satisfy section 9; kept small and secondary to stay minimal per section 4.
- Niche tag colour set to --grey-soft (#A6A6AE) per the prototype and the
  section 10 note. This is below WCAG AA on --ground at rest; flagged for the
  stage 5 / accessibility remediation (darken on mobile-at-rest and focus).
- Font families are not tokenised in CONCEPT 3.1, so --font-sans/--font-mono/
  --font-system are declared in a separate :root below the verbatim token
  block, leaving 3.1 untouched.
- Added a synchronous static paint in the dot-grid resize() so the grid is
  never blank before the first rAF (belt-and-braces, no behavioural change to
  the animated tint).

### Stage 2 - Left column complete
- Status: BUILT, awaiting verification. All asset references bumped ?v=1 to
  ?v=2 (css link, js script, two @font-face src). Files changed: index.html,
  css/styles.css, js/main.js.

- Decode/scramble (main.js initDecode + scrambleElement): chars resolve left
  to right via rAF, 650ms, linear reveal per frame, on mount, once. Guarded by
  data-scrambleDone so it never re-fires. Whitespace is held in place (also
  keeps monospace widths fixed, so no layout shift). Reduced motion: skipped
  entirely, the final text already in the HTML stays. Pool is uppercase
  alphanumerics plus "/ # *".
  data-scramble elements chosen (all short mono UPPER labels, so the decode
  reads as a coherent "system labels booting" motif and monospace guarantees
  zero width shift): the welcome line "Select a project" (required by 3.4 V1),
  the name kicker "Freelance / Web", both section labels "Index" and
  "How it works", and the panel header label "Preview / No selection".
  Deliberately NOT scrambled: the numeric row indices and niche tags (tied to
  row states, would be busy), the proof strip (long, body-like) and prose.

- Block fade-in (CSS .fade-block + main.js initFadeIn): opacity 0 to 1,
  translateY 6px to 0, 500ms ease. Initial state and transition in CSS;
  per-block stagger delay set inline via --fade-delay. Seven blocks mapped to
  the seven spec delays: name-block 0, positioning 120, index 180, how 240,
  proof 320, footer 350, panel 400 (ms). JS flips .is-in after a double rAF so
  the from-state paints first. Transform+opacity only, so no post-load layout
  shift. Reduced motion: CSS forces the blocks visible with no transition.

- Rows 01 to 05 states (CSS): R1 rest unchanged from stage 1. R2 hover
  (:not(.row--cta):hover) fill --accent-fill-hover, --shadow-row-hover, index
  to accent, name to ink, tag opacity to 0, glyph opacity 0 to 1 with x -4px
  to 0; colour/opacity/glyph 160ms, background 160ms, shadow 220ms (from the
  .row base transition). R3 active (.is-active) fill --accent-fill-active,
  index accent, name ink, tag hidden, glyph shown, no shadow (so no trails
  implication) unless also hovered. R4 = .is-active plus :hover: active fill
  wins (rule ordered after :hover) and the hover shadow still applies.
  Selection in main.js initRowSelection: one active row at a time, real
  buttons (enter/space native), aria-pressed reflects the active row. The
  panel is intentionally untouched (stage 3).

- Row pointer trails (CSS .trail-dot + main.js initRowTrails): 12px dot, blur
  12px, colours alternate --trail-a / --trail-b, opacity driven by WAAPI over
  a 2200ms lifetime with offsets at 0, 20ms (delay), 320ms (peak
  --trail-opacity 0.32), 1000ms (hold), 2200ms (0); node removed on finish.
  Spawn throttled to at most every 100ms. Fixed to the viewport at the cursor.
  Not bound at all under reduced motion; each move ignored when pointerType is
  touch.

- CTA pill row 06 (CSS .row--cta + main.js initCta), replacing the stage 1
  placeholder. C1 rest: three drift layers (--cta-layer1/2/3 at --cta-bg-size)
  on the button background with cta-drift 22s ease-in-out infinite (2D
  four-point background-position path); light pass (--cta-lightpass) on
  ::before with cta-lightpass 30s (2D reverse path); static edge lift
  (--cta-edge-lift) on ::after; white inset rim --cta-rim; ink text
  --cta-text; index --cta-index; radius --radius-pill; overflow hidden to clip
  the press bloom. C2 hover: drift to 14s, light pass to 19s, filter
  saturate(1.25) brightness(1.03) over 240ms, plus hover mist (--cta-hover-mist
  node) following the cursor with a 900ms lag via CSS transition
  cubic-bezier(0.22,0.61,0.36,1), opacity 0 to 0.5 in 420ms; placed instantly
  on enter so it does not slide in from the corner. C3 press: one press bloom
  per pointerdown from the exact pointer/tap point (--cta-press-mist), scale
  0.25 to 1, opacity 0 to 0.5 to 0 over 600ms ease-out via WAAPI, node removed
  at 700ms; no scale on the pill itself. C5: no persistent selected class on
  the CTA (its click never sets .is-active). Reduced motion: CSS sets drift and
  light pass animation:none with a static background-position; hover mist not
  bound; press bloom handler returns before spawning. Touch: mist not rendered;
  press bloom does fire from the tap point (no touch guard on pointerdown).

### Stage 2 deviations / judgement calls
- Light-pass layer needs a background-size and there is no token for it; used a
  literal 200% 200% with a comment (the three drift-layer sizes use the
  --cta-bg-size token as specified).
- CTA decorative layers use ::before (light pass), ::after (edge lift) and the
  button background (drift); the label spans are lifted with .row--cta > *
  { position: relative; z-index: 5 } so text stays above every glow. Mist
  (z-index 2) and bloom (z-index 3) sit below the text, above the fill.
- Trail dots are position:fixed on <body> at z-index 2 (above page content);
  the 12px blur at 0.32 max opacity keeps row text legible. Chosen over
  per-row absolute nodes to avoid overflow clipping and neighbour overlap.
- aria-pressed is set on the index rows to expose the single-selection state
  to assistive tech now; stage 3 adds the aria-live panel announcement.
- Verification note: the Browser pane could not evaluate this file (file://
  tab stays document.hidden; javascript_tool timed out, same limitation logged
  at stage 1). JS was syntax-checked with `node --check` (pass). Full
  behavioural verification is left to the verifier subagent.
