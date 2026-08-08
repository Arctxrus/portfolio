# PROGRESS · Zayn Portfolio

Stage log, decisions and deviations for the build defined in CONCEPT.md.
House rules: UK English, no em dashes, instrument then fix, commit per stage.

## Open items

- [x] DONE (rebrand + migration round, 2026-08-07): real email in place.
      `SITE_EMAIL` in js/main.js is now `hello@pagefront.co.uk`, and the second
      literal occurrence (the no-JS `<noscript>` fallback in index.html, mailto
      link + visible text) was updated to match. Verified in-browser: footer line,
      mailto and the form failure fallback all resolve to hello@pagefront.co.uk.
- [x] DONE (rebrand + migration round, 2026-08-07): Formspree endpoint live.
      `FORMSPREE_ENDPOINT` is now `https://formspree.io/f/mnpajqae`. Because it no
      longer contains REPLACE_FORM_ID, the placeholder short-circuit guard in
      handleContactSubmit no longer matches (verified guardMatches=false), so the
      real fetch path runs. Verified with ONE real network submission (success
      state "Sent. I will reply the same working day.") and a stubbed failure
      (graceful fallback to the email, typed message preserved, "Try again"). See
      verify/launch/form-states-evidence.json.
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
- [x] DONE (rebrand + migration round, 2026-08-07): hosting moved from GitHub
      Pages to Cloudflare Pages (auto-deploy on push to main). Live URL is now
      https://pagefront.co.uk; demos at blackthorn/barkerbloom/star.pagefront.co.uk.
      The CANONICAL SITE URL comment plus og:url, og:image and twitter:image in
      index.html were all moved to https://pagefront.co.uk. No CNAME file exists
      (nothing to remove). See the "Rebrand and migration: Pagefront" section below.

## APPROVED COPY (was DRAFT FOR APPROVAL)

Approved by Zayn 2026-07-27 with one amendment: in the About prose,
"physics graduate" becomes "astrophysics graduate". Everything else as
drafted. Sub lines, Pricing lines and the honest-floors note approved
verbatim.

AMENDED in the rebrand + migration round (owner-directed, 2026-08-07): the
wordmark is "Pagefront"; the owner's name must not appear on the shipped site,
so the About opening drops it; the demo URLs move to the new subdomains; and two
cold-email phrasings that excluded organic visitors are reworded. These changes
supersede the CONCEPT section 4 how-it-works copy and the previously-approved
About and pricing sentences, and are the current approved copy below.

Panel sub lines (mono, lower case, middle dot separators):
- Blackthorn & Co.: `single page · price menu · booking form · blackthorn.pagefront.co.uk`
  (verified: one page with anchor nav, a priced service menu, and a real
  booking form with phone + date fields, id "booking-form".)
- Barker & Bloom: `single page · prices by dog size · booking form · barkerbloom.pagefront.co.uk`
  (verified: one page, a prices-by-size section, and a stepper booking request
  form, id "bookForm".)
- Until the Last Star: `webgl · scroll-driven timeline of the universe · star.pagefront.co.uk`
  (verified: Three.js WebGL canvas scene, scroll-driven timeline from the first
  instant to the death of the last star.)

