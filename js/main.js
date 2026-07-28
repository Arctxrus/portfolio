/* ==========================================================================
   Zayn portfolio - main.js
   Stage 1: single email constant, footer wiring, dot grid canvas.
   Stage 2: decode/scramble, block fade-in, row selection (R1 to R4),
            row pointer trails, CTA hover mist and press bloom.
   Stage 3: panel controller (row/CTA to view swap, V5 animation, active-state
            sync, aria-live announcement, contact-form submit stub).
   Stage 4: contact form wiring (Formspree fetch, success/failure states,
            honeypot, native + trim validation, in-flight guard, aria).
   Round 4: project previews reverted to muted autoplay loop (the round-3
            scroll-scrub controller is retired by owner direction).
   Round 6: project rows 01 to 03 open a DETAIL state (left column morphs to a
            project header + conversion cluster; the panel shows a scrollable
            stack of section cards). Back control, Escape and browser back exit
            it; About / Pricing / form keep the normal index model.
   Round 7: the flat two-phase morph is replaced by a FLIP choreography (the
            clicked name travels into the title, the two other projects travel
            into chips, the group slides down and fades, the cards stagger in).
            The two OTHER projects become chips under the back control; a chip
            switches the open project in place (a FLIP swap). All FLIP is skipped
            under reduced motion (no clones spawned, no transforms bound).
   Vanilla JS only. UK English. No em dashes.
   ========================================================================== */

'use strict';

/* --------------------------------------------------------------------------
   Motion environment guards (CONCEPT.md 3.3). Evaluated once at load; the
   reduced-motion query is also observed so a mid-session change is honoured
   for anything created afterwards.
   -------------------------------------------------------------------------- */

const reducedMotionQuery = window.matchMedia('(prefers-reduced-motion: reduce)');
function prefersReducedMotion() {
  return reducedMotionQuery.matches;
}

/* Real touch device (CONCEPT.md section 8): a coarse pointer with no hover.
   Used to fully skip binding the pointer-trail and CTA-hover-mist listeners on
   phones (the dot grid already keys off the same query). The per-event
   pointerType === 'touch' checks are kept as well, so a hybrid laptop that
   reports hover/fine still filters its own touch events correctly. */
const coarsePointerQuery = window.matchMedia('(hover: none) and (pointer: coarse)');
function isTouchDevice() {
  return coarsePointerQuery.matches;
}

/* --------------------------------------------------------------------------
   Theme (Client feedback round 5). System / light / dark, via ONE mechanism:
   the stored preference is resolved to a concrete theme and written as
   data-theme on <html>; the CSS only reads [data-theme="dark"] (there is no
   prefers-color-scheme query in the styles). An inline head script applies the
   resolved theme before first paint (no flash); this controller wires the footer
   toggle, persists the choice in localStorage, live-updates when the OS scheme
   changes while following the system, and fires a 'themechange' event so the dot
   grid canvas can re-read its colours and repaint. aria and reduced-motion
   behaviour are unchanged by the theme.
   -------------------------------------------------------------------------- */

const THEME_STORAGE_KEY = 'zayn-theme';
const themeMediaQuery = window.matchMedia('(prefers-color-scheme: dark)');

function resolveTheme(pref) {
  if (pref === 'dark' || pref === 'light') {
    return pref;
  }
  return themeMediaQuery.matches ? 'dark' : 'light';   /* system */
}

function readThemePref() {
  try {
    const v = localStorage.getItem(THEME_STORAGE_KEY);
    if (v === 'light' || v === 'dark' || v === 'system') {
      return v;
    }
  } catch (e) { /* storage unavailable: fall through to the default */ }
  return 'system';
}

function applyResolvedTheme(pref) {
  const resolved = resolveTheme(pref);
  document.documentElement.setAttribute('data-theme', resolved);
  document.dispatchEvent(new CustomEvent('themechange', {
    detail: { pref: pref, resolved: resolved }
  }));
}

function initTheme() {
  const buttons = Array.prototype.slice.call(document.querySelectorAll('.theme-opt'));
  if (!buttons.length) {
    return;
  }

  let pref = readThemePref();

  function reflect() {
    buttons.forEach(function (btn) {
      const active = btn.dataset.themeChoice === pref;
      btn.setAttribute('aria-pressed', active ? 'true' : 'false');
    });
  }

  /* The inline head script already set data-theme for this pref, so only the
     button state needs syncing on load (no redundant re-apply / themechange). */
  reflect();

  buttons.forEach(function (btn) {
    btn.addEventListener('click', function () {
      pref = btn.dataset.themeChoice;
      try {
        localStorage.setItem(THEME_STORAGE_KEY, pref);
      } catch (e) { /* ignore: the choice still applies for this session */ }
      reflect();
      applyResolvedTheme(pref);
    });
  });

  /* Live-update on an OS scheme change, but only while following the system. */
  function onSystemChange() {
    if (pref === 'system') {
      applyResolvedTheme(pref);
    }
  }
  if (themeMediaQuery.addEventListener) {
    themeMediaQuery.addEventListener('change', onSystemChange);
  } else if (themeMediaQuery.addListener) {
    themeMediaQuery.addListener(onSystemChange);   /* older Safari */
  }
}

/* --------------------------------------------------------------------------
   Contact email - defined exactly once so it can be swapped in one edit.
   Placeholder until the real address is supplied (see PROGRESS.md).
   -------------------------------------------------------------------------- */

const SITE_EMAIL = 'hello@placeholder.invalid';

/* --------------------------------------------------------------------------
   Formspree endpoint - defined exactly once. The contact form's action
   attribute is set from this constant when the form view is rendered (see
   initPanel/renderView), so there is a single place to edit the endpoint and
   the plain POST target matches it. The real form ID is an open item
   (see PROGRESS.md); the placeholder is deliberately obvious.
   -------------------------------------------------------------------------- */

const FORMSPREE_ENDPOINT = 'https://formspree.io/f/REPLACE_FORM_ID';

/* --------------------------------------------------------------------------
   Footer wiring: build the email line and mailto from SITE_EMAIL, and stamp
   the copyright year (CONCEPT.md section 9).
   -------------------------------------------------------------------------- */

function wireFooter() {
  const emailLine = document.querySelector('[data-email-line]');
  if (emailLine) {
    const link = document.createElement('a');
    link.href = 'mailto:' + SITE_EMAIL;
    link.textContent = SITE_EMAIL;

    emailLine.textContent = '';
    emailLine.appendChild(link);
    emailLine.appendChild(document.createTextNode(' · typically reply same day'));
  }

  const year = document.querySelector('[data-year]');
  if (year) {
    year.textContent = String(new Date().getFullYear());
  }
}

/* --------------------------------------------------------------------------
   Dot grid canvas.

   Fixed, decorative canvas behind everything. Dots sit on a --dot-spacing
   lattice at --dot-size, at rest colour --dot-rest. When the cursor is within
   RADIUS px of a dot, that dot lerps toward --dot-warm and its alpha rises
   from the rest value toward MAX_ALPHA, easing about EASE per frame
   (exponential approach) in a rAF loop.

   Guards (CONCEPT.md 3.3 "Dot grid tint", section 8):
   - prefers-reduced-motion: grid is static, no mousemove listener bound.
   - touch-only devices: grid is static, no mousemove listener bound.
   Both cases still draw one static frame and handle DPR and resize.
   -------------------------------------------------------------------------- */

const DOT_MAX_ALPHA = 0.48;   /* motion table: alpha 0.06 to 0.48 */
const DOT_EASE = 0.12;        /* motion table: about 12% per frame */
const DOT_RADIUS = 100;       /* motion table: within 100px of cursor */

function readNumberVar(styles, name) {
  return parseFloat(styles.getPropertyValue(name));
}

