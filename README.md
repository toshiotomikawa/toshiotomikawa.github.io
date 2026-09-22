# Yuri Toshio Tomikawa: Portfolio

English/Portuguese portfolio for LATAM remote operations-management roles.

## Current milestone

Phase 2: working homepage and MGS case, adapted from the approved Claude Design.
The prototype stays on `codex/working-prototype`; **not deployed**. GitHub Pages
currently publishes `main` at the repository root.

## Preview

Requires Python 3.12+; no installation or runtime framework needed.

```powershell
python scripts/build.py
python scripts/preview.py
```

Open http://127.0.0.1:4173/. Explicit routes: `/en/`, `/pt/`,
`/en/work/mgs/`, `/pt/work/mgs/`. Stop the preview with Ctrl+C.

## Structure

- `content/`: matching EN/PT copy.
- `assets/site.css`: shared Claude-derived design, responsive layouts, both palettes.
- `assets/preferences.js`: theme and locale enhancement; content does not depend on it.
- `scripts/build.py`: dependency-free static renderer. Generated `dist/` is ignored.
- `tests/`: preference-contract, route, static-content, and palette checks.

The small build script shares markup across languages and pages without shipping
a framework. Google Fonts supplies Archivo and DM Mono; system fonts are the fallback.

## Verification

```powershell
python scripts/build.py
python tests/static_test.py
node --test tests/preferences.test.cjs
```

Node is only needed for the preference tests. To inspect script-unavailable behavior:

```powershell
python scripts/preview.py --port 4174 --without-script
```

See [CHECKPOINT.md](CHECKPOINT.md) for checked behavior and remaining scope;
[PLAN.md](PLAN.md) for delivery gates; [AGENTS.md](AGENTS.md) for project guidance.
