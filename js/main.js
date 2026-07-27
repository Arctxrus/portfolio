/* ==========================================================================
   Zayn portfolio - main.js
   Stage 1: single email constant, footer wiring, dot grid canvas.
   Stage 2: decode/scramble, block fade-in, row selection (R1 to R4),
            row pointer trails, CTA hover mist and press bloom.
   Stage 3: panel controller (row/CTA to view swap, V5 animation, active-state
            sync, aria-live announcement, contact-form submit stub).
   Stage 4: contact form wiring (Formspree fetch, success/failure states,
            honeypot, native + trim validation, in-flight guard, aria).
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
  const rest = parseColour(rootStyles.getPropertyValue('--dot-rest').trim());
  const warm = parseColour(rootStyles.getPropertyValue('--dot-warm').trim());
  const restAlpha = rest.a;

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

/* Client feedback round 3 (item 2): desktop project previews are scroll-scrubbed.
   The view's scroll progress drives video.currentTime with a small rAF lerp so
   the scrub feels smooth (about 18% of the remaining gap closed per frame, inside
   the briefed 15 to 20%). Under reduced motion the currentTime snaps to the
   scroll target with no rAF (scrubbing is user-driven and allowed, but no
   autonomous smoothing animation runs). Mobile (below 900px) keeps the muted
   autoplay loop. Attributes are managed in JS per breakpoint on the same cloned
   <video> element (see configureProjectVideo in initPanel). */
