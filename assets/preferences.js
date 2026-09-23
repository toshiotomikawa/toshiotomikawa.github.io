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
})();
