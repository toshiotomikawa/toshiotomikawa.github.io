# Phase 4: Published and verified

Completed 2026-09-21. Yuri Toshio Tomikawa's bilingual portfolio is live on GitHub Pages.
Live URL: https://toshiotomikawa.github.io/
Branch: `main` (tracked at `origin/main`).

## Implementation

- Deployed the complete bilingual portfolio to GitHub Pages:
  - Homepage in English (`/en/`) and Portuguese (`/pt/`) with automatic language detection and neutral entry (`/`).
  - Core Case Study 01: Michael Ghelfi Studios operations (`/en/work/mgs/`, `/pt/work/mgs/`).
  - Core Case Study 02: Mapa da Bella interactive simulator (`/en/work/mapa/`, `/pt/work/mapa/`; repository `MapaFinanceiro`).
  - Supporting project: Grok MCP Bridge architecture card.
  - Background, Availability, Contact (`mailto:toshiotomikawa@gmail.com` and GitHub), and Resume qualifications summary.
  - Custom 404 error page (`/404.html`) with bilingual return navigation.
  - Production `robots` meta tag (`index, follow` on content pages; `noindex` on 404).
  - Clean OpenGraph, Twitter card, canonical links, and inline SVG favicon.
  - Theme styling: Pure white canvas (#ffffff) with Crimson Red accent (#bc002d) for markers, lines, and links.
  - GitHub Actions automated deployment workflow (`.github/workflows/deploy.yml`) using `actions/upload-pages-artifact@v3` and `actions/deploy-pages@v4`.

## Live Production Verification

- HTTP route check: All 10 live URLs return HTTP 200 with complete UTF-8 HTML/CSS/JS payloads:
  - `https://toshiotomikawa.github.io/` (neutral entry)
  - `https://toshiotomikawa.github.io/en/`
  - `https://toshiotomikawa.github.io/pt/`
  - `https://toshiotomikawa.github.io/en/work/mgs/`
  - `https://toshiotomikawa.github.io/pt/work/mgs/`
  - `https://toshiotomikawa.github.io/en/work/mapa/`
  - `https://toshiotomikawa.github.io/pt/work/mapa/`
  - `https://toshiotomikawa.github.io/404.html`
  - `https://toshiotomikawa.github.io/assets/site.css`
  - `https://toshiotomikawa.github.io/assets/preferences.js`
- Live headless Chromium CDP audit against production URL (`https://toshiotomikawa.github.io`):
  - 0 horizontal overflow at 360px, 390px, 768px, and 1440px across all routes.
  - Live theme cycling (System → Light → Dark → System) tested and confirmed.
  - Live cross-locale navigation (`/en/work/mapa/` → `/pt/work/mapa/` → `/pt/#work`) tested and confirmed.
- Automated test suite (12 local checks) passes completely:
  - 5 Python static tests (`tests/static_test.py`).
  - 7 Node preference and locale tests (`tests/preferences.test.cjs`).
  - Google Chrome and Microsoft Edge dual-engine CDP tests.

## Post-Launch Enhancements (2026-09-22 - 2026-09-23)

- Surface and Palette: Refined featured card background to soft pearl (`#f8f9fa`) on pure white canvas (`#ffffff`), with crimson red accent (`#bc002d`) and ink (`#16181a`).
- Unified Font Superfamily: Replaced fragmented font imports with Geist (sans-serif) and Geist Mono (monospace), served with system fallbacks.
- Strict 5-Tier Typography Scale: Consolidated font sizing into a semantic scale (`--text-xs: 12px`, `--text-base: 15px`, `--text-lg: 18px`, `--text-2xl: clamp(24px, 3.2cqi, 32px)`, `--text-hero: clamp(36px, 6cqi, 72px)`).
- Content Quality and Unicode Hygiene: Enforced standards from `blader/humanizer` and `guillaumemeyer/watermarks-remover` across all content via `scripts/clean_text.py` and `tests/static_test.py`.
- Interactive Collapsible FAQ: Added accessible `<details>`/`<summary>` accordion on the homepage in English and Portuguese with crimson toggle indicators (`+` / `×`), covering:
  1. Agentic tools experience (Antigravity, Claude Code, Codex, Grok Build, OpenCode)
  2. AI background and Google certification
  3. English fluency and EF SET C2 certification
- In-Page Tab Navigation: Used `history.replaceState` and smooth scrolling for section tabs (`#work`, `#background`, `#qualifications`) in `assets/preferences.js`, preventing browser back-button history expansion in fresh tabs.
- Custom Letter-T Favicon Suite: Processed `letter-t-.png` into crimson red (`#bc002d`) squircle with opaque white (`#ffffff`) "T" and transparent outer corners across 32x32, 192x192, apple-touch-icon, favicon.ico, and SVG.
- Automated Test Suite: Passes completely across 8 static tests, 9 Node preference tests, text watermark audit, and CDP browser audits.

## Rollback Procedure

- To roll back:
  1. `git revert HEAD` (or checkout the desired commit) on `main`.
  2. `git push origin main`.
  3. GitHub Actions will automatically rebuild and deploy the reverted static output to GitHub Pages within ~20 seconds.

## Backups

- `G:\My Drive\Desktop\Coding\Portfolio`: Full backup hash-verified; Git integrity passed.
- `W:\Desktop\Coding\Portfolio`: Full backup synchronized, hash-verified, and Git integrity passed.
