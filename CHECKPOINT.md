# Phase 4 — Published and verified

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

## Rollback Procedure

- To roll back:
  1. `git revert HEAD` (or checkout the desired commit) on `main`.
  2. `git push origin main`.
  3. GitHub Actions will automatically rebuild and deploy the reverted static output to GitHub Pages within ~20 seconds.

## Backups

- `G:\My Drive\Desktop\Coding\Portfolio`: Full backup hash-verified; Git integrity passed.
- `W:\Desktop\Coding\Portfolio`: Drive unmounted; backup pending remount.
