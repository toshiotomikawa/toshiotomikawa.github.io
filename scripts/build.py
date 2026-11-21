"""Render the complete bilingual release candidate using only the Python standard library."""
import json
import shutil
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "dist"
BASE_URL = "https://toshiotomikawa.github.io"

# Line icons share one 16px grid; brand marks are filled.
ICONS = {
    'globe': '<svg aria-hidden="true" viewBox="0 0 16 16"><circle cx="8" cy="8" r="6.4"/><ellipse cx="8" cy="8" rx="2.8" ry="6.4"/><path d="M1.6 8h12.8"/></svg>',
    'up': '<svg aria-hidden="true" viewBox="0 0 16 16"><path d="M8 13.4V2.8M3.4 7.4 8 2.8l4.6 4.6"/></svg>',
    'instagram': '<svg aria-hidden="true" viewBox="0 0 16 16"><rect x="1.8" y="1.8" width="12.4" height="12.4" rx="3.6"/><circle cx="8" cy="8" r="2.9"/><circle class="dot" cx="11.7" cy="4.3" r=".5"/></svg>',
    'github': '<svg class="mark" aria-hidden="true" viewBox="0 0 16 16"><path d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27.68 0 1.36.09 2 .27 1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.01 8.01 0 0 0 16 8c0-4.42-3.58-8-8-8z"/></svg>',
    'linkedin': '<svg class="mark" aria-hidden="true" viewBox="0 0 24 24"><path d="M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433c-1.144 0-2.063-.926-2.063-2.065 0-1.138.92-2.063 2.063-2.063 1.14 0 2.064.925 2.064 2.063 0 1.139-.925 2.065-2.064 2.065zm1.782 13.019H3.555V9h3.564v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 23.227.792 24 1.771 24h20.451C23.2 24 24 23.227 24 22.271V1.729C24 .774 23.2 0 22.222 0h.003z"/></svg>',
    'x': '<svg class="mark" aria-hidden="true" viewBox="0 0 24 24"><path d="M18.244 2.25h3.308l-7.227 8.26 8.502 11.24H16.17l-5.214-6.817L4.99 21.75H1.68l7.73-8.835L1.254 2.25H8.08l4.713 6.231zm-1.161 17.52h1.833L7.084 4.126H5.117z"/></svg>',
}
SOCIALS = [
    ('github', 'GitHub', 'https://github.com/toshiotomikawa'),
    ('instagram', 'Instagram', 'https://www.instagram.com/toshiotomikawa/'),
    ('linkedin', 'LinkedIn', 'https://www.linkedin.com/in/toshiotomikawa/'),
    ('x', 'X', 'https://x.com/toshiotomikawa'),
]


def e(value):
    return escape(str(value), quote=True)


def pairs(items, cls):
    return f'<dl class="{cls}">' + "".join(
        f'<div><dt>{e(label)}</dt><dd>{e(value)}</dd></div>' for label, value in items
    ) + '</dl>'


def arrow(label, href, back=False, external=False):
    glyph = '<span aria-hidden="true">←</span>' if back else ('<span aria-hidden="true">↗</span>' if external else '<span aria-hidden="true">→</span>')
    rel = ' rel="noopener noreferrer" target="_blank"' if external else ''
    return f'<a class="arrow" href="{href}"{rel}>{glyph if back else ""}{e(label)}{(" " + glyph) if not back else ""}</a>'


