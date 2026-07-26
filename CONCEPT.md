# CONCEPT — Zayn Portfolio (wrapper site)

Status: DRAFT. Do not build until this document is approved with the literal word APPROVED.

This document is the single source of truth. The Claude Design prototype is superseded by
the spec embedded here; where anything conflicts, this document wins. UK English throughout.
No em dashes in any copy or code comments.

---

## 1. Purpose and audience

A one-page portfolio that converts warm leads. Visitors arrive from cold outreach emails
(barbers, dog groomers, other local business owners) and are checking one thing: is this
person real and worth replying to. The site's job is to confirm and remove friction, not
to hard-sell. No urgency tactics, no fake social proof, no sticky CTA bars.

Secondary audience: recruiters and technical visitors following the GitHub link. The site
must not embarrass a developer CV, but the barber comes first in every trade-off.

Success criteria: legible in three seconds, loads fast on a cheap Android phone, one clear
action (Get in touch), pricing visible, proof visible, the three live builds one click away.

## 2. Stack and hard rules

- Plain HTML + CSS + vanilla JS. One page. No frameworks, no build step, no React, no
  Tailwind, no shadcn, no component libraries, no npm dependencies at runtime.
- The two 21st.dev reference components (hover-button, button-colorful) are visual
  references only. Their mechanics are reimplemented in vanilla JS/CSS. Never import them
  or scaffold a React project to host them.
- Files: index.html, css/styles.css, js/main.js, media/ (webm previews + poster jpgs),
  fonts/ (self-hosted, see 4), references/ (create it, with a REFERENCES.md describing
  any pasted reference images Zayn drops in).
- Repo: github.com/Arctxrus/portfolio, deployed to GitHub Pages. Cache-bust every asset
  with ?v=N, starting at v=1, bumped on every push.
- Performance budget: first load under 300KB excluding the preview videos (which lazy-load).
  No layout shift after the load-in animation. Lighthouse mobile 90+ across the board.

## 3. Embedded design spec (from the approved prototype)

The full token, type, motion and state specification extracted from the approved Claude
Design prototype is reproduced below verbatim as sections 3.1 to 3.4. Implement exactly.
Deviations require a note in PROGRESS.md with a reason.

### 3.1 Design tokens

```css
:root {
  /* Ground & ink */
  --ground:            #FAFAFA;
  --ink:               #141416;
  --ink-body:          #43434A;
  --ink-mid:           #54545C;
  --grey-label:        #8E8E96;
  --grey-soft:         #A6A6AE;
  --grey-placeholder:  #9A9AA2;

  /* Accent, sea blue */
  --accent:            #1A6FD4;
  --accent-rgb:        26,111,212;
  --accent-fill-active:#E7F1FB;
  --accent-fill-hover: #EDF4FC;
  --accent-hairline:   rgba(26,111,212,0.16);
  --accent-innershade: rgba(26,111,212,0.08);
  --accent-ghost:      rgba(26,111,212,0.07);

  /* Pointer trails (row hover) */
  --trail-a:           #8FC3EE;
  --trail-b:           #B9DDF5;
  --trail-opacity:     0.32;

  /* Borders & surfaces */
  --border:            #E8E8EC;
  --border-width:      1px;      /* the only border width on the page */
  --surface-white:     #FFFFFF;
  --surface-field:     #FAFAFA;
  --surface-preview:   #F4F4F7;
  --surface-panelhead: rgba(250,250,250,0.7);
  --submit-ink:        #141416;
  --submit-ink-hover:  #000000;

  /* CTA pill (row 06), pastel water fill drifting on x and y */
  --cta-layer1: radial-gradient(70% 180% at 20% 15%, #DCEEF9 0%, rgba(220,238,249,0) 62%);
  --cta-layer2: radial-gradient(60% 170% at 75% 85%, #CFDDF3 0%, rgba(207,221,243,0) 64%);
  --cta-layer3: linear-gradient(100deg, #D6E9F7, #C6D9F1, #D9E7F6, #D6E9F7);
  --cta-bg-size: 260% 260%, 240% 240%, 300% 200%;
  --cta-lightpass: radial-gradient(55% 150% at 50% 50%, rgba(255,255,255,0.30) 0%, rgba(255,255,255,0) 68%);
  --cta-edge-lift: radial-gradient(120% 160% at 50% 50%, rgba(255,255,255,0) 42%, rgba(255,255,255,0.34) 100%);
  --cta-rim:    inset 0 0 0 1px rgba(255,255,255,0.62), inset 0 1px 0 rgba(255,255,255,0.85);
  --cta-hover-mist: radial-gradient(circle, rgba(233,246,253,0.55) 0%, rgba(233,246,253,0.26) 44%, rgba(233,246,253,0) 72%);
  --cta-press-mist: radial-gradient(circle, rgba(255,255,255,0.75) 0%, rgba(255,255,255,0.40) 42%, rgba(255,255,255,0) 72%);
  --cta-text:          #141416;
  --cta-index:         rgba(20,20,22,0.5);

  /* Dot grid (canvas, fixed, behind everything) */
  --dot-rest:  rgba(20,20,22,0.06);
  --dot-warm:  rgb(26,111,212);
  --dot-size:  1.5px;  --dot-spacing: 26px;

  /* Radii, exactly two values */
  --radius-pill:    999px;
  --radius-surface: 16px;

  /* Spacing scale (all values in use) */
  --sp-2: 2px;  --sp-4: 4px;  --sp-6: 6px;  --sp-10: 10px; --sp-12: 12px;
  --sp-14: 14px; --sp-16: 16px; --sp-18: 18px; --sp-22: 22px; --sp-26: 26px;
  --sp-32: 32px; --sp-36: 36px; --sp-48: 48px; --sp-56: 56px; --sp-76: 76px;
  --sp-80: 80px;
  /* Row vertical padding 11px. Field padding 14px 18px. Submit 15px 26px. */

  /* Shadows: no drop shadows anywhere, inset only */
  --shadow-row-hover: inset 0 0 0 1px rgba(26,111,212,0.16), inset 0 -3px 12px rgba(26,111,212,0.08);
  --shadow-field-focus: inset 0 0 0 1px #1A6FD4;
}
```

