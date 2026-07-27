# PROGRESS · Zayn Portfolio

Stage log, decisions and deviations for the build defined in CONCEPT.md.
House rules: UK English, no em dashes, instrument then fix, commit per stage.

## Open items

- [ ] OPEN BLOCKER (gates outreach, not deploy, per Zayn 2026-07-27):
      replace placeholder email. `hello@placeholder.invalid` is the single
      constant `SITE_EMAIL` in js/main.js, which populates every on-page use.
      SECOND LITERAL OCCURRENCE (added in the approval round, deviation 5c): the
      no-JS `<noscript>` fallback in index.html hard-codes the same address
      (mailto link + visible text), because with JS off it cannot read the
      constant. When the real address lands, edit BOTH: `SITE_EMAIL` in
      js/main.js AND the literal in the index.html `<noscript>` (a comment there
      points back to SITE_EMAIL).
- [ ] OPEN BLOCKER (gates outreach, not deploy, per Zayn 2026-07-27):
      Formspree endpoint ID. Until it exists the submit path short-circuits to
      the graceful failure state pointing at the email line.
- [ ] OPEN BLOCKER (gates outreach): the canonical 14-item de-vibe audit list
      arrived as an unfilled paste placeholder in the approval message; the
      House Tier was approved and run instead. Paste the canonical list into
      docs/de-vibe-audit.md and run the full audit before outreach.
- [x] Panel sub lines: APPROVED 2026-07-27 as drafted.
- [x] About and Pricing prose: APPROVED 2026-07-27, one amendment applied
      ("physics graduate" to "astrophysics graduate").
- [x] De-vibe checklist structure: House Tier approved 2026-07-27; canonical
      14-item list still awaited (see OPEN BLOCKER above).
- [x] Stage 6 video capture: DONE. The three webm previews and poster jpgs are
      recorded, processed and integrated (see the Stage 6 log). Re-record on any
      demo push via tools/README.md; add "re-record clips" to the push checklist.
- [x] /favicon.ico 404 (flagged at stage 6): RESOLVED at stage 7. rel=icon
      links are declared; a headed probe confirmed Chromium fetches favicon.svg
      and no longer requests /favicon.ico. No favicon.ico added.
- [ ] Stage 10 waits on Zayn confirming the deployed URL loads for him:
      https://arctxrus.github.io/portfolio/ (deployed 2026-07-27, Pages built,
      all assets 200, live smoke clean). When the final URL is known,
      update the CANONICAL SITE URL comment plus og:url, og:image and
      twitter:image in index.html together (they carry the domain literally).

## APPROVED COPY (was DRAFT FOR APPROVAL)

Approved by Zayn 2026-07-27 with one amendment: in the About prose,
"physics graduate" becomes "astrophysics graduate". Everything else as
drafted. Sub lines, Pricing lines and the honest-floors note approved
verbatim.

Panel sub lines (mono, lower case, middle dot separators):
- Blackthorn & Co.: `single page · price menu · booking form · arctxrus.github.io/blackthorn-demo`
  (verified: one page with anchor nav, a priced service menu, and a real
  booking form with phone + date fields, id "booking-form".)
- Barker & Bloom: `single page · prices by dog size · booking form · arctxrus.github.io/barker-bloom-demo`
  (verified: one page, a prices-by-size section, and a stepper booking request
  form, id "bookForm".)
- Until the Last Star: `webgl · scroll-driven timeline of the universe · arctxrus.github.io/cosmic-dawn`
  (verified: Three.js WebGL canvas scene, scroll-driven timeline from the first
  instant to the death of the last star.)

About (V3, ~51 words):
> I'm Zayn, an astrophysics graduate who shipped a game played by more than
> three million people. These days I build fast, polished websites for local
> businesses, the kind of shop or salon that deserves better than the usual
> off-the-peg site. I work quickly and directly: no agencies, no templates,
> no jargon.

Pricing (V3, three mono-labelled lines plus an honest-floor note):
- WEBSITES FROM £300 - A single page, written and built for your business.
- CARE PLAN FROM £25/MONTH - Hosting, edits, and keeping it fast.
- FREE HOMEPAGE MOCKUP - Reply to the email and see it before you pay.
- Note: `"From" prices are honest floors: a bigger job is quoted higher.`

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

### Stage 1 · Scaffold
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

### Stage 3 - Panel views (V1 to V5), keyboard, aria-live
- Status: BUILT, awaiting verification. All asset references bumped ?v=2 to
  ?v=3 (css link, js script, two @font-face src). New media references in the
  view templates carry ?v=3. Files changed: index.html, css/styles.css,
  js/main.js, PROGRESS.md.

- View system: V1 welcome stays in the markup as the initial panel content.
  V2 (three projects), V3 (About, Pricing) and V4 (form) live as
  `<template id="view-...">` blocks at the end of index.html and are cloned
  into `.panel-body` by main.js `initPanel` on selection. This keeps the real
  markup in HTML (verifier-visible, tokens in CSS) and gives natural
  lazy-loading: a project's placeholder video only enters the DOM when its row
  is chosen (section 5).

- V2 project view: framed preview area (16/9, `--surface-preview`, 1px
  `--border`, `--radius-surface`) that is itself an anchor to the live URL
  (target _blank, rel noopener); a `<video>` inside with poster wired to the
  future media path and autoplay/muted/loop/playsinline/preload="none" per
  section 5, source pointing at the future webm. Then project title (Archivo
  34px/600/-0.015em), mono sub line (10.5px lower), a caption bar with a 1px
  top rule (mono 10.5px/0.04em/UPPER, exact section-4 captions), and a quiet
  secondary "Visit live site" pill (ink outline, `--radius-pill`, NOT the CTA
  treatment) to the same URL, target _blank rel noopener.

- Placeholder media: the real webm/poster arrive at stage 6. Until then the
  framed `--surface-preview` box is the placeholder. A `<video>` whose poster
  and source 404 shows no broken-image icon (unlike `<img>`); the styled
  surface shows instead. Verified over http: the webm requests return 404 as
  expected and there are no console errors. Stage 6 drops the files in at the
  same paths; no markup change needed.

- V3 About/Pricing views: as V2 without a caption bar. About is a single
  Archivo 14px paragraph (~51 words, section-6 shape: two sentences on who,
  one on how). Pricing is three mono-labelled lines (no table, no cards) with
  the "£" figures in accent, plus a small honest-floor note. Drafts recorded
  above.

- V4 form view: white card, `--radius-surface` 16px, 440px wide, centred in
  the body. Mono "GET IN TOUCH" label; three fields (Name, Business, textarea
  rows=4 resize:none "What do you need built?") with F1 rest
  (`--surface-field` + `--border`), F2 focus (accent border, white background,
  inset accent ring `--shadow-field-focus`, no outer halo, 150ms) and F3
  filled via `:not(:placeholder-shown)`. Submit pill uses `--submit-ink`,
  white 600 label, no border/shadow, hover to `--submit-ink-hover` in 150ms,
  no press state, label "Send · I typically reply same day". POST skeleton in
  place (method="post", action="" for the Formspree endpoint, name attributes,
  honeypot `_gotcha`); a submit stub in JS prevents default so nothing
  navigates. Stage 4 only adds the fetch wiring and success/failure states.

- V5 swap: `.panel-body` fades to opacity 0 and translateY 6px over 130ms
  (`.is-swapping`), content is committed at the midpoint, then the class is
  dropped to ease back in (130ms; 260ms total). Reduced motion: `initPanel`
  calls `commit()` directly, so the content still swaps with no animation.

- Keyboard and aria: rows are the stage-2 real buttons; enter/space select
  natively. On selection the visible panel header becomes "PREVIEW / <name>"
  and the same text is mirrored into a visually-hidden
  `role="status" aria-live="polite"` region for a concise announcement.
  Decorative glyphs stay aria-hidden; the placeholder videos are
  aria-hidden/tabindex=-1 so the anchor is the single focus stop. Verified
  keyboard-only: focus is retained on the row after activation.

- Row-to-panel wiring: rows 01 to 05 swap to their V2/V3 view and take the
  single-selection active state (R3, aria-pressed). The CTA row 06 swaps to V4
  and clears every index row's active state, so the two stay in sync; the CTA
  itself never gets a persistent selected style (C5) and carries no
  aria-pressed. Verified: after selecting the CTA no index row is active.

### Stage 3 deviations / judgement calls
- Re-selecting the already-shown view is a no-op (no swap replay): `initPanel`
  tracks `currentView` and returns early when the clicked row matches. Chosen
  because replaying the 260ms fade for the row you are already on reads as a
  glitch, not feedback. Verified: re-clicking the active row does not
  re-render the view node.
