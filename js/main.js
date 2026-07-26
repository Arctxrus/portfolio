/* ==========================================================================
   Zayn portfolio - main.js
   Stage 1: single email constant, footer wiring, dot grid canvas.
   Vanilla JS only. UK English. No em dashes.
   ========================================================================== */

'use strict';

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

/* -------------------------------------------------------------------------- */

function init() {
  wireFooter();
  initDotGrid();
}

if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', init);
} else {
  init();
}