def home(c, locale):
    sup = c['supporting']

    # Featured cases, in display order: key, period, name.
    featured = [('mgs', '2021-2025', 'Michael Ghelfi Studios'), ('tomi', '2026', 'Tomi ESL'), ('mapa', '2026', 'Mapa da Bella')]
    case_cards = ''.join(f'''<article class="featured" data-reveal data-tilt style="--d:{i * .08:.2f}s"><div class="feature-grid">
        <div><span class="node" aria-hidden="true"></span><p class="mono dim">{i + 1:02} / {period}</p><p class="studio">{e(name)}</p><p class="skills mono">{'<br>'.join(map(e, c['cases'][key]['skills']))}</p></div>
        <div><h3>{e(c['cases'][key]['title'])}</h3><p class="feature-text">{e(c['cases'][key]['summary'])}</p>{arrow(c['read'], f'/{locale}/work/{key}/')}</div>
      </div></article>''' for i, (key, period, name) in enumerate(featured))

    # Supporting Case: Grok MCP Bridge
    points = ''.join(f'<li>{e(pt)}</li>' for pt in sup['points'])
    grok_card = f'''<article class="supporting-feature" data-reveal>
        <div class="supporting-header">
          <span class="node" aria-hidden="true"></span>
          <p class="mono dim">{e(sup['eyebrow'])}</p>
          <h3>{e(sup['title'])}</h3>
          <p class="feature-text">{e(sup['summary'])}</p>
        </div>
        <ul class="supporting-points">{points}</ul>
        <p class="supporting-status mono dim">{e(sup['status'])}</p>
      </article>'''

    experience = ''.join(f'<li data-reveal><p class="date mono"><span class="node" aria-hidden="true"></span>{e(date)}</p><div><h3>{e(role)}</h3><p>{e(org)}</p></div></li>' for date, role, org in c['experience'])

    resume_links = ''.join(f'{arrow(label, url)}' for label, url in c['resumeLinks'])

    faq_items = ''.join(
        f'''<details class="faq-item" data-reveal>
          <summary class="faq-question"><span>{e(item['q'])}</span><span class="faq-icon" aria-hidden="true">+</span></summary>
          <div class="faq-answer"><p>{e(item['a'])}</p></div>
        </details>'''
        for item in c.get('faqItems', [])
    )
    faq_section = f'''<section class="faq" id="faq"><div class="split">
      <h2 class="label">{e(c['faq'])}</h2>
      <div class="faq-list">{faq_items}</div>
    </div></section>''' if faq_items else ''

    return f'''
    <section class="hero">
      <div class="tiles" aria-hidden="true"></div>
      <p class="eyebrow mono rise">{e(c['eyebrow'])}</p>
      <h1 class="rise" style="--d:.12s">{e(c['title'])}</h1>
      <div class="hero-bottom rise" style="--d:.28s"><p class="intro">{e(c['intro'])}</p>{pairs(c['meta'], 'hero-meta mono')}</div>
    </section>
    <section class="work" id="work">
      <div class="section-heading mono" data-reveal><h2>{e(c['selected'])}</h2><span data-count="4" data-count-pad="2">04</span></div>
      {case_cards}
      {grok_card}
    </section>
    <section class="background" id="background"><div class="split" data-reveal>
      <h2 class="label">{e(c['background'])}</h2><div><p class="lead">{e(c['backgroundText'])}</p><ul class="experience">{experience}</ul></div>
    </div></section>
    {faq_section}
    <section class="availability" id="availability"><div class="split" data-reveal>
      <h2 class="label">{e(c['availability'])}</h2><p class="body-copy">{e(c['availabilityText'])}</p>
    </div></section>
    <section class="contact" id="contact"><div class="split" data-reveal>
      <h2 class="label">{e(c['contact'])}</h2>
      <div>
        <p class="lead">{e(c['contactText'])}</p>
        <div class="contact-actions">
          {arrow(c['email'], f"mailto:{c['email']}")}
          {arrow(c['githubLabel'], c['githubUrl'], external=True)}
        </div>
        <div class="resume-box">
          <p class="mono dim">{e(c['resumeTitle'])}</p>
          <p class="resume-summary">{e(c['resumeSummary'])}</p>
          <div class="resume-actions">{resume_links}</div>
        </div>
      </div>
    </div></section>'''


def case(c, case_data, locale):
    steps = ''.join(f'<li data-reveal style="--d:{(i - 1) * .09:.2f}s"><span class="node" aria-hidden="true"></span><span class="step-number mono" aria-hidden="true">{i:02}</span><p>{e(step)}</p></li>' for i, step in enumerate(case_data['steps'], 1))
    def section(i, body, cls=''):
        return f'<section class="case-section {cls}"><div class="case-split" data-reveal><h2 class="label">{e(case_data["labels"][i])}</h2><div>{body}</div></div></section>'
    return f'''<article>
      <div class="case-hero"><span class="rise">{arrow(c['nav'][0][1], f'/{locale}/#work', True)}</span><p class="case-eyebrow mono rise" style="--d:.06s">{e(case_data['eyebrow'])}</p><h1 class="rise" style="--d:.14s">{e(case_data['title'])}</h1><div class="rise" style="--d:.28s">{pairs(case_data['meta'], 'case-meta mono')}</div></div>
      {section(0, f'<p class="lead">{e(case_data["context"])}</p>')}
      {section(1, pairs(case_data['items'], 'responsibilities'))}
      {section(2, f'<p class="body-copy">{e(case_data["decisions"])}</p>')}
      {section(3, f'<h3 class="sample-title">{e(case_data["sampleTitle"])}</h3><ol class="steps">{steps}</ol><div class="credits"><p>{e(case_data["credit"])}</p><p>{e(case_data["reach"])}</p><p>{arrow(case_data["linkLabel"], case_data["linkUrl"], external=True)}</p></div>', 'sample')}
      {section(4, f'<p class="also-copy">{e(case_data["also"])}</p>' + arrow(case_data['back'], f'/{locale}/#work', True), 'last')}
    </article>'''