/* Parse "rgba(20,20,22,0.06)" or "rgb(26,111,212)" into {r,g,b,a}. */
function parseColour(value) {
  const nums = value.replace(/rgba?\(/, '').replace(')', '').split(',').map(function (n) {
    return parseFloat(n.trim());
  });
  return { r: nums[0], g: nums[1], b: nums[2], a: nums.length > 3 ? nums[3] : 1 };
}

function initDotGrid() {
  const canvas = document.getElementById('dot-grid');
  if (!canvas) {
    return;
  }
  const ctx = canvas.getContext('2d');
  if (!ctx) {
    return;
  }

  const rootStyles = getComputedStyle(document.documentElement);
  const spacing = readNumberVar(rootStyles, '--dot-spacing');
  const size = readNumberVar(rootStyles, '--dot-size');

  /* Colours are re-read on a theme change (Client feedback round 5) so the grid
     flips to light-on-dark or dark-on-light and repaints. spacing/size are
     theme-neutral and read once above. */
  let rest, warm, restAlpha;
  function readColours() {
    const s = getComputedStyle(document.documentElement);
    rest = parseColour(s.getPropertyValue('--dot-rest').trim());
    warm = parseColour(s.getPropertyValue('--dot-warm').trim());
    restAlpha = rest.a;
  }
  readColours();

  const prefersReduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  const isTouchOnly = window.matchMedia('(hover: none) and (pointer: coarse)').matches;
  const isStatic = prefersReduced || isTouchOnly;

  let dpr = 1;
  let cssWidth = 0;
  let cssHeight = 0;

  /* Dot lattice and per-dot animated state (0..1 warmth, current alpha). */
  let cols = 0;
  let rows = 0;
  let originX = 0;
  let originY = 0;
  let warmth = null;   /* Float32Array */
  let alpha = null;    /* Float32Array */

  const pointer = { x: -9999, y: -9999, active: false };
  let rafId = 0;
  let running = false;

  function buildLattice() {
    cols = Math.floor(cssWidth / spacing) + 1;
    rows = Math.floor(cssHeight / spacing) + 1;
    /* Centre the lattice so resize does not shift the pattern visibly. */
    originX = (cssWidth - (cols - 1) * spacing) / 2;
    originY = (cssHeight - (rows - 1) * spacing) / 2;
    const count = cols * rows;
    warmth = new Float32Array(count);
    alpha = new Float32Array(count).fill(restAlpha);
  }

  function resize() {
    dpr = Math.max(1, window.devicePixelRatio || 1);
    cssWidth = window.innerWidth;
    cssHeight = window.innerHeight;
    /* Buffer in device pixels, CSS box unchanged: no layout shift. */
    canvas.width = Math.round(cssWidth * dpr);
    canvas.height = Math.round(cssHeight * dpr);
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    buildLattice();
    /* Paint one static frame immediately so the grid is never blank before
       the first rAF (and stays correct when the loop is not running). */
    drawStatic();
  }

  function drawDot(x, y, r, g, b, a) {
    ctx.beginPath();
    ctx.arc(x, y, size / 2, 0, Math.PI * 2);
    ctx.fillStyle = 'rgba(' + r + ',' + g + ',' + b + ',' + a + ')';
    ctx.fill();
  }

  /* One static frame: every dot at rest colour and rest alpha. */
  function drawStatic() {
    ctx.clearRect(0, 0, cssWidth, cssHeight);
    for (let iy = 0; iy < rows; iy++) {
      const py = originY + iy * spacing;
      for (let ix = 0; ix < cols; ix++) {
        const px = originX + ix * spacing;
        drawDot(px, py, rest.r, rest.g, rest.b, restAlpha);
      }
    }
  }

  function frame() {
    ctx.clearRect(0, 0, cssWidth, cssHeight);
    const r2 = DOT_RADIUS * DOT_RADIUS;
    for (let iy = 0; iy < rows; iy++) {
      const py = originY + iy * spacing;
      for (let ix = 0; ix < cols; ix++) {
        const idx = iy * cols + ix;
        const px = originX + ix * spacing;

        let target = 0;
        if (pointer.active) {
          const dx = px - pointer.x;
          const dy = py - pointer.y;
          const d2 = dx * dx + dy * dy;
          if (d2 < r2) {
            target = 1 - Math.sqrt(d2) / DOT_RADIUS;
          }
        }

        /* Exponential approach toward the proximity target. */
        warmth[idx] += (target - warmth[idx]) * DOT_EASE;
        const targetAlpha = restAlpha + (DOT_MAX_ALPHA - restAlpha) * target;
        alpha[idx] += (targetAlpha - alpha[idx]) * DOT_EASE;

        const w = warmth[idx];
        const cr = Math.round(rest.r + (warm.r - rest.r) * w);
        const cg = Math.round(rest.g + (warm.g - rest.g) * w);
        const cb = Math.round(rest.b + (warm.b - rest.b) * w);
        drawDot(px, py, cr, cg, cb, alpha[idx]);
      }
    }
    rafId = window.requestAnimationFrame(frame);
  }

  function onPointerMove(event) {
    pointer.x = event.clientX;
    pointer.y = event.clientY;
    pointer.active = true;
  }

  function onPointerLeave() {
    pointer.active = false;
  }

  /* Throttled resize so rapid drags do not rebuild the lattice every event. */
  let resizeTimer = 0;
  function onResize() {
    window.clearTimeout(resizeTimer);
    resizeTimer = window.setTimeout(resize, 120);
  }

  resize();
  window.addEventListener('resize', onResize);

  /* Repaint on a theme change: re-read the dot colours, then draw a static frame.
     In the animated case the running rAF loop immediately continues with the new
     colours; in the static case this is the repaint. Registered before the static
     early-return so it applies in both modes (CONCEPT 3.3 dot-grid guards are
     unchanged: no mousemove listener is bound on touch/reduced-motion). */
  document.addEventListener('themechange', function () {
    readColours();
    drawStatic();
  });

  if (isStatic) {
    /* No mousemove listener bound, no rAF loop: static grid only. */
    return;
  }

  window.addEventListener('mousemove', onPointerMove);
  window.addEventListener('mouseleave', onPointerLeave);
  running = true;
  rafId = window.requestAnimationFrame(frame);

  /* Pause the loop when the tab is hidden to save cycles. */
  document.addEventListener('visibilitychange', function () {
    if (document.hidden) {
      if (running) {
        window.cancelAnimationFrame(rafId);
        running = false;
      }
    } else if (!running) {
      running = true;
      rafId = window.requestAnimationFrame(frame);
    }
  });
}

/* --------------------------------------------------------------------------
   Decode / scramble (CONCEPT.md 3.3 "Decode/scramble")
   Text characters resolve left to right over 650ms via rAF, linear per frame,
   on mount, once, on [data-scramble] elements, never re-firing. Whitespace is
   left in place so the reveal reads cleanly and monospace widths never shift.
   Reduced motion: skipped entirely, the final text (already in the HTML) stays.
   -------------------------------------------------------------------------- */

const SCRAMBLE_DURATION = 650;
const SCRAMBLE_POOL = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789/#*';

function scrambleElement(el) {
  if (el.dataset.scrambleDone === 'true') {
    return;
  }
  el.dataset.scrambleDone = 'true';

  const finalText = el.textContent;
  const total = finalText.length;
  const start = performance.now();

  function frame(now) {
    const t = Math.min(1, (now - start) / SCRAMBLE_DURATION);
    const revealed = Math.floor(t * total);   /* linear reveal, left to right */
    let out = '';
    for (let i = 0; i < total; i++) {
      const ch = finalText[i];
      if (i < revealed || ch === ' ') {
        out += ch;
      } else {
        out += SCRAMBLE_POOL[(Math.random() * SCRAMBLE_POOL.length) | 0];
      }
    }
    el.textContent = out;
    if (t < 1) {
      window.requestAnimationFrame(frame);
    } else {
      el.textContent = finalText;
    }
  }

  window.requestAnimationFrame(frame);
}

function initDecode() {
  const targets = document.querySelectorAll('[data-scramble]');
  if (prefersReducedMotion()) {
    /* Skipped: text renders final immediately (it is already in the markup). */
    return;
  }
  targets.forEach(scrambleElement);
}

/* --------------------------------------------------------------------------
   Block fade-in (CONCEPT.md 3.3 "Block fade-in")
   The initial hidden state and 500ms transition live in CSS (.fade-block);
   per-block stagger delays are set inline via --fade-delay. Here we simply
   flip .is-in after first paint so the transition runs. Under reduced motion
   the CSS forces the blocks visible, so this is a harmless no-op.
   -------------------------------------------------------------------------- */

function initFadeIn() {
  const blocks = document.querySelectorAll('.fade-block');
  /* Double rAF: guarantee the initial (opacity 0) state is painted first. */
  window.requestAnimationFrame(function () {
    window.requestAnimationFrame(function () {
      blocks.forEach(function (block) {
        block.classList.add('is-in');
      });
    });
  });
}

/* --------------------------------------------------------------------------
   Panel controller (CONCEPT.md 3.4 V2 to V5, sections 5, 6, 10)

   Rows 01 to 05 swap the panel to their V2 project or V3 section view; the CTA
   row 06 swaps to the V4 form (C4). Index rows carry the single-selection
   active state (R3) and aria-pressed; the CTA never keeps a selected style
   (C5), and selecting it clears any active index row so the two stay in sync.

   Each selection: update active states, then run the V5 swap (body fades and
   lifts 6px in 130ms, content switches at the midpoint, reverse 130ms). Under
   reduced motion the content swaps instantly with no animation. The new panel
   header text is mirrored into a polite aria-live region for a concise
   announcement. Re-selecting the already-shown view is a no-op (no replay).
   -------------------------------------------------------------------------- */

const SWAP_HALF = 130;   /* ms: out phase; the in phase mirrors it (260 total) */

/* Client feedback round 6: rows 01 to 03 are projects and open the DETAIL state
   (left column morphs, panel shows a scrollable stack of section cards). Rows 04
   About and 05 Pricing and 06 the CTA keep the normal index model. */
const PROJECT_KEYS = ['blackthorn', 'barker', 'star'];

/* Detail-state choreography timing (Client feedback round 7). The flat two-phase
   crossfade of round 6 is replaced by a FLIP move: the clicked project name
   travels and scales into the detail title, the two sibling rows travel into
   their chips, the outgoing group slides down 8px and fades, and the section
   cards stagger in. House easing only (ease), transform + opacity only, no bounce
   or overshoot. Total within ~350ms for the primary travel; the card stagger
   finishes around 500ms. All of this is skipped under reduced motion (no clones
   spawned, no transforms bound; the states just apply). */
const FLIP_MS = 340;            /* primary travel (title / chips), within ~350ms */
const FLIP_EASE = 'ease';       /* house easing, no bounce */
const GROUP_FADE_MS = 260;      /* outgoing / incoming group slide + fade */
const GROUP_SHIFT = 8;          /* px slide of the fading group (6 to 10px band) */
const CARD_STAGGER_MS = 60;     /* per-card step, same rhythm as the load-in blocks */
const CARD_FADE_MS = 300;       /* per-card opacity + 6px translateY */
/* Defer the section-video decode until just after the primary travel completes
   (round 7 verifier FAIL: starting decode mid-travel dropped a 41 to 48ms frame on
   the 3-video star). Measured from the start of the choreography; a small margin
   past FLIP_MS keeps it clear of the clone reveal. */
const SECTION_START_DELAY = FLIP_MS + 40;   /* 380ms from the choreography start */

/* Panel-into-view scroll (CONCEPT.md section 8). After a selection on mobile the
   panel header must be on screen. The test is on the panel's top edge, measured
   in px and independent of viewport height. A visible-fraction test does not
   work once the panel is frozen at 60vh (stage-5 fix 1): the visible fraction
   then depends only on viewport height and stops crossing any fixed threshold on
   tall phones (the crossover sits near 777px, so 780/812/844 never scrolled).
   Rule: do not scroll when the top edge already sits in a small band near the
   viewport top (the user tapped a second row after the first scroll settled);
   otherwise scroll the panel up so its header shows.
   Tolerance band (judgement call): -8px to 20% of the viewport height. The -8px
   floor ignores sub-pixel/rounding negatives without a needless re-scroll; the
   0.2 * vh ceiling treats "panel top within the first fifth of the screen" as
   already placed, while a panel sitting below the index (well past that fifth)
   scrolls. Desktop is excluded outright by the mobile-layout media query, not by
   the geometry, so the panel beside the index never scrolls there. */
const PANEL_TOP_MIN = -8;         /* px: floor of the already-placed band */
const PANEL_TOP_BAND = 0.2;       /* ceiling as a fraction of viewport height */
const mobileLayoutQuery = window.matchMedia('(max-width: 900px)');

function initPanel() {
  const panelBody = document.querySelector('.panel-body');
  const panel = document.querySelector('.panel');
  const page = document.querySelector('.page');
  const headerLabel = document.querySelector('.panel-head-label');
  const liveRegion = document.querySelector('[data-panel-live]');
  const rows = Array.prototype.slice.call(document.querySelectorAll('.row'));
  const indexRows = rows.filter(function (row) {
    return !row.classList.contains('row--cta');
  });
  const ctaRow = rows.filter(function (row) {
    return row.classList.contains('row--cta');
  })[0] || null;

  /* Detail-state elements (round 6). */
  const indexList = document.querySelector('.index-list');
  const indexSection = document.querySelector('.index');
  const howSection = document.querySelector('.how');
  const proofEl = document.querySelector('.proof');
  const detailEl = document.querySelector('.detail');
  const detailCopySlot = document.querySelector('[data-detail-copy]');
  const detailBack = document.querySelector('[data-detail-back]');
  const detailChipsSlot = document.querySelector('[data-detail-chips]');
  const conversionEl = document.querySelector('.conversion');
  const conversionPrice = document.querySelector('.conversion-price');

  if (!panelBody || !rows.length) {
    return;
  }

  /* Map each row key to its row element and display name (round 7). The chips
     and the FLIP clones both use the project name, so the travelling text is the
     same string at both ends (a chip label morphs cleanly into the title). */
  const rowByKey = {};
  const PROJECT_NAMES = {};
  rows.forEach(function (row) {
    const key = row.dataset.view;
    if (key) {
      rowByKey[key] = row;
      const nameEl = row.querySelector('.row-name');
      PROJECT_NAMES[key] = nameEl ? nameEl.textContent : '';
    }
  });
  function chipByKey(key) {
    return detailChipsSlot
      ? detailChipsSlot.querySelector('[data-chip-key="' + key + '"]')
      : null;
  }
  function detailTitleEl() {
    return detailCopySlot ? detailCopySlot.querySelector('.detail-title') : null;
  }
  function rowNameEl(key) {
    return rowByKey[key] ? rowByKey[key].querySelector('.row-name') : null;
  }

  /* The six rows form one single-selection group with aria-pressed; exactly one
     is pressed at a time (or none, at the welcome and on exit). */
  indexRows.forEach(function (row) {
    row.setAttribute('aria-pressed', 'false');
  });
  if (ctaRow) {
    ctaRow.setAttribute('aria-pressed', 'false');
  }

  /* The leaving / entering sets for the detail-state choreography. On entering
     detail the leaving set fades out and the entering set flies/fades in; on exit
     the roles reverse. */
  const leavingEls = [indexSection, howSection, proofEl];
  const enteringEls = [detailEl, conversionEl];

  let currentView = null;      /* V1 welcome is showing; no view key yet. */
  let swapTimer = 0;
  let groupTimer = 0;          /* pending hide+unpin of a faded-out group */
  let inDetail = false;        /* the detail state is open */
  let detailKey = null;        /* which project is open */
  let detailOriginRow = null;  /* the row that opened it (focus returns here) */
  let detailPushed = false;    /* a history entry was pushed for this detail */
  let sectionObserver = null;  /* gates section-video playback by visibility */
  let sectionStartTimer = 0;   /* deferred playback start (round 7 FAIL fix) */

  /* ---- panel content ---------------------------------------------------- */

  /* Section-card videos (round 6, verifier round-6 FAIL 1). The markup keeps
     autoplay for mobile robustness, but starting every clip at once (three at a
     time for the star) overran the decoder and dropped 15 to 29% of frames. So
     an IntersectionObserver gates playback on ALL breakpoints: only a card
     substantially in view (>= 50%) plays; the rest are paused. On setup every
     clip is paused first (cancelling the autoplay start), so at most the one or
     two visible clips ever decode together. root is the viewport (null): the
     panel's overflow:hidden and the stack's overflow-y:auto clip off-screen
     cards, so their intersection ratio is ~0 and they stay paused; this works on
     desktop (internal panel scroll) and mobile (page scroll) alike. The observer
     is torn down on every view swap (before the old nodes are removed) so it
     never leaks or fights the About / Pricing / form / welcome views, and it does
     not touch reduced motion (a muted preview loop was accepted there; the
     observer only manages play/pause by visibility, binds no transition and
     spawns no node). */
  const SECTION_PLAY_RATIO = 0.5;

  function teardownSectionObserver() {
    if (sectionObserver) {
      sectionObserver.disconnect();
      sectionObserver = null;
    }
    /* Cancel any deferred playback start (round 7 verifier FAIL): if the user
       exits or switches before the start fires, there is no zombie timer. */
    window.clearTimeout(sectionStartTimer);
    sectionStartTimer = 0;
  }

  /* Round 7 verifier FAIL fix. Starting the section-video decode synchronously at
     mount collided with the FLIP clone travel and dropped a 41 to 48ms frame on
     the 3-video star (image-only projects were clean). Playback is now split from
     the mount: primeSectionVideos() runs synchronously at mount and only PAUSES
     the clips (cancelling the autoplay-attribute decode, so nothing decodes during
     the travel while the posters still render); startSectionVideos() attaches the
     visibility observer and lets it play the in-view clip(s), and is scheduled to
     run after the primary travel (SECTION_START_DELAY) or immediately (delay 0)
     on the reduced-motion / non-animated paths. */

  function primeSectionVideos() {
    const vids = panelBody.querySelectorAll('.section-video');
    vids.forEach(function (v) {
      v.muted = true;
      try { v.pause(); } catch (e) { /* ignore: cancel the autoplay decode */ }
    });
  }

  function startSectionVideos() {
    teardownSectionObserver();
    const vids = Array.prototype.slice.call(
      panelBody.querySelectorAll('.section-video'));
    if (!vids.length) {
      return;
    }
    /* Keep them paused until the observer decides who is visible. */
    vids.forEach(function (v) {
      v.muted = true;
      try { v.pause(); } catch (e) { /* ignore */ }
    });

    if (!('IntersectionObserver' in window)) {
      /* No observer support: fall back to the autoplay attribute (play them). */
      vids.forEach(function (v) {
        const p = v.play();
        if (p && p.catch) { p.catch(function () {}); }
      });
      return;
    }

    sectionObserver = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        const v = entry.target;
        if (entry.isIntersecting) {
          const p = v.play();
          if (p && p.catch) { p.catch(function () {}); }
        } else {
          try { v.pause(); } catch (e) { /* ignore */ }
        }
      });
    }, { threshold: SECTION_PLAY_RATIO });

    vids.forEach(function (v) { sectionObserver.observe(v); });
  }

  /* Schedule the playback start: 0 (or falsy) starts it now; a positive delay
     defers it past the travel. teardownSectionObserver (run at the top of every
     renderView, and on exit) clears a pending start, so exiting or switching
     within the window never leaves a zombie timer or a start on removed nodes. */
  function scheduleSectionVideos(delay) {
    window.clearTimeout(sectionStartTimer);
    if (!delay) {
      sectionStartTimer = 0;
      startSectionVideos();
      return;
    }
    sectionStartTimer = window.setTimeout(function () {
      sectionStartTimer = 0;
      startSectionVideos();
    }, delay);
  }

  function renderView(viewKey) {
    const tpl = document.getElementById('view-' + viewKey);
    if (!tpl) {
      return;
    }
    /* Disconnect the previous section observer before the old nodes leave the
       DOM (covers project -> project, project -> welcome and every other swap). */
    teardownSectionObserver();
    const frag = tpl.content.cloneNode(true);

    if (PROJECT_KEYS.indexOf(viewKey) !== -1) {
      /* A project template carries a .detail-copy (for the left header) and a
         .section-stack (for the panel). Only the stack goes in the panel here;
         the copy is placed by fillDetailCopy when the detail state opens. */
      const stack = frag.querySelector('.section-stack');
      if (stack) {
        panelBody.replaceChildren(stack);
        /* Mount only: pause the clips now (cancel autoplay); the observer and any
           play() are deferred by commit via scheduleSectionVideos so the decode
           does not collide with the FLIP travel (round 7 verifier FAIL). */
        primeSectionVideos();
      }
      return;
    }

    /* welcome / about / pricing / form: the whole view goes in the panel. */
    panelBody.replaceChildren(frag);
    if (viewKey === 'form') {
      /* Inject the Formspree endpoint into the freshly cloned form (single
         source of truth; also the plain POST target if fetch is unavailable). */
      const form = panelBody.querySelector('[data-contact-form]');
      if (form) {
        form.action = FORMSPREE_ENDPOINT;
      }
    }
  }

  function announce(text) {
    if (liveRegion) {
      liveRegion.textContent = text;
    }
  }

  function commit(viewKey, headerText, videoDelay) {
    renderView(viewKey);   /* mounts + primes (paused); teardown clears old timer */
    if (headerLabel) {
      headerLabel.textContent = headerText;
    }
    announce(headerText);
    /* Start the section videos: 0 (default) is immediate (reduced motion and the
       non-animated views, where there are no section videos anyway); a positive
       delay defers the decode past the FLIP travel (animated project enter/switch).
       Scheduled after renderView so its teardown does not clear this timer. */
    scheduleSectionVideos(videoDelay || 0);
    /* Only the normal index-model views scroll the panel into view on mobile
       (round 6): the detail state morphs in place and its header sits in the left
       column, so a project selection must not scroll the panel over that header.
       The welcome restore stays at the top so the restored index is visible. */
    if (viewKey === 'about' || viewKey === 'pricing' || viewKey === 'form') {
      scrollPanelIntoView();
    }
  }

  /* videoDelay (round 7 FAIL fix) is passed through to commit so a project switch
     defers its section-video decode past the FLIP travel. commit runs at the swap
     midpoint (SWAP_HALF in), so the caller passes the delay measured FROM the
     midpoint; 0 for the reduced-motion and non-video paths. */
  function swap(viewKey, headerText, videoDelay) {
    if (prefersReducedMotion()) {
      commit(viewKey, headerText, 0);   /* instant, content still swaps */
      return;
    }
    window.clearTimeout(swapTimer);
    panelBody.classList.add('is-swapping');   /* out: opacity 0, translateY 6px */
    swapTimer = window.setTimeout(function () {
      commit(viewKey, headerText, videoDelay || 0);   /* switch at the midpoint */
      /* Flush the opacity 0 state with the new content, then drop the class so
         the body eases back in (130ms). A layout read is used rather than rAF
         so the fade-in is not left stuck when the tab is backgrounded. */
      void panelBody.offsetWidth;
      panelBody.classList.remove('is-swapping');
    }, SWAP_HALF);
  }

  /* Bring the panel into view on selection. Mobile only: on desktop (>900px) the
     panel sits beside the index and must never scroll, so the whole function is
     guarded on the mobile-layout media query rather than relying on geometry. */
  function scrollPanelIntoView() {
    if (!panel || !mobileLayoutQuery.matches) {
      return;
    }
    const top = panel.getBoundingClientRect().top;
    const vh = window.innerHeight || document.documentElement.clientHeight;
    if (top >= PANEL_TOP_MIN && top <= PANEL_TOP_BAND * vh) {
      return;   /* already at or near the viewport top: do not re-scroll */
    }
    panel.scrollIntoView({
      behavior: prefersReducedMotion() ? 'auto' : 'smooth',
      block: 'start'
    });
  }

  /* ---- detail-state building blocks ------------------------------------- */

  function showEl(el) { if (el) { el.removeAttribute('hidden'); } }
  function hideEl(el) { if (el) { el.setAttribute('hidden', ''); } }
  function clearFx(el) {
    if (el) {
      el.style.transition = '';
      el.style.opacity = '';
      el.style.transform = '';
    }
  }

  /* The Get in touch CTA is ONE element. In the normal model it is row 06 in the
     index list; in the detail state it is relocated into the conversion cluster
     (its click, drift, rim, mist and bloom listeners travel with the node). The
     relocation itself is not a FLIP: on entering, the CTA fades in with the
     conversion cluster; on exit it fades in with the restored index (item 3, a
     gentle move via the container fades rather than a bespoke animation). */
  function moveCtaToConversion() {
    if (ctaRow && conversionEl && ctaRow.parentElement !== conversionEl) {
      conversionEl.appendChild(ctaRow);
    }
  }
  function moveCtaToIndex() {
    if (ctaRow && indexList && ctaRow.parentElement !== indexList) {
      indexList.appendChild(ctaRow);   /* back as the last index row */
    }
  }

  function fillDetailCopy(key) {
    const tpl = document.getElementById('view-' + key);
    if (!tpl || !detailCopySlot) { return; }
    const frag = tpl.content.cloneNode(true);
    const copy = frag.querySelector('.detail-copy');
    if (copy) {
      detailCopySlot.replaceChildren(copy);
    }
  }

  /* Build the two chips for the OTHER two projects (round 7). The chip label is
     the project name, so the FLIP clone carries the same string at both ends
     (chip <-> title). aria-pressed is intentionally NOT set: a chip is one-shot
     navigation (it switches the open project), not a toggle, and the open project
     is never itself a chip, so there is no pressed/unpressed chip to reflect. The
     switch is announced through the panel aria-live region (announce). */
  function renderChips(currentKey) {
    if (!detailChipsSlot) { return; }
    const others = PROJECT_KEYS.filter(function (k) { return k !== currentKey; });
    const frag = document.createDocumentFragment();
    others.forEach(function (k) {
      const btn = document.createElement('button');
      btn.type = 'button';
      btn.className = 'chip';
      btn.setAttribute('data-chip-key', k);
      btn.textContent = PROJECT_NAMES[k];
      frag.appendChild(btn);
    });
    detailChipsSlot.replaceChildren(frag);
  }

  function setPressed(key) {
    indexRows.forEach(function (r) {
      r.classList.remove('is-active');
      r.setAttribute('aria-pressed', r.dataset.view === key ? 'true' : 'false');
    });
    if (ctaRow) {
      ctaRow.classList.remove('is-open');
      ctaRow.setAttribute('aria-pressed', 'false');
    }
  }

  function pushDetailHistory() {
    try {
      history.pushState({ zaynDetail: 1 }, '');
      detailPushed = true;
    } catch (e) {
      detailPushed = false;
    }
  }
  function consumeDetailHistory() {
    if (detailPushed) {
      try { history.replaceState(null, ''); } catch (e) { /* ignore */ }
      detailPushed = false;
    }
  }

  function nameOf(row) {
    const nameEl = row.querySelector('.row-name');
    return nameEl ? nameEl.textContent : '';
  }

  function clearAllSelection() {
    indexRows.forEach(function (r) {
      r.classList.remove('is-active');
      r.setAttribute('aria-pressed', 'false');
    });
    if (ctaRow) {
      ctaRow.classList.remove('is-open');
      ctaRow.setAttribute('aria-pressed', 'false');
    }
  }

  /* ---- FLIP primitives (round 7) ---------------------------------------- */

  /* Pin an element out of flow at its current on-screen box (measured against the
     positioned .page, so it is scroll-safe on both layouts). Used to freeze the
     outgoing group where it sits so the column can reflow to the final layout
     while the group fades in place. */
  function pinAbsolute(el, pageRect) {
    if (!el) { return; }
    const r = el.getBoundingClientRect();
    el.style.position = 'absolute';
    el.style.margin = '0';
    el.style.left = (r.left - pageRect.left) + 'px';
    el.style.top = (r.top - pageRect.top) + 'px';
    el.style.width = r.width + 'px';
    el.style.zIndex = '3';
    el.style.pointerEvents = 'none';
    el.dataset.pinned = 'true';
  }
  function unpin(el) {
    if (!el) { return; }
    el.style.position = '';
    el.style.margin = '';
    el.style.left = '';
    el.style.top = '';
    el.style.width = '';
    el.style.zIndex = '';
    el.style.pointerEvents = '';
    clearFx(el);
    if (el.dataset.pinned) { delete el.dataset.pinned; }
  }

  /* Fade + slide a pinned set out, then hide and unpin it. */
  function playSetOut(els) {
    els.forEach(function (el) {
      if (!el) { return; }
      el.style.transition = 'opacity ' + GROUP_FADE_MS + 'ms ease, transform ' +
        GROUP_FADE_MS + 'ms ease';
      void el.offsetWidth;
      el.style.opacity = '0';
      el.style.transform = 'translateY(' + GROUP_SHIFT + 'px)';
    });
    window.clearTimeout(groupTimer);
    groupTimer = window.setTimeout(function () {
      els.forEach(function (el) { hideEl(el); unpin(el); });
    }, GROUP_FADE_MS + 40);
  }

  /* Reveal a set from a slid/faded state to rest (in flow). Measure any FLIP Last
     rects BEFORE calling this: the from-state applies a translateY that would
     otherwise offset the measurement. */
  function fadeSetIn(els) {
    els.forEach(function (el) {
      if (!el) { return; }
      showEl(el);
      el.style.transition = 'none';
      el.style.opacity = '0';
      el.style.transform = 'translateY(' + GROUP_SHIFT + 'px)';
    });
    if (els[0]) { void els[0].offsetWidth; }
    els.forEach(function (el) {
      if (!el) { return; }
      el.style.transition = 'opacity ' + GROUP_FADE_MS + 'ms ease, transform ' +
        GROUP_FADE_MS + 'ms ease';
      el.style.opacity = '1';
      el.style.transform = 'translateY(0)';
    });
    window.setTimeout(function () { els.forEach(clearFx); }, GROUP_FADE_MS + 40);
  }

  /* Fly a text clone from a First rect to a Last rect, scaling by width so it
     resolves to the destination type. The clone is a fixed overlay (no layout
     effect) borrowing the destination class for its type; it is removed on finish
     (and the real destination is revealed by onDone). fadeOutEnd dissolves the
     clone into an already-visible destination (used on exit, where the rows are
     shown). Never called under reduced motion. */
  function flyText(text, cls, first, last, opts) {
    opts = opts || {};
    if (!first || !last) { if (opts.onDone) { opts.onDone(); } return null; }
    const clone = document.createElement('span');
    clone.className = cls + ' flip-clone';
    clone.setAttribute('aria-hidden', 'true');
    clone.textContent = text;
    clone.style.left = last.left + 'px';
    clone.style.top = last.top + 'px';
    if (opts.wrap) {
      clone.style.width = last.width + 'px';
      clone.style.whiteSpace = 'normal';
    }
    clone.style.willChange = 'transform, opacity';
    document.body.appendChild(clone);

    const dx = first.left - last.left;
    const dy = first.top - last.top;
    const scale = (first.width && last.width) ? (first.width / last.width) : 1;
    const startT = 'translate(' + dx + 'px,' + dy + 'px) scale(' + scale + ')';
    const endT = 'translate(0px,0px) scale(1)';
    const frames = opts.fadeOutEnd
      ? [{ transform: startT, opacity: 1 },
         { transform: endT, opacity: 1, offset: 0.7 },
         { transform: endT, opacity: 0 }]
      : [{ transform: startT }, { transform: endT }];
    const anim = clone.animate(frames, {
      duration: FLIP_MS, easing: FLIP_EASE, fill: 'both'
    });
    let settled = false;
    function done() {
      if (settled) { return; }
      settled = true;
      if (clone.parentNode) { clone.remove(); }
      if (opts.onDone) { opts.onDone(); }
    }
    anim.onfinish = done;
    anim.oncancel = done;
    /* Belt and braces: if the finish/cancel event is ever missed (e.g. the clone
       is detached out from under the animation), reveal the target and drop the
       clone anyway. Idempotent via the settled guard. */
    window.setTimeout(done, FLIP_MS + 80);
    return anim;
  }

  /* Move a persisting element from its First to Last position (transform-only,
     no clone). Used for the third chip when the two swapping chips reorder it. */
  function flipMove(el, first, last) {
    if (!el || !first || !last) { return; }
    const dx = first.left - last.left;
    const dy = first.top - last.top;
    if (Math.abs(dx) < 0.5 && Math.abs(dy) < 0.5) { return; }
    el.animate([
      { transform: 'translate(' + dx + 'px,' + dy + 'px)' },
      { transform: 'translate(0px,0px)' }
    ], { duration: FLIP_MS, easing: FLIP_EASE });
  }

  /* Stagger the section cards in: opacity + 6px translateY, 60ms steps, the same
     rhythm as the load-in blocks. Skipped under reduced motion (cards just show).
     will-change is set for the move and cleared afterwards. */
  function staggerCards() {
    if (prefersReducedMotion()) { return; }
    const cards = Array.prototype.slice.call(
      panelBody.querySelectorAll('.section-card'));
    if (!cards.length) { return; }
    cards.forEach(function (c) {
      c.style.transition = 'none';
      c.style.opacity = '0';
      c.style.transform = 'translateY(6px)';
      c.style.willChange = 'opacity, transform';
    });
    void panelBody.offsetWidth;
    cards.forEach(function (c, i) {
      const delay = i * CARD_STAGGER_MS;
      c.style.transition = 'opacity ' + CARD_FADE_MS + 'ms ease ' + delay +
        'ms, transform ' + CARD_FADE_MS + 'ms ease ' + delay + 'ms';
      c.style.opacity = '1';
      c.style.transform = 'translateY(0)';
    });
    const total = (cards.length - 1) * CARD_STAGGER_MS + CARD_FADE_MS + 60;
    window.setTimeout(function () {
      cards.forEach(function (c) {
        c.style.transition = '';
        c.style.opacity = '';
        c.style.transform = '';
        c.style.willChange = '';
      });
    }, total);
  }

  function focusAfterFlip(el) {
    if (!el) { return; }
    if (prefersReducedMotion()) {
      el.focus();
    } else {
      window.setTimeout(function () {
        if (el && el.isConnected) { el.focus(); }
      }, FLIP_MS);
    }
  }

  /* ---- enter / exit / switch (round 7 FLIP choreography) ---------------- */

  /* Enter the detail state from a project row (index visible). The clicked name
     travels into the title; the two sibling rows travel into their chips; the
     non-project rows, INDEX label, HOW IT WORKS and proof strip slide down and
     fade as a group; the section cards stagger in. */
  function enterDetail(row, key) {
    const others = PROJECT_KEYS.filter(function (k) { return k !== key; });
    detailOriginRow = row;
    detailKey = key;

    if (prefersReducedMotion()) {
      fillDetailCopy(key);
      renderChips(key);
      moveCtaToConversion();
      page.classList.add('is-detail');
      leavingEls.forEach(function (el) { hideEl(el); clearFx(el); });
      enteringEls.forEach(function (el) { showEl(el); clearFx(el); });
      inDetail = true;
      pushDetailHistory();
      setPressed(key);
      commit(key, 'Preview / ' + PROJECT_NAMES[key]);
      currentView = key;
      if (detailBack) { detailBack.focus(); }
      return;
    }

    const pageRect = page.getBoundingClientRect();
    const titleFirst = rowNameEl(key).getBoundingClientRect();
    const chipFirst = others.map(function (k) {
      return rowNameEl(k).getBoundingClientRect();
    });

    /* Pin the outgoing group out of flow so the column reflows to the final
       detail layout (needed to measure the Last rects), while the group stays
       visible where it was to fade out. */
    leavingEls.forEach(function (el) { pinAbsolute(el, pageRect); });

    fillDetailCopy(key);
    renderChips(key);
    moveCtaToConversion();
    page.classList.add('is-detail');
    enteringEls.forEach(showEl);
    inDetail = true;
    pushDetailHistory();
    setPressed(key);
    /* panel stack, no fade; defer the section-video decode past the FLIP travel */
    commit(key, 'Preview / ' + PROJECT_NAMES[key], SECTION_START_DELAY);
    currentView = key;

    /* Last rects, measured with the entering set at its resting transform. */
    const titleEl = detailTitleEl();
    const titleLast = titleEl ? titleEl.getBoundingClientRect() : null;
    const chipEls = others.map(function (k) { return chipByKey(k); });
    const chipLast = chipEls.map(function (c) {
      return c ? c.getBoundingClientRect() : null;
    });

    /* Hide the real targets until their clones land. */
    if (titleEl) { titleEl.style.opacity = '0'; }
    chipEls.forEach(function (c) { if (c) { c.style.opacity = '0'; } });

    playSetOut(leavingEls);      /* outgoing group fades + slides out */
    fadeSetIn(enteringEls);      /* detail + conversion fade + slide in */

    flyText(PROJECT_NAMES[key], 'detail-title', titleFirst, titleLast, {
      wrap: true,
      onDone: function () { if (titleEl) { titleEl.style.opacity = ''; } }
    });
    others.forEach(function (k, i) {
      const c = chipEls[i];
      flyText(PROJECT_NAMES[k], 'chip', chipFirst[i], chipLast[i], {
        onDone: function () { if (c) { c.style.opacity = ''; } }
      });
    });

    staggerCards();
    focusAfterFlip(detailBack);
  }

  /* Switch project in place (a chip click). The clicked chip travels up into the
     title while the current title travels down into the vacated chip slot; the
     panel cards crossfade via the existing swap. */
  function switchProject(newKey) {
    if (!inDetail || newKey === detailKey) { return; }
    const oldKey = detailKey;
    const thirdKey = PROJECT_KEYS.filter(function (k) {
      return k !== oldKey && k !== newKey;
    })[0];

    if (prefersReducedMotion()) {
      detailKey = newKey;
      detailOriginRow = rowByKey[newKey];
      fillDetailCopy(newKey);
      renderChips(newKey);
      setPressed(newKey);
      commit(newKey, 'Preview / ' + PROJECT_NAMES[newKey]);
      currentView = newKey;
      if (detailBack) { detailBack.focus(); }
      return;
    }

    /* First rects (before the mutation). */
    const clickedChip = chipByKey(newKey);
    const chipFirst = clickedChip ? clickedChip.getBoundingClientRect() : null;
    const titleElOld = detailTitleEl();
    const titleFirst = titleElOld ? titleElOld.getBoundingClientRect() : null;
    const thirdChipOld = thirdKey ? chipByKey(thirdKey) : null;
    const thirdFirst = thirdChipOld ? thirdChipOld.getBoundingClientRect() : null;

    detailKey = newKey;
    detailOriginRow = rowByKey[newKey];
    fillDetailCopy(newKey);
    renderChips(newKey);          /* chips now show oldKey + thirdKey */
    setPressed(newKey);
    /* panel crossfade; defer the video decode to FLIP_MS+40 from this click. swap
       commits at SWAP_HALF, so pass the delay measured from that midpoint. */
    swap(newKey, 'Preview / ' + PROJECT_NAMES[newKey], SECTION_START_DELAY - SWAP_HALF);
    currentView = newKey;

    /* Crossfade the supporting copy (sub, blurb, See it live); the title inside
       it stays hidden for its clone. */
    if (detailCopySlot) {
      detailCopySlot.style.transition = 'none';
      detailCopySlot.style.opacity = '0';
      void detailCopySlot.offsetWidth;
      detailCopySlot.style.transition = 'opacity ' + GROUP_FADE_MS + 'ms ease';
      detailCopySlot.style.opacity = '1';
      window.setTimeout(function () {
        detailCopySlot.style.transition = '';
        detailCopySlot.style.opacity = '';
      }, GROUP_FADE_MS + 40);
    }

    /* Last rects (new elements). */
    const titleElNew = detailTitleEl();
    const titleLast = titleElNew ? titleElNew.getBoundingClientRect() : null;
    const oldChipNew = chipByKey(oldKey);
    const oldChipLast = oldChipNew ? oldChipNew.getBoundingClientRect() : null;
    const thirdChipNew = thirdKey ? chipByKey(thirdKey) : null;
    const thirdLast = thirdChipNew ? thirdChipNew.getBoundingClientRect() : null;

    if (titleElNew) { titleElNew.style.opacity = '0'; }
    if (oldChipNew) { oldChipNew.style.opacity = '0'; }

    flyText(PROJECT_NAMES[newKey], 'detail-title', chipFirst, titleLast, {
      wrap: true,
      onDone: function () { if (titleElNew) { titleElNew.style.opacity = ''; } }
    });
    flyText(PROJECT_NAMES[oldKey], 'chip', titleFirst, oldChipLast, {
      onDone: function () { if (oldChipNew) { oldChipNew.style.opacity = ''; } }
    });
    if (thirdChipNew) { flipMove(thirdChipNew, thirdFirst, thirdLast); }

    /* Keep focus in the chips row: land on the previously-open project's chip. */
    focusAfterFlip(chipByKey(oldKey));
  }

  /* Exit the detail state back to the welcome (back / Escape / browser back). The
     title travels back into its row, the chips grow back into their rows, the
     hidden group fades/slides back in, and the panel cards fade out first. */
  function exitDetail() {
    if (!inDetail) { return; }
    const origin = detailOriginRow;
    const key = detailKey;
    const others = PROJECT_KEYS.filter(function (k) { return k !== key; });

    if (prefersReducedMotion()) {
      moveCtaToIndex();
      page.classList.remove('is-detail');
      enteringEls.forEach(function (el) { hideEl(el); clearFx(el); });
      leavingEls.forEach(function (el) { showEl(el); clearFx(el); });
      clearAllSelection();
      inDetail = false;
      detailKey = null;
      detailPushed = false;
      swap('welcome', 'Preview / No selection');
      currentView = null;
      if (origin) { origin.focus(); }
      return;
    }

    const pageRect = page.getBoundingClientRect();
    const titleEl = detailTitleEl();
    const titleFirst = titleEl ? titleEl.getBoundingClientRect() : null;
    const chipFirst = others.map(function (k) {
      const c = chipByKey(k);
      return c ? c.getBoundingClientRect() : null;
    });

    moveCtaToIndex();                       /* CTA rejoins the index, fades in */
    enteringEls.forEach(function (el) { pinAbsolute(el, pageRect); });
    page.classList.remove('is-detail');
    leavingEls.forEach(showEl);
    clearAllSelection();

    const titleLast = rowNameEl(key) ? rowNameEl(key).getBoundingClientRect() : null;
    const chipLast = others.map(function (k) {
      const n = rowNameEl(k);
      return n ? n.getBoundingClientRect() : null;
    });

    playSetOut(enteringEls);                /* detail + conversion fade out */
    fadeSetIn(leavingEls);                  /* index / how / proof fade in */

    /* Clones dissolve into the rows (which are already fading in). */
    flyText(PROJECT_NAMES[key], 'detail-title', titleFirst, titleLast, {
      wrap: true, fadeOutEnd: true
    });
    others.forEach(function (k, i) {
      flyText(PROJECT_NAMES[k], 'chip', chipFirst[i], chipLast[i], {
        fadeOutEnd: true
      });
    });

    inDetail = false;
    detailKey = null;
    detailPushed = false;
    swap('welcome', 'Preview / No selection');   /* cards fade out, welcome in */
    currentView = null;
    focusAfterFlip(origin);
  }

  /* Leave the detail state onto a normal view (Pricing via the conversion line,
     or the form via the relocated CTA). A quiet group crossfade (no title/chip
     FLIP, since we are moving to a different view, not back to the index). */
  function exitDetailToView() {
    moveCtaToIndex();
    if (prefersReducedMotion()) {
      page.classList.remove('is-detail');
      enteringEls.forEach(function (el) { hideEl(el); clearFx(el); });
      leavingEls.forEach(function (el) { showEl(el); clearFx(el); });
    } else {
      const pageRect = page.getBoundingClientRect();
      enteringEls.forEach(function (el) { pinAbsolute(el, pageRect); });
      page.classList.remove('is-detail');
      playSetOut(enteringEls);
      fadeSetIn(leavingEls);
    }
    inDetail = false;
    detailKey = null;
    consumeDetailHistory();
  }

  /* Rows 04 About, 05 Pricing, 06 CTA: the normal index model. If the detail
     state is open, exit it onto the chosen view first. */
  function selectNormal(row, key) {
    const cameFromDetail = inDetail;
    if (!cameFromDetail && key === currentView) {
      return;   /* no-op re-select of the shown view */
    }
    if (cameFromDetail) {
      exitDetailToView();
    }

    indexRows.forEach(function (r) {
      const active = (r === row);
      r.classList.toggle('is-active', active);
      r.setAttribute('aria-pressed', active ? 'true' : 'false');
    });
    if (ctaRow) {
      const ctaSelected = (key === 'form');
      ctaRow.classList.toggle('is-open', ctaSelected);
      ctaRow.setAttribute('aria-pressed', ctaSelected ? 'true' : 'false');
    }

    swap(key, 'Preview / ' + nameOf(row));
    currentView = key;
  }

  function select(row) {
    const key = row.dataset.view;
    if (!key) { return; }
    if (PROJECT_KEYS.indexOf(key) !== -1) {
      if (inDetail) { switchProject(key); }
      else { enterDetail(row, key); }
    } else {
      selectNormal(row, key);
    }
  }

  function selectByKey(key) {
    const row = rowByKey[key];
    if (row) { select(row); }
  }

  /* The back control and Escape route through the history entry when one was
     pushed, so browser back, the button and the key all land in the same place. */
  function closeDetail() {
    if (!inDetail) { return; }
    if (detailPushed) {
      history.back();   /* triggers popstate -> exitDetail */
    } else {
      exitDetail();
    }
  }

  rows.forEach(function (row) {
    row.addEventListener('click', function () {
      select(row);
    });
  });

  if (detailChipsSlot) {
    /* Delegated so freshly rendered chips are always wired. */
    detailChipsSlot.addEventListener('click', function (event) {
      const chip = event.target.closest('[data-chip-key]');
      if (chip && inDetail) {
        switchProject(chip.dataset.chipKey);
      }
    });
  }

  if (conversionPrice) {
    conversionPrice.addEventListener('click', function () {
      selectByKey('pricing');
    });
  }

  if (detailBack) {
    detailBack.addEventListener('click', closeDetail);
  }

  document.addEventListener('keydown', function (event) {
    if (event.key === 'Escape' && inDetail) {
      closeDetail();
    }
  });

  window.addEventListener('popstate', function () {
    if (inDetail) {
      detailPushed = false;   /* the entry has already been popped */
      exitDetail();
    }
  });
}

