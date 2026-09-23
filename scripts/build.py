"""Render the complete bilingual release candidate using only the Python standard library."""
import json
import shutil
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "dist"
BASE_URL = "https://toshiotomikawa.github.io"


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
    mgs = c['cases']['mgs']
    mapa = c['cases']['mapa']
    sup = c['supporting']

    # Case 01: MGS
    mgs_card = f'''<article class="featured"><div class="feature-grid">
        <div><span class="node" aria-hidden="true"></span><p class="mono dim">01 / 2021-2025</p><p class="studio">Michael Ghelfi Studios</p><p class="skills mono">{'<br>'.join(map(e, mgs['skills']))}</p></div>
        <div><h3>{e(mgs['title'])}</h3><p class="feature-text">{e(mgs['summary'])}</p>{arrow(c['read'], f'/{locale}/work/mgs/')}</div>
      </div></article>'''

    # Case 02: Mapa da Bella
    mapa_card = f'''<article class="featured"><div class="feature-grid">
        <div><span class="node" aria-hidden="true"></span><p class="mono dim">02 / 2026</p><p class="studio">Mapa da Bella</p><p class="skills mono">{'<br>'.join(map(e, mapa['skills']))}</p></div>
        <div><h3>{e(mapa['title'])}</h3><p class="feature-text">{e(mapa['summary'])}</p>{arrow(c['read'], f'/{locale}/work/mapa/')}</div>
      </div></article>'''

    # Supporting Case: Grok MCP Bridge
    points = ''.join(f'<li>{e(pt)}</li>' for pt in sup['points'])
    grok_card = f'''<article class="supporting-feature">
        <div class="supporting-header">
          <span class="node" aria-hidden="true"></span>
          <p class="mono dim">{e(sup['eyebrow'])}</p>
          <h3>{e(sup['title'])}</h3>
          <p class="feature-text">{e(sup['summary'])}</p>
        </div>
        <ul class="supporting-points">{points}</ul>
        <p class="supporting-status mono dim">{e(sup['status'])}</p>
      </article>'''

    experience = ''.join(f'<li><p class="date mono"><span class="node" aria-hidden="true"></span>{e(date)}</p><div><h3>{e(role)}</h3><p>{e(org)}</p></div></li>' for date, role, org in c['experience'])

    resume_links = ''.join(f'{arrow(label, url)}' for label, url in c['resumeLinks'])

    faq_items = ''.join(
        f'''<details class="faq-item">
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
      <p class="eyebrow mono">{e(c['eyebrow'])}</p>
      <h1>{e(c['title'])}</h1>
      <div class="hero-bottom"><p class="intro">{e(c['intro'])}</p>{pairs(c['meta'], 'hero-meta mono')}</div>
    </section>
    <section class="work" id="work">
      <div class="section-heading mono"><h2>{e(c['selected'])}</h2><span>03</span></div>
      {mgs_card}
      {mapa_card}
      {grok_card}
    </section>
    <section class="background" id="background"><div class="split">
      <h2 class="label">{e(c['background'])}</h2><div><p class="lead">{e(c['backgroundText'])}</p><ul class="experience">{experience}</ul></div>
    </div></section>
    {faq_section}
    <section class="availability" id="availability"><div class="split">
      <h2 class="label">{e(c['availability'])}</h2><p class="body-copy">{e(c['availabilityText'])}</p>
    </div></section>
    <section class="contact" id="contact"><div class="split">
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
    steps = ''.join(f'<li><span class="node" aria-hidden="true"></span><span class="step-number mono" aria-hidden="true">{i:02}</span><p>{e(step)}</p></li>' for i, step in enumerate(case_data['steps'], 1))
    def section(i, body, cls=''):
        return f'<section class="case-section {cls}"><div class="case-split"><h2 class="label">{e(case_data["labels"][i])}</h2><div>{body}</div></div></section>'
    return f'''<article>
      <div class="case-hero">{arrow(c['nav'][0][1], f'/{locale}/#work', True)}<p class="case-eyebrow mono">{e(case_data['eyebrow'])}</p><h1>{e(case_data['title'])}</h1>{pairs(case_data['meta'], 'case-meta mono')}</div>
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
    languages = ''.join(f'<a data-locale="{key}" href="/{key}/{suffix}" lang="{lang}" hreflang="{lang}" {"aria-current=\"page\"" if key == locale else ""}>{key.upper()}</a>' for key, lang in [('en', 'en'), ('pt', 'pt-BR')])

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
  <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Geist:wght@300;400;500;600;700&amp;family=Geist+Mono:wght@400;500;600&amp;display=swap">
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
  <main id="main" tabindex="-1">{body_content}</main>
  <footer>Yuri Toshio Tomikawa</footer>
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

        # Case studies: mgs and mapa
        for case_key in ['mgs', 'mapa']:
            case_path = OUT / locale / 'work' / case_key
            case_path.mkdir(parents=True, exist_ok=True)
            (case_path / 'index.html').write_text(document(c, locale, case_key=case_key), encoding='utf-8')

    # Root neutral-entry fallback
    (OUT / 'index.html').write_text(document(contents['en'], 'en', neutral=True), encoding='utf-8')

    # 404 missing-page document
    (OUT / '404.html').write_text(document(contents['en'], 'en', is_404=True), encoding='utf-8')

    (OUT / '.nojekyll').touch()
    print('Built homepage, MGS case, Mapa da Bella case, and 404 in EN/PT with neutral entry.')


if __name__ == '__main__':
    build()
