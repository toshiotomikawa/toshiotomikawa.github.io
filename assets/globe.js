/* Slowly spinning ASCII Earth for the hero. Land map: Natural Earth 1:110m land (public domain), 2-degree grid. */
(() => {
  'use strict';
  const LAND = 'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAf4AP/AAAAAAAAAAAAAAAAAAAAAAAAX/z///+AAAAAAAABAAAAAAAAAAAAAYd8P///wAA+AAAAAA8AAAAAAAAAAAwAnw////4AAIAAAAAAGAAAAAAAAAAADivwAf//wAAAAADAAf/wAHYAAAAAADoi3sAP//gAAAAAMAD///sAAAAgBgACfwz/AD/+gAAAwAEHf///+/8gBAP/7/nJdjwD/+AAAH/AA7f///////f4P//////h8H/gAAAf/6//f////////Mf/////9H4D8AeAA+ev///////////AP/////4A0B4AAAD5/////////////Af3////gHgA4AAAH5///////////LwAHgH///gHkAAAAAH4/////////+CIAABAB///4D+AAAAGCx/////////4A8AAIAAf///n/gAAAOCD/////////wA4AAAAAf///n/wAAAbP///////////AgAAAAAP/////wAAADf//////////9AAAAAAAF////0YAAAB///////////9AAAAAAAD////8EAAAB///////////5AAAAAAAD////2AAAAB/f5fP//////wAAAAAAAD////gAAAAfxnwPP//////jAAAAAAAD////AAAAAPCb3/n/////+CAAAAAAAD///8AAAAAfALf/n////+ECAAAAAAAB///8AAAAAGHQP/n/////mMAAAAAAAA///8AAAAAH+Ai///////E8AAAAAAAAf//wAAAAAP/AA///////BgAAAAAAAAP//gAAAAAf/73///////gAAAAAAAAAD/AQAAAAAf////f/////gAAAAAAAAAF+AQAAAAB///+/n/////AAAAAAAAAAC+AAAAAAB///+f0H////AAAAAAAAAAAeAwAAAAD////f/B///8gAAAAAAAAAAeGEAAAAH////v+B/z/AAAAAAAAAAAAPMAgAAAD////n+A/B+gAAAAAAAAAAAD8AAAAAD////n4AeB/AgAAAAAAAAAAAPAAAAAH////3gAcAfAgAAAAAAAAAAADAAAAAD////6AAcAfggAAAAAAAAAAABDwAAAD////8wAMATAIAAAAAAAAAAAAr/AAAB/////gAKASAAAAAAAAAAAAAAH/gAAA/////gACAAAIAAAAAAAAAAAAH/8AAAaH///AAAAsGAAAAAAAAAAAAAH/+AAAAB//+AAAAUOAAAAAAAAAAAAAP/+AAAAB//8AAAAYegAAAAAAAAAAAAP//gAAAD//4AAAAMeBgAAAAAAAAAAAP//8AAAB//wAAAAGdiuAAAAAAAAAAAf///AAAA//wAAAACAQHgAAAAAAAAAAP///gAAA//wAAAABwAHwgAAAAAAAAAH///AAAA//wAAAAACIDQIAAAAAAAAAH//+AAAAf/wAAAAAAAAAAAAAAAAAAAD//+AAAA//wgAAAAABxAAAAAAAAAAAD//+AAAA//wgAAAAAPxgBAAAAAAAAAA//8AAAA//jgAAAAAf5gAAAAAAAAAAAf/8AAAA//DgAAAAAf/gAAAAAAAAAAAf/8AAAAf/DAAAAAD//4CAAAAAAAAAAf/wAAAAf/DAAAAAH//4AAAAAAAAAAAf/AAAAAf+CAAAAAH//8AAAAAAAAAAAf/AAAAAP8AAAAAAH//+AAAAAAAAAAA/+AAAAAP8AAAAAAH//+AAAAAAAAAAA/+AAAAAH4AAAAAAD//+AAAAAAAAAAA/8AAAAAHwAAAAAADwf8AAAAAAAAAAA/gAAAAAAAAAAAAACAH4AIAAAAAAAAB/wAAAAAAAAAAAAAAAD4AEAAAAAAAAB+AAAAAAAAAAAAAAAAAAAGAAAAAAAAB6AAAAAAAAAAAAAAAAAwAMAAAAAAAAA8AAAAAAAAAAAAAAAAAQAYAAAAAAAAB4AAAAAAAAAAAAAAAAAAAwAAAAAAAAB4AAAAAAAAAAAAAAAAAAAAAAAAAAAADwAAAAAAAAAACAAAAAAAAAAAAAAAAADgAAAAAAAAAAAAAAAAAAAAAAAAAAAABwAAAAAAAAAAAAAAAAAAAAAAAAAAAAAwAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACAAAAAAAAAAAAAAAAAAAAAAAAAAAAAMAAAAAAAAAeAAIP+f/gAAAAAAAAAAAMAAAAAAABP/+H//////AAAAAAAAAAA+AAAAAf////8////////AAAAAAAOEAPAAAB///////////////gAAAP//T//8AAAH//////////////+AAAH/////4AAAH///////////////8AAE//////4ABw////////////////8AAAD//////gCA////////////////wAAAf/////////////////////////+A/4A///////////////////////////////////////////////////////////////////////////////////////';
  const W = 180, H = 90;
  const bits = Uint8Array.from(atob(LAND), c => c.charCodeAt(0));
  const land = (lat, lon) => {
    const r = Math.min(H - 1, Math.floor((90 - lat) / 2));
    const c = ((Math.floor((lon + 180) / 2) % W) + W) % W;
    const i = r * W + c;
    return (bits[i >> 3] >> (7 - (i & 7))) & 1;
  };
  const LAND_RAMP = '.:-=+*#%@';
  const SEA_RAMP = '...:';
  const TILT = 23.4 * Math.PI / 180;
  const cosT = Math.cos(TILT), sinT = Math.sin(TILT);
  const light = (() => { const v = [-.35, .35, .87]; const n = Math.hypot(...v); return v.map(x => x / n); })();

  function start(pre) {
    let cols = 0, rows = 0, cw = 0, lh = 0;
    const measure = () => {
      const probe = document.createElement('span');
      probe.textContent = 'M'.repeat(20);
      pre.append(probe);
      cw = probe.getBoundingClientRect().width / 20;
      probe.remove();
      lh = parseFloat(getComputedStyle(pre).lineHeight) || cw * 1.7;
      cols = Math.max(16, Math.floor(pre.clientWidth / cw));
      rows = Math.max(8, Math.round(cols * cw / lh));
    };
    const draw = spin => {
      let out = '';
      for (let i = 0; i < rows; i++) {
        let line = '', run = '', inLand = false;
        const y = 1 - (2 * i + 1) / rows;
        for (let j = 0; j < cols; j++) {
          const x = (2 * j + 1) / cols - 1;
          const r2 = x * x + y * y;
          let ch = ' ', isLand = false;
          if (r2 <= 1) {
            const z = Math.sqrt(1 - r2);
            const lit = Math.max(0, x * light[0] + y * light[1] + z * light[2]);
            // Undo the axial tilt, then read latitude and longitude.
            const xr = x * cosT + y * sinT, yr = -x * sinT + y * cosT;
            const lat = Math.asin(Math.max(-1, Math.min(1, yr))) * 180 / Math.PI;
            const lon = Math.atan2(xr, z) * 180 / Math.PI + spin;
            isLand = !!land(lat, ((lon + 540) % 360) - 180);
            const ramp = isLand ? LAND_RAMP : SEA_RAMP;
            ch = ramp[Math.min(ramp.length - 1, Math.floor((isLand ? .3 + lit * .7 : lit) * ramp.length))];
          }
          if (isLand !== inLand) { line += inLand ? '<b>' + run + '</b>' : run; run = ''; inLand = isLand; }
          run += ch;
        }
        line += inLand ? '<b>' + run + '</b>' : run;
        out += line + (i < rows - 1 ? '\n' : '');
      }
      pre.innerHTML = out;
    };

    let reduced = false;
    try { reduced = matchMedia('(prefers-reduced-motion: reduce)').matches; } catch { /* Full motion. */ }
    const t0 = performance.now();
    // Brazil faces the viewer first; it turns west to east, once every 90 seconds.
    const spinAt = now => -50 - ((now - t0) / 90000) * 360;
    measure();
    draw(spinAt(t0));
    pre.classList.add('is-ready');
    // Remeasure once the web font has replaced the fallback.
    document.fonts?.ready.then(() => { measure(); draw(spinAt(performance.now())); });
    if (reduced) return;
    let visible = true, last = 0;
    if ('IntersectionObserver' in window) new IntersectionObserver(([e]) => { visible = e.isIntersecting; }).observe(pre);
    const tick = now => {
      if (visible && now - last > 66) { last = now; draw(spinAt(now)); }
      requestAnimationFrame(tick);
    };
    requestAnimationFrame(tick);
    let resize = 0;
    addEventListener('resize', () => { cancelAnimationFrame(resize); resize = requestAnimationFrame(() => { measure(); draw(spinAt(performance.now())); }); });
  }

  const boot = () => { const pre = document.querySelector('.globe'); if (pre) try { start(pre); } catch { pre.remove(); } };
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', boot);
  else boot();
})();