Desktop layout: height 100vh, min-height 860px, grid-template-columns 460px 1fr, gap 80px,
padding 76px 76px 56px. Left column is a flex column with min-height 0; the proof strip is
pinned to the bottom with margin-top auto. Preview panel: 1px border, 16px radius,
overflow hidden. Panel body is a 1fr by 1fr grid so all states centre.

### 3.2 Type spec

Families: Archivo 400/500/600 (all prose and UI) and Martian Mono 300/400/500 (all labels,
indices, tags, captions). Self-host both as variable woff2 in fonts/ (same approach as
Barker & Bloom); do not load from Google Fonts at runtime.

| Style | Family | Size | Weight | Tracking | Line height | Case |
|---|---|---|---|---|---|---|
| Name "Zayn" | Archivo | 31px | 600 | -0.015em | normal | as typed |
| FREELANCE / WEB | Mono | 10px | 400 | normal | normal | UPPER |
| Positioning line | Archivo | 16px | 400 | normal | 1.6 | sentence |
| "£300" inline | Mono | 14px | 400 | normal | inherit | accent colour |
| INDEX / HOW IT WORKS labels | Mono | 10px | 400 | normal | normal | UPPER |
| Row index 01 to 06 | Mono | 11px | 400 | normal | normal | zero padded |
| Row name | Archivo | 15.5px | 500 | normal | normal | as typed |
| Row name (CTA 06) | Archivo | 15.5px | 600 | normal | normal | as typed |
| Niche tag | Mono | 10px | 400 | normal | normal | UPPER |
| Expand glyph (rows/CTA) | system | 14px | 400 | normal | 1 | n/a |
| Expand glyph (welcome) | system | 340px | 400 | normal | 0.8 | n/a |
| How-it-works index | Mono | 10px | 400 | normal | normal | zero padded |
| How-it-works text | Archivo | 13.5px | 400 | normal | normal | sentence |
| Proof strip | Mono | 10.5px | 400 | normal | 1.7 | UPPER |
| Footer email line | Archivo | 13px | 400 | normal | normal | sentence |
| Panel header label | Mono | 10.5px | 400 | normal | normal | UPPER |
| Welcome line | Mono | 11px | 400 | 0.1em | normal | UPPER |
| Panel project title | Archivo | 34px | 600 | -0.015em | normal | as typed |
| Panel sub line | Mono | 10.5px | 400 | normal | normal | lower |
| Caption bar | Mono | 10.5px | 400 | 0.04em | normal | UPPER |
| Form label | Mono | 10px | 400 | normal | normal | UPPER |
| Form inputs/textarea | Archivo | 14px | 400 | normal | normal | sentence |
| Submit button | Archivo | 14px | 600 | normal | normal | sentence |