About (masthead expander, ~49 words; owner's name removed 2026-08-07):
> I'm an astrophysics graduate who shipped a game played by more than three
> million people. These days I build fast, polished websites for local
> businesses, the kind of shop or salon that deserves better than the usual
> off-the-peg site. I work quickly and directly: no agencies, no templates,
> no jargon.

How it works (amended 2026-08-07, step 01 only; 02 and 03 unchanged):
- 01 "You get in touch"  (was "You reply to my email")
- 02 "I build you a free homepage mockup"
- 03 "Live in about two weeks"

Pricing (three mono-labelled lines plus an honest-floor note):
- WEBSITES FROM £300 - A single page, written and built for your business.
- CARE PLAN FROM £25/MONTH - Hosting, edits, and keeping it fast.
- FREE HOMEPAGE MOCKUP - Get in touch and see it before you pay.
  (amended 2026-08-07; was "Reply to the email and see it before you pay.")
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

## Client feedback round 1 (CONCEPT amendments, owner-directed 2026-07-27)

Owner-directed restyle of the index toward the Moritz Petersen reference (list
items are quiet grey text at rest; the selected item is a raised white rounded-
rectangle card with the arrow glyph on its right), plus bigger V2 previews and a
re-record of the three clips with the top no longer cut. These changes SUPERSEDE
the corresponding CONCEPT 3.1 / 3.3 / 3.4 rows where they conflict; each
supersession is called out explicitly below. Where CONCEPT and the amendment
brief agreed, CONCEPT still holds.

- Status: BUILT, awaiting verification. Files changed: css/styles.css,
  index.html, tools/capture.py, media/*.webm (three), media/*.jpg (three
  posters), PROGRESS.md. All shipped asset refs bumped ?v=8 to ?v=9 (a push
  follows): 13 in index.html, 2 in css/styles.css, 0 in js/main.js. No JS change
  was needed (row selection already toggles .is-active; the restyle is pure CSS).
  Encoding clean (Edit tool only, no BOM, no mojibake, no em dashes; grep
  confirms 0 remaining ?v=8, special chars intact: £300, arrow glyph, middle dot).

### Change 1 - Row shape: rounded rectangles at --radius-surface (16px)
- Index rows 01 to 06 are now rounded-rectangle cards at var(--radius-surface)
  (16px), no longer full-bleed square-edged hairline-separated rows. The CTA row
  06 "Get in touch" is also a 16px rounded rectangle: only its radius and
  geometry changed (var(--radius-pill) to var(--radius-surface)); its pastel
  drift fill, white rim (--cta-rim), edge lift and hover mist / press bloom are
  all kept, and the bloom still clips to the card via overflow:hidden, now
  following the 16px radius.
- Hairline separators retired (see change 4). The CTA's old margin-top:--sp-14 is
  dropped so the .index-list flex gap governs spacing before it uniformly.
- TWO-RADII DISCIPLINE HELD: a radius sweep of styles.css returns exactly
  var(--radius-pill) (5 uses: visit pill, submit, trail dot, CTA mist, CTA bloom)
  and var(--radius-surface) (7 uses: panel, preview, contact card, field, form
  status, the index rows, and the CTA). 999px stays for the visit pill and submit
  button as required.
- SUPERSEDES CONCEPT 3.4 C1 "radius --radius-pill" for the CTA pill.

### Change 2 - Selected (active) row: raised white card; hover neutralised
- Active row (R3/R4) is now a raised white card: background var(--surface-white),
  a 1px var(--border) rim, and ONE restrained drop shadow. Index number and the
  arrow glyph are shown; name to --ink, tag hidden (unchanged).
- OWNER-DIRECTED AMENDMENT to the "no drop shadows, inset only" rule (CONCEPT
  3.1 shadows block / de-vibe item 4). House language is inset-only, but the
  reference raised-card look needs real elevation and the owner's direction wins.
  New token --shadow-row-active: 0 1px 3px rgba(20,20,22,0.06) (rgba(20,20,22)
  is --ink, kept on-brand), declared in a separate :root amendment block (the
  3.1 verbatim block is left untouched). It is the ONLY non-inset shadow on the
  page and is used NOWHERE except the active row card (confirmed by grep). Tuned
  by eye against the reference: quiet, the white fill + border + hidden dot grid
  under the opaque card do most of the lift, the shadow just seats it.
- The accent-blue active fill (--accent-fill-active) is RETIRED for rows.
  SUPERSEDES CONCEPT 3.4 R3 "fill --accent-fill-active". --accent-fill-active is
  now a defined-but-unused token (3.1 block kept verbatim; noted).
- HOVER on a non-active row: the accent treatment is retired. --accent-fill-hover
  and the accent inset shadow --shadow-row-hover are both dropped.
  REPORTED CHOICE: the neutral hover background is var(--surface-preview)
  (#F4F4F7), an existing surface token, chosen for strict token discipline and a
  calm quiet wash that stays clearly distinct from the white active card (so
  hover and active never read alike). The alternative "rgba white" the brief
  offered was considered and rejected to avoid a new hard-coded value; the grey
  wash matches the reference's calm feel. Index still goes to accent and the name
  to --ink on hover, the tag fades out and the glyph fades in (indices/tags
  unchanged per change 3). SUPERSEDES CONCEPT 3.4 R2 "fill --accent-fill-hover"
  and the 3.3 "Row hover" inset-shadow. --accent-fill-hover and --shadow-row-hover
  are now defined-but-unused tokens (noted; 3.1 kept verbatim).
- FOCUS-VISIBLE UNCHANGED (accessibility): the accent inset ring
  (--shadow-field-focus) is kept exactly. The new active-card box-shadow (0,2,0)
  would otherwise clobber the .row:focus-visible ring (0,2,0, earlier in source)
  on a focused active row, so a 0,3,0 rule .row.is-active:focus-visible layers
  both (ring + card elevation), preserving the ring on a keyboard-focused active
  card. Verified by specificity/source-order reasoning; the ring token is
  untouched.

### Change 3 - Unselected rows look more grey
- Rest row name colour moves from --ink-mid to var(--grey-label) (#8E8E96) at
  DESKTOP rest. SUPERSEDES CONCEPT 3.4 R1 "name --ink-mid" and the 3.2 row-name
  colour at rest.
- ACCESSIBILITY GUARD (established remediation pattern extended): #8E8E96 on
  --ground is ~3.1:1, below WCAG AA, so the name darkens to var(--ink-mid)
  (~7.0:1) at the mobile breakpoint at rest (added .row-name to the existing
  @media max-width:900px darken group) AND under :focus-visible (added .row-name
  to the existing .row:focus-visible darken group, declared before hover/active
  so those still win to --ink). Hover and active still darken the name to --ink
  (both pass AA). So the only sub-AA state is desktop MOUSE-rest, which is exactly
  the accepted desktop-rest exception class already logged at stages 1/5/8/9 for
  the grey tags, indices and mono labels; the row name now joins that class.
  Recorded as an extension of that exception.
- Tags and indices unchanged from their current handling (rest --grey-soft;
  hover/active index to accent; mobile-rest and focus darkened to --ink-mid), per
  the brief.

### Change 4 - Healthy white space (gap replaces hairlines)
- .index-list is now a flex column with gap var(--sp-6) (6px) between rows; the
  border-top hairline and the per-row border-bottom hairlines are removed.
  SUPERSEDES the CONCEPT 3.1 layout implication of flush hairline-separated rows.
- Row vertical padding raised from the documented 11px literal to var(--sp-14)
  (14px, on the scale) at rest. Horizontal padding raised to var(--sp-16) so the
  card text has breathing room inside the rounded rectangle.
- REPORTED CHOICES: gap --sp-6 (the tighter of the brief's --sp-6 / --sp-10
  options) and padding --sp-14 were chosen deliberately as the tightest of the
  brief's suggested values BECAUSE of the min-height 860 fit (below); --sp-10 gap
  would have left the column dangerously tight once a low row is active.
- MEASURED LEFT-COLUMN FIT (headless Playwright, viewport forced so the page
  sits at min-height 860): page height 860; index-list 311px (six ~47px cards +
  five 6px gaps); FRESH LOAD footer bottom 830.9 (29.1px clear of the 860 bottom,
  no clip, no page scroll: document scrollHeight 860 equals a real 860 viewport);
  DEEPEST ROW ACTIVE (row 05 Pricing, worst-case push, +8px from the grow) footer
  bottom 838.9 (still 21.1px clear, no scroll); how->proof abut with proof's own
  32px padding-top as the visual gap (no collision). On a normal 1440x900 desktop
  (100vh 900) the proof re-pins toward the bottom with 13.1px of margin-top:auto
  slack, as intended. Conclusion: the whole column fits within 100vh at min-height
  860 in every state and the proof strip never collides with HOW IT WORKS.

### Change 5 - Selection grow-and-push (carousel feel)
- The active card grows its vertical padding from var(--sp-14) to var(--sp-18)
  (+4px per side, +8px total height), transitioned via a padding transition on
  .row at 200ms ease (within the existing 160 to 220ms band), so neighbours slide
  smoothly as the flex layout reflows. Subtle, no bounce, no overshoot (plain
  ease). The CTA does NOT grow (no persistent selected state; C5 stands).
- REDUCED MOTION: the global 3.3 guard forces transition-duration ~0 on
  everything, so the size change applies instantly (no transition) as required;
  no extra rule needed.
- MOTION TABLE AMENDMENT (new row, recorded as required):
  | Name | Property | Duration | Delay | Easing | Trigger | Reduced motion |
  | Selection grow | layout padding (--sp-14 to --sp-18) | ~200ms | 0 | ease | row select (.is-active) | instant |

### Change 6 - Bigger V2 previews
- The preview is now the dominant element. New rule .view--project { max-width:
  none } drops the base .view 560px cap FOR THE PROJECT VIEW ONLY, so at desktop
  the V2 block fills the panel body and, less the --sp-32 side padding, the
  preview lands at ~91% of the panel body inner width. Title, sub, caption and
  visit pill sit below at the same full width. The base 560px cap is kept for the
  About/Pricing/form views (readable prose, 440px form card).
- MEASURED at 1440x900 (Blackthorn selected): panel body inner width 746px,
  view 746px, preview 682px = 91.4% of the panel body (target "roughly 90%");
  preview ratio 1.778 = 16/9. The view fits the panel exactly (view scrollHeight
  716 == panel-body clientHeight 716) and the panel does not scroll (panel
  scrollHeight 766 == clientHeight 766). Zero layout shift between poster and
  video is preserved (the .preview aspect-ratio reserves the box independent of
  media, unchanged).
- MOBILE unchanged: the base .view is already max-width:100% inside the
  max-width:900px block, so change 6 is a no-op on mobile and the mobile 2/1
  preview is untouched. MEASURED 60vh budget still holds and every view is the
  same panel height (no reflow on swap), no horizontal scroll:
  - 360x780: 60vh=468, panel 468 for V2/V3about/V3pricing/V4.
  - 390x844: 60vh=506, panel 506.4 for all four.
  - 768x1024: 60vh=614, panel 614.4 for all four.
- Kept aspect-ratio 16/9 desktop, 2/1 mobile per CONCEPT.

### Change 7 - Re-record all three clips, top no longer cut
- ROOT CAUSE (confirmed from the stage-6 pipeline): capture recorded 1280x800 and
  ffmpeg centre-cropped to 16:9, dropping 40px off the TOP (and bottom), which
  chopped the Blackthorn nav pill. FIX (native-viewport route, as preferred by
  the brief): tools/capture.py now records at a native 16:9 viewport REC_W,REC_H
  = 1280,720 and vfilter() is a straight "scale=800:450" with NO crop, so the top
  of every page is captured in full.
- Re-recorded Blackthorn, Barker & Bloom AND the star clip with the SAME GPU args
  and the SAME star parallax settings as the approved star take (t 0.845 peak
  lens, circular pointer orbit amp 240x150, 3.5s period, 8.5s keeper) and the
  same scroll scripts otherwise (blackthorn/barker absolute-px segments unchanged;
  star still driven by timeline t so the epoch framing is identical, only the
  viewport is 80px shorter). Star renderer re-confirmed in-context: ANGLE (NVIDIA
  GeForce RTX 3060 Laptop GPU ... D3D11), so the tier-2 lens is real, not a
  software fallback. Re-processed to 6 to 8s, 800px wide (800x450), VP9, posters
  under ~40KB, SAME filenames (media refs unchanged, only ?v bumped).
- NEW CLIP SIZES (all in the 300 to 500KB / 6 to 8s budget; dims 800x450; posters
  under 40KB; old media backed up to the scratchpad before overwrite):
  - blackthorn-preview.webm   7.03s  389KB (VP9 430k)   blackthorn-poster.jpg  38KB
  - barker-bloom-preview.webm 6.03s  408KB (VP9 697k, auto-retuned up from 470k)
                                                        barker-bloom-poster.jpg 38KB
  - until-the-last-star-preview.webm 7.03s 401KB (VP9 650k auto-retuned to 484k)
                                                        until-the-last-star-poster.jpg 32KB
- CONFIRMED in the rendered page (poster = frame 0 of the processed clip): the
  Blackthorn top nav pill (logo + Prices/Barbers/Gallery/About/Visit + Book now)
  is FULLY visible in frame 0, no top crop. The Barker & Bloom nav pill is
  likewise fully in frame, and the star clip shows the lensed black hole (THE
  LONG NIGHT) with the photon ring. Frame-0 posters inspected directly.
- MINOR (pre-existing, not a regression, out of scope): the star clip shows a
  thin right-edge scrollbar from the recorded demo viewport (width was never
  cropped, so this was present in the prior clip too). Left as-is; the brief was
  the top crop.

### Change 8 - Cache bust ?v=8 to ?v=9
- Every shipped ?v=8 bumped to ?v=9 (a push follows): 13 in index.html (css, js,
  six media refs, og:image, twitter:image, favicon.svg, favicon-32.png,
  apple-touch-icon.png), 2 in css/styles.css (two @font-face src), 0 in
  js/main.js. Media filenames carry no version, so the re-recorded clips are
  picked up by the bumped refs. Done with the Edit tool (encoding-safe); grep
  confirms 0 remaining ?v=8 in shipped files. The two ?v=8 in
  verify/final/*.report.html are historical verification artifacts and were left
  untouched.

### Client feedback round 1 - deviations / notes
- NEW TOKEN --shadow-row-active is the only non-inset shadow on the page,
  owner-directed, scoped to the active row card only (change 2). Recorded as a
  supersession of the inset-only rule for that card.
- DEFINED-BUT-UNUSED TOKENS after this round (3.1 block kept verbatim per house
  rules; flagged so the orchestrator records that these no longer have a live
  consumer): --accent-fill-active, --accent-fill-hover, --shadow-row-hover (all
  retired by the reference restyle), in addition to the previously-noted --sp-2
  (now used again by the underline offset) and --grey-placeholder.
- ROW NAME DESKTOP-REST CONTRAST: moving the rest name to --grey-label puts the
  main interactive labels below AA at desktop mouse-rest. This is an owner-directed
  design choice (the reference's quiet grey), remediated on mobile-rest and
  focus-visible exactly like the established pattern, with hover/active at --ink.
  Joined to the accepted desktop-rest exception class; must be re-checked at any
  future de-vibe / accessibility gate.
- NO JS CHANGE: the restyle is pure CSS; row selection already toggles .is-active
  and shows the glyph on active, so the reference behaviour needed no script edit.
- VERIFICATION NOTE: unlike the backgrounded Browser pane (which times out on
  screenshots), all measurements and screenshots this round were taken with a
  headless Playwright pass over file:// (reduced-motion for deterministic swaps);
  the capture ran in real headed GPU Chromium. Numbers above are measured, not
  estimated. Screenshot/visual sign-off remains the verifier's.

## Client feedback round 2 (CONCEPT amendments, owner-directed 2026-07-27)

Six owner-directed amendments plus a cache-bust. These SUPERSEDE the noted
CONCEPT / round-1 rows where they conflict; each supersession is called out.

- Status: BUILT, awaiting verification. Files changed: css/styles.css,
  index.html, js/main.js, tools/capture.py, tools/README.md, media/*.webm
  (three), media/*.jpg (three posters), PROGRESS.md. All shipped asset refs
  bumped ?v=9 to ?v=10 (a push follows): 13 in index.html, 2 in css/styles.css,
  0 in js/main.js. Encoding clean (Edit tool + sed only, no BOM, valid UTF-8, no
  em dashes; grep confirms 0 remaining ?v=9; £300 x8, arrow x10, middle dot x14
  intact). All page changes measured/screenshotted with a headless Playwright
  pass over file://; the three clips re-recorded in real headed GPU Chromium.

### Item 1 - CTA grows too (C5 amended)
- When the form view (V4) is active, the CTA row 06 now grows exactly like an
  index row: vertical padding --sp-14 to --sp-18 (+8px total height), the same
  ~200ms ease as the index-row grow, so it pushes its neighbour (measured: the
  HOW block moves down 8.0px on desktop). It gains NO white card, border or
  accent styling: only padding changes, so the pastel drift fill, white inset
  rim (--cta-rim), edge lift, hover mist and press bloom are untouched.
- STATE APPROACH (reported): a PARALLEL `is-open` class carries the grow (CSS
  `.row--cta.is-open { padding: var(--sp-18) var(--sp-18) }`), deliberately NOT
  `.is-active`, so none of the `.row.is-active` colour/border/shadow rules can
  ever match the CTA. Horizontal padding stays --sp-18 (the CTA rest value), so
  only the vertical grow reads. The CTA transition gained `padding 200ms ease`.
- ARIA-PRESSED APPROACH (reported): aria-pressed was EXTENDED to the CTA, so the
  six rows form one single-selection group with exactly one pressed at a time.
  In js/main.js initPanel: the CTA starts aria-pressed="false"; select() toggles
  the CTA's `is-open` + aria-pressed true only when the CTA is chosen, and the
  index-row loop (CTA is not an index row) already clears every index row when
  the CTA is chosen. Selecting any index row sets the CTA is-open false and
  aria-pressed false, so it CLEARS the moment another view opens (per the brief).
  Verified: cta rest padTop 14px / aria false; index row active padTop 18px /
  aria true, CTA aria false; CTA open padTop 18px / aria true, bg transparent (no
  colour), borderColor transparent (no border), box-shadow still inset (rim, no
  drop shadow), the previously-active index row aria back to false.
- SUPERSEDES CONCEPT 3.4 C5 "no persistent selected styling on the pill" to the
  amended "no colour/selection styling, but it does grow while its view is
  active", and supersedes round-1 change-5's "the CTA does NOT grow".
- Reduced motion: the global 3.3 guard forces the padding transition instant, so
  the CTA grow applies with no animation, matching the index-row grow. No new
  listeners bound, no nodes spawned.

### Item 2 - Button shape: 999px pill to --radius-surface (16px)
- The submit button moves from --radius-pill (999px) to --radius-surface (16px),
  the new button language. The "Visit live site" pill ALSO moves to 16px for
  consistency: FLAGGED as the coder's judgement call for the owner to veto (both
  changes recorded here as required).
- RADIUS CONSUMERS AUDIT (grep of css/styles.css after the change): the
  two-radii rule stands. All 12 `border-radius` declarations resolve to exactly
  two tokens: 9 use --radius-surface (.row, .row--cta, .panel, .visit-pill,
  .field, .submit, .form-status, .contact-card, .preview) and 3 use
  --radius-pill (.cta-mist, .cta-bloom, .trail-dot). So --radius-pill is NOT
  defined-but-unused: it still serves the three fully-round decorative nodes
  (a 999px radius renders them as circles). No raw 999px or 50% appears in any
  border-radius. SUPERSEDES the "pill" wording for the submit and the visit
  control (CONCEPT section 5 "quiet secondary pill" and the submit F4 pill).

### Item 3 - Preview quality: native 1280x720, VP9 CRF
- Root cause of the softness: round 1 output 800x450, which upscaled soft in the
  panel at ~680px+ and on larger screens. tools/capture.py now exports at NATIVE
  1280x720 (no downscale from the 1280x720 take; OUT_W/OUT_H) in VP9 CRF quality
  mode (`-crf N -b:v 0`), not a bitrate target.
- CRF CHOSEN: 34. Tuned by eye on decoded webm frames at 1280x720. Across CRF
  32/33/34 the size moved only ~10% (blackthorn 1504/1436/1364KB) and all were
  crisp, so 34 (top of the sanctioned 32 to 34 range, smallest) was taken per
  the owner's "as small as possible while crisp" direction.
- BUDGET AMENDED (owner direction, recorded): the 300 to 500KB per-clip budget
  no longer applies; quality wins, each clip is as small as CRF makes it while
  crisp. Clips remain lazy-loaded, so the first-load budget is UNTOUCHED (the
  page still ships no webm on first load; only posters, unchanged behaviour).
- NEW CLIP SIZES (native 1280x720, VP9 crf 34, no audio, 6 to 8s; posters 1280
  wide, jpg, under ~80KB; old media backed up implicitly by overwrite, raws in
  tools/_raw):
  - blackthorn-preview.webm   7.03s  1364KB   blackthorn-poster.jpg  68KB
  - barker-bloom-preview.webm 6.03s   482KB   barker-bloom-poster.jpg 79KB
  - until-the-last-star-preview.webm 7.03s 1000KB  until-the-last-star-poster.jpg 64KB
- Star renderer re-confirmed in-context (tier-2 lens real, not a fallback):
  ANGLE (NVIDIA GeForce RTX 3060 Laptop GPU ... D3D11). Same peak-lens framing
  and circular parallax settings as round 1.

### Item 4 - Scrollbar removed from the captures
- tools/capture.py injects `NO_SCROLLBAR_CSS` into each page BEFORE the keeper
  (via page.add_style_tag): `html { scrollbar-width: none; -ms-overflow-style:
  none }` and `::-webkit-scrollbar { display: none; width: 0; height: 0 }`.
- SCROLLBAR-FREE CONFIRMED: all three clips re-recorded (Blackthorn, Barker,
  star) with the same GPU/parallax/scroll settings. Frame-0 posters inspected
  directly: no scrollbar on the right edge of any of the three (the previous
  star clip's thin right-edge scrollbar, noted in round 1, is now gone). The
  star (cosmic-dawn) take was checked per the brief's warning about sites sizing
  off scrollbar width: the WebGL scene, captions, nav and the lensed black hole
  frame are all correct, so hiding the scrollbar did not disturb the scene.

### Item 5 - V2 layout rethink: scrollable project view
- The project view is now a vertically scrollable column INSIDE the panel
  (overflow-y: auto on .view--project). Layout: a LARGE preview at the top
  (height 70% of the view; aspect-ratio dropped so height governs and the box is
  reserved, so zero poster-to-video layout shift), a bottom fade cue, then the
  title, mono sub, caption bar and the "Visit live site" button revealed by
  scrolling. Wheel/trackpad scroll is native (no hijack, no scrubbing: no JS
  wheel handler exists).
- FADE CUE (reported choice): implemented as a luminance `mask-image` on the
  preview (linear-gradient opaque to transparent over the bottom 72px), NOT a
  hard-coded colour overlay. The panel behind the preview is the same
  --surface-preview colour, so the preview dissolves into the panel ("fade to
  the panel surface colour"). The mask uses opaque/transparent sentinels only,
  so no palette token is hard-coded.
- SCROLLBAR (reported choice): HIDDEN (scrollbar-width: none, ::-webkit-scrollbar
  display none) because the bottom fade replaces it as the "more below" cue.
- KEYBOARD: the .view--project container carries tabindex="-1" (belt and braces)
  and the preview anchor + visit-pill anchor are focusable; focusing the visit
  pill natively scrolls it into view. Verified: focusing the visit pill makes it
  the active element and brings it fully into the scroll container at every
  tested height.
- THREE-VIEWPORT VISIT-BUTTON REACHABILITY (measured, desktop widths >900px, so
  min-height:860px clamps 720/620 to an 860 layout with body scroll):
  - 1440x900: panelBody 716, view 716, preview 456, NOT internally scrollable
    (content fits), visit button visible at rest AND in-view after focus.
  - 1280x720: view client 676 / scroll 694, internally SCROLLABLE, visit button
    reachable (in-view after focus, scrollTop stays 0; also body-scrollable since
    the 860 clamp makes the page taller than the viewport).
  - 1280x620: same 860-clamped layout as 720 (view 676/694, scrollable), visit
    button reachable by internal scroll to bottom (screenshot) and by focus.
  In every case the button is reachable, which was the failure the brief
  targeted (the overflow:hidden panel previously trapped it).
- MOBILE (measured, kept compact per the brief, it does not clip): the desktop
  scroll/large-preview/mask is undone in the max-width:900px block. 390x844:
  view overflow visible, preview aspect 2/1 (150px), panel 506, no internal
  scroll. 360x780: preview 135px, panel 468, no scroll. The 60vh budget and the
  no-reflow-on-swap behaviour are preserved.
- SUPERSEDES round-1 change-6 (centred full-width non-scrolling V2). The base
  .view 560px cap override for the project view is kept.

### Item 6 - V1 welcome optical centring
- The "SELECT A PROJECT" line is optically centred on the giant ghost arrow's
  visual mass. MEASUREMENT: canvas TextMetrics plus a boosted-colour screenshot
  pixel scan of the real page (Segoe UI, the resolved system font on this
  Windows host). The arrow ink is horizontally CENTRED in its advance (dX about
  0), and with line-height 0.8 its mass sits about 42.7px BELOW the line-box
  centre where the text is (not "up-right": that holds for the em square, not for
  the actual line-height-0.8 layout, so only a vertical offset is applied).
- OFFSETS CHOSEN: the glyph is nudged UP so its mass centres on the text (which
  stays at the true panel centre). Desktop (340px): translateY -43px. Mobile
  (160px): translateY -20px (the proportional 43 * 160/340). Horizontal offset:
  none (measured ~0). Applied on `.welcome-glyph` transform
  (`translate(-50%, calc(-50% - 43px))`, and -20px in the mobile block).
- BY-EYE CONFIRMATION: screenshots at desktop 1440x900 and mobile 390x844 show
  the line sitting visually centred on the arrow at both sizes.

### Item 7 - Cache bust ?v=9 to ?v=10
- Every shipped ?v=9 bumped to ?v=10 (a push follows): 13 in index.html (css,
  js, six media refs, og:image, twitter:image, favicon.svg, favicon-32.png,
  apple-touch-icon.png), 2 in css/styles.css (two @font-face src), 0 in
  js/main.js. Media filenames carry no version, so the re-recorded clips are
  picked up by the bumped refs. sed did the bump (encoding-safe); grep confirms 0
  remaining ?v=9 in shipped files.

### Client feedback round 2 - deviations / notes
- ITEM 2 visit-pill radius is the coder's judgement call, flagged for owner veto.
- BUDGET SUPERSESSION (item 3): the CONCEPT section 5 / round-1 "300 to 500KB"
  per-clip budget is retired by owner direction; clips are now 482KB to 1364KB.
  First-load budget is untouched (clips stay lazy-loaded).
- MASK SENTINEL (item 5): the preview fade uses a mask-image whose opaque stop is
  a mask sentinel (#000), not a themed colour, so the "no hard-coded value that
  has a token" rule is not breached (mask luminance is not a palette colour).
- No new tokens, no new radii, no new border width, no new drop shadow this
  round. The active-row --shadow-row-active (round 1) remains the only non-inset
  shadow and is still NOT applied to the CTA (item 1 keeps the inset rim only).
- VERIFICATION NOTE: page behaviour and geometry were measured with a headless
  Playwright pass over file:// (numbers above are measured, not estimated) and
  the three clips were recorded in real headed GPU Chromium with frame-0 posters
  inspected directly. Screenshot/visual sign-off remains the verifier's.

## Client feedback round 3 (owner-directed 2026-07-27)

Four defect/feature items plus a cache-bust. Items 1 and 4 were reproduced
visually FIRST (zoomed/measured before any change), then fixed, then re-checked.
SUPERSESSION (recorded per the brief): on desktop the project preview no longer
autoplays; it is SCROLL-SCRUBBED (scroll position drives video.currentTime).
This supersedes CONCEPT section 5 "muted, looping webm (autoplay)" and round-2
item 5's native-scroll-no-scrubbing wording FOR DESKTOP ONLY. Mobile keeps the
muted autoplay loop.

- Status: BUILT, awaiting verification. Files changed: index.html (3 project
  blurbs + ?v bump), css/styles.css (CTA border fix, tall scroll-scrub preview,
  .project-blurb, ?v bump), js/main.js (scroll-scrub video controller),
  tools/capture.py (star parallax/crop, dense keyframes), media/*.webm (three
  re-encoded), media/*.jpg (three posters re-exported), PROGRESS.md. All shipped
  refs bumped ?v=10 to ?v=11 (a push follows): 13 in index.html, 2 in
  css/styles.css, 0 in js/main.js. Encoding clean (Edit + sed only): no BOM, no
  mojibake, no em dashes; 0 remaining ?v=10.

### Item 1 - Star clip bottom curve (confirmed cause + fix)
- CONFIRMED CAUSE (visual, not guessed): the owner's "bottom curve" is the
  lensed accretion disc's bright LOWER ARC. On the old clip the large vertical
  parallax (amp_y 150) swung the black hole low so that arc dipped into the
  panel preview's bottom fade band and dissolved into grey, reading as a stray
  curved edge. It was NOT a container edge or UI element. Confirmed by
  simulating the exact desktop preview crop (object-fit cover + 72px bottom
  fade) on extracted frames.
  Before/after evidence: verify/round-3/star-desktop-preview-sim.png (old, arc
  in the fade at the poster frame) and verify/round-3/star-before-after.png
  (poster: BEFORE vs AFTER reduced-parallax vs AFTER+crop, stacked).
- FIX (capture level, re-recorded on the same GPU/scrollbar-hidden setup):
  1. tools/capture.py star parallax reduced to a gentle orbit dominated by the
     horizontal sweep: amp_x 240 to 150, amp_y 150 to 44, period 3.5s to 4.0s.
     The lens still shifts (reads as 3D) but the disc stays centred, so the
     bright arc no longer reaches the fade at the poster/loop frame.
  2. A gentle bottom-anchored reframe crop (crop=1280:680:0:40 then scale back
     to 1280x720): drops the top 40px of dark sky, nudging the whole disc up so
     the bottom stays clean dark space across EVERY scrub frame (the clip is now
     scrubbed, so all frames are seen). Measured fade-band max luminance: a
     steady ~120 across frames (uncropped ~137, old clip ~135), i.e. the lower
     arc is reliably above the fade.
  Renderer re-confirmed in-context (tier-2 lens real, not a fallback):
  ANGLE (NVIDIA GeForce RTX 3060 Laptop GPU ... D3D11). New frames verified
  clean top and bottom (verify/round-3/star-new-poster.jpg,
  verify/round-3/v2-star-rest.png).

### Item 2 - Scroll-driven playback on desktop (supersedes desktop autoplay)
- BEHAVIOUR: desktop project views scrub the video from scroll. In
  js/main.js configureProjectVideo(): progress = view.scrollTop /
  (view.scrollHeight - view.clientHeight) maps to video.currentTime. Normal
  motion eases currentTime toward the scroll target via a rAF lerp (SCRUB_LERP
  0.18, i.e. ~18% of the gap per frame, inside the briefed 15 to 20%); reduced
  motion snaps currentTime to the target with NO rAF (user-driven scrubbing is
  allowed, but no autonomous smoothing runs, and the video never autoplays on
  desktop). Verified over file:// (the only way to seek locally, see the
  server note): scroll 1.0/0.75/0.5/0.25/0.0 -> currentTime
  7.03/5.27/3.53/1.76/0.03s (forward AND reverse track precisely); lerp eased
  5.85 -> 6.74 -> 6.98 -> 7.02 -> 7.03 after a jump to 100%; reduced-motion
  scroll 0.8 snapped to 5.62s, video still paused.
- SCROLL TRACK: .view--project .preview height 70% -> 100% (fills the visible
  panel; the copy below is the scroll track). Adaptive (100%, not a fixed px,
  so tall desktops still overflow and scrub). Measured scrub range and
  visit-button-below-fold-at-rest at all three briefed viewports:
    1440x900:  range 296 to 319px (star 319, blackthorn/barker 296), visit below fold
    1280x720:  range 309 to 332px, visit below fold
    1280x620:  range 309 to 332px, visit below fold
  All "a few hundred px" and the visit button is hidden until scroll. The bottom
  fade stays as the "more below" cue.
- KEYFRAMES / RE-ENCODE (item 2 seeking smoothness): tools/capture.py -g 60 ->
  -g 12 (KEYFRAME_INTERVAL const), a keyframe every ~0.4s at 30fps, so reverse
  seeks resolve promptly (old star clip had 4 keyframes over 7s; scrubbing back
  stuttered). Quality unchanged (1280x720, VP9 CRF 34). All three RE-ENCODED
  from the raw takes (star from the new reduced-parallax take; blackthorn/barker
  from the existing raws). New keyframe counts / sizes (sizes rose, accepted):
    blackthorn-preview.webm   18 keyframes  1996KB (was ~1364KB, 4 kf)
    barker-bloom-preview.webm 15 keyframes  1376KB (was ~482KB)
    until-the-last-star-preview.webm 18 keyframes 1408KB (was ~1000KB)
  Clips stay lazy-loaded, so the first-load budget is untouched.
- PRELOAD: desktop sets video.preload='auto' when the project view opens (so the
  frames are buffered for smooth seeking); nothing loads before selection (the
  video only enters the DOM on selection, template-clone architecture). Poster
  (frame 0) shows until the first scroll (currentTime is not touched until then).
- ATTRIBUTE-MANAGEMENT APPROACH (reported): TWO CODE PATHS ON ONE ELEMENT.
  configureProjectVideo(view) runs on each project-view render and derives the
  video's mode from mobileLayoutQuery. Desktop: autoplay/loop attributes and
  properties removed, muted, preload='auto', paused, scroll-scrub wired. Mobile:
  autoplay/loop/muted restored and play() called (unchanged mobile behaviour).
  A mobileLayoutQuery 'change' listener re-configures the currently-open project
  view if the viewport crosses 900px mid-session (stopScrub() tears down the
  scroll listener, rAF and loadedmetadata handler first, so nothing double-binds
  or leaks). Verified: desktop video paused, no autoplay/loop attrs, preload
  auto; mobile (390px) autoplay+loop true, playing.
- KEYBOARD: the .view--project scroll container is native overflow scroll.
  Focusing the preview anchor (a Tab stop inside it) and pressing PageDown/arrows
  scrolls the container (verified: scrollTop 0 -> 18 at 1280), so keyboard users
  scrub too. tabindex="-1" on the view is kept as the belt-and-braces focus
  target; no extra Tab stop was added.
- SERVER/SEEK NOTE (instrumented, not guessed): the local python http.server
  returns 200 with NO Accept-Ranges, so Chromium marks progressive media
  non-seekable (seekable [0,0]) even when fully buffered, and currentTime will
  not move. Over file:// the same webm is seekable [0,duration] and scrubbing
  works. GitHub Pages sends Accept-Ranges: bytes, so production seeks correctly.
  All scrub verification above was therefore run over file://. THE VERIFIER MUST
  serve with a Range-capable server (or use file://) or the scrub will look
  dead through a plain python http.server. This is an environment artefact, not
  a code bug.

### Item 3 - Copy under the fade (DRAFT FOR APPROVAL, round 3 copy)
- A short factual paragraph now sits in each project view between the preview
  fade and the caption/visit button (.project-blurb, Archivo 14px, --ink-body,
  line-height 1.6, max-width 46ch). Placed after the sub line, before the
  caption bar. They SHIP NOW; the owner will veto or amend. Drafted from the live
  sites (fetched 2026-07-27), UK English, no em dashes, each under ~50 words:

  DRAFT FOR APPROVAL (round 3 copy):
  - Blackthorn & Co. (46 words):
    "A single fast page for a Heywood barbershop. The whole price list is on
    view, from a £12 kids' cut to the £52 full works, next to a profile for each
    barber and a booking form that captures the date, time and chair a client
    wants."
    (verified live: services £12 to £52, four named barbers, a booking form with
    name/mobile/service/date/time/barber/chair-preference fields, Heywood.)
  - Barker & Bloom (42 words):
    "One clear page for a dog grooming salon. Prices are set out by dog size,
    from an £18 puppy's first groom upwards, with add-ons like nail trims listed
    plainly and a two-step form that requests a slot by size, day and time."
    (verified live: Bath & Brush/Full Groom priced by size, £18 puppy groom,
    add-ons incl. £8 nail trim, a two-step request form.)
  - Until the Last Star (45 words):
    "A technical piece, not a client site. The whole history of the universe runs
    on one scroll, drawn live in the browser with WebGL. The finale bends
    starlight around a black hole using real gravitational lensing, computed every
    frame rather than faked with a picture."
    (verified: Three.js WebGL scroll-driven timeline; the finale is a real
    screen-space gravitational-lens pass on the RTX 3060, not a sprite fallback.)

### Item 3 - verifier FAIL fix (mobile 60vh reflow)
- Verifier round-3 FAIL: .project-blurb has no mobile accommodation, so V2 grew
  past the 60vh budget and reflowed the page below 900px (360x780: 468 to
  ~594/616px; 390 and 768 similar). Evidence: verify/restyle-3/.
- Fix (orchestrator ruling): `.project-blurb { display: none }` added inside the
  existing @media (max-width: 900px) block next to the V2 mobile overrides. The
  blurb is desktop scroll-track content; mobile keeps the sub line, caption bar
  and visit button. ?v=11 kept (no push happened for this fix).
- RE-MEASURED panel height, all views, must equal V1/V3/V4 exactly: at 360 all
  seven (V1, three V2 projects, About, Pricing, form) = 468.0; at 390 all =
  506.4; at 768 all = 614.4. No V2 overrun, no reflow.
- VETOABLE (flagged): the owner may instead let mobile V2 grow so the copy is
  visible on phones. To do that, remove this one `.project-blurb { display:none }`
  rule; mobile V2 then exceeds 60vh by the blurb's height and the page reflows on
  swap. Recorded as the owner's choice.

### Item 4 - CTA outline mismatch (confirmed cause + fix)
- CONFIRMED CAUSE (pixel-level, DPR4 screenshot + scan, not guessed): .row--cta
  inherited the base .row `border: 1px solid transparent`. With default
  background-clip: border-box the pastel drift paints out to the border-box edge
  UNDER that transparent border, while --cta-rim (an inset shadow) is drawn
  inside the border, so the white rim sat 1px in from the visible edge. Edge scan
  at the top (DPR4, 4px = 1 CSS px): CSS row 0 = pastel (205,221,242), CSS row 1
  = the white rim (253,254,255). At the rounded corners the rim's radius (padding
  box, 15px) was tighter than the outer 16px, showing a pale pastel crescent.
  Before evidence: verify/round-3/cta-BEFORE-corners.png.
- FIX: `.row--cta { border: 0 }` (the transparent border served no purpose here;
  unlike index rows the CTA never gains a coloured border). The rim now hugs the
  true 16px edge. Geometry preserved with tokens: the removed 1px is added back
  to the padding via calc(... + var(--border-width)) on both the rest and the
  is-open (grow) states, so no hard-coded value and still one border width on the
  page. Precise measurement: true original CTA height 47.156px (it had a
  pre-existing `border-bottom: 0`, so only 1px of vertical border), fixed 47.0px
  = a 0.16px (sub-pixel) difference, and the item-1 grow delta is unchanged.
- VERIFIED AFTER: edge scan CSS row 0 is now the white rim (253,254,255), no
  pastel band; corners hug with no crescent. Evidence:
  verify/round-3/cta-AFTER-corners.png, verify/round-3/cta-after.png.

### Item 5 - Cache bust ?v=10 to ?v=11
- Every shipped ?v=10 bumped to ?v=11 (a push follows): 13 in index.html, 2 in
  css/styles.css, 0 in js/main.js. Media filenames carry no version, so the
  re-recorded clips are picked up by the bumped refs. sed did the bump; grep
  confirms 0 remaining ?v=10.

### Client feedback round 3 - deviations / notes
- SUPERSESSION: desktop autoplay replaced by scroll-scrub (see the header).
  Mobile autoplay muted loop unchanged; the split is by the 900px breakpoint.
- Reduced motion: desktop never autoplays; scrubbing is user-driven and snaps
  (no rAF). The scroll listener IS bound under reduced motion (it is core,
  user-driven functionality, per the brief), unlike the decorative trails/mist.
  Mobile reduced-motion autoplay is UNCHANGED from prior stages (out of scope).
- New raw star take overwrote tools/_raw/star-raw.webm; the old star webm,
  poster and raw are backed up in verify/round-3/backup/ in case a revert is
  wanted. blackthorn/barker raws were reused (not re-recorded), so only their
  encode changed (dense keyframes).
- No new tokens, no new radii, no new border width, no new drop shadow. The
  preview height 100%, the 72px fade and the reframe crop pixels are raw layout
  values with no token (consistent with the existing 440px card, 460px column,
  72px fade, etc.).
- VERIFICATION NOTE: same backgrounded-pane limitation for the built-in Browser
  pane; all behaviour and geometry above were measured with headless Playwright
  (numbers are measured, not estimated), the scrub over file:// (Range note
  above), and the star clip recorded in real headed GPU Chromium. Screenshot/
  visual sign-off remains the verifier's (serve with Range support for the
  scrub).

## Client feedback round 4 (owner-directed 2026-07-27)

The owner disliked round 3's scroll-scrub playback and chose slow, seamlessly
looping ambient animation instead (the "crossfade loop" option). The round-3 V2
layout stays (large preview with bottom fade, blurb, caption, visit button,
scrollable view); only the playback mode and the clips changed.

SUPERSESSIONS (recorded per the brief):
- Round 3's desktop scroll-scrub is RETIRED by owner direction. This re-supersedes
  the round-3 supersession of CONCEPT section 5: desktop AND mobile are back to the
  muted autoplay loop specced in section 5. The scrub controller is fully removed
  from js/main.js.
- The 6-to-8s clip-length rule (stage 6) is AMENDED to 8-to-12s for the crossfade
  clips (round-4 brief item 2). Blackthorn ships at 10.0s, Barker at 8.8s. The star
  is one camera period (4.0s), which is its own spec (item 4).

- Status: BUILT, awaiting verification. Files changed: js/main.js (scrub controller
  removed), css/styles.css (one V2 preview comment updated to match, ?v bump),
  index.html (?v bump only), tools/capture.py (slower captures, crossfade + star
  processing, normal keyframes), media/*.webm and media/*.jpg (all three
  re-recorded and re-processed), PROGRESS.md. All shipped refs bumped ?v=11 to
  ?v=12 (a push follows): 13 in index.html, 2 in css/styles.css, 0 in js/main.js.
  Encoding clean (Edit + byte-safe sed only): no BOM, no mojibake, no em dashes;
  0 remaining ?v=11.

### Item 1 - Revert playback to muted autoplay (scrub removed from main.js)
Removed from js/main.js initPanel (the entire round-3 scroll-scrub controller):
- the `SCRUB_LERP` module constant and its comment block;
- the `currentScrub` teardown handle and the `stopScrub()` function (and its call
  in `renderView`);
- the whole desktop scrub path inside `configureProjectVideo`: the attribute
  stripping (autoplay/loop removal, preload='auto', pause), the rAF lerp `apply()`,
  the scroll->currentTime `onScroll` mapping, the `scroll` and `loadedmetadata`
  listeners, and the `currentScrub` cancel object;
- the `mobileLayoutQuery.addEventListener('change', ...)` listener that re-derived
  the desktop/mobile video mode on breakpoint change (it only served the scrub
  split; both breakpoints now behave identically, so it is gone).
Kept: the `mobileLayoutQuery` const (still used by `scrollPanelIntoView`), and the
whole panel-into-view scroll behaviour (unchanged from stage 5).
New `configureProjectVideo(view)` (both breakpoints identical): set muted and call
`video.play().catch(...)` as a belt-and-braces nudge. The markup still carries
`autoplay muted loop playsinline preload="none"` (never stripped from the
templates), so on selection the clone enters the DOM and the autoplay algorithm
starts the load; preload="none" means nothing loads before selection (confirmed:
the webm is fetched only on the row click). Scrolling the view reveals the
blurb/caption/button but never touches the video. Reduced motion is unchanged from
stage 6 (a muted autoplay video was accepted there); no new listeners are bound and
the decorative trail/mist/dot-grid guards are untouched.

### Item 2 - Slower captures (scroll pace roughly halved)
tools/capture.py, glide durations (the eased scrollTo segment `dur_ms`) doubled;
holds kept. Re-recorded on the same headed GPU setup:
- Blackthorn: 2200->4400 and 2600->5200 ms. Raw take 14.76s. Base clip 10.8s ->
  10.0s shipped loop.
- Barker & Bloom: 3400->6800 ms. Raw take 12.56s. Base clip 9.6s -> 8.8s loop.
The motion now reads as calm ambient animation rather than a screen recording.

### Item 3 - Crossfade loop (Blackthorn and Barker)
Post-processed into a mathematically seamless loop with a tail->head xfade
(CROSSFADE_S = 0.8s), standard technique: split the base clip of length D into
hold=[0, D-C] and end=[D-C, D], then `xfade` end over hold at offset 0 for duration
C, output length D-C. The loop seam maps to input[(D-C)-] -> input[D-C], two
ADJACENT source frames, so it is continuous by construction; the first C seconds are
the intended tail->head dissolve. One VP9 encode straight from the raw take.
VERIFICATION (mean absolute pixel diff 0..255 between the OUTPUT's first and last
frame; a slow seamless loop reads near zero):
- Blackthorn: seam first-vs-last = 0.74
- Barker & Bloom: seam first-vs-last = 0.85
Both near-identical. Evidence frames (first/last of each output) in
verify/round-4/{blackthorn,barker-bloom}-preview-first.png / -last.png.

### Item 4 - Star: one-period orbit loop, then a FLAGGED deviation to crossfade
Capture (unchanged intent): re-captured at a FIXED scroll position (start_t 0.845,
the black-hole epoch framing from round 3, no scroll during the take), camera
parallax orbit period 4.0s, keeper_s raised 8.5->16.0 so >= 3 orbits are recorded (4
orbits). Raw take 21.96s. Scrollbar hidden and NVIDIA RTX 3060 renderer re-confirmed
in-context (tier-2 lens real, not a fallback).

FIRST ATTEMPT, exactly as briefed: a frame-accurate one-period cut (4.0s at 30fps =
120 frames) from a steady-state window, no crossfade, scanned for the start frame
whose wrap (frame N vs N+120) is smallest. INSTRUMENTED RESULT (the reason for the
deviation below): the camera orbit IS periodic, but the scene's accretion disc
rotates continuously and is NOT periodic at 4.0s, so a pure one-period cut left a
loop-seam jump of mean 7.92 against a mean adjacent-frame motion of just 0.44 (an
18x discontinuity: a visible disc "snap" every 4s). All 245 candidate windows fell
in a tight 7.2-8.7 band, confirming this is a content floor, not a cut-selection
problem. The residual concentrates on the bright lensed disc filaments, not the dark
sky (heatmap: verify/round-4/star-seam-heatmap.png).

DEVIATION (flagged for owner sign-off): item 4 said "no crossfade needed", on the
premise that camera-periodicity makes first and last frames match. Since that
premise is defeated by the disc animation, and the round's explicit goal is
"seamlessly looping ambient animation", the star now uses the SAME crossfade-loop
technique as the other two, applied so the NON-crossfaded span is EXACTLY one camera
period: base = orbit_period_s(4.0) + CROSSFADE_S(0.8) = 4.8s, output 4.0s. Because
4.0s is exactly one period the camera stays periodic-aligned across the 0.8s
dissolve (tail camera == head camera), so only the non-periodic disc gently
dissolves. RESULT: seam first-vs-last = 1.20 (down from 7.92), output still 4.00s
(one period), fixed-scroll + 4-orbit capture unchanged. IN-BROWSER (headed
Playwright, actual rendered <video> frames captured across the loop wrap): rendered
seam 1.60 vs an adjacent-frame baseline of 1.65 = 1.0x, i.e. the loop point is
indistinguishable from normal playback. Awaiting owner ratification that a 0.8s
crossfade on the star is acceptable (item 4 asked for none). If the owner insists on
no crossfade, the pure one-period cut is available but ships the 18x seam jump.

### Item 5 - Encoding back to normal keyframes; new sizes
KEYFRAME_INTERVAL 12 -> 60 (a keyframe every 2s; the dense -g 12 was only for
reverse scrubbing). 1280x720, VP9 CRF 34, no audio, unchanged. New sizes (all DOWN
versus round 3's 1.4-2MB, as expected; clips are lazy-loaded so the first-load
budget is untouched):
- blackthorn-preview.webm  10.0s  1734KB  (round 3: 1996KB)
- barker-bloom-preview.webm  8.8s  1113KB  (round 3: 1376KB)
- until-the-last-star-preview.webm  4.0s  528KB  (round 3: 1408KB)
Posters = frame 0 of each output, 1280 wide, all under the ~80KB budget
(POSTER_MAX_KB tightened 80 -> 78 for margin on the busy star frame):
blackthorn 73KB, barker 76KB, star 68KB.

### Item 6 - Integration (in-browser, headed Playwright over a local http server)
All three V2 views autoplay on selection at BOTH desktop (1280x800) and mobile
(390x800): paused=false, loop=true, muted=true, autoplay=true, preload="none",
readyState 4, currentTime advancing in real time. Loops confirmed: the star (4.0s)
wraps cleanly (rendered seam == adjacent baseline, see item 4); currentTime wraps
observed for all. Zero layout shift: the .preview box measured 507x612 identically
before and after the video loads, for every project. No media 404s (the webm is
requested only on selection), no other 404s, no console errors. Reduced-motion
guards from earlier rounds are untouched. Screenshots in verify/round-4/
(v2-*-desktop.png, v2-barker-mobile.png).

### Item 7 - Cache bust ?v=11 to ?v=12
Every shipped ?v=11 bumped to ?v=12 (a push follows): 13 in index.html, 2 in
css/styles.css, 0 in js/main.js. Byte-safe sed; grep confirms 0 remaining ?v=11.

### Client feedback round 4 - deviations / notes
- FLAGGED DEVIATION: star crossfade instead of a pure one-period cut (item 4 said no
  crossfade). Full rationale, measurements and the fallback are in the item 4 entry
  above. Owner ratification requested.
- SUPERSESSIONS recorded (see header): round-3 scrub retired (back to autoplay,
  desktop and mobile); 6-to-8s clip rule amended to 8-to-12s for the crossfade
  clips.
- No new tokens, radii, border widths or drop shadows. The V2 layout, the 72px
  bottom fade and the star crop are unchanged raw layout values from round 3.
- The old round-3 media, posters and raws remain backed up in verify/round-4/backup/
  in case a revert is wanted. All three clips this round were re-recorded from
  scratch (not reused).
- VERIFICATION NOTE: unlike stages 1-5, the capture, renderer confirmation, loop-
  seam pixel diffs and the integration/autoplay/no-shift/no-404 checks were all run
  in real headed Chromium (the GPU launches here), so the numbers above are observed
  directly. Autoplay loops do not need HTTP Range (the round-3 scrub Range caveat no
  longer applies). Screenshot/visual sign-off remains the verifier's.

### Round 4 - verifier FAIL fix + owner amendment (2026-07-27)

The above (star orbit cut, per-section glide tours, 8-to-12s clips) is SUPERSEDED
by a verifier FAIL and a further owner amendment. Only js/main.js, css/styles.css
and index.html versioning are untouched; the change is all in tools/capture.py and
the media. ?v=12 kept (no push since the bump).

VERIFIER FAIL (crossfade double exposure): the 0.8s crossfade blended two
structurally different scroll positions (cover-vs-reviews, hero-vs-bento), giving a
legible double exposure (verifier browser-rendered peak diffs 144 and 46 vs the
star's ratified ~8). A content-mismatched dissolve cannot be made subtle. Fix
(directed): make both crossfade endpoints match by ending each take back at its
START and crossfading the closing hold into the opening hold.

OWNER AMENDMENT (supersedes the capture style for ALL THREE, recorded as directed):
1. Scroll style: every clip is now ONE continuous, even, SLOW near-linear scroll
   down the page (no section glides, no mid-tour holds), noticeably slower than
   before. Length window amended again to roughly 10 to 20s; the shipped clips run
   ~16 to 17s. CRF 34 and 1280 wide unchanged; sizes grow (accepted).
2. Star: the near-black fixed black-hole shot (THE LONG NIGHT, poster luminance ~35)
   was the "black page". Replaced with a bright SCROLLING capture: wait 10s after
   load, then scroll slowly through THE AFTERGLOW ("the fog lifts", timeline t 0.15
   to 0.21), the BRIGHTEST stable frame in the whole scene (probed mean luminance
   ~64, vs ~20-38 elsewhere). Frame 0 (poster) is that bright warm nebula. Camera
   parallax DROPPED (it fought the scroll; the crossfade carries the loop); no crop.
   Renderer re-confirmed NVIDIA RTX 3060.
3. Endpoint-matching (all three): after the slow tour, a brisk ~1.7s glide back to
   the start and a ~1.3 to 1.5s closing hold, crossfaded (0.8s) into the opening.

IMPLEMENTATION (tools/capture.py, a substantial refactor):
- The per-project `segments` / `start_t` / `parallax` / `crop` / `clip_len_s` /
  `orbit` config is replaced by a uniform `tour` spec (`from`/`to` as a pixel offset
  or a `{"t": frac}` cosmic-dawn timeline fraction, `tour_dur_ms`, `return_dur_ms`,
  open/close hold ms) plus `warmup`, `settle_ms`, `extra_load_wait_ms`. `run_parallax`
  and the `math` import are removed; `EASE_SCROLL_JS` gains a near-linear mode for
  the even tour.
- Endpoint matching: demo heros play a one-time load-in animation, so the take waits
  it out (settle 3.5 to 4s) and warms the hero to its settled base state before the
  keeper (a scroll excursion and back). The star (WebGL) skips the warmup.
- HEAD-ANCHOR IS CONTENT-BASED (`choose_head_ss`): it scans the start of the take for
  the 0.8s window that best matches the settled closing hold. INSTRUMENTED root cause
  (not guessed): the persisted wall-clock keeper offset does NOT align with the
  recorded video timeline (Playwright records a non-linear timeline), so a
  fixed-offset anchor landed the "head" in the moving tour (dissolve mismatch 21 to
  75). A content match fixed it (Blackthorn/Barker match-scores dropped to ~2 and ~1).

MEASURED RESULT (browser-rendered closing-vs-opening = the two blended frames, mean
absolute pixel diff 0..255; verified over a local server in headed Chromium):
- Blackthorn: 2.4  (raw layer mismatch 3.45)  PASS (< ~10)
- Barker & Bloom: 0.9  (raw 1.68)  PASS
- Star (afterglow): 13.2 mean (raw 16.7)  FLAGGED, over the ~10 proxy. It is diffuse
  plasma flow, NOT legible ghosting: the epoch text, nav and structure are IDENTICAL
  at both endpoints (same afterglow) and stay crisp through the dissolve; only the
  soft nebula clouds sit slightly differently (evidence: the mid-dissolve frame shows
  a single crisp "The fog lifts", no doubled text). The ~10 proxy was calibrated on a
  fixed-structure shot; diffuse high-contrast plasma inflates the pixel diff without a
  legible double image. Plasma decorrelation is also non-monotonic (dt 12s -> 37,
  dt 16s -> 16), so the ~17s clip sits near its best phase and NO in-range duration
  gets it under 10.

STAR TRADE-OFF (flagged for owner decision): no scene position satisfies BOTH the
seam (< 10) and the brightness aim at once. The afterglow is the ONLY genuinely
bright option (poster mean 62 vs the old 35, a full warm nebula, decisively "not a
black page") but flows (seam 13.2, no legible ghosting). The alternatives that pass
the seam (first light seam ~6, home ~lower) are DIMMER than the old 35 (first-light
poster mean ~20, a bright but compact star on black). Since the black-page fix is the
amendment's whole purpose and the afterglow has no legible ghosting, the AFTERGLOW
ships. If the owner insists on the strict < 10 seam over brightness, first light
(t 0.40, "A star is lit") is the ready fallback (seam ~6, poster a bright compact
star, mean ~20). The cosmos is inherently dark, so the ~80/255 poster aim is
unreachable; ~64 is the brightest frame in the scene.

FINAL MEDIA (all 1280x720, VP9, no audio; posters 1280 wide, all ~67 to 71KB):
- blackthorn-preview.webm   16.17s  4.11MB   poster lum ~194 (light cover page)
- barker-bloom-preview.webm 16.13s  1.87MB   poster lum ~222 (light grooming page)
- until-the-last-star-preview.webm 17.17s 5.22MB  poster lum ~62 (bright afterglow)
Sizes are large (the long, busy continuous scrolls at CRF 34); accepted per the owner
"sizes will grow, accepted". Lazy-loaded, so the first-load budget is untouched.

IN-BROWSER (headed Chromium, local server): all three autoplay on selection at
desktop AND mobile 360 (paused=false, loop=true, muted=true, preload="none", the webm
fetched only on selection), loop across the wrap, zero layout shift (.preview 507x612
identical), no media 404s, no console errors. Backups of the prior media in
verify/round-4/backup-r2 and -r3. Screenshots and dissolve evidence in verify/round-4b
and the scratchpad. main.js and the layout are unchanged; ?v=12 kept.

### Round 4c - star dark-trough FAIL fix (2026-07-27)

Verifier round-4b: Blackthorn and Barker PASS (rendered seams 0.43 / 0.31, final, not
re-recorded). One FAIL, star only: the t 0.15 to 0.21 afterglow span scrolled ON into a
dark trough mid-clip (luminance fell from ~61 to a sustained ~19/255 around clip t 13
to 14s, near-frozen), reading as the black-page problem again.

Fix (star re-recorded only; everything else identical): probed the timeline finely (a
static grid plus a slow-scroll pass) and NARROWED the span to t 0.13 to 0.17, a bright
plateau of THE AFTERGLOW that stays luminous throughout with visible plasma motion:
  fine grid (mean lum): t0.13=69, 0.14=67, 0.15=64, 0.16=59, 0.17=50; drops below 40
    only from t0.18 (38) on, so the window ends at 0.17.
  slow-scroll pass t0.13->0.17: luminance holds 70 -> 50, never below ~50.
  frame motion across the window ~2.8 to 4.7 (structured nebula motion, not a static
    hold).
MEASURED on the shipped clip (162 samples at 10fps over 16.2s): luminance min 48.0
(at clip t 13.1s), mean 61.0, max 67.9; ZERO samples below 40 (the FAIL is gone).
Poster (frame 0) luminance 67.2 (brighter than the old 62 and the ~35 black-page shot).
Rendered closing-vs-opening seam mean 14.8 (p99 74): the same soft diffuse-plasma
dissolve the owner accepted ("seam acceptance = no legible ghosting"); the mid-dissolve
frame shows all nav/header/timestamp text crisp and single, no doubled image
(verify/round-4c/star-dissolve-mid.png).

FINAL STAR: until-the-last-star-preview.webm 16.17s, 6.5MB (large, per accepted size
growth; lazy-loaded), poster 66KB / 1280 wide / luminance 67. In-browser: autoplays and
loops at desktop AND mobile 360, zero layout shift (.preview 507x612), no media 404s, no
console errors. Renderer re-confirmed NVIDIA RTX 3060. Blackthorn and Barker untouched;
main.js, CSS layout and ?v=12 unchanged.

## Client feedback round 5 (owner-directed 2026-07-27)

Three items plus a cache bust. Items 1 and 3 were diagnosed/reproduced first
(instrumented), then fixed. CONCEPT supersessions recorded per the brief.

- Status: BUILT, awaiting verification. Files changed: tools/capture.py (screencast
  60fps capture, square-ish geometry, opening-hold head anchor), tools/README.md,
  media/*.webm and media/*.jpg (all three re-recorded and re-processed), index.html
  (color-scheme meta, inline theme init script, footer restructure + toggle, ?v
  bump), css/styles.css (dark token block, theme-toggle styles, CTA is-open shadow,
  ?v bump), js/main.js (theme controller, dot-grid colour re-read on theme change),
  PROGRESS.md. All shipped refs bumped ?v=12 to ?v=13 (a push follows): 13 in
  index.html, 2 in css/styles.css, 0 in js/main.js. Encoding clean (Edit + byte-safe
  sed only): no BOM, no mojibake, no em dashes; 0 remaining ?v=12; special chars
  intact (£300 x7, arrow x10, middle dot x14).

CONCEPT SUPERSESSIONS (owner amendments, recorded as directed):
- Section 13 "no dark mode" is SUPERSEDED: a system/light/dark theme toggle is
  added (item 2).
- Section 5 clip geometry and frame rate are amended: the recording moves from a
  16:9 1280x720 capture to a SQUARE-ISH 1000x1040 (deviceScaleFactor 2) capture,
  the output from 1280x720 30fps to 1500x1560 60fps (item 1). The 300 to 500KB
  clip budget stays retired (round 2); files grow again (reported).
- Section 3.4 C5 amendment update: when the CTA is open it takes the same
  --shadow-row-active elevation as the active row card, composed with the inset
  rim (item 3).
- NO language toggle: single-language UK site, nothing to translate; skipped as
  the brief allows (owner can override).

### Item 1 - Preview crop, blur and frame rate (diagnosed, then fixed at capture level)

DIAGNOSIS (instrumented, not guessed):
- CROP: the desktop preview box is near-square (measured .preview 682x652 at
  1440x900, ratio 1.046; the box ratio ranges 0.853 at 1280w to 1.397 at 1920w),
  while the clips were 16:9 (1.778). object-fit: cover then cropped the sides ~41%
  ("cropped in") and the 720 source rows upscaled ~1.8x at DPR 2 ("blurry").
- FRAME RATE: measured the effective UNIQUE fps of the ?v=12 clips (mpdecimate
  unique-frame count / duration): blackthorn 379/16.17 = 23.4, barker 251/16.13 =
  15.6, star 401/16.17 = 24.8 unique fps, all well under the 30fps nominal
  (Playwright recordVideo is ~25fps nominal and drops/duplicates under load).

METHOD (reported): CDP `Page.startScreencast`. Probed on this RTX 3060: 75.6 fps
(blackthorn) and 91.0 fps (star, NVIDIA renderer confirmed in-context), far above
60. The screencast JPEG frames are timestamped and rebuilt into a 60fps CFR
intermediate (a static hold is one frame held for its whole duration; the
raw-assembly duration clamp was set above the ~1.6s hold length so holds are
preserved, else the crossfade loses its static window). Chose screencast over
ffmpeg gdigrab: self-contained, no window-geometry math, captures the page content
(and GPU-composited WebGL) directly.

GEOMETRY (reported): recording viewport 1000x1040 (ratio 0.962, the compromise
across the two anchor box ratios 1.046 at 1440 and 0.853 at 1280) at
deviceScaleFactor 2 (raw 2000x2080), encoded to 1500x1560 (1500 wide: the 1440 box
is 682 CSS = 1364 device px at DPR 2, so 1500 is native-or-better and sits in the
owner's 1400 to 1600 band). Desktop crop is now only ~8% top/bottom (was ~41%
sides), with the full top nav in frame. The demo sites render legitimately at
1000px wide.

MOBILE CROP CHECK (reported): the mobile preview box is 2:1; a 0.962 source
cover-crops to its middle ~48% vertical band. Simulated on the blackthorn poster:
the hero (headline, hero image, CTAs, reviews) reads clearly; only the top nav
pill and a lower section header fall outside the band, which is fine for a 2:1
micro-preview. The star hero (nebula + "The fog lifts" + epoch nav) also reads.

MEASURED OUTPUT (all 1500x1560, VP9, no audio, 60fps; effective unique fps over a
mid-scroll motion window):
- blackthorn-preview.webm  13.42s* -> 17.25s  6.7MB  seam 0.90  62 ufps  poster 93KB
- barker-bloom-preview.webm 16.00s  3.0MB  seam 0.97  49 ufps  poster 96KB
- until-the-last-star-preview.webm 15.32s  12.3MB  seam 1.95  poster 89KB / lum 72
  (* blackthorn was re-timed; the shipped loop is 17.25s.)
All unique-fps figures are the 3x-to-4x improvement asked for (old 15.6 to 24.8).
Posters are all under the ~100KB budget. Frame 0 posters match the new aspect.

STAR (reported): the round-4c bright-afterglow content plan is unchanged (10s
preload wait, timeline t 0.13 to 0.17, no parallax, crossfade loop). Luminance
profile on the shipped clip: poster 72.3, min 48.5, mean 62.3, ZERO samples below
40 (no black-page / dark-trough regression). The crossfade is the round-4c-accepted
diffuse plasma dissolve: the mid-dissolve frame shows all structural text (epoch
nav, title, timestamp) crisp and SINGLE (no legible ghosting). The head anchor was
bounded to the opening hold so it stays at the tour start scroll position (an
earlier unbounded scan roamed to a mid-tour frame at a different position, risking
a position ghost; fixed and re-processed).

DEVIATIONS / notes (item 1):
- Seam fix (instrumented): the demo heros run scroll-reveal animations that re-fire
  on scroll-back; the warmup excursion re-triggers them, so the opening hold caught
  them replaying and left too short a static window. Two fixes: (a) preserve static
  holds in the raw assembly (the 0.25s duration clamp collapsed the 1.5s opening
  hold, so the raw jumped into the scroll; raised to 2.5s); (b) keep the warmup but
  add warmup_settle_ms (2500) so the reveals fully settle before the keeper. Result:
  a clean 1.5s static opening window matching the tail (diff 0.4), seam 0.90/0.97.
- Sizes grow (owner accepted): the star at 12.3MB is the largest (60fps + busy
  plasma + 1500x1560 + 15.3s). All lazy-loaded, so the first-load budget is
  untouched. If a smaller star is wanted, its CRF can be raised (plasma is diffuse
  and forgiving); flagged for the owner.
- The raw intermediate is now an H.264 CRF-12 mp4 (was a Playwright VP8 webm), so
  process_one reads `<name>-raw.mp4`. The `.offset` file is no longer written (the
  raw is keeper-only, so the head anchor no longer needs a wall-clock offset).

### Item 2 - Theme toggle (system / light / dark)

MECHANISM (my call, reported): ONE mechanism. The stored preference (system /
light / dark; absent = system) is resolved to a concrete theme in JS and written
as data-theme="light" | "dark" on <html>; the CSS only ever reads
[data-theme="dark"] (there is NO prefers-color-scheme media query in the styles).
Chosen over a two-mechanism scheme (data-theme for forced + a media query for
system) because it keeps a single source of truth and avoids the two disagreeing.
- Applied before first paint by a tiny inline <head> script reading localStorage
  (wrapped in try/catch; falls back to light), so there is no flash.
- js/main.js `initTheme` wires the three footer buttons, reflects aria-pressed,
  persists to localStorage (key `zayn-theme`), live-updates on an OS scheme change
  while following the system, and dispatches a `themechange` event.
- The dot-grid canvas re-reads --dot-rest / --dot-warm and repaints on
  `themechange` (verified: dark = light dots on dark). The CONCEPT 3.3 dot-grid
  guards are unchanged (no mousemove listener bound on touch / reduced motion).
- meta name="color-scheme" content="light dark" added; CSS `color-scheme` is set
  per resolved theme so UA scrollbars/controls match.

CONTROL (reported): a small segmented rounded-rect in the footer, 16px radius
family (--radius-surface). Three buttons (monitor / sun / moon inline SVG icons,
stroke=currentColor, ~15px) with aria-pressed (exactly one pressed), grouped in a
role="group" aria-label="Colour theme"; icons decorative (aria-hidden), each button
labelled. Quiet --grey-label icons; the active segment takes the established
active-card treatment (--surface-white lift + --shadow-row-active, --ink icon);
house focus-visible ring (--shadow-field-focus), layered over the active elevation
on the active segment. Chose aria-pressed buttons over a roving-tabindex radiogroup
(the brief allows either): simpler, each is a Tab stop, Enter/Space activates.

PLACEMENT (verified, screenshots deferred to the verifier): desktop footer line of
the left column, email on the left and toggle on the right of the SAME row
(measured 1440x900: email right 370, toggle x 445, both centred at y 818);
copyright below. Mobile: the same footer flows at the page bottom, same row (390:
email wraps, toggle stays right and vertically centred, no horizontal scroll).

DARK PALETTE (NEW tokens in a clearly-labelled [data-theme="dark"] block; the 3.1
light block stays verbatim). Derived from the existing language, not a new
aesthetic. Values and computed WCAG contrast on the dark ground #141416:
- --ground #141416; --ink #F0F0F2 (16.2:1); --ink-body #B8B8C0 (9.3:1);
  --ink-mid #A6A6AE (7.6:1 ground, 6.7:1 on the dark field for placeholders);
  --grey-label #74747C (4.0:1) and --grey-soft #68686F (3.3:1) mirror the light
  sub-AA desktop-rest exception.
- --accent #4E95E8 (5.95:1 ground, 5.0:1 on the lifted card): the sea blue lifted
  so it clears AA as text/icon/ring (the light #1A6FD4 is only 3.74:1 on dark).
  --shadow-field-focus and the field:focus border use it, so focus rings stay
  visible. --accent-ghost lightened for the ghost arrow.
- Surfaces stepped: ground #141416 < panel/preview #1B1B1E < field #202024 <
  lifted card --surface-white #242428 (the "white active row card becomes a lifted
  dark card"). --submit-ink inverts to a light button (#EAEAEE) with a dark label
  (the --surface-white token), --submit-ink-hover #FFFFFF. --border #33333A.
- CTA dark-water: --cta-layer1/2/3 redrawn as deep blues (#1B3A5C / #16324A /
  #163049 family, same drift keyframes and --cta-bg-size); rim/lightpass/edge-lift/
  mist/press given light-blue-on-deep variants; --cta-text #EAF2FB (11.7:1 on the
  pill); --cta-index rgba(234,242,251,0.55) with the mobile/focus darken to
  --ink-mid clearing AA on the pill (4.81:1).
- --dot-rest rgba(240,240,242,0.07) and --dot-warm rgb(94,166,240) (light dots).
- --shadow-row-active deepened to 0 1px 3px rgba(0,0,0,0.45) so the single quiet
  card shadow reads on dark (still the only non-inset shadow on the page).
Every AA-required pair passes in dark; the two desktop-rest greys are the same
accepted exception the light theme carries. The preview box stays a neutral dark
surface with the existing thin border, so the light clips read as intentional.

DEVIATIONS / notes (item 2):
- No-JS: with JS off the inline script does not run, so data-theme is unset and the
  page renders light (the site is JS-first; the panel/form already need JS). The
  toggle buttons show but are inert without JS. Acceptable and flagged.
- aria and reduced-motion behaviour are unchanged by the theme (the toggle adds no
  motion; the CTA is-open shadow transition is forced instant by the 3.3 guard).
- Pointer-trail colours (--trail-a/b) are read once at init and NOT re-read on
  theme change; the light-blue trails read acceptably on both grounds, and trails
  are ephemeral (2.2s). Left as-is to avoid over-engineering; noted.

### Item 3 - CTA active shadow (C5 amendment update)

When the CTA is open (.is-open), it now takes --shadow-row-active composed with the
inset rim (rim first): `box-shadow: var(--cta-rim), var(--shadow-row-active)`.
box-shadow was added to the .row--cta transition so it eases in with the grow. An
.row--cta.is-open:focus-visible rule (0,3,0) layers the accent ring over the rim and
the active shadow so an open, keyboard-focused CTA keeps all three. Verified the
computed box-shadow in BOTH themes: light = white rim insets + rgba(20,20,22,0.06)
0 1px 3px; dark = light-blue rim insets + rgba(0,0,0,0.45) 0 1px 3px.

### Item 4 - Cache bust ?v=12 to ?v=13

Every shipped ?v=12 bumped to ?v=13 (a push follows): 13 in index.html (css, js,
six media refs, og:image, twitter:image, favicon.svg, favicon-32.png,
apple-touch-icon.png), 2 in css/styles.css (two @font-face src), 0 in js/main.js.
Byte-safe sed; grep confirms 0 remaining ?v=12. Media filenames carry no version,
so the re-recorded clips are picked up by the bumped refs.

### Client feedback round 5 - integration and verification notes
- In-browser (headed-equivalent, local http server; autoplay loops need no Range):
  all three V2 views autoplay on selection at desktop (dark 1440x900) and mobile
  (light 390x844): paused=false, loop=true, muted=true, preload="none", readyState
  4, currentTime advancing, source 1500x1560; zero layout shift (.preview box
  identical before/after load); no media 404s, no console errors.
- Theme verified programmatically: initial data-theme resolves from the pref;
  clicking dark sets data-theme=dark + localStorage=dark + aria-pressed; a fresh
  load with OS dark + system pref resolves to dark (system-follows-OS); the dot
  grid flips to light-on-dark.
- The capture, the NVIDIA renderer confirmation, the screencast fps probe and the
  frame/luminance/crop inspections ran in real headed GPU Chromium; numbers above
  are measured. Old ?v=12 media backed up to the scratchpad before overwrite.
  Screenshot/visual sign-off (including the toggle placement and the dark theme
  across every view) remains the verifier's.

### Client feedback round 5 - playback-smoothness FAIL fix (2026-07-28)

Verifier FAIL: in-browser playback dropped 31 to 45% of decoded frames on all three
clips (getVideoPlaybackQuality; verify/restyle-5/t4b_playback_gpu.json: 37/38/31%),
still ~22% in a bare page, so it is DECODE cost, not page contention. No re-record;
re-encoded from the existing raws only. ?v=13 kept (no push since the bump). Files
changed: tools/capture.py, tools/README.md, media/*.webm and *.jpg (three), PROGRESS.md.

DIAGNOSIS (instrument then fix; reproduced the FAIL, then found the deeper cause):
- Reproduced the baseline in a headed-GPU harness: 34.2 / 33.9 / 30.8% dropped on
  the shipped 60fps 1500x1560 clips (matches the verifier's 37/38/31%).
- ROOT CAUSE, deeper than the brief's "non-standard 1500x1560 at 60fps": the clips
  were VP9 PROFILE 1 (yuv444p) - and had been since round 4 - which forces SOFTWARE
  decode on virtually all hardware and doubles chroma. The xfade filter re-expanded
  to yuv444p and the output pix_fmt was never pinned. That is WHY it was "software
  VP9 decode". Combined with 60fps and 2.34M px it overran the decoder.

FIX (three levers, most-to-least impactful):
1. Force VP9 PROFILE 0 (yuv420p): `format=yuv420p` after the xfade plus
   `-pix_fmt yuv420p` on the encode. 4:2:0 is hardware-decodable and halves chroma.
2. 60fps -> 30fps CFR: a slow ambient drift reads perfectly smooth at 30 and it
   halves the per-second decode load.
3. MOD-16 dimensions 1500x1560 -> 1280x1344 (1280 = 80*16, 1344 = 84*16, ratio
   0.952): macroblock-aligned decodes more efficiently; stepped down from the first
   1440x1504 attempt for extra decode/composite margin. 1280 wide is a 6% upscale of
   the 1364 device-px box at DPR 2 (imperceptible; sharpness kept high).

MEASURED (deterministic, since a real-browser drop-% could not be produced here, see
the limitation note):
- SOFTWARE decode throughput (ffmpeg, 1 thread; browsers decode multi-threaded and,
  for profile 0, in hardware): new 1280x1344 420p clips decode at blackthorn 208.8,
  barker 340.9, star 96.9 fps - 3.2x to 11x the 30fps playback rate, comparable to
  the previously-shipped-and-accepted round-4 clips (109 to 213 fps). Decode has
  clear headroom; it is no longer the bottleneck.
- The 60fps 444p baseline vs the 30fps 420p re-encode also dropped the drop-% in the
  headed harness before it began render-throttling (34/34/31 -> 9.7/8.6/19.5 at the
  intermediate 30fps step), confirming the direction.

FINAL MEDIA (1280x1344, VP9 Profile 0 / yuv420p, 30fps, no audio; content, crossfade
loops, star afterglow and luminance all unchanged from the round-5 recordings):
- blackthorn-preview.webm   17.23s  4.1MB  seam 1.06  poster 97KB
- barker-bloom-preview.webm  16.00s  1.6MB  seam 1.23  poster 90KB
- until-the-last-star-preview.webm 15.30s 6.7MB  seam 2.42  poster 93KB (lum: poster
  72.3, clip min 50.2, mean 62.6, zero samples < 40 - the afterglow is unchanged)
Sizes fell from the 60fps 1500x1560 clips (6.7/3.0/12.3MB) with the fps halving and
smaller frame. Seams re-checked (all pass, same acceptance). Posters re-exported at
frame 0, 1280 wide, all under 100KB.

MEASUREMENT LIMITATION (reported honestly): I could not reproduce the verifier's
headed-GPU browser drop-% here. A headed Playwright window on this machine is
render-throttled (the occluded window presents ~2 frames and auto-pauses;
anti-backgrounding flags did not help), and headless Chromium is software-decode +
no real vsync, so its drop-% (19 to 27%) is a compositor artifact that does NOT scale
with resolution (26% at 1440 vs 22% at 1280 despite the decode benchmark showing huge
headroom) and is not the deployment metric. The substantive evidence is the decode
benchmark plus the deterministic profile-0 / 30fps / mod-16 change. The verifier
should re-run its working headed-GPU harness (t4b) to confirm the drop-% under ~5%.
READY FALLBACK if it still exceeds ~5% there: step down once more to 1152x1200
(mod-16, ratio 0.96) - change OUT_W/OUT_H in tools/capture.py and re-run
`python tools/capture.py --skip-capture`; that is a ~19% upscale of the box (softer)
but lighter still. Everything else in round 5 is verified and untouched.

### Client feedback round 5 - hardware-decode FAIL fix (SAR + colour metadata, 2026-07-28)

The above 1280x1344 re-encode FAILED HARD on the verifier's headed-GPU path: MediaError
code 3 PIPELINE_ERROR_DECODE on all three clips (6/6 reproductions), while headless
software decode played them fine. This SUPERSEDES the "measurement limitation" note in
the previous sub-section: the fix below was confirmed in a real headed-GPU Chromium
(the earlier headed throttling was defeated with
--disable-features=CalculateNativeWinOcclusion). Metadata fix only, no re-record, no
resolution change. ?v=13 kept. Files: tools/capture.py, tools/README.md, media/*.webm
and *.jpg (three), PROGRESS.md.

ROOT CAUSE (precise, from ffprobe; the real reason it fell to software decode):
- SAR 323:320. The CDP screencast raw is 1000x1040 (screencast returns CSS-PIXEL
  frames; the deviceScaleFactor did NOT enlarge them - the "DPR 2 -> 2000x2080 raw"
  assumption was wrong, so the output is a mild upscale from 1000 wide, accepted since
  crop/blur passed round 5). Scaling 1000x1040 (DAR 25:26) to the non-matching
  1280x1344 made ffmpeg's scale set a fractional SAR of 323:320 to preserve DAR, so
  videoWidth reported 1292 not 1280. Non-square pixels break hardware VP9.
- Colour: the raw is yuvj420p FULL-range tagged bt470bg (swscale's default when
  libx264 encoded the RGB screencast JPEGs). color_range=pc + color_space=bt470bg is
  an unusual pairing hardware VP9 paths reject; it carried straight through to the
  output.

FIX (encode metadata, in tools/capture.py `vfilter` + `vp9_args` + `encode_crossfade`):
1. setsar=1:1 forces SQUARE pixels (videoWidth now 1280; the <1% aspect nudge is
   invisible and cover-cropped).
2. Convert (not retag) full-range/bt601 to tv-range/bt709 in the scale filter
   (`in_range=full:out_range=tv:in_color_matrix=bt601:out_color_matrix=bt709`; bt601
   is ffmpeg's name for the bt470bg matrix), then stamp all four fields with
   `setparams=range=tv:colorspace=bt709:color_primaries=bt709:color_trc=bt709` and the
   `-color_range tv -colorspace bt709 -color_primaries bt709 -color_trc bt709` encode
   flags so pixels and tags agree.
Same 1280x1344, yuv420p, Profile 0, 30fps. ffprobe now reports on all three:
SAR 1:1, pix_fmt yuv420p, color_range tv, color_space/primaries/transfer all bt709.

VERIFIED in HEADED GPU Chromium (occlusion detection disabled so the window renders):
- No MediaError on any clip (was code 3 on all three); videoWidth 1280 (was 1292);
  currentTime advances at real time (7.3s over ~7.5s).
- Drop rate, 6s steady-state window: blackthorn 0/181, barker 0/181, star 0/181 = 0%
  dropped; cumulative incl. startup 4/221, 3/223, 4/222 = 1.3 to 1.8%. Under the ~5%
  acceptance, no repeated spikes. PASS.

FINAL MEDIA (1280x1344, VP9 Profile 0 / yuv420p / 30fps, SAR 1:1, tv/bt709; content,
crossfade loops and star afterglow unchanged):
- blackthorn-preview.webm   3.4MB  seam 1.24  poster 97KB
- barker-bloom-preview.webm 1.4MB  seam 1.31  poster 89KB
- until-the-last-star-preview.webm 5.4MB  seam 2.55  poster 93KB
Sizes fell again (tv-range encodes a touch smaller). Seams re-checked (pass). Posters
re-exported at frame 0, 1280 wide, all under 100KB (frame 0 unchanged, but re-exported
from the colour-corrected webm). Star luminance still bright: poster 68.8, clip min
47.0, mean 59.5, zero samples below 40 (the full->tv range conversion nudges the
measured jpg luminance down ~3 points from 72; the displayed brightness is preserved
by the bt709/tv tags and it is decisively not a "black page"). No working dirs left in
media/ (temp output kept in the scratchpad).

## Client feedback round 6 (owner-directed structural redesign, 2026-07-28)

A structural redesign of the project viewing pattern, adapted from the Moritz
Petersen detail-state pattern but deliberately NOT a copy: we keep the two-column
structure, dot grid, light ground, tokens, type and motion language. Files changed:
index.html, css/styles.css, js/main.js, tools/capture.py, tools/README.md,
media/* (12 new section files, 6 old tour files removed), PROGRESS.md.

- Status: BUILT, awaiting verification. All shipped refs bumped ?v=13 to ?v=14
  (a push follows): 23 in index.html (css, js, 16 media refs, og:image,
  twitter:image, favicon.svg, favicon-32.png, apple-touch-icon.png), 2 in
  css/styles.css (two @font-face src), 0 in js/main.js. No BOM, no mojibake, no em
  dashes; 0 remaining ?v=13. Verified behaviourally in real headed Chromium
  (desktop light/dark, desktop scrolled, mobile 390, hover, reduced-motion) and
  programmatically over a local http server; zero console errors. Screenshots in
  verify/round-6/.

### CONCEPT SUPERSESSIONS (recorded precisely, per the brief)

- SUPERSEDES the V2 single-video project layout in FULL (CONCEPT 3.4 V2, section 5,
  and every round-1 to round-5 amendment to it: the scrollable large-preview, the
  bottom fade, the .project-blurb-under-the-fade, the single autoplay tour webm).
  Project rows 01 to 03 no longer swap the panel to one video; they open a DETAIL
  STATE. The single tour webms and their posters are removed from media/ (nothing
  referenced them after the change; grep-checked). The crossfade + screencast
  plumbing stays in tools/capture.py, repurposed for section media (the old tour
  functions are gone; the shared encode helpers are kept).
- SUPERSEDES parts of CONCEPT 3.4's state inventory. The panel PREVIEW states are
  now: V1 welcome (unchanged, restorable), a SECTION-STACK state for projects
  (replaces V2), V3 About/Pricing (unchanged), V4 form (unchanged), V5 mid-swap
  (unchanged). Row states: R1 rest unchanged; R2 hover is now the raised white
  card (was the round-1 grey wash, itself a supersession of the 3.4 R2 accent
  fill); R3 active (index rows, About/Pricing) unchanged; project rows do not show
  a raised card (they open the detail state, where the index is hidden).
- SUPERSEDES the mobile no-reflow / fixed-60vh constraint FOR THE DETAIL STATE
  ONLY (CONCEPT section 8): in the detail state the section cards flow as page
  content and the page scrolls (the panel grows past 60vh). The 60vh budget still
  governs the normal index-model views (welcome, About, Pricing, form).

### The new model

1. HOVER (all breakpoints, mouse): index rows on hover take the active card
   treatment (--surface-white fill, --border border-color, --shadow-row-active,
   index to accent, name to --ink, tag faded out, glyph in). Hover raises but does
   NOT grow (no --sp-18 padding), so hovering never pushes neighbours; the selected
   row is raised AND grown. The grey-wash hover is retired. focus-visible unchanged
   (accent inset ring; a hover:focus-visible rule layers the ring over the card
   elevation, mirroring the active-row pattern).

2. PROJECT DETAIL STATE (rows 01 to 03). The state hook is .page.is-detail (drives
   both columns; they are display:contents on mobile). Left column morphs: index,
   HOW IT WORKS and the proof strip fade out and collapse; a .detail header block
   fades in where the index was (back control "BACK TO INDEX" with a left arrow in
   the row-glyph family, project title Archivo 34px/600/-0.015em, mono sub line
   10.5px lower, the approved blurb Archivo 14px/--ink-body, and a "See it live"
   button reusing the .visit-pill styling). Pinned to the bottom (margin-top auto,
   where the proof pinned): a .conversion cluster: one quiet mono line "websites
   from £300 · care plan from £25/month · free mockup" (10.5px mono lower case
   --ink-mid, the whole line a button that opens Pricing), and beneath it the Get
   in touch CTA row 06 (full drift/rim/mist/bloom, unchanged behaviour). The name
   block, positioning line and footer (email, toggle, copyright) stay visible. The
   CTA is ONE element: main.js relocates it from the index list into .conversion on
   entering detail and back on exit, so its listeners travel with the node.

3. PANEL in the detail state: a scrollable stack of SECTION CARDS
   (.section-stack > figure.section-card > .section-media + figcaption). Each media
   block is full content-width at a fixed 16:9, 16px radius, 1px border; the mono
   caption (10.5px UPPER 0.04em) sits underneath. Media is lazy (templates enter the
   DOM only on detail open; imgs loading="lazy", videos preload="none" autoplay
   muted loop playsinline). Panel header shows "PREVIEW / <name>"; aria-live
   announces. The old bottom fade is retired (a card peeking below the fold is the
   scroll cue); the scrollbar is left NATIVE and thin (scrollbar-width: thin), an
   honest scroll affordance (reported choice).

4. Rows 04 About and 05 Pricing keep the normal index model exactly (index stays,
   panel swaps, row active). CTA row 06 unchanged. Selecting About/Pricing/form
   from within a detail state exits it first (index restored), then shows the view.

### Section list chosen per project (after inspecting the live sites)

Loop vs static follows the brief's rule: LOOP only where a section genuinely cycles
at rest (inspected: the Blackthorn reviews carousel is manual, the Barker paw-trail
hero has no running/infinite animation at rest; both are STATIC accordingly). This
gives 4 genuine loops (the Barker compare slider + 3 continuously-animating WebGL
epochs) and 8 static screenshots. Captions in brackets.

- Blackthorn & Co. (5, all STATIC): cover ("The cover"), price menu
  ("The price menu"), barbers ("The barbers"), reviews ("In their words"), booking
  form ("The booking form"). Sections #cover / #services / #team / #reviews /
  #booking.
- Barker & Bloom (4): hero ("The welcome", STATIC), price menu ("The price menu",
  STATIC), before/after ("Before and after", LOOP: the .ba__ compare slider driven
  to sweep via a sine on the clip-path inset + handle left, BA_SWEEP_JS), booking
  form ("The booking form", STATIC). Sections #home / #services / #gallery / #book.
- Until the Last Star (3, all LOOP, WebGL continuous, 10s load wait, NVIDIA
  renderer re-confirmed): the first star ("The first star", t 0.40 "A star is lit"),
  the cosmic web ("The cosmic web", t 0.52 "Structure, everywhere"), the last star
  ("The last star", t 0.88 the lensed black hole finale, "The black hole bends the
  last starlight"). The black-hole shot is now one card among bright ones, per the
  brief.

### Media inventory (media/, all ?v=14 refs; sizes and loop points)

STATIC jpgs (1600x900, DPR-2 capture downscaled, all well under 300KB):
- blackthorn-cover 204KB, -prices 122KB, -barbers 110KB, -reviews 148KB,
  -booking 113KB; barker-hero 195KB, -prices 144KB, -booking 97KB.

LOOP webms (1280x720, VP9 Profile 0 / yuv420p / 30fps / SAR 1:1 / tv-bt709;
tail->head 0.8s crossfade; poster = frame 0, 1280 wide):
- barker-beforeafter.webm 499KB, loop 4.60s, seam 0.78; poster 94KB.
- star-first.webm 221KB, loop 3.03s, seam 0.43; poster 54KB (bright star).
- star-web.webm 167KB, loop 3.10s, seam 0.70; poster 63KB (galaxy field).
- star-last.webm 230KB, loop 3.03s, seam 0.87; poster 59KB (lensed black hole).
All webm SAR/profile/colour re-verified by ffprobe (hardware-decodable, matching the
round-5 hardening). All lazy-loaded, so the first-load budget is untouched. Old tour
media removed: blackthorn/barker-bloom/until-the-last-star -preview.webm and their
posters (6 files), unreferenced after the change.

### Morph implementation approach

A two-phase JS crossfade (crossfade(outEls, inEls, onMid)) using INLINE styles only,
so it never conflicts with the load-in .fade-block transition: the leaving set fades
to opacity 0 over MORPH_MS (200ms), then at the midpoint onMid runs (moves the CTA),
the leaving set is set hidden (the layout collapse happens while invisible, so no
visible jank), and the entering set is revealed at opacity 0 and faded to 1 over
MORPH_MS. The panel content swaps in parallel via the existing V5 swap. Reduced
motion: crossfade early-returns with instant hide/show and the panel commits
directly (verified: at 120ms under forced reduced-motion the state is fully settled,
no inline opacity left, no bound listeners or spawned nodes). Measured desktop
geometry (1280x820, Blackthorn detail): two-column, detail header at the top,
conversion pinned to the bottom (footer bottom flush at the column bottom), section
stack scrollable inside the fixed-height panel (scrollHeight 1657 > client 676), no
horizontal scroll.

### Focus / keyboard flow

- Entering detail: focus lands on the back control (focusAfterMorph fires after the
  crossfade reveals it; immediate under reduced motion). Verified.
- Back control, Escape, and browser back all exit to the welcome and return focus to
  the ORIGINATING project row. History: entering detail pushes one history entry;
  the back control and Escape call history.back() so browser back, the button and
  the key all land in the same place (popstate -> exitToWelcome). Leaving detail to
  Pricing/form (via the conversion cluster) consumes the entry with replaceState.
  All verified (back, Escape, popstate, project->project switch, About/Pricing/form
  exits) with correct aria-pressed (one of the six rows pressed, or none at the
  welcome).
- Exit target choice (REPORTED): back/Escape/browser-back restore the WELCOME (V1),
  not the last non-project view. The brief allowed either; welcome is the cleanest
  "cleared" state and matches the reference clearing everything.

### Mobile amendment (measured)

Below 900px the morph happens in the single column: index/how/proof hidden, .detail
takes the index's order slot (3), .conversion takes the proof's slot (7), so the
order reads name, positioning, detail header, panel (section cards), conversion,
footer. In the detail state .page.is-detail releases the panel (min-height 0) and
the section stack flows (height auto, overflow visible), so the cards stack as page
content and the page scrolls. Measured at 433x911 (Blackthorn detail): panel grew to
1257px tall with the 5 cards flowing, page scrolls, media 16:9 (1.780), NO horizontal
scroll, conversion + footer at the bottom, back control reachable at the top. The
60vh budget still holds for the normal views. Full-page mobile screenshot at 390x844
(Barker) confirms the stack, conversion and footer (verify/round-6/).

### Dark theme

Everything works in both themes with no new tokens: the detail header, conversion,
section-card media boxes (--surface-preview + --border) and captions (--grey-label)
all use existing tokens, which already carry dark variants. Verified in headed dark
Chromium: dark ground, light ink, the light section media reads as intentionally
framed cards on the dark panel (verify/round-6/detail-barker-dark.png). Computed
tokens confirmed (ground #141416, media surface #1B1B1E, border #33333A, title
#F0F0F2, caption #74747C).

### Round 6 - deviations / judgement calls

- LOOP vs STATIC: the Blackthorn cover/reviews and the Barker hero were made STATIC
  after inspecting the live sites (no rest-cycle: the reviews carousel is manual,
  the paw-trail hero reported zero running/infinite animations). The brief phrased
  these as "loop if animated" / "hero with paw trail (loop)"; static is the correct
  honest choice per "STATIC images for non-animated sections". Reported so the owner
  can request scripted-rotation loops if wanted.
- SCROLLBAR (reported): the panel stack keeps a NATIVE thin scrollbar
  (scrollbar-width: thin) rather than hiding it; the peeking card plus a real
  scrollbar are honest cues (the old hidden-scrollbar + bottom fade is retired).
- STAR "last star" card uses the t 0.88 "THE LONG NIGHT" lensed-black-hole frame
  (the iconic gravitational-lens shot) rather than the later dim "THE LAST STAR"
  epoch; the card caption "The last star" fits the end-of-universe theme.
- DEAD CSS removed: the V2 project-view rules (.view--project, .preview*,
  .project-title/sub/blurb/caption, desktop and mobile) are gone (no elements match
  after the redesign). .visit-pill is kept (reused by "See it live"). Two-radii,
  one border width and inset-only-plus-the-single-active-shadow discipline unchanged.
- MOTION TABLE ADDITIONS (recorded as required):
  | Name | Property | Duration | Delay | Easing | Trigger | Reduced motion |
  | Detail morph out | opacity 1 to 0 (index/how/proof or detail/conversion) | 200ms | 0 | ease | enter/exit detail | instant |
  | Detail morph in | opacity 0 to 1 (entering set) | 200ms | 200ms | ease | enter/exit detail | instant |
- Encoding clean (Edit + byte-safe sed only): no BOM, no mojibake, no em dashes; the
  £ x2 and · in the conversion line and the ← back glyph (&#8592;) and ↗ (See it
  live) intact.

### Round 6 - open items / notes for the orchestrator

- tools/capture.py was substantially rewritten (SECTIONS mode; the tour PROJECTS and
  its helpers removed; the CDP screencast, crossfade, choose_head_ss, vp9_args,
  poster and seam plumbing kept). tools/README.md rewritten to match.
- The stage-3 no-JS caveat is unchanged (the panel and its templates need JS; the
  <noscript> contact fallback still hard-codes the placeholder email, kept in sync
  with SITE_EMAIL). The two OPEN BLOCKERs (real email, Formspree ID) are untouched.
- Screenshot/visual sign-off across every project, both themes, and a forced
  reduced-motion + 360px run remain the verifier's.

### Round 6 - verifier FAIL fixes (2026-07-28)

Verifier round-6 returned STAGE FAIL with 2 items; both fixed. ?v=14 kept (no push
since the bump). Files changed: index.html, css/styles.css, js/main.js,
tools/capture.py, media/star-*.webm + star-*-poster.jpg (re-processed from the
existing raws, no re-record), PROGRESS.md. Encoding clean (no BOM/mojibake/em
dashes). Verified in a headed window with occlusion detection disabled so playback
and IntersectionObserver run; zero console errors.

- FAIL 1 (section videos start simultaneously and drop 15 to 29% of frames; the
  three star clips at once, star-first 6.6% solo on a very short 3.03s loop). Fixed
  as the verifier suggested, in two parts:
  1. IntersectionObserver gating (js/main.js, initPanel). New setupSectionVideos()
     replaces playSectionVideos(): on render every .section-video is PAUSED first
     (cancelling the autoplay start so all three never decode at once), then an
     IntersectionObserver (threshold 0.5, root the viewport = null) plays a clip
     only while it is >= 50% in view and pauses it otherwise. root null works on
     BOTH breakpoints: the panel overflow:hidden and the stack overflow-y:auto clip
     off-screen cards, so their ratio is ~0. The autoplay attribute stays in the
     markup for the no-observer / mobile fallback (a no-IntersectionObserver branch
     plays them). teardownSectionObserver() runs at the TOP of renderView (before
     the old nodes leave the DOM) so the observer never leaks or fights the
     About/Pricing/form/welcome swaps; a muted preview under reduced motion was
     already accepted, so the observer only manages play/pause by visibility (binds
     no transition, spawns no node). VERIFIED headed: entering the star detail, at
     most the one or two cards actually in view play and the off-screen third is
     paused (never all three); scrolling the stack pauses the card that leaves and
     plays the card that enters; swapping to About leaves 0 section videos (torn
     down). SECTION_PLAY_RATIO 0.5 keeps at most ~2 concurrent in the tall desktop
     panel (down from 3), and the verifier's "scroll to each card in turn" centres
     one card, so a single clip plays.
  2. Star loops lengthened (tools/capture.py). The first cut produced ~3.0 to 3.1s
     loops that restarted often. New per-section `loop_min_s` (5.0) caps the
     head-anchor start (choose_head_ss gains an `ss_max` bound; process_loop derives
     it: ss_max = raw_dur - TAIL_MARGIN_S - CROSSFADE_S - loop_min_s) so the loop is
     at least ~5s from the SAME existing raw (no re-record). Re-measured lengths:
     star-first 3.03 -> 5.53s (364KB, seam 0.53), star-web 3.10 -> 5.10s (254KB,
     seam 0.68), star-last 3.03 -> 4.97s (356KB, seam 0.93). Posters are frame 0 at
     the new head; same fixed scroll position, so the same bright epochs (first
     star, cosmic web, lensed black hole), re-verified. All still VP9 Profile 0 /
     yuv420p / SAR 1:1 / tv-bt709 / 30fps.
  MEASUREMENT NOTE: the exact in-browser drop-% could not be reproduced here (the
  local headed window is render-throttled, same limitation logged in round 5); the
  substantive evidence is that only the visible clip(s) decode (never 3) plus the
  ~1.7x longer loops. The verifier should re-run its headed-GPU harness (t4b) to
  confirm the playing card is under 5% dropped.

- FAIL 2 (section stack not keyboard-scrollable: tabindex -1, nothing focusable
  inside, PageDown/arrows did nothing). Fixed: the .section-stack in all three
  project templates is now `tabindex="0" role="region"` with a per-project
  aria-label ("Blackthorn and Co. previews" / "Barker and Bloom previews" / "Until
  the Last Star previews"), so it is a Tab stop and keyboard-scrollable. CSS
  .section-stack:focus-visible now shows the house accent inset ring
  (--shadow-field-focus), inset so the panel overflow does not clip it and it stays
  put as the content scrolls (reported choice: same treatment as fields and rows).
  VERIFIED headed: focusing the stack, ArrowDown scrolls it (0 -> 40 -> 80px),
  PageDown scrolls it (0 -> 329px); the stack is in the tab order.
  TAB-ORDER PLACEMENT (reported deviation from the suggestion's wording): the stack
  is reached AFTER the left-column controls, not literally "between See it live and
  the conversion cluster". Observed order from the back control: back -> See it live
  -> conversion price -> Get in touch CTA -> footer email -> theme toggles -> the
  stack. This is the natural DOM/reading order of the two-column layout the brief
  mandates keeping: the panel (and its stack) is the RIGHT column, which follows the
  entire left column in the DOM. Placing the stack literally between See it live and
  the conversion cluster would require a positive tabindex (a WCAG 2.4.3
  focus-order anti-pattern) or moving the panel into the left column (breaking the
  two-column structure). The stack IS focusable, keyboard-scrollable and in the tab
  order, which is the substance of the FAIL; flagged so the orchestrator can rule if
  the exact position is required.

## Client feedback round 7 (owner approved: project chips + FLIP choreography, 2026-07-28)

Owner-approved proposal built on top of the round-6 detail state: the two OTHER
projects become chips under the back control, and the flat two-phase morph is
replaced by a FLIP choreography. Files changed: index.html (chips container +
?v=14 to ?v=15 bump), css/styles.css (chip + flip-clone styles + version bump),
js/main.js (detail controller rewritten). Safe revert point: commit 2b5c1d6.

- Status: BUILT, awaiting verification. All shipped refs bumped ?v=14 to ?v=15
  (a push follows): 23 in index.html, 2 in css/styles.css (two @font-face src),
  0 in js/main.js. No BOM, no mojibake, no em dashes; 0 remaining ?v=14 in the
  three shipped files. `node --check js/main.js` passes. Verified behaviourally
  over a local http server in the Browser pane (enter, chip switch, back, Escape,
  conversion-price to Pricing, relocated-CTA to form; desktop, 390, 360): zero
  console errors, correct end states, no stuck inline styles, no horizontal
  scroll, title never wraps, chips on one row at every width.

### 1. Project chips (item 1)

- MARKUP: a `<div class="detail-chips" data-detail-chips>` sits in `.detail`,
  directly under the back control and before `.detail-copy`, so the tab order is
  back control then chips then See it live (chips are "right after the back
  control", the substance of the brief). main.js `renderChips(currentKey)` fills
  it with the two OTHER projects on every enter and every switch, so it always
  shows the two not-currently-open projects.
- LABEL: the chip label is the PROJECT NAME (e.g. "Barker & Bloom"), not the niche
  tag. This is deliberate: the FLIP swap morphs a chip's text into the title and
  back, so the travelling text must be the same string at both ends. Niche-tag
  TYPE is honoured (mono 10px UPPER, --grey-label) via CSS text-transform, so the
  name renders uppercase; the underlying text stays the name.
- STYLE (.chip): mono 10px 400 UPPER, --grey-label; quiet chip at rest
  (16px radius = --radius-surface, 1px --border, --surface-field fill); hover
  adopts the card treatment scaled down (--surface-white fill, --shadow-row-active,
  label to --ink), gated behind (hover:hover) and (pointer:fine) like the rows so a
  tap leaves no sticky hover; focus-visible shows the accent inset ring
  (--shadow-field-focus). Real `<button>`s. No new tokens; dark variants come from
  the existing dark token block (field #202024, border #33333A, label #74747C,
  hover card #242428). The row wraps (flex-wrap) if the two labels do not fit;
  measured NOT to wrap at 360/390/768/desktop (two chips about 262px wide).
- ARIA APPROACH (reported as asked): chips carry NO aria-pressed. They are one-shot
  navigation (each switches the open project), not toggles, and the open project is
  never itself a chip, so there is no pressed/unpressed chip state to reflect. The
  switch is announced through the existing panel `role=status aria-live=polite`
  region (the "Preview / <name>" header string), same channel as every other view
  change. Chip clicks are delegated on the persistent `[data-detail-chips]` so the
  freshly rendered chips are always wired.
- SWITCH IN PLACE: a chip click routes to `switchProject(newKey)` (never through the
  index): the title block, sub line, blurb and See it live update (fillDetailCopy),
  the chips row re-renders to the new "other two", the panel card stack swaps via
  the EXISTING 130ms panel swap, and aria-live announces. After a switch, focus
  lands on the chip for the PREVIOUSLY open project (which now sits where the
  clicked chip was), so keyboard users stay in the chips row for continued
  switching.

### 2. FLIP choreography (item 2)

- TECHNIQUE (reported): a real FLIP. First rects are measured with the current
  layout live; the DOM is mutated to the final layout; Last rects are measured; then
  the travelling pieces are animated from First to Last. Two mechanisms, by role:
  - TRAVELLING TEXT (title, chips): fixed-position CLONES animated with WAAPI
    (`element.animate`). A `<span>` borrowing the destination class (.detail-title
    or .chip) is placed at the Last rect and inverted to the First rect
    (translate + scale by width ratio, transform-origin top-left), then played to
    identity. The real destination is hidden (opacity 0) until the clone's onfinish
    reveals it and removes the clone; a belt-and-braces setTimeout(FLIP_MS+80)
    guarantees cleanup if a finish/cancel event is ever missed. Clones are
    aria-hidden, pointer-events:none, position:fixed, so they never affect layout or
    hit-testing (verified: 0 clones and 0 stuck inline styles after every settle).
  - GROUP FADE + PANEL CARDS: CSS transitions (opacity + transform) on the real
    elements, driven by inline styles. The outgoing group (INDEX label + rows 04 to
    06 via the whole .index, plus .how and .proof) is pinned out of flow
    (position:absolute against the positioned .page, scroll-safe on both layouts) so
    the column reflows to the final detail layout for the Last measurement, then
    fades + slides down GROUP_SHIFT (8px, in the 6 to 10px band) over GROUP_FADE_MS
    (260ms) and is hidden. The section cards stagger in (opacity + 6px translateY,
    CARD_STAGGER_MS 60ms steps, CARD_FADE_MS 300ms each), same rhythm as the load-in
    blocks; will-change is set for the move and cleared afterwards.
- ENTER: clicked row NAME travels + scales into the detail title (clone; real title
  fades in under it at the end); the two sibling rows travel into their chips
  (clones); the group slides down and fades; the entering .detail + .conversion fade
  and slide in (with the title/chips held hidden until their clones land); the cards
  stagger. Primary travel FLIP_MS 340ms (within the ~350ms budget); card stagger
  finishes about (n-1)*60 + 300 = about 540ms for 5 cards (inside "around 500ms").
  Focus moves to the back control after the travel.
- EXIT (back / Escape / browser back): reverse. Title travels back into its row and
  the chips grow back into their rows (clones, with a fadeOutEnd so they dissolve
  into the already-visible rows); .detail + .conversion pin and fade out; the group
  fades + slides back in; the panel cards fade out first via the existing swap to
  welcome. Focus returns to the ORIGINATING project row (verified: enter blackthorn,
  switch to barker, Escape returns focus to the barker row, i.e. the open project).
- CHIP SWITCH: the clicked chip text travels + scales up into the title while the
  current title shrinks + travels into the vacated chip slot (two clones); the third
  (persisting) chip is FLIP-moved by transform if it reorders; the supporting copy
  (sub / blurb / See it live) crossfades (200ms) with the title held hidden for its
  clone; the panel cards crossfade via the existing 130ms swap.
- HOUSE EASING: `ease` everywhere (FLIP_EASE), no bounce/overshoot, transform +
  opacity only. will-change used on clones and staggering cards and removed after.
- REDUCED MOTION: enter / exit / switch / exit-to-view each early-return into an
  instant branch guarded by prefersReducedMotion(): states apply directly, no
  clones spawned, no transforms bound, staggerCards and flyText are no-ops. The
  global CSS reduced-motion rule zeroes transition durations as before. Keyboard and
  pointer triggers run identical code.

### 3. CTA relocation (item 3, judgement call reported)

The Get in touch CTA is still ONE element relocated between the index list and the
conversion cluster. Its "gentle move" is carried by the CONTAINER fades rather than
a bespoke animation: on entering it fades in with the .conversion cluster (part of
the entering set), on exit it rejoins the index and fades in with the restored
group. No separate CTA transition was added (cheap, and duplicating a fade on the
node would double up with the container fade). Reported as the judgement the brief
invited.

### 4. Mobile (item 4, measured)

Same choreography with the single-column geometry; the clones are fixed overlays so
the travel works regardless of column layout. Measured at 360 and 390 (and 768 /
desktop): the longest title "Until the Last Star" (34px, -0.015em) fits ONE line at
360 (w about 316 in a 316 box) so the title clone never wraps; the two chips fit one
row at every width (no wrap needed, though flex-wrap is available); NO horizontal
scroll; the round-6 page-as-scroller detail behaviour is unchanged (section-stack
overflow visible, page scrolls). Enter/switch/exit all settle with no stuck styles
at 360/390.

### 5. Preserved behaviour

Observer-gated section-video playback (setupSectionVideos, teardown on every view
swap), focus flow, aria-live announcements, the contact form / About / Pricing
flows, the welcome exit target, history (one pushState per detail; back/Escape route
through history.back; conversion-price/CTA exits consume the entry with
replaceState) are all unchanged. Exit target on back/Escape/browser-back stays the
WELCOME (V1), as in round 6.

### Frame-trace / performance (reported honestly)

The choreography is compositor-only after a single synchronous setup: measure First,
pin, renderView, measure Last, write styles, spawn clones. That setup chunk measured
4.3ms for the heaviest enter (the 3-video star) in the Browser pane, well under a
16.7ms frame, let alone the ~33ms bar. During the animation nothing reads layout
(only transform / opacity change), so no per-frame layout thrash is expected. A true
rAF frame-delta trace could NOT be captured here: the Browser pane tab stays
document.hidden (visibilityState "hidden"), which freezes rendering and animation
currentTime at 0 (confirmed via getAnimations()), the same paused-pane limitation
logged at stages 1 to 6. The enter and switch FLIPs were observed to settle fully
(clones removed, inline styles cleared, cards at opacity 1) while the pane was
foreground; the exit end-state was confirmed by force-finishing the animations
(getAnimations().finish()) and reading the settled DOM. The verifier's headed-GPU
harness should capture the rAF frame trace (no frame over ~33ms) as the sign-off.

### Round 7 - deviations / judgement calls

- CHIP LABEL is the project name (uppercased by CSS), not the niche tag, so the
  chip-to-title FLIP text is coherent at both ends (see item 1). Reported.
- GROUP FADE clones nothing: the whole .index (including the three project rows,
  which are covered by their title/chip clones) plus .how and .proof are pinned out
  of flow and fade as one, which is simpler and jank-free than cloning each label /
  row. The clones fly over the top, so the covered project rows fading underneath
  are never seen.
- MEASURE-THEN-ANIMATE with a pin: the outgoing group is pinned absolute BEFORE the
  Last measurement so the column reflows to the final layout in one pass (no
  measure/revert dance, no flash). Pins are against the positioned .page, so the
  approach is identical and scroll-safe on the desktop grid and the mobile flex/
  page-scroller layouts.
- EXIT clones use a fadeOutEnd (dissolve into the visible rows) rather than a hard
  reveal, since on exit the destination rows are already fading in; ENTER clones use
  a hard reveal (real title/chip held at opacity 0 until the clone lands).
- FLIP-clone z-index 50 (above content) with pointer-events:none: a clone can never
  block interaction, and the belt-and-braces timeout guarantees it is gone within
  FLIP_MS+80 even if an event is dropped.
- MOTION TABLE ADDITIONS (recorded as required, superseding the round-6 "Detail
  morph out/in" rows):
  | Name | Property | Duration | Delay | Easing | Trigger | Reduced motion |
  | Detail title/chip travel | transform (translate+scale) on a fixed clone; opacity reveal | 340ms | 0 | ease | enter / exit / chip switch | instant, no clone |
  | Detail group fade | opacity 1..0 + translateY 8px (out) / 0..1 (in) on index/how/proof or detail/conversion | 260ms | 0 | ease | enter / exit detail | instant |
  | Section card stagger | opacity 0..1 + translateY 6px..0 | 300ms | 60ms per card | ease | enter detail | instant |
  | Supporting copy crossfade | opacity 0..1 on .detail-copy | 260ms | 0 | ease | chip switch | instant |
- Encoding clean (Edit + byte-safe sed only): no BOM, no mojibake, no em dashes; the
  £ and · in the conversion line and the arrows are intact.

### Round 7 - open items / notes for the orchestrator

- The two OPEN BLOCKERs (real email, Formspree ID) and the de-vibe canonical list
  are untouched by this round.
- Screenshot / visual sign-off and the rAF frame-delta trace across enter / exit /
  switch, both themes, plus a forced reduced-motion and a 360px run, remain the
  verifier's (the Browser pane cannot render the animation while backgrounded).

### Round 7 - verifier FAIL fix (deferred video decode, 2026-07-28)

Verifier round-7 passed everything except ONE FAIL: entering or chip-switching TO
the star project dropped a 41 to 48ms frame at about 90 to 180ms into the travel
(3/3 reproducible; image-only projects clean; exit clean). Cause: the previous
build mounted AND started the section-video decode synchronously inside commit()
(setupSectionVideos), so for the three star clips the decode collided with the FLIP
clone animation. Evidence: verify/restyle-7/results-frametrace-positions.json and
results-frametrace-exit-switch.json. Fixed exactly per the verifier's suggestion;
?v=15 kept (no push since the bump). Files changed: js/main.js, PROGRESS.md.

- MOUNT is split from PLAYBACK. renderView still mounts the .section-stack in the
  panel (so FLIP geometry / Last measurement stays correct) and now calls
  primeSectionVideos(), which ONLY pauses + mutes every clip synchronously. That
  cancels the autoplay-attribute decode (the collision), while the poster attribute
  keeps rendering (paused, preload="none", so the poster shows and NOTHING decodes
  during the travel). No observer is attached and no play() is called at mount.
- PLAYBACK START is deferred. startSectionVideos() (the old setup body: attach the
  IntersectionObserver at threshold 0.5, or the no-observer fallback play) is
  scheduled by commit via scheduleSectionVideos(delay). The animated project enter
  passes SECTION_START_DELAY (FLIP_MS + 40 = 380ms); the animated chip switch passes
  SECTION_START_DELAY - SWAP_HALF through swap (commit runs at the 130ms swap
  midpoint, so the start still lands 380ms from the click, just past the 340ms
  travel and its clone reveal). The reduced-motion and non-animated paths (enter /
  switch reduced, About / Pricing / form / welcome) pass 0, so the start is
  immediate exactly as before (those views have no section videos anyway).
- NO ZOMBIE TIMERS. teardownSectionObserver() now also clears sectionStartTimer and
  runs at the TOP of every renderView (and on exit), so exiting or switching within
  the defer window cancels the pending start before the old nodes are removed; a
  fresh mount then schedules its own. The start is set AFTER renderView inside
  commit, so the teardown-clear does not wipe the just-scheduled timer.
- GATING UNCHANGED once started: only in-view cards play. Verified behaviourally in
  the Browser pane over local http: on entering star all three clips are mounted
  with posters and sources but PAUSED (paused=true x3) during the travel window; a
  moment later (start fired) the two in-view cards play and the off-screen third
  stays paused (paused = [false, false, true], currentTime advancing on the first
  two); exiting leaves the welcome with zero section videos and zero playing
  anywhere (full teardown). Zero console errors throughout.
- The definitive rAF frame-delta re-run on the star enter/switch (no frame over
  ~33ms) is the verifier's headed-GPU harness: the Browser pane stays
  document.hidden and freezes rendering, so the frame trace cannot be captured here.
  The collision CAUSE is removed (nothing decodes during the travel), which is the
  substance of the fix.

### Round 7 - verifier FAIL fix (deferred stack MOUNT, 2026-07-28)

Post-push frame trace on the live build: the video-decode deferral worked (first
play about 490ms, gating intact) but frames still dropped: enter star max deltas
34.7 / 55.6 / 104.2ms, chip switch 48.7 to 55.5ms at about 199 to 208ms, 3/3. With
the videos deferred, the remaining cost was the section stack MOUNT itself inside
commit() at the swap midpoint: decoding three posters plus 1600px jpgs and laying
out the stack while the clones animate. Fixed per the verifier's suggestion; every
?v=15 bumped to ?v=16 (a push follows). Files changed: index.html (decoding="async"
on the 8 section imgs + version bump), css/styles.css (flip-layer + version bump),
js/main.js.

- MOUNT moved OUT of the travel window. commit now renders the panel header plus an
  EMPTY stack SHELL: renderView(viewKey, shellOnly) clones the .section-stack but
  strips its .section-card children, so during the travel the panel shows a calm
  empty stack surface (NO cards, NO videos, NO imgs, so no poster/jpg decode and no
  stack layout in the 0..FLIP_MS window). WHAT SHOWS DURING THE TRAVEL (reported):
  on enter the welcome is replaced by the empty shell (calm --surface-preview); on
  switch the old stack fades out (is-swapping, as before) then the empty shell fades
  back in. No skeleton, no placeholder flash.
- CARDS mount at TRAVEL END. mountStackCards(key) appends the .section-card children
  into the shell, then runs the stagger (so the stagger IS the entrance) and starts
  the videos SECTION_START_AFTER_MOUNT (140ms) later. It is scheduled by commit via
  scheduleStackCards at SECTION_CARDS_DELAY (FLIP_MS = 340ms) from the choreography
  start: enter passes SECTION_CARDS_DELAY (commit at t0); switch passes
  SECTION_CARDS_DELAY - SWAP_HALF through swap (commit at the 130ms midpoint), so the
  mount still lands 340ms from the click. A guard skips a double-mount if a stray
  timer fires (only fills an empty shell).
- decoding="async" added to all 8 section imgs (loading="lazy" kept), so the jpgs
  decode off the main thread: the travel-end mount is layout-only and the images
  resolve async under the stagger.
- KEYBOARD / ARIA UNAFFECTED. The empty shell keeps the region attributes
  (role="region", tabindex="0", per-project aria-label), so the scroll region and
  Tab stop exist throughout the travel: the tab flow never hits a missing region
  mid-travel. Verified in-pane (shell present with role/tabindex/aria-label during
  the travel window).
- NO ZOMBIE MOUNT. teardownSectionObserver() now also clears sectionMountTimer and
  is called at the top of every renderView AND immediately at the start of
  switchProject / exitDetail / exitDetailToView, so exiting or switching within the
  window cancels the pending mount before the old nodes are removed. Verified:
  entering star then exiting in the same tick leaves the welcome with zero section
  cards (the mount timer was cancelled, no zombie), zero videos, nothing playing.
- REDUCED MOTION / immediate paths mount in FULL immediately (renderView shellOnly
  false mounts the cards and commit starts the videos with delay 0), exactly as
  before. swap forces the full immediate mount under reduced motion.
- MOBILE h-scroll (found while re-smoking, fixed): the FLIP clones are fixed
  overlays, and a clone edge briefly crossed the viewport during the travel, adding
  a transient horizontal scrollbar on mobile (post-settle was always clean; missed
  earlier because only the settled state was measured). Fixed: the clones now live
  inside one .flip-layer (position:fixed, inset:0, overflow:hidden, pointer-inert),
  and each clone is position:absolute inside it, so an overflowing edge is CLIPPED
  instead of adding scroll. Verified at 390: horizontal overflow is 0 across the
  whole travel (structurally impossible now), the FLIP still lands correctly, and
  the settled state is unchanged.
- SMOKE RE-CHECK (Browser pane, local http): enter star shows the empty shell during
  travel (0 cards/videos, region present) then mounts 3 cards + gates videos (2
  in-view play, off-screen paused) at travel end; chip switch to blackthorn lands 5
  cards with decoding="async" + loading="lazy"; exit is clean (0 cards/videos,
  welcome, index restored); zombie-cancel holds; no horizontal scroll at 390; zero
  console errors. The synchronous enter handler chunk is now about 7ms (the image
  decode + stack layout is no longer in it; cards=0 at commit time confirms the
  mount is deferred). The rAF frame-delta re-run on star enter/switch stays the
  verifier's headed-GPU harness (the Browser pane freezes rendering while hidden).

### Round 7 - verifier FAIL fix (incremental card mount, 2026-07-28)

Frame trace round 3: the travel window (0 to 340ms) is now clean, but the
over-budget frames moved to the one-shot card-mount BURST at ~400 to 450ms (enter
median 55.5, switch median 62.5; mount lands ~406 to 427ms, first video ~576 to
584ms) because the whole stack mounted in a single heavy figure-layout + poster/jpg
decode. Evidence verify/restyle-7/results-postfix2-*.json. Fixed per the verifier's
suggestion; ?v=16 kept (no push since the bump). File changed: js/main.js (plus this
log). No index.html / css changes this round.

- INCREMENTAL MOUNT. mountStackCards now appends the FIRST card immediately (at
  travel end) and each subsequent card on its own CARD_STAGGER_MS (60ms) beat via a
  setTimeout chain; appendCard(stack, card) appends one figure, fades it in
  (opacity + 6px translateY, CARD_FADE_MS) and wires its video. A single figure's
  layout fits comfortably in a frame and its img decodes async (decoding="async"),
  so the cost is spread one figure per frame instead of one burst: the stagger IS
  the mount. Measured append cadence (Browser pane): star cards land at ~345 / 406 /
  468ms from the click (60ms beats from travel end); blackthorn mounts all 5.
- PER-CARD VIDEO OBSERVATION (spreads the decode too). The IntersectionObserver is
  created once (ensureSectionObserver) and each card's clip is primed + observed AS
  it mounts (wireCardVideo), so the video decode spreads across the beats and only
  in-view clips play (gating unchanged). The old one-shot scheduleSectionVideos /
  SECTION_START_AFTER_MOUNT deferral is retired for the animated path (kept only for
  the reduced-motion / immediate full-mount via commit). staggerCards() (the old
  all-at-once CSS stagger) is removed; the per-card fade in appendCard replaces it.
- FIRST CARD STABLE (verified, the acceptance point). Cards append at the END of the
  stack, so earlier cards never move: only scrollHeight grows. Desktop (1280x820,
  blackthorn, 5 appends): the first card's offsetTop stays 149 across every append,
  the stack clientHeight stays 676 (a fixed-height scroll container) while its
  scrollHeight grows 676 -> 680 -> 1005 -> 1331 -> 1657; no horizontal scroll.
  Mobile flow layout (433 wide): first card offsetTop stays 572 across all 5
  appends; no horizontal scroll (the page-scroller grows downward, first card fixed).
- CANCELLATION MECHANISM (reported). Each deferred append step is guarded on a
  generation token: mountStackCards captures `gen = ++sectionMountGen` and every
  scheduled step returns early unless `gen === sectionMountGen` (and unless the stack
  is still connected). teardownSectionObserver bumps sectionMountGen (and clears the
  deferred-start timer and disconnects the observer) and runs at the top of every
  renderView AND at the start of switchProject / exitDetail / exitDetailToView, so a
  rapid exit or switch cancels the rest of the chain: no zombie appends. Verified:
  switching Blackthorn (mid / post chain) to Barker yields exactly Barker's 4 cards
  (captions all Barker sections), no leftover Blackthorn card, first card stable, no
  errors; exit leaves 0 cards.
- REDUCED MOTION unchanged: mountStackCards' reduced branch appends every card at
  once (the one-shot cost is fine when nothing animates), and the reduced-motion enter
  / switch still take the immediate full-mount path via commit (renderView full +
  startSectionVideos). aria / tabindex / keyboard are untouched (the region shell and
  its role / tabindex / aria-label are unchanged; cards append inside it).
- HONESTY NOTE for the verifier's 5-trial rerun: the per-frame rAF trace still cannot
  be captured in the Browser pane (it freezes rendering while document.hidden), so
  the target (no frame over ~33ms) is the verifier's headed-GPU harness. The
  structural change spreads the mount to one figure per 60ms beat; the residual risk
  the coordinator flagged is a single VIDEO card whose POSTER decode alone might
  exceed a frame (video posters have no decoding="async" equivalent). If that still
  spikes, the numbers should be reported as a documented entrance-phase hitch rather
  than chased further, per the coordinator's steer.

### Round 7 performance acceptance (orchestrator ruling, 2026-07-28)
- After three fix rounds the FLIP travel window (0 to 340ms) traces clean.
  Residual: roughly one-frame slips (median 34.7/34.8ms vs the ~33ms budget,
  occasional 41 to 56ms) scattered through the card-entrance band (400 to
  620ms) while cards fade in from opacity 0, measured on a machine running
  heavy concurrent workloads. Ruled ACCEPTED: the entrance is the least
  perceptible moment, the slips are not at a fixed repeating instant, and
  the original complaint (clunky transitions) is addressed by the clean
  travel. Evidence: verify/restyle-7/results-postfix3-frametrace.json.
- First-card mount lands ~70 to 85ms after the 345ms target (406 to 427ms
  observed): noted, not chased; the beat spacing itself holds at ~60ms.

## Client feedback round 8 (owner approved the research-backed package, 2026-07-28)

Owner-approved restructure on top of the round-7 detail state. Four parts: an
asymmetric (no-travel) detail exit, a static About/Pricing restructure (the
index drops to four rows), a footer copy-email button, and hygiene/renumbering.
Files changed: index.html, css/styles.css, js/main.js, PROGRESS.md. All shipped
refs bumped ?v=16 to ?v=17 (a push follows): 23 in index.html, 2 in
css/styles.css (two @font-face src), 0 in js/main.js; 0 remaining ?v=16. No BOM,
no mojibake, no em dashes. `node --check js/main.js` passes; zero console errors.

- Status: BUILT, awaiting verification. Behaviour verified programmatically over
  a local http server in the Browser pane (the pane stays document.hidden, so
  rAF and CSS-transition/WAAPI timelines are frozen: visual opacity/animation is
  the verifier's, but layout, state, focus, aria and DOM logic were all exercised
  directly). Height budget measured with fonts loaded at 1280x860.

### CONCEPT SUPERSESSIONS (recorded precisely, owner-directed)

- SUPERSEDES CONCEPT section 4's index list. The index is now four rows:
  01 Blackthorn & Co., 02 Barker & Bloom, 03 Until the Last Star, 04 Get in touch
  (zero-padded). The old 04 About and 05 Pricing rows are removed; the CTA
  renumbers 06 to 04 and keeps its full pastel-drift/rim/mist/bloom treatment.
- SUPERSEDES the V3 About and Pricing panel views entirely (already superseded in
  part by round 6's detail state; now removed outright). About folds into the
  masthead as an inline disclosure; Pricing becomes an always-on static block in
  the left column. The `view-about` and `view-pricing` templates and all their
  wiring are deleted. The only cloned non-project view is now `view-form` (04).
- SUPERSEDES the round-7 EXIT choreography (the reverse FLIP). Enter and
  chip-switch flights are unchanged; the exit no longer travels anything.

### Part 1 - Asymmetric exit (no travel)

- exitDetail rewritten. The detail header (.detail) and conversion cluster
  (.conversion) are pinned in place and fade out with a downward drift
  (GROUP_SHIFT 8px, inside the 6 to 10px band) via the existing playSetOut, while
  the index group (index, PRICING, how, proof) fades back in beneath via the
  existing fadeSetIn; the panel card stack fades out via the existing welcome
  swap. Nothing is cloned, so the exit is frame-trace friendly by construction.
  Focus returns to the originating project row (focusAfterFlip). Escape and
  browser-back are identical (both route through exitDetail via history.back ->
  popstate; the back control too). Reduced motion is the unchanged instant branch.
- DEAD EXIT-FLIGHT CODE REMOVED: the exit's First/Last rect measurement and its
  two flyText calls are gone, and flyText's now-unused `fadeOutEnd` branch (only
  the exit used it) is removed. flyText and flipMove remain (enter / chip-switch).
- DURATION JUDGEMENT CALL (reported): the brief asked for ~200ms on the detail
  fade-out and "existing group fade timing" on the index fade-in. Rather than add
  a fourth duration constant, the exit reuses the existing GROUP_FADE_MS (260ms)
  group-fade primitives (playSetOut / fadeSetIn) for BOTH sides. This keeps the
  enter flight byte-identical (it shares playSetOut/fadeSetIn), keeps the drift in
  the sanctioned 6 to 10px band, and the ~200/260 difference is within the brief's
  "~" tolerance. If a distinct 200ms fade-out is wanted, it is a one-line constant.
- Motion table (supersedes the round-7 exit rows):
  | Name | Property | Duration | Delay | Easing | Trigger | Reduced motion |
  | Detail title/chip travel | transform (translate+scale) on a fixed clone | 340ms | 0 | ease | enter / chip switch ONLY | instant, no clone |
  | Detail group fade (exit) | opacity 1..0 + translateY 8px on detail/conversion; opacity 0..1 on index/pricing/how/proof | 260ms | 0 | ease | exit detail | instant |

### Part 2 - Static About and Pricing (restructure)

- ABOUT (masthead disclosure). Under the positioning line: a quiet mono button
  (Archivo-column kicker type: mono 10px UPPER, --grey-label) labelled "More",
  with an inline chevron SVG. GLYPH TREATMENT (reported): one inline chevron SVG
  (stroke-width 1.4, currentColor, same stroke family as the theme-toggle icons)
  that rotates 180deg when open, giving the single consistent treatment the brief
  asked for. Clicking reveals the approved About prose (byte-identical to the
  APPROVED COPY block, the astrophysics version) via a grid-template-rows 0fr->1fr
  + opacity reveal over 180ms (inside 150 to 200ms); aria-expanded and
  aria-controls are wired, aria-hidden gates the collapsed prose from AT, the
  label flips More <-> Less, and focus stays on the button. Collapsed by default
  on every breakpoint. Under reduced motion the global guard zeroes the transition
  (instant); the click handler binds no motion listeners and spawns no nodes.
  Verified: aria-expanded/hidden/is-open/label all toggle, focus stays on toggle.
- PRICING (static block). Always visible on every breakpoint between the index and
  HOW IT WORKS (desktop) / between the panel and HOW IT WORKS (mobile). A "PRICING"
  section label matching INDEX/HOW IT WORKS, then three approved lines, each a mono
  head (10.5px UPPER, "£" figure in accent) plus an Archivo 13.5px description
  matching the how-it-works type. Verbatim approved copy.
- NOTE DROPPED (judgement call, reported prominently). The optional honest-floors
  note ("From prices are honest floors: ...") is OMITTED. The brief made it
  conditional ("if it fits"); it does not fit. See the height budget below: the
  pre-round-8 left column already sat at the 860 bottom edge (near-zero slack), so
  the always-on pricing block (~184px with the note) plus the About expander
  net-add ~156px over the ~106px freed by removing two rows. Keeping the note
  forced a ~1px safety buffer even with aggressive compaction; dropping it plus a
  coherent compaction gives a comfortable buffer. If the owner wants the note, the
  cleanest options are raising the 860 min-height or accepting a short-viewport
  scroll; flagged for the orchestrator.
- CONVERSION PRICING LINE now static (reported). The detail-state conversion
  cluster's pricing line was a button that opened the Pricing view; with no
  Pricing view it is now a plain <p> with the same mono line. Its click handler,
  hover and focus-visible rules are removed; no dangling data-view or aria.
- HEIGHT BUDGET (measured at 1280x860, fonts loaded). Baseline after the
  restructure (before compaction): docScrollH 1011, overflow 151px. Root cause:
  the round-7 left column already filled 860 with near-zero bottom slack, so the
  net +156px addition overflowed. Compaction applied, tokens only, from the
  existing scale: positioning margin-top 22->16; about margin-top 14->10; the
  three section margins (index/pricing/how) 48->26; the three list margin-tops
  16->12; index-list gap 6->4; pricing-list and how-list gap 12->6; proof
  padding-top 32->22; footer margin-top 16->12; honest-floors note dropped. RESULT
  (About collapsed): docScrollH 860, no scroll, footer bottom 843, proof pinned
  with a ~17 to 23px bottom buffer. The extra space on taller viewports pools in
  the proof's margin-top:auto exactly as before, so the tighter rhythm is
  consistent, not top-heavy. With the About expander OPEN the natural content is
  ~983px: it needs a ~983px-tall viewport to fit and scrolls below that (the brief
  sanctions this on short viewports); the collapsed default always fits at 860. In
  the DETAIL state at 860 the page never scrolls even with the expander open
  (fewer left-column blocks; the card stack scrolls internally).
- MOBILE. Order re-measured at 390x844: name block, positioning, About expander,
  INDEX (4 rows), panel, PRICING block, HOW IT WORKS, proof, footer (verified,
  0 horizontal scroll). Detail-state order verified: name, positioning, About,
  detail header, panel, conversion, footer (pricing/how/proof/index hidden). Every
  flattened child carries an explicit `order` (about=3, pricing=7 added; the rest
  renumbered). The panel keeps its 60vh reserve. scrollPanelIntoView now triggers
  only for the form view (about/pricing are no longer views); the top-edge
  threshold logic is unchanged and, with the shorter index, still scrolls the
  panel up on a form tap and does not re-scroll when already placed (no regression
  in the band logic).
- ABOUT-IN-DETAIL (judgement call, reported): the About expander is part of the
  persistent masthead (like the name and positioning lines), so it stays visible
  in the detail state and is not collapsed on enter. If a project is opened while
  About is expanded, the prose shows above the detail header; acceptable and it
  still fits at 860. Not coupled to the detail choreography by design.

### Part 3 - Copy email

- A quiet mono "Copy" button (10px UPPER, --grey-label, focus-visible accent ring)
  sits beside the mailto in the footer, both built by wireFooter from the single
  SITE_EMAIL constant (the address is never scattered). Click copies via
  navigator.clipboard.writeText with an execCommand textarea fallback (and the
  fallback also runs if the promise rejects), then flips the label to "Copied" for
  1.5s and back, an instant text swap with no animation loop. aria-live="polite"
  on the button announces the change; the accessible name is the textContent
  ("Copy"/"Copied"), CSS only uppercases it. Both themes via tokens (the dark
  --grey-label / --ink hover). Verified: click flips to "Copied" then resets.

### Part 4 - Hygiene

- Every ?v=16 bumped to ?v=17 (byte-safe sed): 23 in index.html, 2 in
  css/styles.css, 0 in js/main.js; 0 ?v=16 remain.
- Renumbering: row indices are 01 to 04 zero-padded (CTA 06 -> 04). No functional
  reference to the old 04/05/06 numbering remains; the load-bearing structural
  comments in index.html/css/js were updated, and the dead `selectByKey` helper
  (only the removed conversion-price button called it) was deleted. Historical
  PROGRESS references are left as-is.
- Contrast (section 10): the two new sub-AA mono controls (.about-toggle,
  .copy-email at --grey-label) and the mobile labels get the established
  mobile-at-rest --ink-mid remediation (verified with transitions disabled:
  #54545C light / #A6A6AE dark, both AA). The new pricing block uses --ink /
  --accent / --ink-body (all AA). Both themes verified on the new elements (a
  transition-freeze artifact in the hidden pane briefly showed mid-values; with
  transitions off all resolve to the correct token).
- Reduced-motion: the About reveal and chevron rotation are CSS transitions the
  global guard zeroes; the exit reduced branch is the unchanged instant path.

### Round 8 - deviations / judgement calls (summary)

1. Honest-floors pricing note DROPPED to fit the 860 height budget (brief allowed
   "if it fits"; it does not). Flagged for the orchestrator/owner.
2. Exit fade reuses the existing 260ms group-fade primitives for both sides rather
   than adding a distinct ~200ms constant (keeps the enter flight identical).
3. About expander glyph is a single inline chevron SVG (theme-toggle stroke
   family) rotating 180deg; reported as the one consistent treatment.
4. About expander persists (and can be open) in the detail state, as part of the
   masthead; not collapsed on enter.
5. Left-column section rhythm compacted globally from 48px to 26px (and other
   scale-token trims) to fit the always-on pricing block at the 860 minimum;
   consistent everywhere, extra space pools above the pinned proof as before.

### Client feedback round 9 - mobile "snap a little down" on tapping a project row

- Status: BUILT, awaiting verification. Owner report: on mobile, tapping a project
  row (e.g. Blackthorn) makes the page "snap a little down" right after the tap; the
  animations themselves are right. All shipped asset refs bumped ?v=17 to ?v=18 (a
  push follows): 23 in index.html, 2 in css/styles.css (js/main.js carries none).
  Files changed: js/main.js, index.html (version bump only), css/styles.css (version
  bump only), PROGRESS.md.

- DIAGNOSIS (instrumented, not guessed; measured over a local http server at 360x780,
  scrollY / body min-height / document height sampled every 8ms around the tap). The
  prime suspect (focusAfterFlip focusing the back control without preventScroll) was
  NOT the cause of the reported snap: at the tap the back control ends up in view and
  the focus delta measured 0. The real cause is a transient DOCUMENT-HEIGHT COLLAPSE
  during the synchronous enter:
  - Pre-tap: scrollY 100, documentElement.scrollHeight 1353, maxScroll 573.
  - Synchronously inside enterDetail: the outgoing group (index 224 + pricing 126 +
    how 81 + proof 58 = about 489px) is pinned position:absolute out of flow, and the
    panel renders an EMPTY stack shell (round-7 smoothness fix defers the cards to
    travel end). documentElement.scrollHeight collapses 1353 -> 807, maxScroll drops
    573 -> 27, and the browser CLAMPS scrollY 100 -> 27.
  - Cards mount at travel end: scrollHeight grows back to 1849, but the clamp is never
    released, so scrollY stays 27. Net: a -73px upward scroll, i.e. the content
    "snaps down". overflow-anchor:none (stage-5) is still applied on mobile and is not
    the cause; this is a hard scroll clamp, which anchoring cannot prevent.
  - EXIT has the mirror collapse (a tall detail, e.g. 1849, shrinks to the short
    welcome, e.g. 1353) plus a second contributor: focusAfterFlip(origin) had no
    preventScroll, so on exit it also scrolled the origin row to the top. Measured
    exit from the detail bottom (scrollY 1069): 1069 -> 0.

- FIX (js/main.js). Two parts, applied symmetrically to enter / switch / exit; both
  guarded to the mobile layout (max-width: 900px), so desktop, where the panel sits
  beside the index and never scrolls, is untouched.
  1. HEIGHT RESERVE across the morph. New closure helpers holdDocHeight /
     releaseDocHeight / scheduleReleaseDocHeight in initPanel. holdDocHeight pins the
     document at its current height with an inline min-height on <body> (the scroll
     root) BEFORE the flow is mutated, so maxScroll can never fall below the current
     scrollY mid-morph and the browser has nothing to clamp. It is released once the
     incoming layout's own height is in effect (enter/switch: HEIGHT_HOLD_ENTER_MS =
     SECTION_CARDS_DELAY + 5*CARD_STAGGER_MS + 120 = 760ms, past the last of up to
     five card mounts; exit: HEIGHT_HOLD_EXIT_MS = FLIP_MS + 120 = 460ms). If the
     settled layout is genuinely SHORTER than the held offset (exit from deep inside a
     tall detail), releaseDocHeight does the single unavoidable adjustment INSTANTLY
     at release (window.scrollTo to the new bottom) rather than letting the browser
     clamp part-way through the animation. The inline min-height is always cleared on
     release (verified: no leftover inline style after settle).
  2. MODALITY-AWARE FOCUS. New module-level input-modality heuristic: a click with
     event.detail === 0 is a keyboard-synthesised activation (Enter / Space on a
     button), detail >= 1 is a pointer tap; Escape is keyboard; the history popstate
     path (browser back, no event) falls back to a recent-pointerdown timestamp. The
     new applyFocus(el, viaKeyboard) focuses with { preventScroll: true } for pointer
     activations (so the focus does not scroll-snap) and with natural scroll for
     keyboard (so the newly focused control is brought into view, as required). The
     flag is threaded through select -> enterDetail / switchProject, and closeDetail
     (stashed across the history.back -> popstate hop) -> exitDetail; every
     focusAfterFlip / reduced-motion focus call now passes it. So the earlier focus
     suspicion is real but only for larger tap offsets and for EXIT: preventScroll is
     both a fix (it removes the exit 573 -> 0 focus jump and any enter focus-snap when
     the back control starts above the fold) and belt-and-braces for the common case.

- BEFORE / AFTER traces (360x780 unless noted; pointer tap = pointerdown + click
  detail:1; keyboard = click detail:0 / Escape keydown; scrollY sampled every 8ms):
  - ENTER Blackthorn, pointer, scrollY 100:
    BEFORE 100 -> 27 at t=14ms (netDelta -73, the snap); focus delta 0.
    AFTER  100 held throughout (min 100 / max 100, netDelta 0); min-height 1353px held
    t=10..758 then cleared; focus detail-back preventScroll:true, delta 0.
  - ENTER, pointer, scrollY 0 (360): netDelta 0, back control in view (top 185), clean.
  - ENTER, pointer, scrollY 180, index partially scrolled (360): netDelta 0, back in
    view (top 5), clean.
  - ENTER, pointer, scrollY 100 (390x844): netDelta 0, back in view (top 85), clean.
  - ENTER, KEYBOARD, scrollY 250 (390): back control focused and scrolled into view
    (focus delta -250, endY 0, preventScroll:false) - the desired keyboard behaviour,
    unchanged.
  - EXIT traces: see the "verifier follow-up" section below. The exit numbers first
    recorded here came from calling exitDetail() directly, which never goes through
    the history popstate the real back control / Escape / browser-back use, so they
    did not capture the browser's native scroll restoration; they have been replaced
    by the real-path measurements below.
  - CHIP SWITCH (Blackthorn -> Barker), pointer, scrollY 40: netDelta 0, min-height
    held then cleared, chip focused preventScroll:true, clean.
  - FORM ("Get in touch"), pointer, scrollY 0: intentionally scrolls the panel into
    view (panel top 435 -> 1, scrolled), no reserve involved - the intended behaviour
    is preserved.
  - DESKTOP (1280x800), pointer: holdDocHeight is a no-op (mobile-layout query false),
    scrollY stays 0, enters detail, no reserve, unaffected.
  - REDUCED MOTION (forced for the test via a temporary prefersReducedMotion hook,
    since the browser pane cannot emulate the media query; hook removed afterwards):
    enter mounts the full five-card stack synchronously (scrollHeight 1353 -> 1849 in
    the same frame, no empty-shell transient), so scrollY stays 100 with NO clamp and
    no reserve; exit does only the intended instant keyboard focus return to origin,
    no spurious collapse snap.

- Instrumentation discipline: all measurement was via a wrapped HTMLElement focus and
  an 8ms scrollY sampler injected from the browser console over a local http server;
  two temporary in-source probes (a counter in holdDocHeight and a window.__forceRM
  branch in prefersReducedMotion, used only to exercise the reduced-motion path) were
  added, used, and REMOVED before completion (grep-confirmed: no __forceRM / __hold in
  the source). A no-store dev server was used because the browser was serving a cached
  js/main.js at the unchanged ?v query during iteration; the shipped ?v bump to 18
  cache-busts this for real users. node --check passes; no console errors; no em
  dashes; UK English throughout.

- Judgement calls (round 9):
  1. Reserve on <body> min-height (the scroll root) rather than a dedicated spacer
     div: simplest, no new markup, and cleared to '' on release. On mobile body height
     is auto, so the inline min-height purely holds the transient; on desktop the
     helper never runs.
  2. Release timings are timers sized from the existing motion constants (760ms enter,
     460ms exit) rather than a completion callback, because a card's height is in flow
     the instant it is appended (the stagger is transform/opacity only), so the
     settled height is reached shortly after the last append; the margins cover up to
     five cards.
  3. Height reserve applied to switchProject as well (chips crossfade the panel to an
     empty shell too); measured clean, kept for symmetry and robustness.
  4. exitDetailToView (project -> form / pricing) deliberately does NOT reserve: it
     hands off to the normal index model whose form path intentionally scrolls the
     panel into view; reserving there would fight that intended scroll.
  5. popstate (genuine browser back, no event) is treated as pointer-driven when a
     pointerdown was seen in the last 700ms, else keyboard; this keeps a swipe-back
     from scroll-snapping while letting a hardware/keyboard back bring focus into view.

### Client feedback round 9 - verifier follow-up (scrollRestoration, exit re-trace)

> NOTE (superseded in part by the next subsection): setting scrollRestoration = 'manual'
> was NECESSARY but NOT SUFFICIENT. A later re-verify showed Chromium still zeroes scrollY
> intrinsically during the same-document back BEFORE popstate even with 'manual', so the
> real-path exit numbers below (settle to 573 / 547) did not reproduce on the deployed
> paths; they came from a harness whose timing read before the zeroing. The complete fix
> (scroll tracking + restore) and the correct, reproduced numbers are in the subsection
> "intrinsic scroll-zeroing" that follows.

- Verifier finding (verify/restyle-9/exit-scroll-restoration-findings.json): the enter,
  switch, reserve and focus fixes passed, but BOTH exit fails traced to one root cause
  my first self-trace masked. history.scrollRestoration was left at the browser default
  'auto', so on every popstate (the back control and Escape both route through
  history.back(), and a genuine hardware / browser back fires the same popstate) the
  browser NATIVELY restored the entry-time scrollY in the first frame, BEFORE exitDetail
  ran (measured about 16ms: 1069 -> 0; a 300 -> 0 -> 50 double-jump; Escape 200 -> 100;
  reduced motion identical). My earlier PROGRESS exit numbers were unreproducible because
  the traces called exitDetail() directly (never through popstate) and, separately, my
  test harness set scrollRestoration = 'manual' itself, hiding the native restore.

- Fix (js/main.js, one line plus guard): set history.scrollRestoration = 'manual' once,
  early in initPanel, in the same defensive try/catch style as the pushState /
  replaceState calls. With manual, the browser leaves the scroll where it is on popstate
  and exitDetail's height reserve + single settle + modality-aware focus own the final
  position. No other change; ?v stays 18.

- Exit re-traced through the REAL interaction paths (back control tapped, Escape pressed,
  and a genuine browser back via the pane's Back), with the harness NO LONGER touching
  scrollRestoration (the page owns it; confirmed history.scrollRestoration reads "manual"
  on load). scrollY sampled every 8ms; first-frame value checked for a native restore:
  - 360x780, welcome maxScroll 573:
    - Pointer BACK from the detail bottom (scrollY 1069): first frame 1069 (NO native
      restore), held at 1069 through the whole morph, then ONE instant settle to 573 at
      release (t=473); origin focused preventScroll:true, delta 0. Snap-free; settles to
      573, not 0.
    - Escape from the detail bottom (scrollY 1069): first frame 1069, held through the
      morph, then the keyboard focus return scrolls the origin row into view AFTER the
      travel (focus at t=345, delta -1069, endY 0, preventScroll:false).
    - Genuine browser BACK from the detail bottom (scrollY 1069): first frame 1069 (no
      native restore), held, then keyboard-style focus return to origin (recentPointer
      false on a chrome back, delta -1069, endY 0); exits cleanly, origin focused.
  - 390x844, welcome maxScroll 547:
    - Pointer BACK from the detail bottom (scrollY 1089): first frame 1089, held through
      the morph, ONE instant settle to 547 at release (t=472); origin focused
      preventScroll:true, delta 0.
    - Escape from a shallow position (scrollY 50, origin already visible): first frame
      50, no movement at all through the exit, origin focused (delta 0). No settle needed
      (50 < 547).
  All exits: min-height reserve cleared after settle (no leftover inline style), no
  console errors.

- scrollRestoration = 'manual' side effect, checked as asked: navigating away from the
  site entirely and back (Back to the page) lands at the TOP (returnedScrollY 0) rather
  than restoring the prior welcome scroll, and the page is fully functional (re-enters
  detail, no errors). This is the full-reload case (the test server sends no-store, which
  also disables bfcache); it is sensible for a one-page site. On normal caching a bfcache
  restore would preserve the scroll independently of scrollRestoration. Accepted; noted
  here as the documented behaviour.

### Client feedback round 9 - verifier follow-up 2 (intrinsic scroll-zeroing on back)

- Verifier finding (verify/restyle-9/exit-fix-results.json): with scrollRestoration =
  'manual', Chromium STILL zeroes scrollY intrinsically during a same-document back
  navigation, BEFORE popstate fires (they wrapped scrollTo / scrollIntoView / focus: no
  app call precedes the drop; the scroll event at y=0 arrives before popstate). So every
  exit with in-detail scroll drift snapped to 0 (1069 -> 0, Escape 300 -> 0, go_back 500
  -> 0, reduced motion 400 -> 0). My follow-up-1 settle-to-573/547 numbers again did not
  reproduce through the real paths: my harness read scrollY before the zeroing, and it
  drove the exit in a way that sometimes skipped the zeroing entirely (Chromium's zeroing
  is intermittent in the automation pane; I reproduced it deterministically by dispatching
  a real popstate after a scroll-to-0, which matches the verifier's "y=0 before popstate").

- Fix (js/main.js), covering all three triggers including hardware back (which never
  passes through closeDetail, so a per-click stash alone is insufficient):
  1. While a detail is open, a PASSIVE scroll listener records the live offset in
     lastDetailScrollY (started in enterDetail, both branches; removed on every exit, so
     no leak). A guard ignores a y === 0 event while the tracked offset is still above 60px
     (DETAIL_ZERO_GUARD): the intrinsic zeroing lands at exactly 0 in one jump from a large
     offset, whereas a real user reaches the top gradually, and exiting from a genuine top
     is snap-free anyway. So the browser's pre-popstate zeroing cannot clobber the stored
     offset.
  2. exitDetail's FIRST action (before holdDocHeight or any DOM mutation) is
     restoreDetailScroll(): stop the tracking, then window.scrollTo(0, lastDetailScrollY)
     to undo the zeroing. The held morph and the single settle at release then proceed, and
     releaseDocHeight's correction actually engages because scrollY once again exceeds the
     settled welcome max.
  3. closeDetail (the back control and Escape) ALSO captures lastDetailScrollY =
     window.scrollY synchronously right before history.back(), independent of scroll-event
     timing, so those two paths are robust even if the listener has not fired for the last
     pixel of a fast flick. A genuine hardware back cannot be intercepted and relies on the
     passive listener (which fires continuously during real scrolling) plus the guard.
  4. Genuine browser / hardware back modality corrected: a popstate with no closeDetail
     stash now defaults to false = POINTER-like (preventScroll focus, settle to the true
     welcome max), not keyboard. The earlier recentPointer heuristic wrongly made a chrome
     back keyboard, which scrolled the origin to the top (the "go_back 500 -> 0" the
     verifier flagged). The now-unused recentPointer / lastPointerDownAt module block was
     removed. ?v stays 18.

- Reproduced through the REAL interaction paths (harness no longer sets scrollRestoration;
  the browser's pre-popstate zeroing reproduced deterministically by a scroll-to-0 then a
  dispatched popstate for the genuine-back paths; the back control and Escape drive
  closeDetail for real). scrollHeight welcome max is 573 at 360x780 and 547 at 390x844:
  - 360, pointer BACK, entered 0 / scrolled to the bottom 1069: settles to 573; origin
    focused preventScroll, no focus scroll. (No-zeroing run also verified: identical 573.)
  - 360, Escape deep (1069): held, then the intended keyboard focus return to the origin
    AFTER the morph (focus delta -1069, endY 0). Origin focused, visible.
  - 360, Escape mismatched (entered 50, scrolled 300): intended keyboard focus return to
    the origin (focus delta -300, endY 0).
  - 360, GENUINE back deep with the zeroing (scroll forced to 0 before popstate): the guard
    preserved lastDetailScrollY = 1069, restoreDetailScroll recovered it, settled to 573;
    origin focused preventScroll (pointer-like), delta 0. Zeroing fully absorbed.
  - 390, GENUINE back deep with the zeroing: recovered and settled to 547.
  - 360, shallow pointer BACK (scrolled 30): no drift, held at 30 (welcome max 573 > 30, no
    settle). Origin focused preventScroll.
  - REDUCED MOTION mismatched (entered 50, scrolled 300, genuine back with zeroing):
    recovered to 300 (welcome max 573 > 300, no settle); origin focused preventScroll. No
    snap to 0. Reduced-motion enter is untouched (full synchronous mount, no reserve).
  - Enter untouched: pointer enter at scrollY 100 still nets 0 movement.
  - Multi-cycle smoke (enter -> chip switch -> back -> re-enter -> back -> form): all state
    transitions correct, body min-height clean after every exit (no leak / no accumulation),
    the form CTA still scrolls the panel into view (panel top 435 -> 1). No console errors.

- Instrumentation discipline: the scroll listener / restore were exercised with a wrapped
  HTMLElement focus and an 8ms sampler from the console; three temporary in-source probes
  (a counter/log in onDetailScroll and restoreDetailScroll, and a window.__forceRM branch
  in prefersReducedMotion to drive the reduced-motion path the pane cannot emulate) were
  added, used, and REMOVED (grep-confirmed: no __forceRM / __scLog / __restLog / __hold in
  the source). node --check passes; no em dashes; UK English. A no-store dev server was
  used again so file edits reloaded past the ?v=18 cache during iteration.

## Client feedback round 10 (owner-directed, five items + version bump, 2026-07-29)

Status: BUILT, awaiting verification. Files changed: index.html (version bump only),
css/styles.css, js/main.js, PROGRESS.md. All shipped asset refs bumped ?v=18 to
?v=19 (index.html 23, css/styles.css 2, js/main.js 0). Encoding clean (Edit tool +
byte-preserving sed; no BOM, no mojibake, no em dashes; grep-confirmed). Instrumented
in a headed pane over a local http server at 950/1000/1100/1200/1250/1440 and
360/390/768.

### CONCEPT SUPERSESSIONS (owner-directed)

- SUPERSEDES CONCEPT 3.3 "Row pointer trail" motion row entirely (item 2). The row
  pointer trails are removed: the spawn code, the pointermove listeners, the
  .trail-dot rule and the TRAIL_ constants are deleted. The --trail-a / --trail-b /
  --trail-opacity tokens STAY in the verbatim 3.1 block but are now UNUSED (kept so
  the 3.1 block remains byte-verbatim). CONCEPT 3.4 R2's "trails spawning" clause is
  likewise void. Row hover keeps motion via the CTA mist (item 3), not particles.

### Item 1 - Intermediate two-column widths (css/styles.css)

- New bounded media query: min-width 901px and max-width 1250px. In this band the
  base desktop grid (460px + 80px gap + 76px side padding) starved the 1fr panel:
  measured ~304px at 1000px (owner screenshot: squeezed panel, welcome glyph
  overlapping SELECT A PROJECT). The band now steps down to
  grid-template-columns 400px 1fr; gap var(--sp-36); padding var(--sp-36)
  var(--sp-36) var(--sp-48), and scales the welcome glyph to 240px with a
  proportional optical-centre offset (43 * 240/340 = about 30px up, from the round-2
  item-6 measurement) so the ghost arrow never overlaps the line.
- DEVIATION (reported): the brief floated "gap ~48, padding ~48". I used --sp-36 for
  both the gap and the side padding instead. Reason (instrumented): with a classic
  15px vertical scrollbar reserved, the ~48 values leave the panel at ~415px at a
  950px viewport, just under the owner's ~420 floor. --sp-36 clears it. Measured
  panel widths (pane, with a 15px scrollbar present): 427px @950, 465px @1000,
  ~565px @1100, ~665px @1200, 742px @1250. Panel at least ~420 from 950 up, as
  required.
- 1440+ UNCHANGED: the query caps at 1250px, so 1251px and up keep the base grid.
  Verified at 1440: cols 460px/748px, gap 80px, padding 76px, glyph 340px, glyph
  transform matrix translate about -124/-179 (the -43px optical offset). Pixel-
  identical to today, no regression.
- No horizontal scroll and left column not clipped at 950 (docScrollW 935, hScroll
  false); glyph fits inside the panel horizontally (glyph 629..804 within panel
  484..949 at 1000). Left column at 400px holds the masthead / 4-row index / pricing
  / how / proof / footer without overflow.
- Pixel screenshots at each width and both themes are the verifier's (the pane
  backgrounds the tab); geometry was measured programmatically as above.

### Item 2 - Remove pointer trails (js/main.js, css/styles.css)

- Deleted initRowTrails and its TRAIL_SPAWN_INTERVAL / TRAIL_LIFETIME constants, the
  init() call, and the .trail-dot CSS rule. Verified: zero .trail-dot nodes can spawn
  (grep-clean of trail spawn code; DOM query returns 0). Remaining "trail" text is in
  documentation comments and the unused 3.1 tokens only.

### Item 3 - Row hover gains the CTA mist (js/main.js, css/styles.css)

- REFACTOR (reported): the CTA's inline hover-mist block is extracted into ONE
  generic function wireHoverMist(host) (single node per host, pointerenter /
  pointermove / pointerleave, 900ms lag in the CSS transition, opacity 0 to 0.5 in
  420ms, guarded off under reduced motion and on real touch devices, per-event
  pointerType touch filter kept for hybrids). initCta calls wireHoverMist(cta); a new
  initRowMist() calls it per .row:not(.row--cta) (rows 01 to 03). No duplicated
  implementation.
- CSS: .cta-mist renamed to a shared .hover-mist (same visual). z-index is set per
  context: .row--cta .hover-mist z-index 2 (above the drift layers, below the z-5
  label) and .row:not(.row--cta) .hover-mist z-index -1 (above the hover card fill,
  below the row text). The rows are given overflow: hidden (to clip the mist to the
  16px radius) and isolation: isolate (so the mist's negative z-index is scoped to the
  row, not the page). Verified: row mist node created on a synthetic mouse
  pointerenter, position absolute, z-index -1; CTA mist z-index 2.
- DARK THEME (reported): the mist reuses --cta-hover-mist directly, which already
  carries both theme values (light: pale sea-blue rgba(233,246,253,...); dark: a soft
  blue glow rgba(120,170,230,...)). Verified in the pane (dark theme active) that the
  row mist paints the dark token on the dark hover card. No new token added.

### Item 4 - Glassier rows (css/styles.css)

- The project rows' hover and active/open box-shadows now compose --cta-rim (the CTA
  inset white rim + brighter top-highlight) in front of the single sanctioned outset
  card shadow: box-shadow var(--cta-rim), var(--shadow-row-active) on
  .row:not(.row--cta):hover and .row.is-active, .row.is-active:hover, with the
  focus-visible variants layering the accent ring first
  (var(--shadow-field-focus), var(--cta-rim), var(--shadow-row-active)). Verified
  computed (dark, transition disabled for the read): inset 1px rgba(190,216,244,0.2),
  inset 0 1px 0 rgba(200,224,248,0.3), then outset 0 1px 3px rgba(0,0,0,0.45).
- --cta-rim carries its own dark-theme values, so both themes work with no new token.
  Inset-only-except-the-one-card-shadow and two-radii discipline hold.
- JUDGEMENT CALL (reported): the CTA's edge-lift (::after radial vignette) was NOT
  translated to the rows. The inset rim plus the bright top-highlight already read as
  glass on the white/dark card; adding an extra clipped pseudo-layer risked z-order
  churn against the mist for a marginal gain. No pastel drift added to the rows (per
  the brief). If the verifier judges the rows still read flat vs the CTA, a subtle
  edge-lift can be added.

### Item 5 - Mobile section-card captions (css/styles.css)

- In the mobile detail state the section stack ran padding: 0, so the mono captions
  touched the panel's left edge and the last clipped at the bottom (owner
  screenshot). Changed to padding: 0 var(--sp-16) var(--sp-32): the media AND its
  caption now sit a comfortable 16px in from the panel edge (still aligned to each
  other), and a 32px bottom inset clears the last caption from the panel end and the
  conversion cluster. Verified in the detail state at 360 / 390 (5 cards) and 768 (3
  cards): caption inset from the panel outer edge = 17px (16 stack pad + 1 border),
  caption left aligns with the media left; last caption clears the panel bottom by
  33px (360/390) and 27px (768); panel overflow:hidden no longer clips it.

### Item 6 - Version bump + guard / no-regression re-checks

- ?v=18 to ?v=19 across index.html (23) and css/styles.css (2). js/main.js has no
  versioned refs. UK English, no em dashes, tokens only (400px column and 240px glyph
  are layout/size values with no token, same class as the existing 460px/340px), two
  radii, one border width, inset-only-except-the-card-shadow all held.
- Mist reduced-motion / touch guards: preserved by construction (the extracted
  wireHoverMist keeps the identical prefersReducedMotion() || isTouchDevice()
  early-return that the round-9 CTA mist used, and only binds listeners past it, so no
  nodes spawn and no listeners bind when guarded). Pane reported reducedMotion false /
  touchDevice false, so listeners bound and the mist rendered as expected.
- Round-9 no-scroll-regression re-check at 360: scrolled to y=120, tapped a project
  (enter), then Back (exit). scrollY held at 120 across enter-click, enter-settle,
  exit-click and exit-settle (no snap up or down); detail closed cleanly; no console
  errors through the whole sweep.

### Round 10 - deviations / judgement calls (summary for the orchestrator)

- Intermediate gap/padding are --sp-36, not the ~48 the brief floated (needed to hold
  the panel at least ~420px at 950px once a 15px scrollbar is reserved). See item 1.
- The CTA edge-lift was deliberately NOT added to the rows (item 4 judgement call).
- The --trail-a / --trail-b / --trail-opacity tokens are now unused but kept verbatim
  in the 3.1 block (item 2).
- Verification note: same backgrounded-pane limitation as prior stages (pixel
  screenshots time out); all behaviour above was measured programmatically over a
  local http server. Screenshot / visual sign-off is the verifier's.

### Client feedback round 10 - verifier follow-up (deep-exit scroll regression in the round-9 mechanism)

- Verifier finding (verify/restyle-10/scroll_trace_results.json): everything else passed,
  but a deep exit regressed the round-9 scroll-preservation. At 360x740, enter at 120,
  scroll the detail stack to 1009, tap back: scrollY read 1009 at t=5ms then 0 at t=20ms
  and stayed there, never reaching the correct settle (the index max). Diagnosis: the
  round-9 DETAIL_ZERO_GUARD (60px) only ignores a y===0 event while the tracked offset is
  still above it, but during the back sequence an exit-morph / nav reflow can clamp scroll
  to a small NON-zero value first, which the still-active passive listener records,
  dropping lastDetailScrollY below the 60px threshold; the subsequent y===0 event then
  passes the guard and the real 1009 target is lost, so restoreDetailScroll reads 0.

- Fix (js/main.js, the robust variant the verifier suggested): capture the offset ONCE,
  synchronously, at each exit entry point and pass it as an ARGUMENT all the way to
  restoreDetailScroll's window.scrollTo, so no intervening scroll event (real, or a
  reflow / zeroing clamp) can clobber it between capture and restore. Concretely:
  1. closeDetail (the back control and Escape) snapshots capturedY = window.scrollY and
     STOPS the tracking immediately, before history.back(); it passes capturedY through
     (directly for the no-history path, or via pendingExitScrollY across the
     history.back() -> popstate hop).
  2. The popstate handler's FIRST line stops the tracking, then resolves capturedY =
     (pendingExitScrollY !== null) ? pendingExitScrollY : lastDetailScrollY. A genuine
     hardware back never called closeDetail, so it uses the last tracked value (window.scrollY
     is already zeroed by the browser at popstate, so it cannot be read live); stopping the
     listener on the first line freezes that value so the exit morph cannot clobber it.
  3. exitDetail(viaKeyboard, capturedY) -> restoreDetailScroll(capturedY) does the single
     window.scrollTo(0, capturedY). The DETAIL_ZERO_GUARD is kept as a secondary guard for
     the genuine-back window (before popstate), but correctness no longer depends on it.
  releaseDocHeight's clamp-at-release semantics are unchanged: if the settled welcome is
  shorter than the restored offset, it settles once to the true welcome max. ?v stays 19.

- Re-traced through the REAL interaction paths over a local http server (detail fully
  settled so its height is stable; the browser's pre-popstate zeroing reproduced faithfully
  for the genuine-back paths by a scroll-to-0 then a dispatched popstate; the back control
  and Escape drive closeDetail for real). Welcome maxScroll measured 589 at 360x740 and 547
  at 390x844 with the settled content:
  - THE EXACT FAILING SCENARIO, 360x740, enter 120, scroll the stack to the bottom (1051),
    tap BACK: lands at 589 (min(1051, 589) via the single release settle), never 0. (The
    settle fires; an earlier reading of 1009 was my sampler catching the frame before the
    pane's throttled release timer, not a miss.)
  - 360x740 genuine hardware back from the bottom (1051) WITH the zeroing: guard + last
    tracked value recovered 1051, settled to 589; origin focused preventScroll (pointer-like).
  - 360 shallow BACK (scrolled 30): no drift, held at 30, origin focused preventScroll.
  - 360 Escape from the bottom (1051): held, then the intended keyboard focus return to the
    origin AFTER the morph (focus delta -1051, endY 0). Origin focused, visible.
  - 360 reduced motion mismatched (enter 50): recovered to a valid tracked position with NO
    snap to 0; origin focused preventScroll. (Reduced-motion enter untouched.)
  - 390x844 pointer BACK from the bottom (1031): settled to 547; origin focused preventScroll.
  - 390x844 genuine hardware back from the bottom (1031) with the zeroing and realistic
    (incremental, event-firing) scrolling: recovered and settled to 547.
  No console errors; body min-height clean after every exit (no leak).

- Test-environment note: single synthetic scrollTo(0, big) calls are sometimes coalesced by
  the automation pane so the passive listener never fires for them, which made a couple of
  genuine-back traces read the enter offset instead of the deep one (no snap to 0, just an
  unrepresentative landing); the closeDetail paths (back control / Escape) are unaffected
  because they capture synchronously, and an incremental scroll that fires real scroll
  events reproduced the correct deep recovery. Real user scrolling fires events continuously,
  so lastDetailScrollY is at most a frame stale for genuine hardware back.

- Instrumentation discipline: measured with a wrapped HTMLElement focus and an 8ms scrollY
  sampler from the console; three temporary in-source probes (a log in onDetailScroll and
  releaseDetailScroll region, and the window.__forceRM branch in prefersReducedMotion to
  drive the reduced-motion path the pane cannot emulate) were added, used, and REMOVED
  (grep-confirmed: no __forceRM / __scLog / __restLog / __relLog / __hold in the source).
  node --check passes; no em dashes; UK English; no BOM. A no-store dev server was used so
  edits reloaded past the ?v=19 cache during iteration.

### Client feedback round 10 - verifier follow-up 2 (per-path zeroing ordering, exit-window enforcement)

- Verifier finding (verify/restyle-10/fix_final_evidence.json): the follow-up-1 fix worked
  for a genuine HARDWARE back but NOT for the PRIMARY paths (the back control and Escape).
  The native zeroing ORDERING differs per path: hardware back zeroes BEFORE popstate (so the
  one-shot restoreDetailScroll corrects it), but the button / Escape paths zero AFTER
  restoreDetailScroll runs (the verifier wrapped scrollTo and logged zero calls: the guard
  window.scrollY !== y was false because the scroll was still intact at that instant), and
  the later zeroing was never corrected (the release clamp only fires when scrollY exceeds
  the settled max, and 0 never does).

- Fix (js/main.js): enforce the captured target across the WHOLE exit window instead of a
  one-shot restore. For pointer / hardware exits (viaKeyboard false):
  1. beginScrollEnforcement(target) at the top of exitDetail: an immediate re-assert (covers
     the hardware-back "before" ordering), plus listeners for the duration of the hold:
     a passive `scroll` listener re-asserts the target whenever scrollY drops below
     ENFORCE_FLOOR (8px) without user input (this catches the button / Escape "after"
     ordering), and `wheel` / `touchmove` listeners mark genuine user intent.
  2. At release, releaseDocHeight calls endScrollEnforcement(true): it removes the listeners
     and, unless the user scrolled, settles UNCONDITIONALLY to min(target, settledMax) (this
     corrects a zeroing that landed right at release, which the old "only when over" clamp
     missed). The height reserve keeps the document tall through the hold so the target fits;
     reduced motion has no reserve but the same enforcement window guards the async zeroing
     and settles once (the target is clamped to settledMax, which is the desired landing).
  3. User-intent cancels enforcement: a wheel / touchmove during the window sets userScrolled,
     after which the scroll listener stops re-asserting and the release skips the settle, so a
     user who scrolls during the morph keeps their position (reported mechanism).
  4. Keyboard exits (Escape, keyboard-activated back button) do NOT enforce: focus(origin)
     intentionally scrolls the origin into view and owns the final position; a one-shot
     restore covers the pre-popstate ordering there. A fast re-enter within the window cancels
     any pending enforcement (startDetailScrollTracking calls endScrollEnforcement) so no stale
     target is re-asserted over the new detail. ?v stays 19.

- Re-traced ALL paths through the REAL interaction handlers over a local http server, with the
  per-path zeroing reproduced faithfully (button / Escape: an injected scrollTo(0,0) about
  30ms AFTER the back click, i.e. after restore; hardware: scrollTo(0,0) then a dispatched
  popstate, i.e. before). Detail fully settled; deep offset registered via a real scroll event
  (as continuous user scrolling does). Welcome maxScroll 589 at 360x740, 573 at 390x780:
  - 360x740 button deep (1051) + POST-restore zeroing: minY stayed 589, endY 589 (the injected
    0 was re-asserted within a frame, never visible), origin focused preventScroll. LANDS 589,
    NEVER 0.
  - 360x740 hardware back deep (1051) + pre-popstate zeroing: endY 589, origin preventScroll.
  - 360x740 Escape deep (1051): intended keyboard focus return to origin (delta -1051, endY 0).
  - 360x740 keyboard-activated back button deep (click detail 0): keyboard focus return (endY 0).
  - 360x740 shallow BACK (30) + injected zeroing: held at 30 (minY = maxY = 30), no drift.
  - 360x740 reduced motion deep (1051) + injected zeroing: settled to 589 (settledMax), origin
    preventScroll, no snap to 0. Reduced-motion enter untouched.
  - 360x740 user-intent cancel: pointer back from 1051, then a touchmove + scroll to 400 during
    the morph: ends at 400 (the user's position), not re-asserted and not settled.
  - 390x780 button deep (1095) + POST-restore zeroing: endY 573. Hardware back deep + zeroing:
    endY 573.
  - Multi-cycle (enter -> chip switch -> back -> re-enter -> back -> form): all transitions
    correct, body min-height clean after every exit (no leak), enter / switch untouched. No
    console errors.

- Form scroll-into-view note: unchanged by this fix (scrollPanelIntoView / commit / selectNormal
  untouched). It uses behaviour:'smooth', which is a confirmed no-op in the automation pane
  (verified directly: panel.scrollIntoView smooth left scrollY 0, auto scrolled to 441), so the
  panel does not scroll in the pane; on a real device the smooth scroll runs. Not a regression.

- Test-environment note (carried from follow-up 1): a single synthetic scrollTo(0, big) is
  sometimes coalesced so the passive listener never records it, which only affects the
  genuine-hardware-back path (it reads the tracker); dispatching a real scroll event, as
  continuous user scrolling does, reproduces the correct deep recovery. The button / Escape
  paths capture window.scrollY synchronously in closeDetail and are unaffected.

- Instrumentation discipline: measured with a wrapped HTMLElement focus, an 8ms scrollY sampler,
  and a scrollIntoView spy from the console; faithful zeroing was injected from the test
  harness (never in source); one temporary window.__forceRM branch in prefersReducedMotion (to
  drive the reduced-motion path the pane cannot emulate) was added, used, and REMOVED
  (grep-confirmed clean). node --check passes; no em dashes; UK English; no BOM; ?v=19 held.

### Client feedback round 10 - verifier follow-up 3 (TRUE root cause: focus-scroll zeroes the live scroll before every handler; captured target was 0)

- Methodology correction (accepted): the follow-up-2 traces used INJECTED synthetic zeroing and
  passed, but the verifier's REAL mouse clicks failed. Root-caused this round in a REAL headed
  Chromium launched with the round-5 GPU flags plus --disable-features=CalculateNativeWinOcclusion
  (defeats the automation-pane throttling), driving a real Playwright trusted click. Three
  temporary logs (top of beginScrollEnforcement, in closeDetail, in the popstate handler) settled
  it in one run.

- TRUE root cause (verify/restyle-10 real-click diag): the back control sits at the TOP of the
  column and is NOT sticky, so at a deep scroll it is off-screen. A real / trusted click (and
  Playwright actionability) first scrolls it into view, and the browser's native focus-scroll
  zeroes window.scrollY to 0 BEFORE any of our handlers run. The real-click log showed:
  closeDetail entered with scrollY already 0 and captured 0; popstate saw pendingExitScrollY 0
  but lastDetailScrollY 1009; beginScrollEnforcement received target 0; the doc height held
  (min-height 1749, maxScroll 606 throughout) so the settle computed min(0, 606) = 0. So the fix
  was correct in shape but the TARGET was wrong: every synchronous window.scrollY read at exit
  time is post-focus-scroll (0). The follow-up-1 "capture synchronously in closeDetail" and the
  follow-up-3 first attempt (snapshot on the back-control pointerdown) BOTH failed the same way,
  because Playwright / the browser scrolls the control into view even before pointerdown fires.
  Only the continuously-tracked, guard-preserved lastDetailScrollY held the true offset (1009).

- Fix (js/main.js): make the guard-preserved tracker the single source of the pre-exit offset.
  1. closeDetail no longer reads window.scrollY; it stops the tracker (freezing its value) and
     carries lastDetailScrollY as the captured offset (the pointerdown/keydown snapshot attempt
     was removed as useless: the browser scrolls the off-screen control into view before those
     fire too). The popstate handler already uses pendingExitScrollY else lastDetailScrollY.
  2. The scroll guard is strengthened so the tracker survives BOTH the exact-0 zeroing and the
     round-10 small-non-zero clamp: onDetailScroll ignores any scroll event that lands below
     DETAIL_ZERO_GUARD (60px) while the tracked offset is still above DETAIL_DEEP_GUARD (240px),
     i.e. a SUDDEN deep -> top jump, which is the native focus-scroll / nav zeroing, not a user
     gesture (a real scroll-up arrives gradually, so by the time y is small the tracked value is
     small too). The exit-window enforcement (follow-up 2) is unchanged and now receives the
     correct target. ?v stays 19.

- Re-traced ALL paths with REAL interactions in the headed GPU Chromium (real trusted
  Playwright click for the button, page.keyboard.press('Escape'), page.go_back() for hardware,
  emulate_media reduced-motion; deep scroll driven via real rAF-stepped window scrolling; a
  scrollTo spy recorded the corrective calls). Welcome maxScroll 606 at 360x740, 573 at 390x780:
  - button deep 360x740: preExit 1009 -> endY 606 (scrolls [1009, 606]: immediate re-assert to
    the true target, single settle to 606, no intermediate 0), origin focused, min-height clean.
  - button deep 390x780: preExit 1053 -> endY 573.
  - hardware back deep 360: preExit 1009 -> endY 606.
  - reduced motion deep 360 (emulate_media reduce): preExit 1009 -> endY 606.
  - shallow 360 (scrolled 30): preExit 30 -> endY 30 (no drift).
  - Escape deep 360: preExit 1009 -> endY 0 (intended keyboard focus return to the origin row;
    origin focused).
  All: inDetail false after exit, body min-height clean (no leak).

- Methodology note for future rounds: do NOT validate scroll behaviour with synthetic dispatched
  events or injected zeroing in the throttled preview pane. Real trusted clicks trigger the
  native focus-scroll / actionability auto-scroll that synthetic dispatch does not, which is
  exactly where this defect lived. Use the headed GPU Chromium harness
  (scratchpad/matrix.py, GPU_ARGS incl. --disable-features=CalculateNativeWinOcclusion).

- Instrumentation discipline: three temporary window.__diag log lines (beginScrollEnforcement,
  closeDetail, popstate) were added, used for the one diagnostic run, and REMOVED
  (grep-confirmed: no __diag / armExit / __forceRM in the source). node --check passes; no em
  dashes; UK English; no BOM; ?v=19 held (index 23, css 2).

## Rebrand and migration: Pagefront (owner-directed, 2026-08-07)

Combined rebrand ("Zayn" -> "Pagefront") and hosting migration (GitHub Pages ->
Cloudflare Pages, auto-deploy on push to main). Live URL is now
https://pagefront.co.uk; demos at https://blackthorn.pagefront.co.uk,
https://barkerbloom.pagefront.co.uk, https://star.pagefront.co.uk. This
SUPERSEDES the "Zayn" wordmark, the GitHub Pages URLs and the specific cold-email
copy in CONCEPT (sections 4 and 9); CONCEPT.md itself is left unedited as the
historical spec, per the established supersede-in-PROGRESS pattern. All shipped
asset refs bumped ?v=19 -> ?v=20 (index.html 23, css 2; js/main.js carries none).

Deploy model (NEW): Cloudflare Pages serves the whole repo and auto-deploys on
push to main. There is no build step. ?v= cache-busting still applies and is
still bumped on every push. No CNAME file is used; none existed to remove.

### File by file

- index.html: wordmark name -> "Pagefront"; title, og:title, twitter:title ->
  "Pagefront . Web design for local businesses"; og:site_name -> "Pagefront";
  og:image:alt / twitter:image:alt -> "Pagefront. ..."; canonical comment +
  og:url + og:image + twitter:image -> https://pagefront.co.uk (image at
  og-image.png?v=20). Favicon comment -> "P" letterform. Inline theme script
  localStorage key 'zayn-theme' -> 'pagefront-theme'. About prose opening ->
  "I'm an astrophysics graduate who shipped a game played by more than three
  million people." (owner's name removed; rest unchanged). Footer copy ->
  copyright + "Pagefront". No-JS noscript mailto + text -> hello@pagefront.co.uk.
  Three project sub lines and three "See it live" hrefs -> the new subdomains
  (blackthorn/barkerbloom/star.pagefront.co.uk; the barker subdomain is
  "barkerbloom", no hyphen). How-it-works step 01 -> "You get in touch". Pricing
  free-mockup desc -> "Get in touch and see it before you pay." All ?v=19 -> v=20.
- css/styles.css: header comment and the .name type comment -> "Pagefront".
  New rule .section-stack[hidden] { display: none } (the base .section-stack sets
  display:flex, which outranks the UA [hidden] rule, so hidden stacks need this to
  actually hide). Both @font-face ?v -> v=20.
- js/main.js: header comment -> "Pagefront". THEME_STORAGE_KEY -> 'pagefront-theme'.
  SITE_EMAIL -> 'hello@pagefront.co.uk'. FORMSPREE_ENDPOINT ->
  'https://formspree.io/f/mnpajqae' (comment updated; the placeholder short-circuit
  guard is kept but no longer matches, so the real fetch path runs). history.state
  key { zaynDetail:1 } -> { detailOpen:1 }. Media-persistence restructure (below).
- favicon.svg: hand-authored "P" letterform, same flat ink-on-transparent geometric
  style as the old Z (one filled path, straight stem + single bowl arc, evenodd
  counter). favicon-32.png + apple-touch-icon.png regenerated via tools/favicon_png.py;
  og-image.png regenerated via tools/og_image.py (1200x630 RGB, 39.8 KB) from the
  updated tools/og_source.html (wordmark -> "Pagefront", renders cleanly, no overflow).
- tools/capture.py: the three demo record URLs -> the new pagefront.co.uk subdomains
  (so a re-record targets the migrated sites). Not a shipped file; updated for
  correctness.
- _redirects (NEW, repo root): Cloudflare Pages force-404 rules for every non-site
  path the platform would otherwise serve by path (/PROGRESS.md, /CONCEPT.md,
  /verify/*, /docs/*, /tools/*, /references/*, /.claude/*), because those carry the
  owner's name and full history. Complements the item-4 grep (shipped site files);
  the _redirects covers the rest of the repo at the serving layer. Coordinator-directed.

### Media persistence restructure (task 5)

renderView no longer clones a fresh stack and replaceChildren()s the panel body on
every project entry. Each project's .section-stack is built ONCE into a persistent
container kept in the panel DOM (projectStacks map); selections toggle visibility:

a. ensureStack(key) clones the template's stack SHELL once (region role/tabindex/
   aria-label kept, cards stripped), hides it and appends it. Subsequent entries
   reuse the same node; media is never rebuilt or refetched.
b. First-selection laziness preserved: the shell is empty, so no media loads until a
   project is first opened; the cards (with their video preload=none and lazy imgs)
   mount on first open only, so src attaches then and is never touched again.
c. deactivateProject(key) runs on leaving (exit / chip switch / opening the form):
   it hides the stack and pauses + resets currentTime to 0 on its videos. On return,
   the cards are re-wired to the IntersectionObserver, which plays only the in-view
   clip(s) (existing gating unchanged). Only the visible project's videos ever play.
d. FLIP preserved: FIRST open still renders the empty shell during travel and mounts
   cards incrementally at travel end (the stagger IS the entrance). REVISIT approach
   (reported): the from-state (opacity 0 + 6px) is set synchronously in renderView so
   the panel never flashes the full stack, then revisitStack() staggers a pure-opacity
   + translateY reveal on the EXISTING nodes (no clone, no remount) at travel end.
   Generation-token (sectionMountGen) cancellation retained on both mount and revisit
   chains; teardownSectionObserver bumps it on every renderView/exit. Removed the
   now-dead primeSectionVideos / startSectionVideos / scheduleSectionVideos /
   scheduleStackCards (replaced by activateStack / scheduleActivateStack /
   revisitStack) and the sectionStartTimer.
e. Verified (verify/launch/media-persistence-evidence.json): Blackthorn -> Star ->
   Blackthorn produced ZERO second webm/jpg fetches for Blackthorn (5 resource
   entries, each URL count 1, no duplicates), and the SAME stack + img DOM nodes are
   reused (node identity ===). Star's 3 webms likewise fetched once. Leaving a project
   left its videos paused with currentTime 0. Mobile 360 enter/exit trace: no snap,
   height reserve held across the morph then released (bodyMinHeight cleared), stacks
   persist hidden on exit, no regression. Zero console errors throughout.

### Verification summary

- Identity: grep of the shipped files (index.html, css/, js/, favicon.svg,
  tools/og_source.html) for "zayn"/"arctxrus" returns ZERO matches; no em dashes in
  the shipped source; no standalone word "we" in the rendered copy.
- Form (verify/launch/form-states-evidence.json): live endpoint wired
  (guardMatches=false); ONE real network submission -> success state; stubbed
  aborting route -> failure state with the hello@pagefront.co.uk fallback, typed
  message preserved, "Try again"; stub restored, zero real failure requests sent.
- Wordmark layout: "Pagefront" (9 chars, 31px/600) does not wrap or collide with the
  kicker at 1000px (901-1250 band, 400px column), 360px mobile, or 1440px desktop
  (measured name/kicker rects; no horizontal scroll at 360). The name block is not a
  scramble target (only the mono kicker is), so the longer wordmark is not decoded.
- Both themes verified (dark via screenshots of the detail + failure states; light via
  computed styles: ground #FAFAFA). No console errors. Screenshots of the filled form
  and failure state captured in-session; the Browser pane intermittently times out on
  pixel screenshots (documented backgrounded-pane limitation), so the success/light
  states are confirmed at DOM/computed-style level.

### Open items after this round

- The canonical 14-item de-vibe audit list blocker REMAINS OPEN (unchanged): paste the
  canonical list into docs/de-vibe-audit.md and run the full audit before outreach.
- Not verified by me (coder does not self-verify): full verifier screenshot pass,
  Lighthouse, and a forced reduced-motion run. The reduced-motion code paths are the
  unchanged shellOnly=false branches (no clones, no listeners bound; mount/revisit run
  immediately in full).

### Rebrand + migration: launch-verify FAIL fixes (2026-08-07)

Launch verify found two live FAILs; both fixed. ?v=20 -> ?v=21 across shipped
refs (index.html 23, css 2). No git commands run.

- FAIL 1 (non-site paths served at 200): the _redirects force-404 rules are
  IGNORED by Cloudflare Pages in practice, because a matching static asset is
  served BEFORE _redirects is consulted, so /PROGRESS.md, /CONCEPT.md, /docs/*,
  /tools/*, /references/* and /verify/* all served real content at 200 (evidence:
  verify/launch/redirect-status-summary.json). Fix: functions/_middleware.js
  (NEW), a Cloudflare Pages Function that runs on the edge BEFORE the static asset
  handler. It exports onRequest, lowercases the URL pathname, and returns a plain
  404 Response for the blocklist (exact: /progress.md, /concept.md, /readme.md;
  prefixes: /verify/, /docs/, /tools/, /references/, /.claude/, and /functions/
  itself defensively), else context.next(). Case-insensitive by construction.
  _redirects is KEPT as harmless belt and braces. This is deployment
  configuration, not runtime site code: the file never ships to the browser and is
  not referenced by index.html; Cloudflare compiles functions/ at deploy time on
  its own platform, so no local build step, bundler, package.json or npm runtime
  dependency is added to the repo (the no-build-step rule is not violated).
  Tested locally with node (v22) by importing the module and exercising onRequest
  against 19 sample paths (URL and Response are Node globals): 19/19 correct, all
  blocklist paths -> 404 (including a mixed-case /VERIFY/... and /README.md), all
  site assets (/, index.html, css/js/media/fonts, favicon, og-image, _redirects)
  -> next(). Live confirmation follows the next deploy.

- FAIL 2 (missing canonical tag): added
  <link rel="canonical" href="https://pagefront.co.uk/"> beside og:url, and
  updated the CANONICAL SITE URL comment to list the canonical link alongside
  og:url / og:image / twitter:image as the tags carrying the domain literally.

## Media re-capture: post-migration (2026-08-08, owner-directed)

All section media for the three projects re-captured with tools/capture.py after the
Cloudflare Pages migration, and the STAR section list changed per the owner. ?v bumped
21 -> 22 across index.html (23 refs) and css/styles.css (2 font refs); zero ?v=21
remain in the live files. Cache-bust only, media filenames carry no version.

### STAR: new owner-directed section list (SUPERSESSION)
- The old star cards (star-first t0.40, star-web t0.52, star-last t0.88 = first star /
  cosmic web / last star) are RETIRED and their six files deleted. Replaced by:
  - THE SPARK      -> star-spark      (timeline t 0.08, the inflation flash)
  - THE AFTERGLOW  -> star-afterglow  (t 0.13, the bright plasma plateau)
  - THE DARK AGES  -> star-darkages   (t 0.275, the hydrogen-gathering structure)
- t values chosen from a live headed-GPU luminance / structure sweep across the
  spark (0.04-0.12), afterglow (0.12-0.21) and dark-ages (0.21-0.29) epochs
  (content.js EPOCHS ranges). Afterglow bright plateau reconfirmed on the new site:
  lum t0.13=60, 0.14=58, 0.15=55, 0.16=50, 0.17=42 (holds bright, matches the old
  0.13-0.17 finding). Dark-ages most-structured window is t0.26-0.275 (std ~22,
  gradient ~2.1); t0.275 chosen, the gathering cluster reads clearly.
- LUMINANCE FLOOR SUPERSEDED for the dark-ages card by explicit owner direction: the
  old bright-epoch luminance floor does NOT apply. star-darkages is intentionally dark
  (mean lum ~20) but framed on the most structured window so the structure reads.
- THE SPARK carries the pointer-parallax effect (owner: scene must visibly respond).
  Reused the round-4 parallax driving: a slow, gentle, SMALL scripted circular mouse
  orbit driven as real (isTrusted) page.mouse.move at ~50Hz during the take; the site
  binds pointermove to a spring-smoothed camera orbit. Cursor NOT visible in the CDP
  screencast (verified on a test frame; cursor:none injected as belt-and-braces).
  Parallax confirmed in the OUTPUT: frames 2s apart differ by mean 7.86 and an
  amplified diff shows the whole starfield shifted coherently (a camera orbit, not
  twinkle) plus the central spark displaced.

### Quality bar / resolution trade (MEASURED, not guessed)
- STATICS: captured at DPR-2, exported 1600x900, jpg quality highest-first (q=2 = best;
  step down only to fit ~300KB, never past a q=5 floor so a busy frame keeps detail).
  All eight statics came out at q=2 (highest) and under 300KB. Fine text is crisp at
  DPR-2 (1600 > the ~1364 device px a ~682px card needs at DPR-2, with margin).
- LOOPS: the owner asked to raise 1280x720 -> 1600x900 if playback stays clean. Two
  findings forced 1280x720 instead, reported as the trade:
  1. The CDP screencast returns CSS-pixel frames regardless of deviceScaleFactor
     (verified: a 1280 DPR-2 context yields 1280x720 frames), so a genuine 1600 loop
     needs a 1600-wide CSS viewport. Star is full-bleed aspect-driven WebGL, so it was
     captured at a 1600x900 viewport (no gutters, same composition) - but:
  2. A true 1600x900 build measured 2.25-13.7MB per clip (7-37 Mbps) on the dense /
     animated WebGL, far over the 300-500KB house budget (CONCEPT 5, mobile-first), for
     only ~6% perceptual gain at the card's render size. So star loops OUTPUT 1280x720,
     downscaled from the 1600 raw (supersampled: crisper, smoother, cheaper to encode).
  Barker before/after kept its proven 1280x720 framing (a responsive page; a 1600
  viewport would reframe the tuned gallery for marginal gain on a photo wipe).
- SPARK SIZE (the one heavy card): the parallax moves near/far star layers by different
  amounts (true 3D parallax = no single motion vector) and thousands of point-stars
  flip pixel state, which is maximally adversarial for VP9 (the no-parallax epochs
  compressed to ~300KB; an amp-150 orbit ballooned to 8-28MB). Minimised with a small
  gentle orbit (amp 30x20, period 6.5s), a ~4.7s loop and crf 48 (crf 50 blocks the
  dark navy; 48 stays clean at this small amplitude): 1.84MB. Accepted as the cost of
  the owner-requested visible parallax on a dense starfield.
- AFTERGLOW RESOLUTION: full-frame smooth plasma motion (every block has residual every
  frame, unlike the mostly-static spark/dark-ages the decoder skips). Output at
  1024x576 (mod-16, 16:9) to cut its per-frame decode+composite cost; softening is
  invisible on smooth plasma at the card size. crf 36. 602KB.
- CRF/seam summary: spark 1280x720 crf48 4.73s seam 7.47 (diffuse starfield dissolve,
  no legible ghosting); afterglow 1024x576 crf36 4.97s seam 2.94; dark-ages 1280x720
  crf34 4.97s seam 1.75; barker before/after 1280x720 crf32 4.33s seam 0.72. All VP9
  Profile 0 / yuv420p / SAR 1:1 / tv-range / bt709 tags / 30fps CFR (ffprobe-confirmed).

### BARKER captured from LOCAL (barkerbloom 502 / DNS down)
- barkerbloom.pagefront.co.uk returned net::ERR_NAME_NOT_RESOLVED from Chromium (the
  subdomain is down; star and blackthorn subdomains resolved fine in the same run), so
  per the owner's instruction Barker was captured from a locally served
  C:\Dev\barker-bloom-demo (same code) via python -m http.server, using the
  BK_URL_OVERRIDE env hook added to capture.py. Unsplash hero / gallery images loaded
  (the headed capture browser has network); section ids and .ba__ slider classes match.
- BLACKTHORN captured from the live site; the owner's capped rounded-pill header bar is
  reflected in every frame and no framing went stale (all five sections frame cleanly).

### Integration / in-page verification (headed GPU, occlusion flag on)
- Renderer confirmed NVIDIA RTX 3060 in-context each session; star sessions used a 10s
  load wait and re-confirmed the renderer before capture.
- On the real page: every project's cards resolve the NEW media at ?v=22; all videos
  readyState 4, MediaError null; autoplay when in view, pause when out of view (observer
  gating, threshold 0.5, confirmed lastPausedOutOfView). Cumulative layout shift 0.016
  (well under 0.1; the card fade is transform-only, not a layout shift).
- PERSISTENCE (Blackthorn -> Star -> Blackthorn): media request counter was {} empty on
  the round trip - zero media re-fetched, no double fetch (the persistent per-project
  stacks are unhidden, not rebuilt).
- PLAYBACK dropped-frames: the RTX 3060 decodes these clips cleanly - in isolation (a
  minimal page) ALL clips measured 0% dropped over 12s x3 runs (spark/dark-ages 1280,
  afterglow 1024, plus the accepted barker control 1280). On the full portfolio page
  this session, drops inflated to 10-15% for EVERY clip because the desktop was
  saturated (nvidia-smi showed Discord, Zoom, three browsers, Camo Studio etc. all on
  the GPU at ~41% baseline) and the page runs its own canvas rAF; the numbers were not
  reproducible (an unchanged file swung 4.9% -> 10.9% between runs). PARITY control: the
  already-shipped, accepted barker before/after clip dropped 12.97% in the SAME on-page
  session, mid-range of the star clips (spark 10.1%, afterglow 15.5%, dark-ages 13.7%),
  proving the drops are environmental, not a regression. Verdict: clips are decode-clean
  and on par with production; the literal <5% on-page bar is a quiescent-machine metric
  (met in round 6) and should be re-confirmed by the verifier on an unloaded machine.

### capture.py changes (build-only tool, ships nothing)
- Per-project `viewport` in PROJECT_CFG (star 1600x900, others 1280x720); per-section
  `out_w`/`out_h` (default 1280x720) and `crf`; a `drive_orbit` real-mouse driver for
  `orbit` sections; cursor:none injection on orbit takes; static jpg quality reworked
  highest-first with a floor; BK_URL_OVERRIDE env hook for the local Barker fallback;
  vfilter/encode_crossfade/make_poster/process_loop threaded with output dimensions.
- tools/README.md section-plan updated to the new star list.
