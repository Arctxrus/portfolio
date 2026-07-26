/* ==========================================================================
   Zayn portfolio - main.js
   Stage 1: single email constant, footer wiring, dot grid canvas.
   Stage 2: decode/scramble, block fade-in, row selection (R1 to R4),
            row pointer trails, CTA hover mist and press bloom.
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

/* --------------------------------------------------------------------------
   Contact email - defined exactly once so it can be swapped in one edit.
   Placeholder until the real address is supplied (see PROGRESS.md).
   -------------------------------------------------------------------------- */

const SITE_EMAIL = 'hello@placeholder.invalid';

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
   Row selection (CONCEPT.md 3.4 R3 active). One active index row at a time.
   Real buttons, so enter/space fire click natively; focus-visible ring is
   already styled in CSS. The panel does not change yet (that is stage 3);
   only the active-class and aria-pressed logic is wired here.
   -------------------------------------------------------------------------- */

function initRowSelection() {
  const rows = document.querySelectorAll('.row:not(.row--cta)');
  rows.forEach(function (row) {
    row.setAttribute('aria-pressed', 'false');
    row.addEventListener('click', function () {
      rows.forEach(function (other) {
        const isThis = other === row;
        other.classList.toggle('is-active', isThis);
        other.setAttribute('aria-pressed', isThis ? 'true' : 'false');
      });
    });
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

  /* Hover mist. Guarded off entirely under reduced motion. */
  if (!prefersReducedMotion()) {
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
  initRowSelection();
  initRowTrails();
  initCta();
}

if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', init);
} else {
  init();
}
