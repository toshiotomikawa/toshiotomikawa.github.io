/* Static content remains usable when scripting, storage, or detection is unavailable. */
(() => {
  'use strict';
  const root = document.documentElement;
  const read = key => { try { return localStorage.getItem(key); } catch { return null; } };
  const write = (key, value) => { try { localStorage.setItem(key, value); } catch { /* Optional persistence. */ } };
  const modes = ['system', 'light', 'dark'];
  const saved = read('portfolio-theme');
  let mode = modes.includes(saved) ? saved : 'system';
  let media;
  try { media = window.matchMedia('(prefers-color-scheme: dark)'); } catch { /* Light fallback. */ }
  function applyTheme() {
    root.dataset.theme = mode === 'system' ? (media?.matches ? 'dark' : 'light') : mode;
    root.dataset.themePreference = mode;
  }
  applyTheme();
  let reduced = false;
  try { reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches; } catch { /* Treat as full motion. */ }
  if (!reduced && 'IntersectionObserver' in window) root.classList?.add('motion');
  const onSystemChange = () => { if (mode === 'system') applyTheme(); };
  if (media?.addEventListener) media.addEventListener('change', onSystemChange);
  else if (media?.addListener) media.addListener(onSystemChange);

  if (root.dataset.entry === 'neutral') {
    const savedLocale = read('portfolio-locale');
    const primary = String(navigator.language || '').toLowerCase();
    const locale = ['en', 'pt'].includes(savedLocale) ? savedLocale : (/^pt(?:-|$)/.test(primary) ? 'pt' : 'en');
    // Preserve section links; replace avoids a redirect entry in browser history.
    window.location.replace(`/${locale}/${window.location.hash}`);
  }

  document.addEventListener('DOMContentLoaded', () => {
    try { setupMotion(); } catch { root.classList?.remove('motion'); }
    const button = document.querySelector('.theme-toggle');
    const pt = root.lang.startsWith('pt');
    function labelTheme() {
      const next = modes[(modes.indexOf(mode) + 1) % modes.length];
      const names = { system: 'sistema', light: 'claro', dark: 'escuro' };
      const label = pt ? `Tema: ${names[mode]}. Mudar para ${names[next]}.` : `Theme: ${mode}. Switch to ${next}.`;
      button.setAttribute('aria-label', label);
      button.title = label;
      button.querySelectorAll('[data-icon]').forEach(icon => {
        icon.toggleAttribute('hidden', icon.dataset.icon !== mode);
      });
    }
    if (button) {
      labelTheme();
      button.hidden = false;
      button.addEventListener('click', () => {
        mode = modes[(modes.indexOf(mode) + 1) % modes.length];
        write('portfolio-theme', mode);
        applyTheme();
        labelTheme();
      });
    }
    document.querySelectorAll('[data-locale]').forEach(link => {
      link.addEventListener('click', () => {
        link.hash = window.location.hash;
        write('portfolio-locale', link.dataset.locale);
      });
    });

    // In-page section navigation: update address bar without adding browser history entries.
    document.addEventListener('click', event => {
      if (event.defaultPrevented || event.button !== 0 || event.metaKey || event.ctrlKey || event.shiftKey || event.altKey) {
        return;
      }
      const link = event.target?.closest?.('a');
      if (!link || !link.href) return;
      try {
        const url = new URL(link.href, window.location.href);
        if (url.origin !== window.location.origin) return;

        const norm = p => p.replace(/\/index\.html$/, '').replace(/\/$/, '') || '/';
        if (norm(url.pathname) !== norm(window.location.pathname)) return;

        if (url.hash) {
          const id = decodeURIComponent(url.hash.slice(1));
          const target = document.getElementById(id);
          if (target) {
            event.preventDefault();
            if (window.history?.replaceState) {
              window.history.replaceState(null, '', url.hash);
            }
            const prefersReduced = window.matchMedia?.('(prefers-reduced-motion: reduce)')?.matches;
            target.scrollIntoView({ behavior: prefersReduced ? 'auto' : 'smooth' });
            target.setAttribute('tabindex', '-1');
            target.focus({ preventScroll: true });
          }
        } else if (link.classList.contains('brand') && window.location.hash) {
          event.preventDefault();
          if (window.history?.replaceState) {
            window.history.replaceState(null, '', window.location.pathname + window.location.search);
          }
          const prefersReduced = window.matchMedia?.('(prefers-reduced-motion: reduce)')?.matches;
          window.scrollTo({ top: 0, behavior: prefersReduced ? 'auto' : 'smooth' });
        }
      } catch {
        /* Fallback to default browser navigation if URL parsing fails. */
      }
    });
  });

  // Scroll reveals, count-ups, card tilt, glass header and reading progress.
  function setupMotion() {
    const bar = document.querySelector('.progress');
    const hero = document.querySelector('.hero');
    let pending = false;
    const update = () => {
      pending = false;
      const y = window.scrollY;
      root.classList.toggle('is-scrolled', y > 8);
      root.classList.toggle('show-top', y > window.innerHeight * .6);
      if (bar) {
        const max = root.scrollHeight - window.innerHeight;
        bar.style.setProperty('--progress', max > 0 ? Math.min(1, y / max).toFixed(4) : '0');
      }
      if (hero) hero.style.setProperty('--hero', Math.min(1, y / Math.max(1, hero.offsetHeight)).toFixed(4));
    };
    update();
    // One update per frame keeps scroll-linked effects smooth on slow devices.
    window.addEventListener('scroll', () => {
      if (!pending) { pending = true; requestAnimationFrame(update); }
    }, { passive: true });
    if (!root.classList.contains('motion')) return;

    const countUp = el => {
      const target = Number(el.dataset.count);
      const pad = Number(el.dataset.countPad || 0);
      const start = performance.now();
      const tick = now => {
        const t = Math.min(1, (now - start) / 1200);
        el.textContent = String(Math.round(target * (1 - Math.pow(1 - t, 4)))).padStart(pad, '0');
        if (t < 1) requestAnimationFrame(tick);
      };
      requestAnimationFrame(tick);
    };
    const io = new IntersectionObserver(entries => {
      entries.forEach(entry => {
        if (!entry.isIntersecting) return;
        entry.target.classList.add('is-in');
        entry.target.querySelectorAll('[data-count]').forEach(countUp);
        io.unobserve(entry.target);
      });
    }, { rootMargin: '0px 0px -8% 0px', threshold: 0.12 });
    document.querySelectorAll('[data-reveal]').forEach(el => io.observe(el));

    if (!window.matchMedia('(hover: hover)').matches) return;
    document.querySelectorAll('[data-tilt]').forEach(el => {
      let frame = 0;
      el.addEventListener('pointermove', event => {
        if (event.pointerType !== 'mouse') return;
        cancelAnimationFrame(frame);
        frame = requestAnimationFrame(() => {
          const r = el.getBoundingClientRect();
          const x = (event.clientX - r.left) / r.width;
          const y = (event.clientY - r.top) / r.height;
          el.style.setProperty('--rx', `${((0.5 - y) * 3).toFixed(2)}deg`);
          el.style.setProperty('--ry', `${((x - 0.5) * 4).toFixed(2)}deg`);
          el.style.setProperty('--mx', `${(x * 100).toFixed(1)}%`);
          el.style.setProperty('--my', `${(y * 100).toFixed(1)}%`);
        });
      });
      el.addEventListener('pointerleave', () => {
        cancelAnimationFrame(frame);
        el.style.setProperty('--rx', '0deg');
        el.style.setProperty('--ry', '0deg');
      });
    });
  }
})();