Textarea: rows 4, resize none. The expand glyph must be one consistent treatment (single
character or single inline SVG reused everywhere, same stroke weight).

### 3.3 Motion spec

| Name | Property | Duration | Delay | Easing | Trigger | Reduced motion |
|---|---|---|---|---|---|---|
| Decode/scramble | text chars resolve left to right (rAF) | 650ms | 0 | linear per frame | mount, once, [data-scramble], never re-fires | skipped, text renders final |
| Block fade-in | opacity 0 to 1, translateY 6px to 0 | 500ms | stagger 0/120/180/240/320/350/400ms | ease | mount | instant |
| Row hover | background; inset shadow; index and name colour; tag opacity to 0; glyph opacity 0 to 1 with x -4px to 0 | 160ms (shadow 220ms) | 0 | ease | pointerenter/leave | instant |
| Row pointer trail | 12px dot, blur 12px; opacity 0 to 0.32 in 300ms (20ms delay); 0.32 to 0 over 1200ms starting at 1000ms; node removed at 2200ms | as listed | as listed | ease | pointermove, spawn at most every 100ms | not spawned; also skipped when pointerType is touch |
| Panel swap | opacity 1 to 0 and translateY 0 to 6px over 130ms, content switches at midpoint, reverse 130ms | 260ms total | 0 | ease | row or CTA click | instant, content still swaps |
| CTA fill drift (layer 1) | background-position, 2D four-point path | 22s rest, 14s hover | 0 | ease-in-out infinite | always | animation none, static gradient |
| CTA light pass (layer 2) | background-position, 2D reverse path | 30s rest, 19s hover | 0 | ease-in-out infinite | always | animation none |
| CTA filter | saturate 1 to 1.25, brightness 1 to 1.03 | 240ms | 0 | ease | pointerenter/leave | instant |
| CTA hover mist | position follows cursor with 900ms lag, cubic-bezier(0.22,0.61,0.36,1); opacity 0 to 0.5 in 420ms | as listed | 0 | as listed | pointermove over pill | not rendered |
| CTA press bloom | scale 0.25 to 1, opacity 0 to 0.5 to 0 | 600ms, node removed at 700ms | 0 | ease-out, one iteration | pointerdown, exactly one per press | not spawned |
| Press scale | none anywhere on the page | | | | | |
| Submit hover | background #141416 to #000000 | 150ms | 0 | ease | hover | instant |
| Field focus | border colour, inset ring, background | 150ms | 0 | ease | focus | instant |
| Dot grid tint | per-dot lerp toward accent within 100px of cursor, alpha 0.06 to 0.48, about 12% per frame | rAF loop | 0 | exponential approach | mousemove | static grid, no listener bound |

Global reduced-motion CSS: all animation and transition durations forced to 0.01ms, one
iteration, plus the JS guards above. Nothing may loop or pulse to attract attention except
the CTA drift and light pass, which are sanctioned. Nothing animates while a control is
merely held. No bounce or overshoot easing anywhere.

### 3.4 State inventory

PAGE: P1 load (0 to 800ms, decode plus staggered fade); P2 settled, nothing selected.

PREVIEW PANEL:
- V1 welcome, no selection. Header "PREVIEW / NO SELECTION". Giant expand glyph at
  --accent-ghost behind the welcome line "SELECT A PROJECT" (decodes on load). No caption.
- V2 project shown. Video preview area (see section 5), project title, mono sub line,
  caption bar with 1px top rule. Header "PREVIEW / <name>".
- V3 section shown (About, Pricing). As V2 without caption bar. Real content per section 6.
- V4 form shown. White 16px-radius card, 440px wide, centred.
- V5 mid swap, panel body at opacity 0, translateY 6px.

INDEX ROWS 01 to 05: R1 rest (transparent, index --grey-soft, name --ink-mid, tag shown,
glyph hidden); R2 hover (fill --accent-fill-hover, inset hairline and shade, index accent,
name ink, tag faded out, glyph in, trails spawning); R3 active (fill --accent-fill-active,
index accent, name ink, tag hidden, glyph shown, no trails unless hovered); R4 active plus
hover. Rows 04 and 05 have no niche tag.

CTA ROW 06: C1 rest (drifting pastel fill, white inset rim, edge lift, ink text); C2 hover
(drift quickens, saturate/brighten, lagging hover mist at 0.5); C3 press held (no scale, no
loop, one press bloom from the exact pointer or tap point, clipped by the pill); C4 release
(panel swaps to V4); C5 no persistent selected styling on the pill itself.

