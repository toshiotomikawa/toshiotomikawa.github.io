# Project guidance

## Goal and state
- Build Yuri Toshio Tomikawa's public portfolio to land an operations manager role; creative operations is relevant but must not limit positioning.
- Highlight substantial AI experience through concrete workflows, decisions, and outcomes. The portfolio itself should demonstrate these capabilities; new showcase project ideas are welcome.
- Repository: https://github.com/toshiotomikawa/toshiotomikawa.github.io.git
- Planning stage: target role established; market, content, design, and stack remain undecided. No site implemented or deployment verified.
- Resume reviewed through Google Drive: Portuguese, English, and TubeScience variants. Background includes international studio operations, teaching, community moderation, and products built using coding agents. Target positioning comes from the user's current direction, not a resume variant.
- Authenticated GitHub access can read private projects. Assess candidates by operational problem, personal contribution, workflow, and demonstrated outcome; documentation alone does not establish current runtime success or business impact.
- Private-project review is authorized for planning, not blanket publication. Keep private source, client information, resume contact details, and NDA-covered work out of public artifacts unless approved for publication. Public case studies can use approved summaries and synthetic demos without opening repositories.
- Next discovery question: which hiring market should the portfolio target?

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
