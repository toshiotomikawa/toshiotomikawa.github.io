# Phase 3 — Release candidate

Completed 2026-09-21. Complete bilingual release candidate in English and Portuguese.
Local preview: http://127.0.0.1:4173/. Branch: `codex/working-prototype`.

## Implementation

- Implemented both core case studies (MGS operations and MapaFinanceiro) with dedicated static routes:
  `/en/work/mgs/`, `/pt/work/mgs/`, `/en/work/mapa/`, `/pt/work/mapa/`.
- Implemented Grok MCP Bridge supporting architecture card highlighting controlled task delegation,
  explicit diff reviews, and stable task IDs.
- Added Contact section (`mailto:toshiotomikawa@gmail.com` and GitHub profile) and on-page Resume
  qualifications summary with direct CV inquiry link.
- Added custom `/404.html` with bilingual copy, home redirection, and unified theme styles.
- Injected complete OpenGraph, Twitter card, canonical tags, and inline SVG favicon across all routes.
- Fully preserved cross-locale switching between all case studies (`/en/work/mapa/` ↔ `/pt/work/mapa/`).
- Verified WCAG AA contrast (≥ 4.5:1) for all typography against `--bg` and `--surface` in both palettes.

## Verification

- 7 Node unit tests in `tests/preferences.test.cjs`: preference script, theme cycle, live system
  tracking, storage fallbacks, language detection precedence, and section hash preservation.
- 5 Python static tests in `tests/static_test.py`: 7 generated routes, heading hierarchy (`h1` = 1),
  internal anchor targets, external URL validation, contrast math, cross-locale symmetry, and metadata.
- CDP browser test in `tests/cdp_browser_test.cjs`: automated headless Chromium testing covering:
  - 0 horizontal overflow (`scrollWidth <= innerWidth`) across 360, 390, 768, and 1440px for all 7 routes.
  - Interactive theme cycling (System → Light → Dark → System) via DOM button click.
  - Cross-locale navigation from MapaFinanceiro English to Portuguese and back home.
  - Verified across two independent browser binaries: Google Chrome and Microsoft Edge.
- Script-free fallback verified via `scripts/preview.py --without-script`: 0-byte script payload defaults
  cleanly to readable Light palette, working anchor links, and full static navigation.

## Boundaries / next checkpoint

Phase 3 release candidate is ready for review. Stop here. Next continue authorizes Phase 4 (publication to GitHub Pages), not further prototype iteration.
No deployment performed; GitHub Pages remains configured on legacy `main`/root.
Commit remains on `codex/working-prototype`. G: backup refreshed and hash-verified; W: is unmounted.
