"""Render the two-language prototype using only the Python standard library."""
import json
import shutil
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "dist"


def e(value):
    return escape(str(value), quote=True)


def pairs(items, cls):
    return f'<dl class="{cls}">' + "".join(
        f'<div><dt>{e(label)}</dt><dd>{e(value)}</dd></div>' for label, value in items
    ) + '</dl>'


def arrow(label, href, back=False):
    glyph = '<span aria-hidden="true">←</span>' if back else '<span aria-hidden="true">→</span>'
    return f'<a class="arrow" href="{href}">{glyph if back else ""}{e(label)}{glyph if not back else ""}</a>'


def home(c, locale):
    secondary = ''.join(f'<article><span class="node" aria-hidden="true"></span><p class="mono dim">{e(k)}</p><h3>{e(t)}</h3><p>{e(p)}</p></article>' for k, t, p in c['secondary'])
    experience = ''.join(f'<li><p class="date mono"><span class="node" aria-hidden="true"></span>{e(date)}</p><div><h3>{e(role)}</h3><p>{e(org)}</p></div></li>' for date, role, org in c['experience'])
    return f'''
    <section class="hero">
      <p class="eyebrow mono">{e(c['eyebrow'])}</p>
      <h1>{e(c['title'])}</h1>
      <div class="hero-bottom"><p class="intro">{e(c['intro'])}</p>{pairs(c['meta'], 'hero-meta mono')}</div>
    </section>
    <section class="work" id="work">
      <div class="section-heading mono"><h2>{e(c['selected'])}</h2><span>03</span></div>
      <article class="featured"><div class="feature-grid">
        <div><span class="node" aria-hidden="true"></span><p class="mono dim">01 / 2021—2025</p><p class="studio">Michael Ghelfi Studios</p><p class="skills mono">{'<br>'.join(map(e, c['skills']))}</p></div>
        <div><h3>{e(c['feature'])}</h3><p class="feature-text">{e(c['featureText'])}</p>{arrow(c['read'], f'/{locale}/work/mgs/')}</div>
      </div></article>
      <div class="secondary">{secondary}</div>
    </section>
    <section class="background" id="background"><div class="split">
      <h2 class="label">{e(c['background'])}</h2><div><p class="lead">{e(c['backgroundText'])}</p><ul class="experience">{experience}</ul></div>
    </div></section>
    <section class="availability" id="availability"><div class="split"><h2 class="label">{e(c['availability'])}</h2><p class="body-copy">{e(c['availabilityText'])}</p></div></section>'''


def case(c, locale):
    steps = ''.join(f'<li><span class="node" aria-hidden="true"></span><span class="step-number mono" aria-hidden="true">{i:02}</span><p>{e(step)}</p></li>' for i, step in enumerate(c['steps'], 1))
    def section(i, body, cls=''):
        return f'<section class="case-section {cls}"><div class="case-split"><h2 class="label">{e(c["labels"][i])}</h2><div>{body}</div></div></section>'
    return f'''<article>
      <div class="case-hero">{arrow(c['nav'][0], f'/{locale}/#work', True)}<p class="case-eyebrow mono">{e(c['caseEyebrow'])}</p><h1>{e(c['caseTitle'])}</h1>{pairs(c['caseMeta'], 'case-meta mono')}</div>
      {section(0, f'<p class="lead">{e(c["context"])}</p>')}
      {section(1, pairs(c['responsibilities'], 'responsibilities'))}
      {section(2, f'<p class="body-copy">{e(c["decisions"])}</p>')}
      {section(3, f'<h3 class="sample-title">{e(c["sample"])}</h3><ol class="steps">{steps}</ol><div class="credits"><p>{e(c["credit"])}</p><p>{e(c["reach"])}</p><p><a class="mono" href="https://www.youtube.com/watch?v=sYcOqTKv7B0">{e(c["watch"])} <span aria-hidden="true">↗</span></a></p></div>', 'sample')}
      {section(4, f'<p class="also-copy">{e(c["also"])}</p>' + arrow(c['back'], f'/{locale}/#work', True), 'last')}
    </article>'''