FORM: F1 field rest; F2 focus (accent border, white background, inset accent ring, no outer
halo); F3 filled (as rest with ink text); F4 submit rest (ink pill, white label, no border,
no shadow); F5 submit hover (pure black, 150ms); F6 no distinct press state.

## 4. Content (final copy)

All strings below are final unless marked REPLACE. UK English. No em dashes.

- Name block: "Zayn" and "FREELANCE / WEB".
- Positioning: "I build fast, polished websites for local businesses. From £300."
- Index: 01 Blackthorn & Co. (BARBERSHOP), 02 Barker & Bloom (DOG GROOMING),
  03 Until the Last Star (WEBGL), 04 About, 05 Pricing, 06 Get in touch (tag: SAME DAY REPLY).
- Captions: 01 "BUILT TO TURN PHONE-SCROLLERS INTO BOOKED CHAIRS";
  02 "BUILT TO KEEP THE GROOMING DIARY FULL WITHOUT PHONE TAG";
  03 "BUILT TO SHOW THE WEB CAN FEEL LIKE A GAME".
- How it works: 01 "You reply to my email"; 02 "I build you a free homepage mockup";
  03 "Live in about two weeks".
- Proof strip: "SHIPPED A GAME WITH 3,000,000+ PLAYERS · BSC ASTROPHYSICS · 3 LIVE BUILDS".
- Footer: "<real email> · typically reply same day". REPLACE: hello@zayn.co.uk was a
  prototype placeholder. Zayn supplies the real address before build. The email is plain
  visible text AND a mailto link.
- Welcome line: "SELECT A PROJECT".
- Form: label "GET IN TOUCH"; placeholders "Name", "Business", "What do you need built?";
  submit "Send — I typically reply same day" REPLACE the em dash with a comma or middle dot
  per house style: "Send · I typically reply same day".
- Panel sub lines for projects: one short mono line each, factual, lower case, e.g.
  "single page · booking form · live at arctxrus.github.io/blackthorn-demo". Draft at build
  time for approval in PROGRESS.md; no invented facts.

### 6. About and Pricing panel content

About (V3, short prose, Archivo 14px, max ~70 words): who Zayn is in two sentences
(physics graduate, shipped a game with 3M+ players, builds sites for local businesses),
plus one line on how he works (fast, no agencies, no templates). Draft for approval.

Pricing (V3): three mono-labelled lines, no table, no cards:
- "WEBSITES FROM £300" with one sentence: single page, written and built for your business.
- "CARE PLAN FROM £25/MONTH" with one sentence: hosting, edits, and keeping it fast.
- "FREE HOMEPAGE MOCKUP" with one sentence: reply to the email and see it before paying.
Exact sentences drafted at build for approval. "From" prices are honest floors: larger
scope quotes higher.

### Hidden testimonials slot

A quote strip lives under the index in the left column: one rotating quote, name and
business, small type. Ship it with the `hidden` attribute and real markup and styles, no
content. It is enabled later by removing one attribute. No fake quotes ever.

## 5. Project previews (the panel's V2 content)

- Each project shows a muted, looping webm screen capture (autoplay, muted, loop,
  playsinline, preload none, lazy-loaded on first selection) with a poster jpg shown
  before load and wherever autoplay is unavailable.
- Below the video: the caption bar, then a "Visit live site ↗" pill (styled as a quiet
  secondary pill, ink outline, not the CTA treatment) opening the live URL in a new tab
  (rel noopener). The video itself is also a link to the same URL.
- No iframes anywhere. No embedding the live sites.
- Target file size 300 to 500KB per clip, VP9, about 800px wide, 6 to 8 seconds,
  loop-friendly start and end.

### Capture pipeline (build stage, scripted, not manual)

Use Playwright (webapp-testing skill) with recordVideo per project:
- Blackthorn: glide from the cover through the price menu to the rotating pull-quote.
- Barker & Bloom: hero, paw trail drawing, a peek at the pricing bento.
- Until the Last Star: one epoch transition with lensing visible. Record HEADED with GPU
  on the RTX 3060 so T2 visuals are captured, not the software fallback.
Scripted scroll only (eased scrollTo or mouse.wheel loop). Post-process with ffmpeg: trim
to loop points, scale, strip audio, VP9 target bitrate, export first frame as poster jpg.
Record these late, after the demo sites are final. Add "re-record clips" to the demo push
checklist.

## 7. Contact form wiring