/* --------------------------------------------------------------------------
   Contact form (CONCEPT.md section 7, 3.4 F1 to F6)

   Progressive enhancement over the plain HTML POST form: intercept submit,
   send via fetch with Accept: application/json, and show an inline success or
   failure state inside the card (never a redirect to Formspree). The states
   overlay the fields so the card keeps its dimensions.

   - Honeypot (_gotcha): if filled, silently pretend success without sending.
   - Validation: native `required` blocks empty fields (browser bubble + focus,
     no custom error UI); a JS trim rejects whitespace-only via the same native
     mechanism. No email field exists by design.
   - In flight: the submit button is disabled (double-send guard) and its label
     changes to a static "Sending"; restored on failure.
   - Success clears the fields; failure leaves the typed message intact so it
     can be copied. The failure message offers the visible email as a mailto
     fallback and a quiet "Try again" that returns to the intact form.
   - The outcome is announced via a role=status region inside the card, which
     also takes focus (tabindex -1) so a keyboard user is not stranded.

   The form is cloned fresh each time its view is shown, so state never leaks
   between visits; the listeners are delegated on the persistent panel body.
   -------------------------------------------------------------------------- */

const FORM_SUCCESS_MSG = 'Sent. I will reply the same working day.';

function restoreSubmit(submit) {
  if (!submit) {
    return;
  }
  submit.disabled = false;
  if (submit.dataset.label) {
    submit.textContent = submit.dataset.label;
    delete submit.dataset.label;
  }
}

