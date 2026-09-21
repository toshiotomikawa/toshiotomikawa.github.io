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
  });
})();
