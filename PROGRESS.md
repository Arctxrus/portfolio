# PROGRESS · Zayn Portfolio

Stage log, decisions and deviations for the build defined in CONCEPT.md.
House rules: UK English, no em dashes, instrument then fix, commit per stage.

## Open items

- [ ] Replace placeholder email. `hello@placeholder.invalid` is used everywhere the
      spec says REPLACE email. It lives in a single constant (`SITE_EMAIL` in
      js/main.js, mirrored once in index.html for the no-JS footer text). Swap
      before deploy.
- [ ] Panel sub lines for the three projects: drafted at stage 3, in the page,
      need approval (see DRAFT FOR APPROVAL below).
- [ ] About and Pricing prose: drafted at stage 3, in the page, need approval
      (see DRAFT FOR APPROVAL below).
- [ ] docs/de-vibe-audit.md: the agreed checklist was not supplied in this
      workspace. A draft checklist will be written at stage 8 and submitted for
      approval before the audit runs.
- [ ] Formspree endpoint ID: form is wired with a placeholder endpoint constant;
      real ID needed before deploy.
- [ ] Stage 6 video capture depends on the live demo sites and headed Chromium
      with GPU; may be marked blocked with exact local commands.
- [ ] Stage 10 waits on the confirmed deployed URL.

## DRAFT FOR APPROVAL (stage 3 copy)

All drafted at stage 3 and implemented in the page. Nothing invented: the three
sub lines were written after fetching each live homepage and checking the actual
content (booking forms, price sections, tech). Awaiting Zayn's sign-off.

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
> I'm Zayn, a physics graduate who shipped a game played by more than three
> million people. These days I build fast, polished websites for local
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
