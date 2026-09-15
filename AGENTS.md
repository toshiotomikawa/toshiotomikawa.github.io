# Project guidance

## Goal and state
- Build Toshio Tomikawa's public portfolio to land a job.
- Repository: https://github.com/toshiotomikawa/toshiotomikawa.github.io.git
- Planning stage: target role, audience, content, design, and stack remain undecided. No site implemented or deployment verified.
- Next discovery question: which role is the portfolio targeting?

## Collaboration
- Maximize information density. Use the fewest words that preserve meaning; omit repetition, filler, and unnecessary narration.
- Ask one question at a time.
- Establish requirements with the user before implementing the portfolio.
- Keep this file tracked and public. Include only shareable project guidance.
- Update this file at natural checkpoints: accepted decisions, scope changes, completed milestones, or handoffs. Replace stale facts; avoid a running conversation log. No update needed after every turn.

## Git and backups
- Use focused commits with clear messages; avoid noisy checkpoints, unrelated changes, generated files, and private artifacts.
- Preserve existing user changes. Keep commit identity on GitHub's no-reply email.
- Initial setup was pushed to `main`; verify live Git state before further work.
- Full backups include hidden files and `.git`:
  - `G:\My Drive\Desktop\Coding\Portfolio`
  - `W:\Desktop\Coding\Portfolio`
- Refresh backups at delivery checkpoints; verify file hashes and Git integrity. Never delete destination content blindly. Distinguish local changes, commits, pushes, backups, and deployments when reporting completion.

## Secrets
- Credentials may be consumed operationally, but plaintext secrets must never enter agent context, output, logs, reports, diffs, or repository files.
- Inspect individual key names, presence, or metadata only; never dump environment or secret maps. Use indirect consumption, write-only updates, and redacted wrappers.
- Verify secret updates through metadata or behavior without reading values back.
- If plaintext unexpectedly appears, stop that inspection path; do not reproduce, persist, or reuse it. Report affected key names only and fix the exposure mechanism before continuing.