/* Reveal the success or failure overlay, cover the fields from AT/keyboard,
   and move focus to the message. */
function showFormStatus(form, kind) {
  const statusEl = form.querySelector('[data-form-status]');
  const fields = form.querySelector('[data-form-fields]');
  if (!statusEl) {
    return;
  }

  statusEl.textContent = '';

  const msg = document.createElement('p');
  msg.className = 'form-status-msg';

  if (kind === 'success') {
    msg.textContent = FORM_SUCCESS_MSG;
    statusEl.appendChild(msg);
  } else {
    /* "Something broke. Email me directly at <address>." (address = mailto). */
    msg.append('Something broke. Email me directly at ');
    const link = document.createElement('a');
    link.href = 'mailto:' + SITE_EMAIL;
    link.textContent = SITE_EMAIL;
    msg.appendChild(link);
    msg.append('.');
    statusEl.appendChild(msg);

    const retry = document.createElement('button');
    retry.type = 'button';
    retry.className = 'form-retry';
    retry.setAttribute('data-form-retry', '');
    retry.textContent = 'Try again';
    statusEl.appendChild(retry);
  }

  /* Cover the fields so the covered controls are not reachable behind it. */
  if (fields) {
    fields.inert = true;
  }
  statusEl.classList.add('is-shown');
  statusEl.focus();
}

