"""Check generated routes and core content without executing client JavaScript."""
import re
import unittest
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit, unquote

ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / 'dist'


class Page(HTMLParser):
    def __init__(self, path):
        super().__init__()
        self.ids = set()
        self.links = []
        self.headings = []
        self.lang = None
        self.feed(path.read_text(encoding='utf-8'))

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if 'id' in attrs:
            self.ids.add(attrs['id'])
        if tag == 'a':
            self.links.append(attrs.get('href', ''))
        if re.fullmatch('h[1-6]', tag):
            self.headings.append(int(tag[1]))
        if tag == 'html':
            self.lang = attrs.get('lang')


class StaticPrototype(unittest.TestCase):
    def test_routes_links_and_semantics(self):
        paths = [DIST / 'index.html', DIST / '404.html'] + [DIST / l / p for l in ('en', 'pt') for p in ('index.html', 'work/mgs/index.html', 'work/mapa/index.html')]
        allowed_external_prefixes = (
            'https://www.youtube.com/watch?v=sYcOqTKv7B0',
            'https://mapadabella.vercel.app/',
            'https://github.com/toshiotomikawa',
            'mailto:toshiotomikawa@gmail.com',
        )
        for path in paths:
            with self.subTest(path=path):
                page = Page(path)
                self.assertIn(page.lang, ('en', 'pt-BR'))
                self.assertEqual(page.headings.count(1), 1)
                self.assertIn('main', page.ids)
                self.assertGreater(path.stat().st_size, 3000)
                for link in page.links:
                    url = urlsplit(link)
                    if url.scheme in ('http', 'https', 'mailto'):
                        self.assertTrue(any(link.startswith(prefix) for prefix in allowed_external_prefixes), f'Unexpected external link: {link}')
                        continue
                    target = DIST / unquote(url.path).lstrip('/') if url.path else path
                    if target.is_dir():
                        target /= 'index.html'
                    self.assertTrue(target.is_file(), link)
                    if url.fragment:
                        self.assertIn(url.fragment, Page(target).ids, link)

    def test_light_is_unscripted_default(self):
        css = (ROOT / 'assets/site.css').read_text()
        self.assertIn('color-scheme: light;', css.split(':root[data-theme=')[0])
        for locale in ('en', 'pt'):
            html = (DIST / locale / 'index.html').read_text(encoding='utf-8')
            self.assertIn('type="button" hidden', html)
            self.assertIn(f'href="/{locale}/work/mgs/"', html)
            self.assertNotIn('data-theme="dark"', html)

    def test_text_palette_contrast(self):
        def luminance(h):
            rgb = [int(h[i:i+2], 16) / 255 for i in (1, 3, 5)]
            return sum(w * (v / 12.92 if v <= .04045 else ((v + .055) / 1.055) ** 2.4) for w, v in zip((.2126, .7152, .0722), rgb))
        css = (ROOT / 'assets/site.css').read_text()
        for palette in re.findall(r':root[^\{]*\{([^}]+)\}', css):
            values = dict(re.findall(r'--([\w-]+):\s*(#[0-9a-f]{6})', palette))
            for name in ('ink', 'ink2', 'muted', 'dim', 'accent', 'accent-hover'):
                for bg in ('bg', 'surface'):
                    a, b = sorted((luminance(values[name]), luminance(values[bg])))
                    self.assertGreaterEqual((b + .05) / (a + .05), 4.5, f'{name} on {bg}')

    def test_language_cross_linking(self):
        for case in ('mgs', 'mapa'):
            en_case = (DIST / 'en/work' / case / 'index.html').read_text(encoding='utf-8')
            pt_case = (DIST / 'pt/work' / case / 'index.html').read_text(encoding='utf-8')
            self.assertIn(f'href="/pt/work/{case}/"', en_case)
            self.assertIn(f'href="/en/work/{case}/"', pt_case)
            self.assertIn(f'hreflang="pt-BR" href="/pt/work/{case}/"', en_case)
            self.assertIn(f'hreflang="en" href="/en/work/{case}/"', pt_case)

    def test_meta_and_accessibility(self):
        for path in (DIST / 'en/index.html', DIST / 'pt/index.html', DIST / 'en/work/mapa/index.html'):
            content = path.read_text(encoding='utf-8')
            self.assertIn('property="og:title"', content)
            self.assertIn('property="og:description"', content)
            self.assertIn('name="twitter:card"', content)
            self.assertIn('rel="canonical"', content)
            self.assertIn('class="skip-link"', content)
            self.assertIn('id="main"', content)

    def test_no_em_dashes(self):
        content_files = list((ROOT / 'content').glob('*.json'))
        dist_html_files = list(DIST.rglob('*.html'))
        self.assertTrue(content_files)
        self.assertTrue(dist_html_files)
        for path in content_files + dist_html_files:
            text = path.read_text(encoding='utf-8')
            self.assertNotIn('\u2014', text, f'Em dash (-) found in {path}')
            self.assertNotIn('&mdash;', text, f'&mdash; found in {path}')
            self.assertNotIn('&#8212;', text, f'&#8212; found in {path}')

    def test_watermark_removal_hygiene(self):
        """Ensure all content, styles, scripts, and HTML are free of invisible Unicode and space homoglyphs."""
        import sys
        sys.path.insert(0, str(ROOT))
        from scripts.clean_text import audit_text
        files = list((ROOT / 'content').glob('*.json')) + list(DIST.rglob('*.html')) + [
            ROOT / 'assets/site.css',
            ROOT / 'assets/preferences.js'
        ]
        self.assertTrue(files)
        for path in files:
            findings = audit_text(path.read_text(encoding='utf-8'))
            self.assertEqual(len(findings), 0, f'Watermarks/invisible Unicode found in {path}: {findings}')

    def test_humanizer_tell_hygiene(self):
        """Ensure content prose avoids AI formulas, staged contrasts, and corporate buzzwords."""
        forbidden_patterns = [
            r'\brather than\b',
            r'\binstead of\b',
            r'\bnot just\b',
            r'\bnot only\b',
            r'\bat its core\b',
            r'\bthe real question\b',
            r'\bdelve\b',
            r'\btestament\b',
            r'\btapestry\b',
            r'\bbeacon\b',
            r'\bgame-changing\b',
            r'\bseamless\b',
            r'\bfurthermore\b',
            r'\bmoreover\b',
            r'\bem vez de\b',
            r'\bnão apenas\b',
        ]
        content_files = list((ROOT / 'content').glob('*.json'))
        for path in content_files:
            text = path.read_text(encoding='utf-8').lower()
            for pattern in forbidden_patterns:
                match = re.search(pattern, text)
                self.assertIsNone(match, f'Humanizer tell "{pattern}" found in {path}: {match}')


if __name__ == '__main__':
    unittest.main()