def not_found(c, locale='en'):
    is_pt = locale == 'pt'
    title = 'Página não encontrada' if is_pt else 'Page not found'
    message = 'O endereço solicitado não existe ou foi alterado.' if is_pt else 'The requested URL does not exist or has moved.'
    home_label = 'Voltar ao início' if is_pt else 'Back to home'
    return f'''
    <section class="case-hero">
      <p class="case-eyebrow mono">404 / Error</p>
      <h1>{e(title)}</h1>
      <p class="lead">{e(message)}</p>
      <div style="margin-top: 28px;">
        {arrow(home_label, f'/{locale}/', back=True)}
      </div>
    </section>'''


def document(c, locale, case_key=None, neutral=False, is_404=False):
    suffix = f'work/{case_key}/' if case_key else ''
    is_case = case_key is not None

    if is_404:
        title = 'Page not found / Página não encontrada'
        description = 'The requested page could not be found. / A página solicitada não pôde ser encontrada.'
    elif is_case:
        case_data = c['cases'][case_key]
        title = case_data['title']
        description = case_data['context'][:155]
    else:
        title = c['title']
        description = c['intro'][:155]

    nav = ''.join(f'<a href="/{locale}/#{anchor}">{e(label)}</a>' for anchor, label in c['nav'])
    # One icon button that switches to the other language, styled like the theme button.
    other, other_lang, other_name = ('en', 'en', 'English') if locale == 'pt' else ('pt', 'pt-BR', 'Português')
    language = f'<a class="icon-button" data-locale="{other}" href="/{other}/{suffix}" lang="{other_lang}" hreflang="{other_lang}" aria-label="{other_name}" title="{other_name}">{ICONS["globe"]}</a>'
    socials = ''.join(f'<a class="icon-button" href="{url}" rel="noopener noreferrer" target="_blank" aria-label="{name} @toshiotomikawa" title="{name} @toshiotomikawa">{ICONS[key]}</a>' for key, name, url in SOCIALS)
    top_label = 'Voltar ao topo' if locale == 'pt' else 'Back to top'

    page_url = f"{BASE_URL}/{locale}/{suffix}"
    og_locale = "pt_BR" if locale == "pt" else "en_US"
    og_locale_alt = "en_US" if locale == "pt" else "pt_BR"

    if is_404:
        body_content = not_found(c, locale)
    elif is_case:
        body_content = case(c, c['cases'][case_key], locale)
    else:
        body_content = home(c, locale)

    return f'''<!doctype html>
<html lang="{c['lang']}" data-entry="{'neutral' if neutral else 'explicit'}">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  {"<meta name=\"robots\" content=\"noindex\">" if is_404 else "<meta name=\"robots\" content=\"index, follow\">"}
  <title>{e(title)} | Yuri Toshio Tomikawa</title>
  <meta name="description" content="{e(description)}">
  <link rel="canonical" href="{page_url}">
  <meta property="og:site_name" content="Yuri Toshio Tomikawa">
  <meta property="og:title" content="{e(title)}">
  <meta property="og:description" content="{e(description)}">
  <meta property="og:type" content="website">
  <meta property="og:url" content="{page_url}">
  <meta property="og:locale" content="{og_locale}">
  <meta property="og:locale:alternate" content="{og_locale_alt}">
  <meta name="twitter:card" content="summary">
  <meta name="twitter:title" content="{e(title)}">
  <meta name="twitter:description" content="{e(description)}">
  <link rel="icon" type="image/svg+xml" href="/assets/favicon.svg">
  <link rel="icon" type="image/png" sizes="32x32" href="/assets/favicon-32x32.png">
  <link rel="icon" type="image/png" sizes="192x192" href="/assets/favicon-192x192.png">
  <link rel="apple-touch-icon" href="/assets/apple-touch-icon.png">
  <link rel="icon" type="image/png" href="/assets/favicon.png">
  <script src="/assets/preferences.js"></script>
  {'<script src="/assets/hero.js" defer></script>' if not (is_case or is_404) else ''}
  <link rel="preload" href="/assets/fonts/outfit-latin.woff2" as="font" type="font/woff2" crossorigin>
  <link rel="stylesheet" href="/assets/site.css">
  <link rel="alternate" hreflang="en" href="{BASE_URL}/en/{suffix}">
  <link rel="alternate" hreflang="pt-BR" href="{BASE_URL}/pt/{suffix}">
</head>
<body>
<div class="progress" aria-hidden="true"></div>
<a class="skip-link" href="#main">{e(c['skip'])}</a>
<div class="page" id="top" tabindex="-1">
  <header class="header">
    <a class="brand" href="/{locale}/"><span class="node" aria-hidden="true"></span>Yuri Toshio Tomikawa</a>
    <div class="header-controls"><nav class="sections mono" aria-label="{e(c['navLabel'])}">{nav}</nav>
    <div class="preferences"><nav class="languages" aria-label="{e(c['languageLabel'])}">{language}</nav>
    <button class="icon-button theme-toggle" type="button" hidden aria-label="{e(c['themeLabel'])}" title="{e(c['themeLabel'])}">
      <svg data-icon="system" aria-hidden="true" viewBox="0 0 16 16"><rect x="1.6" y="2.4" width="12.8" height="8.6"/><path d="M5.6 13.6h4.8"/></svg>
      <svg data-icon="light" aria-hidden="true" viewBox="0 0 16 16" hidden><circle cx="8" cy="8" r="3.1"/><path d="M8 1v1.7M8 13.3V15M1 8h1.7M13.3 8H15M3.05 3.05l1.2 1.2M11.75 11.75l1.2 1.2M12.95 3.05l-1.2 1.2M4.25 11.75l-1.2 1.2"/></svg>
      <svg data-icon="dark" aria-hidden="true" viewBox="0 0 16 16" hidden><path d="M13.2 9.9A5.8 5.8 0 0 1 6.1 2.8a5.8 5.8 0 1 0 7.1 7.1z"/></svg>
    </button></div></div>
  </header>
  <main id="main" tabindex="-1">{body_content}</main>
  <footer><span>Yuri Toshio Tomikawa</span><nav class="socials" aria-label="{e(c['socialLabel'])}">{socials}</nav></footer>
  <a class="icon-button to-top" href="#top" aria-label="{top_label}" title="{top_label}">{ICONS["up"]}</a>
</div>
</body>
</html>
'''