- Formspree free tier. Plain HTML form POST enhanced by JS: intercept submit, send via
  fetch, show an inline success state inside the form card ("Sent. I will reply the same
  working day.") and an inline failure state with the visible email as fallback ("Something
  broke. Email me directly at <address>."). Never a redirect to Formspree's page.
- Honeypot field for spam. No captcha. Required: all three fields, minimal validation
  (non-empty, email not required since there is no email field: the reply channel is
  their choice in the message or the follow-up).
- Note: unlike the demo sites, this form genuinely sends. No fiction disclaimer here.

## 8. Mobile spec (the prototype was desktop only)

- Below 900px: single column. Order: name block, positioning, INDEX, panel, HOW IT WORKS,
  proof strip, footer. The panel sits directly under the index and swaps exactly as on
  desktop; on selection, smooth-scroll the panel into view (respecting reduced motion).
- Welcome glyph scales down (about 160px). Panel min-height about 60vh so V1 to V4 do not
  reflow the page.
- Touch: no pointer trails, no hover mist, no dot-grid tint (canvas static). Press bloom
  fires from the tap point. All hover-revealed information must be visible at rest on
  touch: niche tags stay visible, the expand glyph is always shown on rows.
- Videos on mobile: same lazy webm with poster; if autoplay is blocked, poster plus a play
  affordance is acceptable.
- Test explicitly at 360px, 390px, 768px widths and at 100vh quirks (URL bar collapse).

## 9. Head, meta and share card

- Title: "Zayn · Web design for local businesses".
- Meta description, one sentence, mirrors the positioning line.
- Open Graph and Twitter card: og:title, og:description, and a purpose-made 1200x630
  og-image.png: ground #FAFAFA, "Zayn" plus positioning line in the site's type, one
  accent element. Built as part of this project, not screenshotted.
- Favicon: simple "Z" mark, ink on transparent, SVG plus PNG fallbacks. No default icon.
- Correct lang="en-GB", charset, viewport. Copyright year in footer generated by JS.

## 10. Accessibility

- Rows and CTA are real buttons (or anchors) with visible focus states: focus-visible
  uses the accent inset ring, same treatment as field focus. Full keyboard operability:
  tab through rows, enter/space selects, panel updates announced via aria-live polite.
- The decorative dot grid canvas and welcome glyph are aria-hidden.
- Contrast: all text combinations must pass WCAG AA. Check --grey-soft (#A6A6AE) 10px
  mono tags on #FAFAFA: if below 4.5:1, darken the tag colour on mobile-at-rest and for
  focus, and note the deviation in PROGRESS.md.
- prefers-reduced-motion fully honoured per the motion spec table.

## 11. De-vibe audit gate

Before the final commit, run the DE-VIBE AUDIT prompt (docs/de-vibe-audit.md; copy the
agreed checklist into the repo) against the built site and record PASS/FLAG per item in
PROGRESS.md. The build does not ship with any Tier 1 flag open. The final check (name
three distinctive deliberate choices) must be answered in PROGRESS.md.

## 12. Build order and verification

Verifier subagent plus PROGRESS.md, same protocol as cosmic-dawn. Screenshots to verify/
at every stage. Commit when done at each stage. ?v= bump on every push.

1. Scaffold: files, tokens, fonts self-hosted, dot grid canvas, static layout desktop.
2. Left column complete: decode, stagger, rows with all four states, trails, CTA pill
   with drift, rim, hover mist, press bloom. Verify against the state inventory.
3. Panel: V1 welcome, V2/V3/V4 with placeholder media, swap animation, keyboard and
   aria-live behaviour.
4. Form: Formspree wiring, success and failure states, honeypot.
5. Mobile pass per section 8, tested at the listed widths.
6. Capture pipeline: record, process and integrate the three webm previews and posters.
7. Head/meta/OG/favicon per section 9.
8. De-vibe audit gate per section 11, fix flags.
9. Final verify run: desktop Chrome, headed; forced reduced-motion run; 360px mobile run;
   Lighthouse. Screenshots to verify/final/. Deploy to GitHub Pages.
10. Post-deploy: set PORTFOLIO_URL in cosmic-dawn's js/content.js to this live URL and
    push that change in the cosmic-dawn repo.

## 13. Out of scope

No blog, no CMS, no analytics beyond (optionally) a privacy-light counter, no dark mode,
no multi-page routing, no service worker, no cookie banners (nothing to consent to), no
testimonial content until real ones exist, no local SEO work (handled by outreach, not
this site).