/* Hide the overlay and return to the intact form (failure "Try again"). */
function hideFormStatus(form) {
  const statusEl = form.querySelector('[data-form-status]');
  const fields = form.querySelector('[data-form-fields]');
  if (statusEl) {
    statusEl.classList.remove('is-shown');
    statusEl.textContent = '';
  }
  if (fields) {
    fields.inert = false;
  }
  const firstField = form.querySelector('.field');
  if (firstField) {
    firstField.focus();
  }
}

function handleContactSubmit(form) {
  const submit = form.querySelector('.submit');

  /* Double-send guard: ignore re-entrant submits while a request is in flight. */
  if (submit && submit.disabled) {
    return;
  }

  /* Honeypot: a real user cannot reach this field. If it is filled, silently
     pretend success without sending. */
  const honeypot = form.querySelector('input[name="_gotcha"]');
  if (honeypot && honeypot.value.trim() !== '') {
    form.reset();
    showFormStatus(form, 'success');
    return;
  }

  /* Non-empty after trim: trim in place, then let the native mechanism report
     any now-empty required field (browser bubble + focus ring, no custom UI). */
  const fields = form.querySelectorAll('.field');
  fields.forEach(function (field) {
    field.value = field.value.trim();
  });
  if (!form.checkValidity()) {
    form.reportValidity();
    return;
  }

  /* Formspree short-circuit (decision 6). While the endpoint is still the
     placeholder there is no real inbox, so do NOT hit the network: go straight
     to the existing inline failure state, which points the visitor at the email.
     When a real form ID replaces REPLACE_FORM_ID the constant no longer matches
     and this block is skipped, so the normal fetch path resumes with no further
     edit. Validation, honeypot and the double-submit guard above all still run. */
  if (FORMSPREE_ENDPOINT.indexOf('REPLACE_FORM_ID') !== -1) {
    showFormStatus(form, 'fail');
    return;
  }

  /* In flight: disable the submit and switch to a static "Sending" label. */
  if (submit) {
    submit.dataset.label = submit.textContent;
    submit.textContent = 'Sending';
    submit.disabled = true;
  }

  fetch(form.action, {
    method: 'POST',
    body: new FormData(form),
    headers: { 'Accept': 'application/json' }
  }).then(function (response) {
    if (response.ok) {
      form.reset();                       /* clearing on success is fine */
      showFormStatus(form, 'success');
    } else {
      restoreSubmit(submit);              /* non-2xx: restore and show failure */
      showFormStatus(form, 'fail');
    }
  }).catch(function () {
    restoreSubmit(submit);                /* network error */
    showFormStatus(form, 'fail');
  });
}

