/* Hero tiles: they light up under the cursor, fade back slowly, and ripple out from a click. */
(() => {
  'use strict';
  const SIZE = 58; // Tile plus gap, matching site.css.

  function tiles(box) {
    const hero = box.parentElement;
    let reduced = false;
    try { reduced = matchMedia('(prefers-reduced-motion: reduce)').matches; } catch { /* Full motion. */ }
    let cells = [], cols = 1, lit = [];
    const fill = () => {
      cols = Math.max(1, Math.floor((box.clientWidth - 6) / SIZE));
      const rows = Math.ceil(box.clientHeight / SIZE);
      if (cells.length !== cols * rows) {
        const frag = document.createDocumentFragment();
        cells = Array.from({ length: cols * rows }, () => frag.appendChild(document.createElement('i')));
        box.replaceChildren(frag);
      }
    };
    const at = (x, y) => {
      const r = box.getBoundingClientRect();
      return [Math.floor((x - r.left - 6) / ((r.width - 6) / cols)), Math.floor((y - r.top - 6) / SIZE)];
    };
    fill();

    let frame = 0, px = 0, py = 0, inside = false;
    const clear = () => { lit.forEach(c => c.classList.remove('lit', 'near')); lit = []; };
    const light = () => {
      frame = 0;
      clear();
      // A frame queued just before the pointer left must not relight a tile.
      if (!inside) return;
      const hr = hero.getBoundingClientRect();
      if (py < hr.top || py > hr.bottom) return;
      const [col, row] = at(px, py);
      for (let dy = -1; dy <= 1; dy++) for (let dx = -1; dx <= 1; dx++) {
        const c = col + dx;
        const cell = c >= 0 && c < cols ? cells[(row + dy) * cols + c] : null;
        if (!cell) continue;
        cell.classList.add(dx || dy ? 'near' : 'lit');
        lit.push(cell);
      }
    };
    hero.addEventListener('pointermove', e => {
      if (e.pointerType === 'touch') return;
      inside = true; px = e.clientX; py = e.clientY;
      if (!frame) frame = requestAnimationFrame(light);
    }, { passive: true });
    const leave = () => { inside = false; cancelAnimationFrame(frame); frame = 0; clear(); };
    hero.addEventListener('pointerleave', leave);
    window.addEventListener('blur', leave);
    // Scrolling moves the tiles under a still pointer, so follow it.
    addEventListener('scroll', () => { if (inside && !frame) frame = requestAnimationFrame(light); }, { passive: true });

    // A click sends a ring of light outward from the tile under it.
    if (!reduced) hero.addEventListener('click', e => {
      if (e.target.closest('a, button')) return;
      const [col, row] = at(e.clientX, e.clientY);
      const wave = [];
      cells.forEach((cell, i) => {
        const d = Math.hypot(i % cols - col, Math.floor(i / cols) - row);
        if (d > 4.5) return;
        cell.classList.remove('wave');
        cell.style.setProperty('--delay', `${(d * .07).toFixed(3)}s`);
        wave.push(cell);
      });
      void box.offsetWidth; // Restart the animation on tiles still rippling.
      wave.forEach(cell => cell.classList.add('wave'));
    });
    box.addEventListener('animationend', e => e.target.classList.remove('wave'));

    let resize = 0;
    addEventListener('resize', () => { cancelAnimationFrame(resize); resize = requestAnimationFrame(fill); });
  }

  const boot = () => { const box = document.querySelector('.tiles'); if (box) try { tiles(box); } catch { box.remove(); } };
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', boot);
  else boot();
})();
