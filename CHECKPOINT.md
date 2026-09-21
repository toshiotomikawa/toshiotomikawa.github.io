# Phase 2 — working prototype

Completed 2026-09-21. Homepage + full MGS case in English and Portuguese.
Local preview: http://127.0.0.1:4173/. Branch: `codex/working-prototype`.

## Implementation

- Adapted approved Claude Design's rendered markup/styles: Archivo, DM Mono,
  asymmetric layout, square markers, connected release steps, Light/Dark palettes.
  Claude archive/direct downloads did not produce a local file; no archive imported.
- Replaced prototype hash routing/runtime with static paths and shared source.
  Python standard-library renderer avoids duplicate templates; no client framework.
- Removed Claude's review toolbar and pending-contact footer. Contact/resume remain
  omitted; secondary projects have descriptive summaries, without dead case links.
- System → Light → Dark cycle, localized icon labels, visible focus, optional
  persistence, live system tracking only in System. Light is the script-free fallback.
- Explicit locale paths win. Neutral entry uses saved choice, primary browser locale,
  then English; equivalent pages and sections survive language switches.
- Slightly darkened Light muted text and link orange for at least 4.5:1 contrast
  on both backgrounds. Original orange markers retained.

## Verification

- 7 Node tests exercise the actual preference script through mocked DOM/storage/media
  boundaries: cycle, icons, labels, saved values, blocked storage, missing detection,
  live system changes, locale precedence, EN/PT/unsupported language, section links.
- 3 Python tests check all five generated pages, internal links/anchors, heading and
  language structure, script-free defaults, and text palette contrast.
- Chromium local browser: home → case → PT, direct case reload, theme persistence,
  Enter/Space activation, saved locale at root, equivalent section switch, Back.
- All four explicit pages: no horizontal overflow at 360, 390, 768, 1440px.
  Desktop homepage and mobile case visually inspected in Light/Dark.
- Separate preview returning no client script: English neutral entry, Light palette,
  hidden theme control, Portuguese switch and complete case navigation verified.
  This tests script-unavailable behavior; browser-wide JavaScript was not disabled.

## Boundaries / next checkpoint

Phase 2 is ready for review. Stop here. Next authorized phase: complete release
candidate, remaining cases, public contact/resume choices, full accessibility scan,
200% zoom, second browser, loading audit, release metadata and deployment preparation.
Actual OS preference changes were covered by mocked media events, not by changing
the user's system settings. Font/network-failure and assistive-technology checks remain.

No deployment or private-source publication. Pages rechecked: legacy `main`/root.
`dist/` carries `noindex` during prototype work; remove only for the approved release.
View count remains dated 2026-09-15; refresh or omit before launch. No MGS media rehosted.
Public email and resume remain unresolved; private review notes stay outside this repo.

## Repository / backup handoff

Prototype commit `b59328c` pushed to `codex/working-prototype`; `main` remains
`757a9d9`. No site deployment. Full G: backup passed SHA-256 comparisons and Git
integrity. W: is currently unmounted: its backup refresh is pending, not verified.
Reconnect W: before the next backup pass; do not substitute another destination.