const SCRUB_LERP = 0.18;

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
  const headerLabel = document.querySelector('.panel-head-label');
  const liveRegion = document.querySelector('[data-panel-live]');
  const rows = Array.prototype.slice.call(document.querySelectorAll('.row'));
  const indexRows = rows.filter(function (row) {
    return !row.classList.contains('row--cta');
  });
  const ctaRow = rows.filter(function (row) {
    return row.classList.contains('row--cta');
  })[0] || null;

  if (!panelBody || !rows.length) {
    return;
  }

  /* Client feedback round 2 (item 1): the CTA now carries aria-pressed too, so
     the six rows form one single-selection group with exactly one pressed at a
     time. It starts unpressed like the index rows. */
  indexRows.forEach(function (row) {
    row.setAttribute('aria-pressed', 'false');
  });
  if (ctaRow) {
    ctaRow.setAttribute('aria-pressed', 'false');
  }

  let currentView = null;   /* V1 welcome is showing; no view key yet. */
  let swapTimer = 0;
  let currentScrub = null;  /* teardown handle for the shown desktop scrub */

  /* Tear down any active scroll-scrub (its scroll listener, rAF and metadata
     handler) before the view is replaced or reconfigured. */
  function stopScrub() {
    if (currentScrub) {
      currentScrub.cancel();
      currentScrub = null;
    }
  }

  /* Client feedback round 3 (item 2). Per-breakpoint video behaviour, managed in
     JS on the same cloned <video> element (two code paths, one element):
     - Mobile (below 900px, no internal scroll): muted autoplay loop, unchanged.
     - Desktop: no autonomous playback. Strip autoplay/loop, preload the frames
       for smooth seeking, and drive currentTime from the view's scroll position.
       progress = scrollTop / (scrollHeight - clientHeight) maps to the duration.
       Normal motion eases currentTime toward that target via a rAF lerp; reduced
       motion snaps it (no rAF). The poster (frame 0) shows until the first scroll.
     The view is re-configured if the breakpoint changes while it is open. */
  function configureProjectVideo(view) {
    const video = view.querySelector('.preview-video');
    if (!video) {
      return;
    }

    if (mobileLayoutQuery.matches) {
      /* Mobile: restore the muted autoplay loop on this element. */
      video.autoplay = true;
      video.loop = true;
      video.muted = true;
      video.setAttribute('autoplay', '');
      video.setAttribute('loop', '');
      const play = video.play();
      if (play && play.catch) {
        play.catch(function () {});
      }
      return;
    }

    /* Desktop: scroll-scrub. No autoplay, no loop, load frames for seeking. */
    video.autoplay = false;
    video.loop = false;
    video.removeAttribute('autoplay');
    video.removeAttribute('loop');
    video.muted = true;
    video.preload = 'auto';
    video.pause();

    const reduced = prefersReducedMotion();
    let target = 0;
    let cur = 0;
    let rafId = 0;
    let looping = false;

    function apply() {
      const d = video.duration;
      if (!isFinite(d) || d <= 0) {
        looping = false;
        return;
      }
      const diff = target - cur;
      if (Math.abs(diff) < 0.01) {
        cur = target;
        try { video.currentTime = cur; } catch (e) { /* not seekable yet */ }
        looping = false;
        return;
      }
      cur += diff * SCRUB_LERP;
      try { video.currentTime = cur; } catch (e) { /* not seekable yet */ }
      rafId = window.requestAnimationFrame(apply);
    }

    function onScroll() {
      const denom = view.scrollHeight - view.clientHeight;
      const progress = denom > 0 ? view.scrollTop / denom : 0;
      const d = video.duration;
      if (!isFinite(d) || d <= 0) {
        return;   /* metadata not ready: poster stays until it can seek */
      }
      target = Math.max(0, Math.min(1, progress)) * d;
      if (reduced) {
        cur = target;
        try { video.currentTime = target; } catch (e) { /* not seekable yet */ }
        return;   /* snap, no rAF: no autonomous motion under reduced motion */
      }
      if (!looping) {
        looping = true;
        rafId = window.requestAnimationFrame(apply);
      }
    }

    view.addEventListener('scroll', onScroll, { passive: true });
    /* If the user scrolled before metadata arrived, catch up once it is ready. */
    video.addEventListener('loadedmetadata', onScroll);

    currentScrub = {
      cancel: function () {
        view.removeEventListener('scroll', onScroll);
        video.removeEventListener('loadedmetadata', onScroll);
        if (rafId) {
          window.cancelAnimationFrame(rafId);
        }
        looping = false;
      }
    };
  }

  function renderView(viewKey) {
    const tpl = document.getElementById('view-' + viewKey);
    if (!tpl) {
      return;
    }
    stopScrub();   /* remove the previous view's scrub before it is detached */
    panelBody.replaceChildren(tpl.content.cloneNode(true));

    /* Inject the Formspree endpoint into the freshly cloned form (single
       source of truth; also the plain POST target if fetch is unavailable). */
    if (viewKey === 'form') {
      const form = panelBody.querySelector('[data-contact-form]');
      if (form) {
        form.action = FORMSPREE_ENDPOINT;
      }
    }

    /* Project views (V2) carry the scroll-scrub / autoplay video (item 2). */
    const projView = panelBody.querySelector('.view--project');
    if (projView) {
      configureProjectVideo(projView);
    }
  }

  function announce(text) {
    if (liveRegion) {
      liveRegion.textContent = text;
    }
  }

  function commit(viewKey, headerText) {
    renderView(viewKey);
    if (headerLabel) {
      headerLabel.textContent = headerText;
    }
    announce(headerText);
    /* Scroll after the content is in the DOM so the geometry is measured
       post-swap. commit() runs synchronously on the reduced-motion path and at
       the swap midpoint on the animated path, so calling from here covers both;
       calling from select() measured the stale pre-swap box (the animated swap
       only schedules the content change 130ms later). */
    scrollPanelIntoView();
  }

  function swap(viewKey, headerText) {
    if (prefersReducedMotion()) {
      commit(viewKey, headerText);   /* instant, content still swaps */
      return;
    }
    window.clearTimeout(swapTimer);
    panelBody.classList.add('is-swapping');   /* out: opacity 0, translateY 6px */
    swapTimer = window.setTimeout(function () {
      commit(viewKey, headerText);             /* switch at the midpoint */
      /* Flush the opacity 0 state with the new content, then drop the class so
         the body eases back in (130ms). A layout read is used rather than rAF
         so the fade-in is not left stuck when the tab is backgrounded. */
      void panelBody.offsetWidth;
      panelBody.classList.remove('is-swapping');
    }, SWAP_HALF);
  }

  /* Bring the panel into view on selection. Mobile only: on desktop (>900px) the
     panel sits beside the index and must never scroll, so the whole function is
     guarded on the mobile-layout media query rather than relying on geometry.
     The top edge is tested against a fixed px band (see PANEL_TOP_MIN /
     PANEL_TOP_BAND); if the header is already near the viewport top no re-scroll
     happens. Reduced motion: an instant jump (no smooth behaviour). */
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

  function select(row) {
    const viewKey = row.dataset.view;
    if (!viewKey || viewKey === currentView) {
      return;   /* judgement call: do not replay the swap for the active view */
    }

    /* Active state (R3). CTA is never active; selecting it clears every row. */
    indexRows.forEach(function (r) {
      const active = (r === row);
      r.classList.toggle('is-active', active);
      r.setAttribute('aria-pressed', active ? 'true' : 'false');
    });

    /* CTA grow-and-push (item 1). The CTA is not an index row, so the loop above
       already clears every index row when the CTA is chosen. The CTA carries a
       parallel `is-open` class (grow only, NO colour/selection styling; see the
       .row--cta.is-open CSS rule) plus aria-pressed, kept in sync so exactly one
       of the six rows is pressed at a time. Selecting any index row sets
       is-open false and aria-pressed false, so the CTA clears the moment another
       view opens (per the brief). */
    if (ctaRow) {
      const ctaSelected = (row === ctaRow);
      ctaRow.classList.toggle('is-open', ctaSelected);
      ctaRow.setAttribute('aria-pressed', ctaSelected ? 'true' : 'false');
    }

    const nameEl = row.querySelector('.row-name');
    const name = nameEl ? nameEl.textContent : '';
    const headerText = 'Preview / ' + name;

    swap(viewKey, headerText);
    currentView = viewKey;
  }

  rows.forEach(function (row) {
    row.addEventListener('click', function () {
      select(row);
    });
  });

  /* Client feedback round 3 (item 2): if the viewport crosses the 900px
     breakpoint while a project view is open, re-configure the video for the new
     mode (desktop scrub <-> mobile autoplay). The view element is unchanged, so
     only its behaviour and attributes are re-derived. */
  mobileLayoutQuery.addEventListener('change', function () {
    const projView = panelBody.querySelector('.view--project');
    if (projView) {
      stopScrub();
      configureProjectVideo(projView);
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