function initContactForm() {
  const panelBody = document.querySelector('.panel-body');
  if (!panelBody) {
    return;
  }

  /* Delegated on the persistent panel body so freshly cloned forms are wired. */
  panelBody.addEventListener('submit', function (event) {
    const form = event.target.closest('[data-contact-form]');
    if (!form) {
      return;
    }
    event.preventDefault();   /* never redirect to Formspree while JS is active */
    handleContactSubmit(form);
  });

  panelBody.addEventListener('click', function (event) {
    const retry = event.target.closest('[data-form-retry]');
    if (!retry) {
      return;
    }
    const form = retry.closest('[data-contact-form]');
    if (form) {
      hideFormStatus(form);
    }
  });
}

/* --------------------------------------------------------------------------
   Row pointer trails (CONCEPT.md 3.3 "Row pointer trail")
   On pointermove over an index row, spawn at most every 100ms a 12px blurred
   dot at the cursor. Opacity: 0 to 0.32 in 300ms (20ms delay), hold, then
   0.32 to 0 over 1200ms starting at 1000ms; the node is removed at 2200ms.
   Not bound under reduced motion; each move ignored when pointerType is touch.
   -------------------------------------------------------------------------- */

const TRAIL_SPAWN_INTERVAL = 100;
const TRAIL_LIFETIME = 2200;

