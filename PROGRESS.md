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