def document(c, locale, is_case=False, neutral=False):
    suffix = 'work/mgs/' if is_case else ''
    title = c['caseTitle'] if is_case else c['title']
    nav = ''.join(f'<a href="/{locale}/#{anchor}">{e(label)}</a>' for anchor, label in zip(['work', 'background', 'availability'], c['nav']))
    languages = ''.join(f'<a data-locale="{key}" href="/{key}/{suffix}" lang="{lang}" hreflang="{lang}" {"aria-current=\"page\"" if key == locale else ""}>{key.upper()}</a>' for key, lang in [('en', 'en'), ('pt', 'pt-BR')])
    return f'''<!doctype html>
<html lang="{c['lang']}" data-entry="{'neutral' if neutral else 'explicit'}">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="robots" content="noindex">
  <title>{e(title)} — Yuri Toshio Tomikawa</title>
  <meta name="description" content="{e(c['context'] if is_case else c['intro'])}">
  <script src="/assets/preferences.js"></script>
  <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Archivo:wdth,wght@62..125,400..700&amp;family=DM+Mono:wght@400;500&amp;display=swap">
  <link rel="stylesheet" href="/assets/site.css">
  <link rel="alternate" hreflang="en" href="/en/{suffix}">
  <link rel="alternate" hreflang="pt-BR" href="/pt/{suffix}">
</head>
<body>
<a class="skip-link" href="#main">{e(c['skip'])}</a>
<div class="page">
  <header class="header">
    <a class="brand" href="/{locale}/"><span class="node" aria-hidden="true"></span>Yuri Toshio Tomikawa</a>
    <div class="header-controls"><nav class="sections mono" aria-label="{e(c['navLabel'])}">{nav}</nav>
    <div class="preferences"><nav class="languages mono" aria-label="{e(c['languageLabel'])}">{languages}</nav>
    <button class="theme-toggle" type="button" hidden aria-label="{e(c['themeLabel'])}" title="{e(c['themeLabel'])}">
      <svg data-icon="system" aria-hidden="true" viewBox="0 0 16 16"><rect x="1.6" y="2.4" width="12.8" height="8.6"/><path d="M5.6 13.6h4.8"/></svg>
      <svg data-icon="light" aria-hidden="true" viewBox="0 0 16 16" hidden><circle cx="8" cy="8" r="3.1"/><path d="M8 1v1.7M8 13.3V15M1 8h1.7M13.3 8H15M3.05 3.05l1.2 1.2M11.75 11.75l1.2 1.2M12.95 3.05l-1.2 1.2M4.25 11.75l-1.2 1.2"/></svg>
      <svg data-icon="dark" aria-hidden="true" viewBox="0 0 16 16" hidden><path d="M13.2 9.9A5.8 5.8 0 0 1 6.1 2.8a5.8 5.8 0 1 0 7.1 7.1z"/></svg>
    </button></div></div>
  </header>
  <main id="main" tabindex="-1">{case(c, locale) if is_case else home(c, locale)}</main>
  <footer>Yuri Toshio Tomikawa</footer>
</div>
</body>
</html>
'''


def build():
    OUT.mkdir(exist_ok=True)
    shutil.copytree(ROOT / 'assets', OUT / 'assets', dirs_exist_ok=True)
    for locale in ['en', 'pt']:
        c = json.loads((ROOT / 'content' / f'{locale}.json').read_text(encoding='utf-8'))
        for is_case in [False, True]:
            path = OUT / locale / ('work/mgs' if is_case else '')
            path.mkdir(parents=True, exist_ok=True)
            (path / 'index.html').write_text(document(c, locale, is_case), encoding='utf-8')
        if locale == 'en':
            (OUT / 'index.html').write_text(document(c, locale, neutral=True), encoding='utf-8')
    (OUT / '.nojekyll').touch()
    print('Built homepage + MGS in EN/PT, with an English neutral-entry fallback.')


if __name__ == '__main__':
    build()