function initRowTrails() {
  if (prefersReducedMotion()) {
    return;   /* not spawned under reduced motion: no listener bound */
  }
  if (isTouchDevice()) {
    return;   /* real touch device (section 8): no trails, no listener bound */
  }

  const rows = document.querySelectorAll('.row:not(.row--cta)');
  if (!rows.length) {
    return;
  }

  const rootStyles = getComputedStyle(document.documentElement);
  const trailA = rootStyles.getPropertyValue('--trail-a').trim();
  const trailB = rootStyles.getPropertyValue('--trail-b').trim();
  const peak = parseFloat(rootStyles.getPropertyValue('--trail-opacity')) || 0.32;

  let lastSpawn = 0;
  let useA = true;

  function spawn(x, y) {
    const dot = document.createElement('div');
    dot.className = 'trail-dot';
    dot.style.background = useA ? trailA : trailB;
    useA = !useA;
    dot.style.transform = 'translate(' + x + 'px, ' + y + 'px) translate(-50%, -50%)';
    document.body.appendChild(dot);

    /* Opacity timeline over the full 2200ms lifetime (offsets are ms/2200):
       0ms 0, 20ms 0 (delay), 320ms peak, 1000ms peak, 2200ms 0. */
    const anim = dot.animate([
      { opacity: 0, offset: 0 },
      { opacity: 0, offset: 20 / TRAIL_LIFETIME },
      { opacity: peak, offset: 320 / TRAIL_LIFETIME },
      { opacity: peak, offset: 1000 / TRAIL_LIFETIME },
      { opacity: 0, offset: 1 }
    ], { duration: TRAIL_LIFETIME, easing: 'ease', fill: 'forwards' });

    anim.onfinish = function () {
      dot.remove();
    };
  }

  function onPointerMove(event) {
    if (event.pointerType === 'touch') {
      return;   /* skipped when pointerType is touch */
    }
    const now = performance.now();
    if (now - lastSpawn < TRAIL_SPAWN_INTERVAL) {
      return;   /* spawn at most every 100ms */
    }
    lastSpawn = now;
    spawn(event.clientX, event.clientY);
  }

  rows.forEach(function (row) {
    row.addEventListener('pointermove', onPointerMove);
  });
}

