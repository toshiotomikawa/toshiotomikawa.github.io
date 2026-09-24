# Yuri Toshio Tomikawa: Portfolio

English/Portuguese portfolio for LATAM remote operations-management roles.
Live URL: https://toshiotomikawa.github.io/

## Current milestone

Published and live on GitHub Pages with post-launch visual, typography, and interactive enhancements.
The repository publishes from `main` via GitHub Actions (`.github/workflows/deploy.yml`).

Post-launch updates:
- Pure white canvas (#ffffff), soft pearl card surface (#f8f9fa), crimson red accent (#bc002d), and ink (#16181a).
- Geist and Geist Mono font superfamily with a strict 5-tier semantic scale.
- Mandatory Blader Humanizer and Guillaume Meyer Watermark Remover standards.
- Interactive collapsible FAQ section (agentic tools, AI background, English fluency).
- Tab navigation history fix using history.replaceState and smooth scrolling.
- Custom crimson and white letter-T favicon suite.

## Preview

Requires Python 3.12+; no installation or runtime framework needed.

```powershell
python scripts/build.py
python scripts/preview.py
```

Open http://127.0.0.1:4173/. Explicit routes: `/en/`, `/pt/`,
`/en/work/mgs/`, `/pt/work/mgs/`, `/en/work/mapa/`, `/pt/work/mapa/`. Stop the preview with Ctrl+C.

## Structure

- `content/`: matching EN/PT copy in clean JSON format.
- `assets/site.css`: shared responsive styles, Geist superfamily, 5-tier typography scale, and themes.
- `assets/preferences.js`: theme cycling, locale switching, and tab navigation history enhancement.
- `scripts/build.py`: dependency-free static renderer. Generated `dist/` is deployed to GitHub Pages.
- `scripts/clean_text.py`: Unicode watermark and invisible character cleaner.
- `tests/`: static content, watermark hygiene, humanizer tells, preference contract, and CDP browser tests.

The small build script shares markup across languages and pages without shipping
a framework. Google Fonts supplies Geist and Geist Mono; system fonts are the fallback.

## Verification

```powershell
python scripts/build.py
python scripts/clean_text.py
python tests/static_test.py
node --test tests/preferences.test.cjs
```

Node is only needed for the preference and browser CDP tests. To inspect script-unavailable behavior:

```powershell
python scripts/preview.py --port 4174 --without-script
```

See [CHECKPOINT.md](CHECKPOINT.md) for checked behavior and remaining scope;
[PLAN.md](PLAN.md) for delivery gates; [AGENTS.md](AGENTS.md) for project guidance.