def build():
    OUT.mkdir(exist_ok=True)
    shutil.copytree(ROOT / 'assets', OUT / 'assets', dirs_exist_ok=True)
    shutil.copy2(ROOT / 'assets' / 'favicon.ico', OUT / 'favicon.ico')

    contents = {}
    for locale in ['en', 'pt']:
        contents[locale] = json.loads((ROOT / 'content' / f'{locale}.json').read_text(encoding='utf-8'))

    # Build locale homepages and case studies
    for locale in ['en', 'pt']:
        c = contents[locale]
        # Homepage
        home_path = OUT / locale
        home_path.mkdir(parents=True, exist_ok=True)
        (home_path / 'index.html').write_text(document(c, locale), encoding='utf-8')

        # Case studies
        for case_key in ['mgs', 'tomi', 'mapa']:
            case_path = OUT / locale / 'work' / case_key
            case_path.mkdir(parents=True, exist_ok=True)
            (case_path / 'index.html').write_text(document(c, locale, case_key=case_key), encoding='utf-8')

    # Root neutral-entry fallback
    (OUT / 'index.html').write_text(document(contents['en'], 'en', neutral=True), encoding='utf-8')

    # 404 missing-page document
    (OUT / '404.html').write_text(document(contents['en'], 'en', is_404=True), encoding='utf-8')

    (OUT / '.nojekyll').touch()
    print('Built homepage, MGS, Tomi ESL and Mapa da Bella cases, and 404 in EN/PT with neutral entry.')


if __name__ == '__main__':
    build()