/* --------------------------------------------------------------------------
   CTA pill interactions (CONCEPT.md 3.4 C2 hover mist, C3 press bloom)
   Hover mist: a node following the cursor with 900ms lag (the lag lives in the
   CSS transition), opacity 0 to 0.5. Not rendered under reduced motion or when
   the pointer is touch. Press bloom: one node per press from the exact pointer
   or tap point, scale 0.25 to 1, opacity 0 to 0.5 to 0 over 600ms ease-out,
   removed at 700ms. The bloom fires on touch too; not spawned under reduced
   motion. No scale is ever applied to the pill itself.
   -------------------------------------------------------------------------- */

function initCta() {
  const cta = document.querySelector('.row--cta');
  if (!cta) {
    return;
  }

  /* Hover mist. Guarded off entirely under reduced motion and on real touch
     devices (section 8: no hover mist on touch). The per-event pointerType
     checks below stay for hybrid pointers. */
  if (!prefersReducedMotion() && !isTouchDevice()) {
    let mist = null;

    function ensureMist() {
      if (!mist) {
        mist = document.createElement('div');
        mist.className = 'cta-mist';
        cta.appendChild(mist);
      }
      return mist;
    }

    /* instant true: place without the 900ms lag (used on first appearance). */
    function moveMist(event, instant) {
      const rect = cta.getBoundingClientRect();
      const node = ensureMist();
      const transform =
        'translate(' + (event.clientX - rect.left) + 'px, ' +
        (event.clientY - rect.top) + 'px) translate(-50%, -50%)';
      if (instant) {
        node.style.transition = 'none';
        node.style.transform = transform;
        void node.offsetWidth;   /* flush so the next change transitions */
        node.style.transition = '';
      } else {
        node.style.transform = transform;
      }
    }

    cta.addEventListener('pointerenter', function (event) {
      if (event.pointerType === 'touch') {
        return;   /* mist not rendered on touch */
      }
      const node = ensureMist();
      /* Appear under the cursor, then fade in; lag only applies while moving. */
      moveMist(event, true);
      window.requestAnimationFrame(function () {
        node.style.opacity = '0.5';
      });
    });

    cta.addEventListener('pointermove', function (event) {
      if (event.pointerType === 'touch' || !mist) {
        return;
      }
      moveMist(event, false);
    });

    cta.addEventListener('pointerleave', function () {
      if (mist) {
        mist.style.opacity = '0';
      }
    });
  }

  /* Press bloom. Fires on touch too; not spawned under reduced motion. */
  cta.addEventListener('pointerdown', function (event) {
    if (prefersReducedMotion()) {
      return;
    }
    const rect = cta.getBoundingClientRect();
    const x = event.clientX - rect.left;
    const y = event.clientY - rect.top;
    const base = 'translate(' + x + 'px, ' + y + 'px) translate(-50%, -50%)';

    const bloom = document.createElement('div');
    bloom.className = 'cta-bloom';
    bloom.style.transform = base + ' scale(0.25)';   /* first-frame position */
    cta.appendChild(bloom);

    bloom.animate([
      { transform: base + ' scale(0.25)', opacity: 0 },
      { transform: base + ' scale(0.625)', opacity: 0.5, offset: 0.5 },
      { transform: base + ' scale(1)', opacity: 0 }
    ], { duration: 600, easing: 'ease-out', fill: 'forwards' });

    window.setTimeout(function () {
      bloom.remove();
    }, 700);
  });
}

/* -------------------------------------------------------------------------- */

function init() {
  wireFooter();
  initTheme();
  initDotGrid();
  initDecode();
  initFadeIn();
  initPanel();
  initContactForm();
  initRowTrails();
  initCta();
}

if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', init);
} else {
  init();
}