- Swap fade-in is removed with a layout flush (`void offsetWidth`) then a
  synchronous class removal inside the midpoint timeout, rather than
  `requestAnimationFrame`. rAF is paused in a backgrounded tab, which left the
  panel stuck at opacity 0; the timer + flush approach clears reliably whether
  or not the tab is visible (confirmed: opacity returns to 1 in the
  backgrounded pane). Behaviour in a visible tab is unchanged (out-phase
  already painted the opacity-0 state, so removing the class transitions in).
- Panel header for every view uses the "Preview / <name>" pattern (CONCEPT
  specifies it for V2; extended to V3 About/Pricing and V4 "Preview / Get in
  touch" for a consistent panel identity and a clean aria-live string).
- Preview area kept on `--surface-preview` with a 1px `--border` frame even
  though the panel itself is `--surface-preview`; the border defines it as an
  intentional media frame rather than a same-colour blend.
- Fields and the form card both use `--radius-surface` (only two radii exist;
  a text input at `--radius-pill` would over-round the textarea).
- Honeypot field (`_gotcha`) added now as part of the POST skeleton so stage 4
  is pure wiring; it is off-screen, out of the tab order and aria-hidden.
- Verification note: the browser pane tab stays backgrounded, so screenshots
  time out (same limitation logged at stages 1 and 2). All behaviour above was
  verified programmatically over a local http server via the pane's JS console
  (views, copy, video attributes, swap timing, active-state sync, aria-live,
  keyboard focus, submit stub, 404 media as expected, no console errors).
  Visual/screenshot verification is left to the verifier subagent.

### Stage 4 - Contact form wiring (Formspree, success/failure, honeypot)
- Status: VERIFIED PASS (verifier run 2026-07-27, 0 FAILs, screenshots and
  results JSON in verify/stage-4/). The earlier cut-off verifier run's
  suspicion about the F2 focus ring was its own measurement error (read
  before the 150ms transition settled); re-measured correct. All asset references bumped ?v=3 to
  ?v=4 (css link, js script, two @font-face src, the six project media refs).
  Files changed: index.html, css/styles.css, js/main.js, PROGRESS.md.

- Formspree endpoint: a single constant `FORMSPREE_ENDPOINT` in js/main.js,
  next to `SITE_EMAIL`, value `https://formspree.io/f/REPLACE_FORM_ID` (open
  item, placeholder deliberately obvious). Single-edit choice: the form's
  `action` is injected from this constant when the form view is rendered
  (initPanel/renderView), NOT hardcoded in the HTML, so there is exactly one
  place to change the endpoint. Caveat: the form lives in a `<template>`
  cloned by JS on selection (stage-3 architecture), so the "plain HTML POST
  when JS is unavailable" fallback is theoretical: with JS off the form is
  never rendered at all. The action is still set correctly for robustness. A
  truly no-JS form would need the markup lifted out of the template, which is
  a stage-3 change and out of scope here. Flagged for the orchestrator.

- Progressive enhancement (section 7): submit is intercepted (delegated on the
  persistent `.panel-body`, so freshly cloned forms are always wired),
  `preventDefault` so it never redirects to Formspree, then `fetch` POST with
  `Accept: application/json` and a `FormData` body. On `response.ok` the
  success state shows; on non-2xx or a rejected promise (network error) the
  failure state shows. Verified all three by stubbing `window.fetch`.

- Success / failure presentation: a `.form-status` element (role=status,
  aria-live=polite, tabindex=-1) inside the card overlays the fields
  (position:absolute, inset:0, opaque white). The interactive parts moved into
  a `.form-fields` wrapper that carries the card's flex/gap/padding, so the
  wrapper defines the card size and the overlay fills it without changing it:
  measured card box is identical (440x359) in the form state and the success
  state, so the panel never reflows (no layout jump). Success copy: "Sent. I
  will reply the same working day." Failure copy: "Something broke. Email me
  directly at <address>." with the address a mailto link built from
  `SITE_EMAIL`. Both messages are Archivo 14px (matches the form inputs) in
  --ink-body; the mailto is --accent. No error/red colour is used (there is no
  token for one; tokens-everywhere kept).

- Failure keeps the typed message: fields are NOT reset on failure (verified
  message intact after both non-2xx and network error). Because the overlay
  covers the fields, the failure state includes a quiet mono "Try again"
  button (--accent text, not the CTA/submit treatment) that hides the overlay
  and returns to the intact form (message still present, submit re-enabled,
  focus to the first field) so the user can copy or resend. Success does reset
  the fields (permitted) and is terminal (no dismiss).

- Validation (section 7): `novalidate` removed from the form so native
  `required` is the primary gate (browser bubble + the field focus ring, no
  custom error UI). For non-empty-after-trim, the handler trims each field in
  place and calls `checkValidity()` / `reportValidity()`, so a whitespace-only
  entry is rejected through the same native mechanism. Verified: empty fields
  are natively invalid (valueMissing) and never fetch; a whitespace-only
  message trims to empty, is reported invalid, and never fetches.

- In-flight guard: on send the submit button is disabled and its label swaps
  to a static "Sending" (no looping spinner; only the CTA drift is
  sanctioned). Re-entrant submits are ignored while disabled (verified: three
  rapid submits = one fetch call). The label/enabled state is restored on
  failure; on success the button stays covered by the terminal overlay.

- Honeypot (`_gotcha`): checked first in the handler; if filled, the form is
  reset and the success state is shown WITHOUT any fetch (verified: zero fetch
  calls, success shown). The field stays off-screen, out of tab order and
  aria-hidden from stage 3.

- Aria / keyboard (section 7 item 5): the in-card role=status region carries
  the outcome text and receives focus (tabindex -1) on success and failure, so
  a keyboard user is not stranded; the covered `.form-fields` wrapper is set
  `inert` while the overlay is shown (removed on "Try again"), so hidden
  controls are unreachable by keyboard or AT.

- Verification note: same backgrounded-pane limitation as stages 1 to 3;
  behaviour was verified programmatically over a local http server by stubbing
  `window.fetch` (and, for the whitespace case, `form.reportValidity` to avoid
  the native bubble hanging the automation) in the pane console. All stubs
  were console-only; no instrumentation was left in the source. Visual and
  screenshot verification is left to the verifier subagent.
- Open items unchanged: the Formspree form ID and the real email remain open.

### Stage 5 - Mobile pass (section 8, tested at 360, 390, 768; contrast per section 10)
- Status: VERIFIED PASS (verifier runs 2026-07-27: initial run 3 FAILs, fix
  round 1 cleared two, fix round 2 cleared the scroll-into-view heuristic;
  final re-verify 0 FAILs across the full width/height matrix, screenshots
  and results JSON in verify/stage-5/). All asset references bumped ?v=4 to
  ?v=5 (index.html: css link, js script, six project media refs = 8; css:
  two @font-face src). js/main.js has no versioned asset refs. Files changed:
  index.html (version bump only), css/styles.css, js/main.js, PROGRESS.md.

- Single-column layout below 900px (CSS @media max-width:900px): the two-column
  grid collapses to a flex column in the section-8 order (name block,
  positioning, INDEX, panel, HOW IT WORKS, proof strip, footer). The panel lives
  in the markup inside .col-right, a grid sibling of .col-left, so to interleave
  it between INDEX and HOW both columns are set to `display: contents` and every
  one of the eight flattened children carries an explicit `order` (1..8). Explicit
  orders on ALL children are required: an unordered flex item defaults to order 0
  and would jump to the top. Testimonials (hidden) is ordered 4, kept under the
  INDEX for when it is later enabled; the panel is 5. Verified visual order at
  360/390/768: name, positioning, index, panel, how, proof, footer.

- Page height released on mobile: height auto, min-height 0, so the desktop
  860px min-height never forces a tall phone page. Nothing critical relies on
  100vh (the page flows); the only vh use is the panel's reserved min-height.

- Panel: min-height 60vh (about 468px at 360x780, 614px at 768x1024) so V1 to V4
  do not reflow the page on swap; height auto so it grows with content; margin-top
  --sp-32 above it. Welcome glyph scales to 160px (from 340px). Proof strip loses
  its desktop margin-top:auto pin (a flex behaviour) and flows with margin-top
  --sp-48.

- Padding step-down from the desktop 76px, values from the spacing scale:
  --sp-48 (48px) at <=900px, --sp-22 (22px) at <=480px. Panel view padding also
  steps to --sp-22 at <=480px so the form card fits at 360px.

- Form card fit at 360px (verified): the panel body centres its single view with
  place-items:center, which on the desktop's wide panel is right but on a narrow
  phone shrink-wraps the view to its 440px card and overflows (clipped by the
  panel's overflow:hidden, so no page scroll but a cut-off card). Fixed with two
  changes inside the breakpoint: `grid-template-columns: minmax(0, 1fr)` (a plain
  1fr keeps an automatic content minimum that the 440px card blows out) and
  `justify-items: stretch` so the view fills the narrow column and the card's
  `max-width: 100%` is measured against the real panel width. Result at 360px:
  view 314, card 270, fields 204, no horizontal scroll. At 768px the 440px card
  fits the wide panel unchanged. No horizontal scroll at 360/390/768.

- Preview area (video, section 5): the 16/9 aspect-ratio already on `.preview`
  applies at every width and reserves the box height independent of the media, so
  the area never collapses to zero when the stage-6 posters/webm land (verified at
  390px: 300x169, ratio 1.778). Judgement call: kept 16/9 (the actual screen-
  capture ratio and a standard reserved ratio) rather than switching to the
  section-8 example 16/10; either prevents collapse, and 16/9 matches the real
  clips.

- Touch rules (section 8):
  - Guards keyed off `(hover: none) and (pointer: coarse)` for real phones, not
    just per-event pointerType. New JS helper `isTouchDevice()` short-circuits the
    binding of the row pointer-trail and CTA hover-mist listeners on touch-only
    devices (same query the dot grid already uses). The per-event
    `pointerType === 'touch'` checks are KEPT as well, so a hybrid laptop that
    reports hover/fine still binds the listeners and filters its own touch events
    correctly. Press bloom is unchanged: it still fires from the tap point on
    touch (no touch guard on pointerdown), only skipped under reduced motion.
  - All hover-revealed information visible at rest on touch: on the mobile
    breakpoint the niche tag stays visible in every row state (including
    .is-active, verified: active Blackthorn row tag opacity 1) and the expand
    glyph is always shown (opacity 1). The glyph moves from an absolute overlay
    (right:0) into normal flow (position:static) with a --sp-10 column-gap in
    .row-end, so tag and glyph sit side by side rather than overlapping.

- Smooth-scroll panel into view on selection (section 8): new `scrollPanelIntoView`
  in initPanel. After a selection, if the panel is not already substantially
  visible it is scrolled into view (block:'start'), smooth normally and an instant
  jump (behavior:'auto') under prefers-reduced-motion. On desktop the panel is
  always beside the index and over the threshold, so it never scrolls (verified:
  no scroll on desktop select). Judgement call on threshold: "substantial" is at
  least 60% of the panel (capped at the viewport height) on screen
  (PANEL_IN_VIEW_RATIO = 0.6); at 360x780 the panel-at-rest ratio is 0.591, just
  under, so a tap on a low row brings it up.

### Stage 5 deviations / judgement calls
- CONTRAST DEVIATION (CONCEPT.md section 10, resolving the stage-1 carry-forward
  flag). --grey-soft (#A6A6AE) 10px mono niche tags and row indices on --ground
  (#FAFAFA) measure about 3.1:1, below WCAG AA (4.5:1). Remediation per section 10
  (darken on mobile-at-rest and for focus), exact colour choice recorded here as
  required:
  - Chosen colour: --ink-mid (#54545C), which measures about 7.0:1 on #FAFAFA and
    passes AA. This is the nearest existing token that passes: --grey-label
    (#8E8E96) is about 3.1:1 and fails, so it was rejected.
  - Applied to `.row-index` and `.row-tag` in two scopes only:
    1. The mobile breakpoint (@media max-width:900px), at rest, since section 8
       shows these at rest on touch (tags never fade on touch).
    2. Desktop `:focus-visible` (`.row:focus-visible .row-index/.row-tag`),
       declared before the hover/active colour rules so an active or hovered row
       still wins (accent index, faded tag) and only the keyboard-focused-at-rest
       row is darkened. Verified rule order: focus rule precedes both the hover
       and active rules.
  - Desktop rest colours are unchanged (both remain --grey-soft; verified on a
    clean 1280 load: index and tag rgb(166,166,174), glyph hidden). The wider
    "desktop rest greys below AA" observation stays open for the stage-8 de-vibe
    gate, exactly as the stage-1 flag stated.
  - CTA row index/tag were left as-is: they sit on the pastel pill fill, not on
    --ground, so this on-ground remediation does not apply to them.

- Files layout unchanged; no new tokens (all new values are from the spacing
  scale: --sp-48, --sp-32, --sp-22, --sp-10). Two radii, one border width and
  inset-only shadows are untouched.

- Encoding incident (recorded for transparency): the ?v=4 to ?v=5 bump was first
  done with a PowerShell Get-Content/Set-Content round-trip, which on this
  PowerShell 5.1 read the no-BOM UTF-8 files as ANSI and re-wrote them
  double-encoded (mojibake on £, ·, ↗, © in index.html and one styles.css
  comment) plus a spurious UTF-8 BOM. Both were fully repaired: the BOM stripped,
  index.html reversed with a verified cp1252 round-trip (0 mojibake markers, valid
  UTF-8, and every special-character line byte-identical to the committed copy),
  and the one styles.css comment fixed by hand. All later edits used the Edit tool
  (encoding-safe). Confirmed final: 0 mojibake markers and no BOM in all three
  files.

- Verification note: same backgrounded-pane limitation as stages 1 to 4 (the
  Browser pane tab stays document.hidden, so pixel screenshots time out). All
  behaviour above was verified programmatically over a local http server via the
  pane console at 360/390/768/1280: order, no horizontal scroll, panel 60vh,
  glyph 160px, form card fit, tag/index contrast, glyph-and-tag both visible at
  rest, active-row tag persistence, desktop unchanged, focus-rule order, no
  console errors. Two pane quirks were observed and worked around, not code bugs:
  (1) getComputedStyle returned stale mobile values on nodes after a
  cross-breakpoint resize (confirmed via CSS-rule enumeration and a clean reload
  that the desktop rules resolve correctly); (2) `behavior: 'smooth'`
  scrollIntoView is a no-op in the pane while instant scroll works, so only the
  reduced-motion (instant) scroll path could be exercised here (the smooth path is
  standard browser behaviour on real devices). Visual/screenshot verification is
  left to the verifier subagent.

### Stage 5 - Verifier FAIL fixes (round 1)
Verifier run returned STAGE FAIL with 3 FAILs; all three fixed and re-verified
programmatically at 360/390/768 (and desktop unaffected). ?v=5 kept as is (no
push happened). Files changed: css/styles.css, js/main.js, PROGRESS.md.

- FAIL 1 (V2 grew the panel past 60vh, pushing HOW IT WORKS down ~10px at 360
  and ~23px at 768; the 16/9 preview scales with panel width and alone is about
  330px at 768). Fix in css/styles.css inside @media max-width:900px, chosen to
  shrink the mobile V2 footprint so every view FITS the 60vh budget (preferred
  over internal panel scrolling, which would look poor, per the spec wording and
  the verifier's steer):
  - `.preview { aspect-ratio: 2 / 1 }` on mobile only (desktop stays 16/9): a
    shorter, still-reserved ratio so posters cause no shift; the placeholder /
    future webm cover-crop the small extra height. This is the main lever, since
    the preview is what scaled with width.
  - `.view { gap: var(--sp-14) }` on mobile (from --sp-18): tighter vertical
    rhythm, buys the last few px at 360 where the title wraps to two lines.
  - `.form-fields { padding: var(--sp-22) }` on mobile (from --sp-32): trims V4,
    which was ~2px over at 360.
  Re-measured: panel height is now a stable 60vh for V1 to V4 at every tested
  width (360: 468 / HOW top 1019; 390: 506 / 1052; 768: 614 / 1186), identical
  across all six views. Judgement call recorded: 2/1 mobile preview over a
  centred/narrowed frame (which would have forced the About and Pricing prose to
  wrap taller and reflow at 768) or internal scrolling.

- FAIL 2 (on touch a tap leaves a sticky :hover, and
  `.row:not(.row--cta):hover .row-tag { opacity: 0 }` at specificity 0,4,0 beat
  the mobile `.row.is-active .row-tag { opacity: 1 }` at 0,3,0, hiding the niche
  tag on the active row). Fix (agreed): the entire row hover reveal/hide block
  is now wrapped in `@media (hover: hover) and (pointer: fine)`, mirroring the JS
  isTouchDevice guard, so it never applies on touch. The CTA :hover block
  (saturate/brighten + faster drift) was wrapped the same way, so a tap does not
  leave persistent selected-looking styling on the pill (C5). Verified: the
  tag-hide rule's parent media is `(hover: hover) and (pointer: fine)`, the
  active-tag-visible rule sits in the `max-width: 900px` block, and an
  active-but-not-hovered row (the post-tap touch state) keeps its tag at
  opacity 1, colour --ink-mid.

- FAIL 3 (on mobile normal motion, tapping row 01 from scrollY 0 never scrolled
  the panel in: select() called scrollPanelIntoView() synchronously right after
  swap() had only scheduled the content change 130ms later, so the ratio was
  measured on the stale pre-swap box). Fix (agreed): scrollPanelIntoView() is now
  called from inside commit() (removed from select()), so it always measures
  post-swap geometry on both the reduced-motion (synchronous commit) and animated
  (deferred commit at the midpoint) paths. Function declarations are hoisted, so
  commit() can call the helper defined later in initPanel. Verified with a
  scrollIntoView spy that forced instant (the pane no-ops behaviour:'smooth',
  which was the only reason the earlier run looked un-scrolled): tapping row 01
  at scrollY 0 now fires exactly one scrollIntoView on `.panel`
  (behaviour:'smooth', block:'start') and moves scrollY 0 to 503 (panel top to
  0). Side benefit of FAIL 1's fix: with the panel now a stable 60vh, the pre-
  and post-swap ratios are identical anyway, so the timing bug can no longer
  bite; the commit() relocation is the belt-and-braces correct fix.

- Re-verification note: same backgrounded-pane limits (pixel screenshots time
  out; `behaviour: 'smooth'` scrollIntoView is a no-op in the pane). All three
  fixes were verified programmatically over the local http server. Encoding
  stayed clean throughout (Edit tool only): 0 mojibake markers, no BOM, ?v=5
  unchanged (8 in index.html, 2 in styles.css). Screenshot verification is left
  to the verifier subagent.

### Stage 5 - Verifier FAIL fixes (round 2)
Re-verify confirmed FAILs 1 and 2 resolved; FAIL 3 remained open with a new root
cause introduced by round-1 fix 1. Fixed and re-verified across viewport heights.
?v=5 unchanged (no push). Files changed: css/styles.css, js/main.js, PROGRESS.md.

- FAIL 3 (new root cause): freezing the panel at exactly 60vh (round-1 fix 1)
  made the old visible-fraction heuristic viewport-height-dependent, so
  (vh-497)/(0.6*vh) crossed 0.6 near vh 777 and never scrolled on tall phones
  (780/812/844) in either motion mode. Replaced it with a viewport-height-
  independent test on the panel's top edge, in js/main.js:
  - New module constants PANEL_TOP_MIN = -8 (px) and PANEL_TOP_BAND = 0.2
    (fraction of viewport height), and mobileLayoutQuery =
    matchMedia('(max-width: 900px)').
  - scrollPanelIntoView() now: returns immediately unless mobileLayoutQuery
    matches (so desktop >900px NEVER scrolls, guarded by the breakpoint rather
    than by geometry); otherwise reads panel top and returns if it is already in
    the band [PANEL_TOP_MIN, PANEL_TOP_BAND * vh] (header already at/near the
    top: an immediate second selection does not re-scroll); otherwise scrolls
    with block:'start', smooth normally and instant under reduced motion. The
    smooth/instant branch and the call site inside commit() are unchanged.
  - Removed the now-dead panelVisibleRatio() and PANEL_IN_VIEW_RATIO.
  - Tolerance band (judgement call, reported): -8px floor to 0.2 * viewport
    height. The -8px floor ignores sub-pixel/rounding negatives; 0.2 * vh treats
    "top within the first fifth of the screen" as already placed, while a panel
    sitting below the index (top about 503px at 360/390 widths, far past that
    fifth at every height) always scrolls.

- Secondary root cause found while verifying (instrument, not guess): with the
  top-edge band, an immediate second selection still triggered one redundant
  re-scroll at 390 widths. Instrumenting scrollIntoView showed the page scroll
  drifted about +13px (panel top 0 to -13, just past the -8 floor) during the
  swap. Cause: the browser's scroll anchoring reacting to the .panel-body
  replaceChildren. Confirmed by toggling overflow-anchor: setting
  overflow-anchor: none on body removed the drift entirely. Fix in
  css/styles.css inside @media max-width:900px: `body { overflow-anchor: none }`
  so the panel stays pinned where scrollPanelIntoView placed it. Kept the -8px
  floor (with anchoring off there is no drift to absorb). This was preferred
  over merely widening the negative floor, which would have left the panel a few
  px above the fold on the second tap; the root-cause fix keeps the header at
  the top.

- Re-verification (programmatic over local http; smooth scroll still no-ops in
  the pane, so a scrollIntoView spy forced instant to observe movement and count
  calls):
  - Tap row 01 from scrollY 0 scrolls the panel in (one scrollIntoView on
    .panel, block:'start') at 360 and 390 widths for heights 640, 667, 780, 812
    and 844. At 844 the short page clamps the scroll so the panel top lands at
    +13px (header still on screen), which the band then treats as placed.
  - Immediate second selection: zero further scrollIntoView calls at every
    tested width/height (no re-scroll).
  - Desktop 1440x900: zero scrollIntoView calls, scrollY stays 0 (guarded off by
    the mobile-layout query).
  - No console errors. Encoding clean throughout (Edit tool only): 0 mojibake, 0
    em dashes, no BOM; ?v=5 unchanged (8 in index.html, 2 in styles.css).
  Pixel screenshots still time out in the pane; that trail is the verifier's.

### Stage 6 - Capture pipeline (record, process, integrate the three previews)
- Status: VERIFIED PASS (verifier run 2026-07-27, 0 FAILs, screenshots,
  extracted frames and results JSON in verify/stage-6/). First-load transfer
  measured at ~141KB, well inside the 300KB budget. One AMBIGUOUS note: the
  Star clip shows the First Light to The Web epoch transition with clear WebGL
  structure, but a visually distinct lensing warp moment is hard to confirm
  from stills; if a stronger lensing shot is wanted, re-record per
  tools/README.md with a different scroll window. No page code changed: index.html,
  css/styles.css and js/main.js are untouched. The media/ filenames already
  referenced by the V2 views were produced exactly, so no reference or ?v=
  edits were needed (names match; ?v=5 stays, no push happened this stage).
  New/changed files: tools/capture.py, tools/README.md (new), .gitignore (new),
  media/*.webm and media/*.jpg (six new), PROGRESS.md.

- NEW BUILD-ONLY FOLDER (deviation, flagged for the orchestrator): tools/ was
  added for the capture script. It is a build-time tool only and ships nothing
  to the page (not referenced by index.html/css/js). The raw Playwright takes
  and ffmpeg pass logs live in tools/_raw/, which the new root .gitignore
  excludes. CONCEPT section 2 fixes the shipped file layout; tools/ sits
  outside that as pipeline tooling, consistent with "scripted, not manual"
  capture in section 5. Recorded here as required since it is a new top-level
  folder.

- Capture (tools/capture.py, Playwright + headed Chromium with GPU args
  --use-angle=d3d11 etc.): viewport recorded at 1280x800, scripted eased
  scrollTo (easeInOutQuad via rAF in-page, no manual driving, no mouse). Per
  project, per section 5:
  - Blackthorn: cover -> price menu (services) -> rotating reviews pull-quote.
  - Barker & Bloom: hero -> paw-trail thread drawing on scroll -> pricing bento.
  - Until the Last Star: First Light -> The Web epoch transition, the cosmic
    web of galaxies lensed along dark-matter filaments, recorded HEADED on the
    GPU. Renderer verified inside the recording context via
    WEBGL_debug_renderer_info before accepting the take (refuses a software
    fallback). Observed renderer string:
    `ANGLE (NVIDIA, NVIDIA GeForce RTX 3060 Laptop GPU (0x00002520) Direct3D11 vs_5_0 ps_5_0, D3D11)`
  Site inspection first (per the brief): none of the three demo sites has a
  first-run overlay blocking the take (probed: no viewport-covering high
  z-index element on any), so the script's Escape + dismiss-selector pass is
  belt and braces only. Before each take: goto wait_until networkidle, wait for
  document.fonts loaded, a second networkidle, then a settle at the start scroll
  (the WebGL scene needs ~1.8s to catch a jumped scroll on star).

- Post-process (ffmpeg): centre-crop the 1280x800 take to 16:9 (drop 40px top
  and bottom), scale to 800x450, strip audio (-an, confirmed no audio stream in
  any output), 30fps, VP9 two-pass to a target bitrate, then export the first
  frame of the processed clip as the poster jpg (poster is exactly frame 0 of
  the loop). Poster quality auto-tuned (mjpeg -q:v stepped up until under 40KB).

- Final files (all in budget: 6 to 8s, 300 to 500KB webm, poster under ~40KB):
  - blackthorn-preview.webm  7.03s  395KB (VP9 430k)   blackthorn-poster.jpg  39KB (q6)
  - barker-bloom-preview.webm 6.03s 343KB (VP9 470k)   barker-bloom-poster.jpg 39KB (q6)
  - until-the-last-star-preview.webm 6.03s 323KB (VP9 520k)  until-the-last-star-poster.jpg 29KB (q3)
  All 800x450, VP9, video-only. (star compresses under its 520k target because
  two-pass VP9 with alt-ref frames undershoots on the busy starfield; still
  comfortably in range, so left as is.)

- Integration check (Playwright headed over a local http server, at desktop
  1280x800 and mobile 390x800): each V2 video autoplays (paused=false,
  currentTime advancing) with autoplay+muted+loop+playsinline+preload="none"
  and its poster attribute set (?v=5). No media 404s (the only 404 is the
  browser's default /favicon.ico request, a stage-7 concern, not a page asset
  reference). No layout shift: the .preview box measured identical before and
  after the video loads at both ratios (desktop 496x279 = 16/9; mobile
  285x142.5 = 2/1), because the box aspect-ratio reserves the height
  independent of the media. object-fit: cover means the 800x450 (16/9) clip
  fills the desktop 16/9 box with no crop and the mobile 2/1 box by trimming a
  little top and bottom: intentional and confirmed to look right at both.
  Poster note: with preload="none" + successful muted autoplay on a fast local
  server, Chromium goes straight to the video frame and the poster jpg is often
  not fetched at all; it is the fallback shown before the first frame and where
  autoplay is unavailable (per section 5), and the attribute/file are correct.

### Stage 6 deviations / judgement calls
- Trim points: the clip is anchored to the END of each raw take (its scripted
  closing hold), taking the last clip_len seconds less a 0.10s tail margin,
  rather than an absolute front offset. Reason (instrumented, not guessed): the
  barker raw take recorded a 9.16s timeline for ~10.1s of wall-clock activity,
  so a front-offset trim overran and clamped to a 5.37s clip (under the 6s
  floor). End-anchoring is robust to that drift because any frames after the
  closing hold are static at the same scroll position. Result: 7.03 / 6.03 /
  6.03s, all in the 6 to 8s window.
- Loop-friendliness: these are one-way scroll tours (cover -> pull-quote, hero
  -> bento, First Light -> The Web), so a seamless first==last frame is not
  achievable without a crossfade. Both ends of every clip sit on a static hold,
  so the muted loop cut lands between two calm frames (minimal visible jump)
  rather than mid-motion. Judged acceptable for a small, muted micro-preview
  and preferred over distorting the narrative to force a return to the start.
- Aspect ratio: recorded 16:10 (1280x800 per the brief) but cropped to a native
  16:9 800x450 output so the clip matches the desktop preview box exactly (no
  cover-crop there). The mobile 2/1 box then cover-crops the small extra height,
  which is the intended reserved-box behaviour noted at stage 5.
- Bitrates chosen per clip (blackthorn 430k / barker 470k / star 520k) to land
  in 300 to 500KB at each duration; capture.py also auto-retunes once if a clip
  falls outside the budget. All three hit the range on the first pass.
- Verification note: unlike stages 1 to 5, this stage's checks ran in a real
  headed Chromium (the orchestrator confirmed the GPU launches here), so the
  capture, the renderer confirmation, the frame-content spot checks and the
  integration/autoplay/no-shift/no-404 checks were all observed directly rather
  than only programmatically. Screenshot/visual sign-off is still the
  verifier's.

### Stage 7 - Head, meta, Open Graph, favicon (section 9)
- Status: VERIFIED PASS (verifier run 2026-07-27, 0 FAILs, screenshots and
  results JSON in verify/stage-7/; first-load transfer ~146KB, favicon.ico
  404 gone, og-image checked at 1200x630 under alpha-free PNG).
  Stage 1 already set lang="en-GB",
  charset, viewport, the title and the description; this stage added the share
  card meta, the built og-image, and the favicon set, and bumped every cache
  bust ?v=5 to ?v=6 (a push follows this stage).

- Cache bust: all shipped refs are now ?v=6. index.html carries 13 (css link,
  js script, six project media refs, plus the five new refs: og:image,
  twitter:image, favicon.svg, favicon-32.png, apple-touch-icon.png);
  css/styles.css carries 2 (the two @font-face src). No BOM, no mojibake, no em
  dashes. sed did the bump; grep confirms zero ?v=5 remain in index.html,
  css/styles.css or js/main.js.

- Open Graph / Twitter (index.html head): og:type website, og:site_name,
  og:url, og:title (mirrors <title>), og:description (mirrors the positioning
  line), og:image + og:image:type/width/height (1200x630) /alt, and the Twitter
  equivalents (twitter:card summary_large_image, title, description, image,
  image:alt). Description and title copy are identical to the on-page strings.

- og-image.png (repo root, 1200x630, RGB no alpha, 33 KB, target was under
  100 KB): BUILT, not screenshotted from the site. Rendered by tools/og_image.py
  from tools/og_source.html with headless Chromium at device_scale_factor 1
  (exactly 1200x630), waiting on document.fonts.ready so the type is the site's
  own self-hosted Archivo and Martian Mono, then flattened onto the ground
  colour (#FAFAFA) with Pillow and saved as an optimised alpha-free PNG. Layout:
  ground #FAFAFA, "Zayn" in Archivo 600 (tracking -0.015em), the positioning
  line in Archivo 400 with "£300" in Martian Mono at accent #1A6FD4, and one
  accent element: a restrained patch of the site's own dot grid (real hard-edged
  dots, no gradient sheen, at the --dot-rest alpha, 1.5px on 26px spacing),
  confined to the right so it reads as a patch, not a full-bleed fill. No
  gradients, no shadows.

- Favicon (CONCEPT section 9: simple "Z" mark, ink on transparent). favicon.svg
  (repo root, 472 bytes) is hand-authored: a clean geometric Z drawn as two
  horizontal bars plus a diagonal parallelogram, fill #141416 (--ink), tight
  32x32 viewBox, transparent. PNG fallbacks rendered from that SVG by
  tools/favicon_png.py (Chromium at 512px, downsampled LANCZOS): favicon-32.png
  (32x32, ink on transparent, 640 bytes) and apple-touch-icon.png (180x180,
  2.1 KB). Head links: rel=icon SVG first, rel=icon PNG 32x32 fallback,
  apple-touch-icon, all ?v=6.

- /favicon.ico resolved (the 404 flagged at stage 6): instrumented, not guessed.
  A headed Chromium over a local http server (temporary probe, since removed)
  recording every request showed the browser fetched favicon.svg?v=6 (200) and
  did NOT request /favicon.ico. So the rel=icon links cover it and no
  favicon.ico is needed; none was added. (Headless Chromium fetches no favicon
  at all, having no tab UI, so the check had to be headed, matching the headed
  run that first saw the stage-6 404.)

- Performance: first-load transfer delta this stage = favicon.svg only, 472
  bytes. The same headed probe confirmed the browser does NOT fetch og-image.png,
  favicon-32.png or apple-touch-icon.png on a normal page load (og-image is a
  crawler asset; the 32px PNG is a fallback only used when SVG icons are
  unsupported; the touch icon is iOS add-to-home only), and there is no
  accidental preload. Budget impact negligible.

### Stage 7 deviations / judgement calls
- Icon/OG asset location: favicon.svg, favicon-32.png, apple-touch-icon.png and
  og-image.png are placed at the repo root. Section 2 fixes the shipped file
  layout as index.html/css/js/media/fonts/references; favicons and the share
  card are conventionally root-level (browsers probe /favicon.ico at root; iOS
  probes /apple-touch-icon.png at root) and are individual files, not a new
  top-level directory, so this stays within the "no new top-level structure"
  rule. Flagged here for the record.
- og:image / twitter:image use ABSOLUTE URLs (not a bare filename). Reason:
  crawlers (Facebook, LinkedIn) resolve relative image URLs unreliably and
  several require absolute. The trade-off is that the deployed domain now appears
  literally in three tags (og:url, og:image, twitter:image); to honour the brief's
  "single obvious place to change it", a labelled CANONICAL SITE URL comment sits
  directly above those tags naming exactly which three to edit if a custom domain
  arrives. og:url is https://arctxrus.github.io/portfolio/ per the brief.
- apple-touch-icon.png is flattened onto the ground colour (#FAFAFA), not left
  transparent, although the SVG mark itself is ink-on-transparent per section 9.
  Reason: iOS composites a transparent touch icon onto black, which would flip
  the mark to look inverted on a dark tile; the ground fill keeps it on-brand.
  The browser tab favicon (SVG and the 32px PNG) stays transparent as specified.
- The dot-grid patch on the og-image is produced with a radial-gradient dot
  technique, but the colour stop is hard-edged (solid to transparent at the same
  0.75px radius), so there is no visible gradient band: it renders as flat dots,
  consistent with the "no gradients" instruction for the card. It is the site's
  own dot token (--dot-rest), so it matches the live background.
- og-image copy: CONCEPT section 9 and the brief both specify "Zayn plus the
  positioning line". I also included the small "FREELANCE / WEB" kicker (Martian
  Mono, grey) above the name. Reason: it faithfully reproduces the site's actual
  name block (name + kicker sit together on the page) and strengthens the brand
  read on the card; it is an addition, not a conflict, since neither spec forbids
  it. Flagged so the orchestrator can veto it if a barer card is preferred.
- Added three build-only files to the existing tools/ folder (og_image.py,
  favicon_png.py, og_source.html). Like capture.py these ship nothing to the
  page and are not referenced by index.html/css/js; raw render masters go to the
  gitignored tools/_raw/. Consistent with the tools/ deviation logged at stage 6.

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

### Approval round fixes (pre stage 8)
- Status: BUILT, awaiting verification. Zayn's post-review decisions applied as a
  single fix round before the stage 8 de-vibe audit. Files changed: index.html,
  css/styles.css, js/main.js, tools/capture.py, media/until-the-last-star-
  preview.webm, media/until-the-last-star-poster.jpg, PROGRESS.md. All shipped
  asset refs bumped ?v=6 to ?v=7 (a push follows): 13 in index.html, 2 in
  css/styles.css, 0 in js/main.js. Encoding clean (UTF-8, no BOM, no mojibake,
  no em dashes); special chars (u+2197, u+00A3, middle dot) intact.

- ITEM 1 - About prose (APPROVED amendment). index.html V3 About: "a physics
  graduate" to "an astrophysics graduate" (also fixed the article a -> an). The
  APPROVED COPY quote block above updated to match. Nothing else changed.

- ITEM 2 - Expand glyph revert (deviation 5a NOT approved, now CLOSED). The "+"
  glyph reverted to the arrow treatment "↗" (U+2197) everywhere the expand glyph
  appears: index rows 01 to 06 (six .row-glyph spans), the CTA row 06 glyph, and
  the giant welcome ghost glyph. One consistent treatment per CONCEPT 3.2: single
  character in the system font stack (var(--font-system)), weight 400, at 14px on
  rows/CTA and 340px on the welcome. No CSS change was needed (the glyph was
  already system-font/weight-400; only the character changed), so the page is now
  fully consistent with the "Visit live site ↗" pills.
  Pre-revert check (instrument, per brief): the stage-1 log records "+" as a
  STYLISTIC choice, not a fix for a rendering problem. Verified ↗ renders
  acceptably before swapping, over a local http server in Chromium:
  - Not tofu: canvas measureText at 340px gives width 249.0 for ↗ vs 219.5 for a
    private-use (guaranteed-absent) codepoint and 219.3 for the .notdef box, so
    Segoe UI (the resolved system font on Windows) has a real U+2197 glyph.
  - Sensible metrics: at 340px / line-height 0.8 a DOM probe renders w 249 / h 272
    (272 = 340 * 0.8); at 14px / line-height 1 it renders w 10.27 / h 14. Both
    non-zero and correctly proportioned. Codepoint confirmed U+2197.
  No real rendering problem, so the revert proceeded. Deviation 5a is closed.

- ITEM 3 - No-JS contact path (deviation 5c, approved with condition). Added a
  <noscript> inside .panel-body (the panel region, per brief) with one sentence
  plus the contact email as a plain mailto link, styled in the site's prose type
  (.noscript-contact: Archivo 14px, --ink-body, accent link) with existing tokens
  only. Verified with JS ON the <noscript> renders nothing (0x0 box, contents are
  raw text, childElementCount 0), so it never shows to a normal visitor; with JS
  OFF the browser parses the <p> as real DOM and renders it. Because .panel-body
  is a centring grid also holding the decorative welcome, the noscript grid item
  is aligned to the bottom of the cell (.panel-body > noscript { align-self: end })
  so the fallback line sits clear of the centred welcome rather than overlapping.
  SECOND LITERAL EMAIL OCCURRENCE: the noscript hard-codes hello@placeholder.invalid
  (it cannot read the SITE_EMAIL constant with JS off); a comment there references
  SITE_EMAIL and the email OPEN BLOCKER above now names both edit sites.
  VERIFIER FIX (approval-round round 1): the first no-JS pass showed a blank page
  on a normal-motion preference. Root cause: every load-in block is .fade-block
  (opacity 0, translateY 6px), cleared only by JS adding .is-in or by the
  reduced-motion CSS override, so with JS off and normal motion nothing but the
  noscript line was ever revealed. Fix (verifier's suggestion): a
  <noscript><style> block in the index.html <head> forcing
  .fade-block { opacity: 1 !important; transform: none !important;
  transition: none !important; }. It applies only when scripting is off and has
  zero effect when JS runs. Confirmed with JS disabled + normal motion (headed
  Chromium, java_script_enabled false, reduced_motion no-preference): the name
  block, positioning, INDEX (all six rows incl. the CTA pill), panel with the
  ghost glyph, panel noscript contact line, HOW IT WORKS, proof strip and footer
  are all visible (screenshot in the scratchpad; verify/ trail is the verifier's).
  ?v=7 kept (no push since the bump).

- ITEM 4 - Formspree graceful short-circuit (decision 6). In handleContactSubmit
  (js/main.js), after honeypot + validation and before the fetch/in-flight block,
  a guard: if FORMSPREE_ENDPOINT contains "REPLACE_FORM_ID", show the existing
  inline failure state and return WITHOUT any network call. Validation, honeypot
  and the double-submit guard all still run. When a real form ID replaces the
  placeholder the constant no longer matches and the normal fetch path resumes
  automatically, no further edit. Failure copy unchanged. Verified over http: a
  valid submit fires 0 fetch calls and shows "Something broke. Email me directly
  at hello@placeholder.invalid." with the mailto link and the Try again control.

- ITEM 5 - Star clip re-record (decision 5h). Re-recorded until-the-last-star to
  a moment that is unmistakably 3D and reactive, replacing the starfield-fade
  read. Same pipeline (tools/capture.py, extended), same output filenames.
  - Exploration (headed GPU, screenshots): cosmic-dawn's timeline t is 0..1 over
    the scroll (scrollY = t * (scrollHeight - innerHeight)). The black hole with
    the lensed accretion disc and photon ring is THE LONG NIGHT epoch (Gargantua,
    t 0.79..0.90; content.js). The real screen-space gravitational-lens pass is
    tier-2 only and is the first thing the FPS governor drops, so the take forces
    ?tier=2. Renderer confirmed in-context: ANGLE (NVIDIA GeForce RTX 3060 Laptop
    GPU ... D3D11); debug overlay read TIER T2+L (lens active) at 131 to 144 FPS
    across the epoch, well above the 55 FPS drop threshold. Peak-lens framing
    chosen at t 0.845 (full face-on disc, complete photon ring, both caption lines
    visible).
  - PARALLAX FEASIBILITY FINDING (brief asked to verify then say so): the site
    DOES respond to pointer. scene.js binds pointermove (mouse-type only) into a
    spring-smoothed CAMERA parallax orbit (px = pointer.x * 2.5, py = pointer.y *
    1.6, decaying to rest after 2500ms of pointer idle); lensing.js/08-longnight.js
    note the pointer never moves the hole, but the camera orbit makes the lensed
    arcs and photon ring shift with the viewpoint. Confirmed empirically: a probe
    saw Playwright mouse.move arrive as pointerType "mouse", isTrusted true, and
    left-vs-right screenshots at the same t showed the whole hole+ring assembly and
    the background starfield shift position (a viewpoint orbit, not just disc
    rotation). So the FIRST LIGHT fallback in the brief was NOT needed.
  - Capture: hold at t 0.845, then a slow eased CIRCULAR mouse orbit (amp 240x150
    px around viewport centre, one orbit per 3.5s, ~50Hz pointer feed so the orbit
    never idles) driven for 8.5s; the last 7.0s are end-anchored out. The orbit is
    periodic in position and velocity, so the trimmed window has calm, near-looping
    ends (the disc's own animation does not loop, same "calm frames" bar as stage
    6). No scripted scroll during the keeper.
  - Output: until-the-last-star-preview.webm 7.03s, 402KB, 800x450, VP9, no audio
    (in the 6 to 8s / 300 to 500KB budget; first pass 532KB at 650k auto-retuned to
    488k -> 402KB). Poster until-the-last-star-poster.jpg = frame 0 (the black
    hole), 34KB (under the ~40KB budget). Frames inspected: lensed black hole with
    photon ring throughout, composition visibly orbiting.
  - Integration (local http, ?v=7): the star V2 video resolves currentSrc to the
    new webm, readyState 4 (fully loaded), no media error, no 404, no console
    errors, and the panel box is identical before/after (no layout shift). The old
    clip was backed up to the scratchpad before overwrite.

- ITEM 6 - Cache bust ?v=6 to ?v=7 (a push follows). sed bump; grep confirms 0
  remaining ?v=6 and 13 (index.html) + 2 (styles.css) ?v=7; media filenames carry
  no version, so the re-recorded clip is picked up by the bumped refs.

- Verification note: same backgrounded-pane limitation as earlier stages (pixel
  screenshots via the pane time out); all page-behaviour checks above ran
  programmatically over a local http server via the pane console, and the star
  capture/exploration ran in real headed GPU Chromium (screenshots and frame
  inspection observed directly). Screenshot/visual sign-off is the verifier's.

### Approval round deviations / judgement calls
- ITEM 2 glyph: kept the expand glyph in the system font stack per CONCEPT 3.2
  (not the mono stack used inside the "Visit live site ↗" pill label). 3.2
  assigns the expand glyph to "system"; the pill arrow is part of a mono text run.
  Both are the same character (↗), which is the brief's consistency goal.
- ITEM 3 noscript placement: put inside .panel-body (a listed option). It is
  removed from the DOM once JS swaps a view (panelBody.replaceChildren), but that
  only happens when JS runs, when the noscript is irrelevant anyway; with JS off
  no selection can occur so it persists and shows. align-self:end added to avoid
  overlap with the centred welcome.
- ITEM 5 star framing: chose t 0.845 (peak lens) held static with camera-orbit
  parallax over any scroll transition, because the lensed orbit is the strongest
  3D/reactive moment and a static scroll keeps clean loop ends. clip_len raised
  from 6.0s to 7.0s (still in range) to give the orbit room. Circular orbit chosen
  over a figure-8 because a circle is periodic in position AND velocity, so the
  seam is smoother under recording-timeline drift.

### Stage 8 - De-vibe audit gate (section 11)
- Status: AUDIT CLEAN (re-verified 2026-07-27 with real keyboard-driven
  Playwright: all five flag fixes confirmed, radius sweep returns exactly
  999px and 16px, placeholder 7.19:1, CTA index passes at mobile rest and
  focus with the desktop-rest exception documented; evidence in
  verify/stage-8/). The House Tier audit (the canonical
  14-item list is still an OPEN BLOCKER, see Open items) was run against the built
  site and returned 5 flags; the orchestrator ruled on each and the coder applied
  the rulings. All shipped asset refs bumped ?v=7 to ?v=8 (the deploy push follows
  stage 9): 13 in index.html, 2 in css/styles.css, 0 in js/main.js. Files changed:
  index.html, css/styles.css, PROGRESS.md. Encoding clean (valid UTF-8, no BOM, no
  mojibake, no em dashes; £300 x7, ↗ x10, middle dot x8 intact).

House Tier audit results (docs/de-vibe-audit.md items 1 to 7):

| # | Item | Result |
|---|------|--------|
| 1 | No em dashes anywhere | PASS |
| 2 | No fake content / claims all true | PASS |
| 3 | No AI-slop tells (no emoji, filler, purple gradients, glassmorphism, drop shadows) | PASS |
| 4 | Token discipline: two radii, one border width, inset shadows only | PASS after fixes (FLAG 1, FLAG 2); FLAG 3 accepted exception noted |
| 5 | Type discipline: only Archivo + Martian Mono + system glyph | PASS |
| 6 | Honest conversion path: no urgency, no fake scarcity, no sticky CTA bars, no popups | PASS |
| 7 | Accessibility floor: keyboard, aria-live, reduced motion, section-10 contrast | PASS after fixes (FLAG 4, FLAG 5); documented desktop-rest exceptions listed |

Flag rulings applied:

- FLAG 1 (FIXED, item 4). `.trail-dot` used `border-radius: 50%`, a third radius
  value beyond the two tokens. Changed to `var(--radius-pill)` in css/styles.css.
  A circle at 12x12 is visually identical under a 999px pill radius, so no visual
  change. All eleven `border-radius` declarations in styles.css now resolve to one
  of exactly two tokens (--radius-pill, --radius-surface); the two-radii rule holds.

- FLAG 2 (FIXED, item 4). Three inline-text focus rings
  (`.footer-email a:focus-visible`, `.form-status-msg a:focus-visible`,
  `.form-retry:focus-visible`) carried `border-radius: var(--sp-2)`, a third corner
  radius. The `border-radius` property was removed from all three; the inset accent
  ring (--shadow-field-focus) now renders square-cornered on inline text, which is
  fine and keeps the two-radii rule. SIDE EFFECT (noted): --sp-2 was the only use
  of that spacing token, so --sp-2 is now defined but unused. The 3.1 token block
  is left verbatim per house rules (tokens not deleted); flag that CONCEPT 3.1's
  "all values in use" annotation no longer holds for --sp-2.

- FLAG 3 (ACCEPTED EXCEPTION, no code change; item 4 / item 6 intent). The audit's
  fixed/sticky-element scan flagged the `position: fixed` `.trail-dot` nodes (and
  the `#dot-grid` canvas). Ruling: the audit item's intent is banning sticky CTA
  chrome (persistent bars/popups that pressure conversion), not ephemeral
  decorative nodes. The trail dots are transient pointer-trail glints spawned on
  pointermove and removed at 2200ms (WAAPI lifetime, section 3.3), never bound on
  touch or under reduced motion, and carry no CTA/navigation. The dot-grid canvas
  is a decorative aria-hidden background. Neither is sticky chrome. Recorded as a
  narrowly scoped, accepted exception: `position: fixed` is permitted ONLY for
  these two ephemeral/decorative nodes and must not be used for any persistent bar,
  banner, CTA or popup.

- FLAG 4 (FIXED, item 7, contrast). `--grey-placeholder` (#9A9AA2) on the field
  background (--surface-field #FAFAFA) measured 2.68:1 and the placeholder is each
  field's only visible label. `.field::placeholder` changed to `var(--ink-mid)`
  (#54545C), measured 7.19:1, clears AA. The `--grey-placeholder` token is left in
  the 3.1 block verbatim and is now UNUSED (noted). Additionally, aria-label
  attributes were added to the three fields ("Name", "Business", "What do you need
  built?") in index.html so screen-reader users do not depend on placeholder
  semantics; invisible, no visual/design change.
  DEVIATION from 3.1 token usage, reason CONCEPT section 10 AA mandate: the spec
  token for the placeholder colour (--grey-placeholder) fails AA as the sole label,
  so it is replaced by --ink-mid (an existing 3.1 token that passes). Contrast
  computed with the WCAG formula: old 2.68:1, new 7.19:1.

- FLAG 5 (FIXED, item 7, contrast). `.row--cta .row-index` at `--cta-index`
  (rgba(20,20,22,0.5)) measured ~3.19 to 3.44:1 across the pastel fill pixels
  (~3.31:1 typical), below AA, and its 0,2,0 specificity was also defeating the
  section-10 mobile and focus remediation. Applied the SAME remediation pattern
  approved for the grey tags (CONCEPT section 10):
  - Desktop rest keeps `--cta-index` per the 3.1 token and the 3.4 C1 state
    (documented desktop-rest exception, the same class of exception already logged
    at stage 5 for grey-soft on --ground at desktop rest).
  - Under `:focus-visible`, `.row--cta:focus-visible .row-index` darkens the index
    to `var(--ink-mid)`. Specificity 0,3,0 strictly exceeds the base 0,2,0 rule and
    the 0,2,0 mobile rule, so it wins whenever focus-visible matches.
  - On mobile at rest (@media max-width:900px), `.row--cta .row-index` darkens to
    `var(--ink-mid)`; equal 0,2,0 specificity to the base rule but later in source,
    so it wins inside the breakpoint.
  New index colour --ink-mid measures 5.21 to 7.19:1 across every pastel pixel, all
  clearing AA. DEVIATION note: --cta-index is retained for desktop rest only (spec
  C1 state), darkened elsewhere for the AA mandate.
  CASCADE VERIFICATION (per the brief's "test computed styles, do not assume"):
  - Reliable initial computed read over a local http server: with the pane at its
    forced 0-width viewport the (max-width:900px) query matches, and the CTA
    `.row-index` resolves to rgb(84, 84, 92) = --ink-mid, confirming the mobile
    rule both applies and beats the base --cta-index rule and the plain 0,1,0
    mobile `.row-index,.row-tag` rule.
  - CSSOM enumeration confirmed the authored rules: `.row--cta .row-index` =
    var(--cta-index); `.row--cta:focus-visible .row-index` = var(--ink-mid);
    mobile `.row--cta .row-index` = var(--ink-mid).
  - The focus-visible path and any post-mutation computed read could NOT be
    exercised in the pane: keyboard Tab does not land focus in the backgrounded
    pane, and getComputedStyle does not re-resolve after DOM changes there (proven:
    an inline `color` override, which always wins the cascade, was not reflected by
    getComputedStyle). This is the same backgrounded-pane limitation logged at every
    prior stage. The focus-visible winner therefore rests on specificity (0,3,0 >
    0,2,0, no !important), which is dispositive per the cascade spec, plus the CSSOM
    confirmation that the rule is authored correctly. Real keyboard-focus screenshot
    verification is left to the verifier subagent.

### Stage 8 - Final check (section 11): three distinctive, deliberate design choices

(1) The decode/scramble load-in: data-scramble labels resolving left to right over 650ms, once, never replayed. It sets the site's tone in its first second, a small system-booting gesture that reads as engineered rather than decorative, ties naturally to the monospace label type so character widths never shift, and then gets out of the way permanently.
(2) The CTA water-drift pill: three layered pastel gradients drifting on independent paths, a cursor-lagging hover mist, a one-shot press bloom clipped to the pill, all built from tokens with inset-only rims. It makes the single conversion action feel considered without shouting, matching the brief's confirm-and-remove-friction mandate.
(3) The inset-only shadow language: every shadow on the page (row hover, field focus, the CTA rim) is inset; there is not a single drop shadow anywhere. One consistent material logic, light pressed into surfaces at the edges, instead of the floating-card look of template output.

### Stage 8 - AMBIGUOUS note (tab order on selection)
- On selecting a row, keyboard focus does NOT jump to the panel; it stays on the
  activated row. This is a DOM-order artefact (the panel markup is a later grid
  sibling of the index). CONCEPT section 10 only requires that panel changes are
  announced via aria-live polite, which fires correctly. Accepted as-is: no spec
  requirement is unmet, and moving focus to a non-interactive panel on every
  selection could be more disruptive than helpful for keyboard users.

### Stage 8 deviations / judgement calls
- --sp-2 (FLAG 2) and --grey-placeholder (FLAG 4) are now defined-but-unused
  tokens. The 3.1 block is kept verbatim per house rules; flagged so the
  orchestrator records that CONCEPT 3.1's "all values in use" (spacing) and the
  placeholder token no longer have a live consumer.
- FLAG 3 position:fixed accepted exception is scoped narrowly to the trail dots and
  the dot-grid canvas only (see the FLAG 3 ruling above).
- CANONICAL 14-ITEM AUDIT still OPEN: only the House Tier was run this stage. The
  full canonical audit must run once the list is pasted, before outreach.

### Stage 9 - Final verify FAIL fixes (contrast)
- Status: VERIFIED PASS (re-verify 2026-07-27, 0 FAILs). Final Lighthouse
  mobile: Performance 98, Accessibility 100, Best Practices 96, SEO 100
  (verify/final/lighthouse-mobile-fixed.report.json). Stage 9 complete;
  deploying to GitHub Pages. The stage 9 final verify (verify/final/)
  returned 2 contrast FAILs; the orchestrator ruled Reading A on both (consistent
  with the CONCEPT section 10 remediation pattern and the stage 8 precedent) and
  the coder applied them exactly. Files changed: css/styles.css, PROGRESS.md.
  ?v=8 kept (no push has happened since the stage 8 bump). Encoding clean (Edit
  tool only, no BOM, no mojibake, no em dashes).

- FAIL 1 (five mono labels below AA on --ground). Lighthouse color-contrast
  (verify/final/lighthouse-mobile-report.report.json) flagged five label
  selectors: .section-label (3.11:1), .how-index (2.31:1), .proof (3.11:1),
  .footer-copy (2.31:1), .panel-head-label (3.06:1). Root token colours:
  .section-label / .proof / .panel-head-label = --grey-label (#8E8E96);
  .how-index / .footer-copy = --grey-soft (#A6A6AE). Fix (Reading A): inside the
  existing @media (max-width: 900px) block, a single grouped rule darkens all
  five to var(--ink-mid) (#54545C), the established passing token measured at
  7.19:1 on --ground. Non-interactive labels, so there is no focus state to
  darken (section 10 prescribes darkening "on mobile-at-rest and for focus"; only
  the mobile-at-rest half applies here). Desktop rest keeps --grey-label /
  --grey-soft per the prototype design.
  - EXCEPTION-CLASS UPDATE (recorded as required): the accepted desktop-rest
    contrast exception (first logged at stage 5 for grey-soft row index/tags on
    --ground, extended at stage 8 to the CTA index) now ALSO covers, at desktop
    rest only: the section labels, the how-it-works index, the proof strip, the
    footer copy and the panel head label. All darken to --ink-mid on mobile at
    rest; all retain the prototype greys at desktop rest.
  - COMPUTED-STYLE EVIDENCE (headless Chromium over a local http server, since
    the Browser pane stays backgrounded; scratchpad script, not shipped):
    - 360px (mobile): all five resolve to rgb(84,84,92) = --ink-mid, contrast
      7.19:1 on ground. PASS.
    - 1440px (desktop): .section-label / .proof / .panel-head-label =
      rgb(142,142,150) = --grey-label (3.11:1); .how-index / .footer-copy =
      rgb(166,166,174) = --grey-soft (2.32:1). Unchanged from the prototype,
      confirming the fix is scoped to the breakpoint only.
  - LIGHTHOUSE NOTE: Lighthouse's mobile emulation runs at 412px CSS width, which
    is below the 900px breakpoint, so all five labels resolve to --ink-mid under
    the audit and color-contrast now passes.

- FAIL 2 (footer mailto colour-only distinguished, link-in-text-block). The
  footer mailto was distinguished from surrounding body text by colour alone
  (accent vs --ink-body, 1.99:1 link-vs-text), which Lighthouse flags. Fix
  (Reading A): add text-decoration: underline to .footer-email a at rest, keeping
  the accent colour. text-underline-offset set to var(--sp-2) (2px, from the
  spacing scale) so the thin default underline clears the descenders in the
  address (the "p" in the placeholder / any real address) rather than cutting
  through them; a quiet, single-pixel-weight underline. This also gives the
  previously defined-but-unused --sp-2 token a live consumer again (it had gone
  unused after the stage 8 FLAG 2 fix).
  - SAME FIX APPLIED TO THE OTHER TWO IN-SENTENCE MAILTOS (instrumented, then
    decided, per the ruling): both are colour-only accent links sitting inside a
    body-text sentence, the same pattern, so both were underlined identically
    (text-decoration: underline, offset var(--sp-2)):
    - .noscript-contact a: the no-JS fallback sentence in the panel. Confirmed
      colour-only inside prose. Verified rendered (JS disabled context):
      decoration=underline, offset=2px, colour rgb(26,111,212).
    - .form-status-msg a: the failure-state mailto inside "Something broke. Email
      me directly at <address>." Confirmed same pattern. Verified by surfacing the
      failure state (valid submit short-circuits to failure on the placeholder
      endpoint): decoration=underline, offset=2px, colour rgb(26,111,212), text
      "Something broke. Email me directly at hello@placeholder.invalid."
  - The .form-retry control and the three :focus-visible rules on these links were
    left untouched: .form-retry is a standalone mono button (not a link in a text
    block), and the focus rings are a separate concern (the stage 8 FLAG 2 fix).
  - Underlines apply at ALL widths (the rules sit outside the media query),
    because link-in-text distinguishability (WCAG 1.4.1) is not viewport-scoped.

### Stage 9 deploy (2026-07-27)
- GitHub Pages enabled on main branch root. Live at
  https://arctxrus.github.io/portfolio/ (index 200, css/js/fonts/media/og
  image/favicon all 200 with ?v=8; live smoke: title correct UTF-8, row swap
  works, video autoplays, zero console errors).
- Note on the "?v bump on every push" rule: this PROGRESS-only log push
  changes no shipped asset, so no bump; the rule's intent is cache
  correctness for changed assets. Any future push touching shipped files
  bumps to ?v=9.
- HOLDING before stage 10 (cosmic-dawn PORTFOLIO_URL) until Zayn confirms
  the URL loads for him, per instruction.
