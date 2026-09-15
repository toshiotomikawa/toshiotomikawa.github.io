# Portfolio delivery plan

## Objective
Help LATAM remote employers assess Yuri Toshio Tomikawa for operations management through clear evidence of ownership, team coordination, process improvement, and practical AI use.

## Working scope
- Restrained, professional homepage: introduction, selected work, experience, resume, contact.
- Two core case studies: MGS operations and MapaFinanceiro. Biosphere illustrates delivery within the broader MGS role; it must not turn the case study into a design-only showcase. Add one supporting case study (Grok MCP Bridge or Togurumi) only if the available evidence clearly demonstrates operational value. Technical complexity alone is not a selection criterion.
- English and Portuguese. At the neutral entry URL, use a saved manual choice if available; otherwise inspect the primary browser language, select Portuguese for `pt`/`pt-*`, and English for everything else. Explicit `/en/` and `/pt/` URLs override saved choices and detection. A visible switch preserves the equivalent page and remembers the choice when storage is available. English content and language links remain usable without JavaScript or storage. A website reads browser language preferences, not the operating system directly.
- Case studies: problem, responsibility, decisions, implementation, evidence, limitations; distinguish individual work from collaborators' contributions.
- Default architecture: semantic HTML, shared CSS, minimal JavaScript, and static language/case-study paths suitable for GitHub Pages. Introduce a small build tool only if it materially reduces duplicated content; record the reason. No backend, CMS, chatbot, analytics, contact form, or new service accounts in version one. Contact uses approved public links.
- The site demonstrates clear communication and reliable execution. Use screenshots and an optional short walkthrough with synthetic examples; do not rebuild MapaFinanceiro calculations. New simulators and additional showcase projects are deferred.

## Execution contract
- This is the audited plan. No portfolio implementation starts until the user continues.
- Each user instruction to continue authorizes the next phase. Complete its routine work and verification autonomously, then stop at its checkpoint.
- Do not pause between individual tasks. Ask only for missing information that materially blocks the phase, one question at a time; continue independent work when possible.
- Revisions requested at a checkpoint stay in that phase unless the user also authorizes advancing.
- At each checkpoint: deliver concrete reviewable artifacts, summarize completion and gaps concisely, update AGENTS.md and this plan, create focused commits for publishable changes, and refresh/verify both full backups. Avoid intermediate WIP commits; inspect staged paths and diffs before committing. Do not rewrite existing published history without a specific reason and authorization.
- This repository is public, including every pushed branch and commit. Ordinary copy based on already approved public facts does not need separate permission per edit. Keep private evidence, unapproved personal/client details, and restricted source/assets outside it; resolve any remaining publication choices together at the content checkpoint. Never copy entire private repositories into the portfolio. Approval for an excerpt does not authorize its underlying source.
- Keep private review notes in `C:\Users\Zen\Desktop\Coding\Portfolio-review`, outside the repository. Record the notes location and checkpoint status without private content in AGENTS.md. Repository backups do not cover that separate directory; report that distinction, and do not copy private notes to the shared backup destinations automatically.
- Check current GitHub Pages configuration before pushing site-bearing files: a push can deploy automatically. Until launch is authorized, keep previews local or use a branch verified not to publish. Documentation pushes are distinct from launch approval.

## Phase 1 — Content and evidence
Work:
- Consolidate existing answers and the supplied MapaFinanceiro report; ask only about consequential gaps. Review up to three representative, current LATAM-eligible operations vacancies to test positioning, not to invent qualifications or turn this into a broad job search. Keep employer requirements separate from demonstrated experience.
- Limit repository research to the selected candidates and material claims. Reuse the supplied report, verify public work links, and distinguish documented features from demonstrated behavior. No exhaustive code audit, paid model calls, device changes, production mutations, or implementation work in other projects.
- Draft the English homepage and two core case studies, plus at most one supporting case study. Keep homepage copy around 300 words or fewer and each case study around 400 words or fewer, excluding captions/credits. Lead with responsibility and decisions, not tool lists. Translate the proposed headline early to catch positioning problems in both languages.
- Maintain a compact claim/evidence list: claim, source/version/date, contribution, verification status, publication status. User-reported experience is usable when accurately attributed; absent quantitative metrics must not block launch. Include supported qualitative outcomes instead. No demand for exhaustive recall, testimonials, or confidential records.
- Inventory screenshots/video links, resume variants, and contact options; identify what can be published. Do not invent metrics or make financial guarantees.

Deliverable: homepage/case-study drafts, section outline, and a compact evidence/assets list with unresolved publication choices. Private review material stays outside the public repository.

Stop: user reviews positioning, claims, selected projects, and proposed public material. The content checkpoint is complete when each core case has a clear responsibility, concrete work sample, and supportable outcome or deliverable; optional gaps are omitted or deferred. No visual build yet.

## Phase 2 — Working visual prototype
Work:
- Confirm the default static architecture, route scheme, and unpublished preview method; inspect Pages settings before any site-bearing push. Establish maintainable page/content structure and shared visual styles.
- Build the homepage and one representative case study with approved content, desktop/mobile layouts, and genuine navigation.
- Implement initial locale selection and manual switching; include enough translated content to demonstrate both languages.
- Use neutral colors, readable typography, restrained motion, and prominent work samples. Establish semantic headings, keyboard access, visible focus, contrast, and reduced-motion support now. Label any temporary placeholders; avoid adding interactions merely to demonstrate technical ability.
- Check the prototype at desktop and mobile sizes and exercise its navigation and language controls.

Deliverable: local browser preview and screenshots showing the actual design, not only a written concept.

Stop: user reviews layout, hierarchy, tone, and interaction before the design spreads across the site. The prototype must show the operations positioning, a complete example case, and working language/navigation behavior at desktop and mobile sizes.

## Phase 3 — Complete, validate, and prepare launch
Work:
- Apply the accepted design to all selected case studies, experience, resume, and contact sections.
- Complete and proofread English/Portuguese content; preserve factual equivalence and attribution.
- Add optimized, approved images and public work links. Include a short MapaFinanceiro walkthrough only if agreed, using synthetic data. Credit the Biosphere composer and original logo designer appropriately; verify and date any view count or omit it. Avoid heavy automatic third-party embeds; use preview links or click-to-load media where appropriate.
- Complete the accessibility work established in Phase 2, page titles, language metadata, share previews, and missing-page handling. Keep core content readable when scripts fail.
- Keep supplementary projects secondary to operations evidence. Remove placeholders and dead controls.

- Run the production build if one exists and focused automated checks for meaningful behavior; avoid snapshot or implementation-mirroring tests without value.
- Verify direct case-study links, refresh behavior, assets, resume/contact links, browser history, language detection (pt-BR, pt-PT, en, unsupported locale), manual override persistence, explicit language links, and unavailable storage/JavaScript.
- Acceptance: both languages complete; no placeholders, broken internal links, horizontal overflow at 360/390/768/1440px, keyboard traps, or missing accessible names on controls. Check visible focus, text contrast, and 200% zoom. Run an accessibility scan and address serious/critical findings, without treating a scan as complete accessibility certification.
- Check mobile loading performance using the production output, document the tool/settings and observed results, and fix avoidable blocking assets or layout shifts. Do not claim universal device performance from a local audit. Browse in Chromium and another available engine; report any unavailable browser/device coverage honestly.
- Review publication scope, claims/credits, dependency needs, public files, and Git history. Ensure no private material or development-only artifacts are included.
- Inspect GitHub Pages readiness and prepare the exact release/deployment steps, rollback procedure, and concise maintenance instructions without publishing the site.

Deliverable: complete tested release candidate in both languages, concise verification summary, reviewed public-file list, and concrete deployment/rollback plan. Record the release commit and approved publication choices; any remaining material defect blocks launch, optional enhancements do not.

Stop: user reviews the complete tested site. Apply requested revisions and repeat only affected checks within this phase. State plainly that the next continue authorizes publication of the reviewed version in Phase 4; do not infer launch approval from a request for revisions.

## Phase 4 — Publish and verify
Work:
- Publish the reviewed release to GitHub Pages; configure the required deployment workflow/settings as needed.
- Verify the live URL, HTTPS, assets, navigation, direct links, both languages, resume/contact, and mobile layout. Mark deployment complete only after actual live verification; a successful push is not enough. If hosting is blocked, leave the tested candidate and name the blocker without expanding into unrelated infrastructure work.
- Record the deployed commit and rollback steps; update project guidance and refresh/hash-verify both full backups, including Git integrity.

Deliverable: live portfolio URL, deployment verification, and maintenance handoff.

Stop: first version complete. Further projects or features become separate work.

## Current checkpoint
- Phase 1 drafted and verified on 2026-09-15; awaiting user content review. No portfolio implementation started.
- Review packet: `C:\Users\Zen\Desktop\Coding\Portfolio-review\REVIEW.md`; English homepage and three case-study drafts in `CONTENT.en.md`; evidence/assets and hiring comparison in `EVIDENCE.md`; local source hashes in `LOCAL-SOURCE-HASHES.txt`. These remain outside the public repository and its backups.
- Core cases: MGS operations and MapaFinanceiro. Proposed supporting case: Grok MCP Bridge, explicitly labeled a personal local project. Headline proposal: "Operations management, with practical AI." / "Gestão de operações com uso prático de IA."
- Verified public Biosphere work link and Mapa page rendering with one synthetic-input recalculation. Reviewed three current LATAM operations/automation-adjacent listings. No exhaustive audit, financial validation, live Grok call, resume edit, or deployment performed.
- Public contact address and final resume/media choices remain unresolved; they do not block independent prototype work. Link-first MGS evidence avoids depending on rehosted artwork.
- Next phase on user instruction to continue: Phase 2, working visual prototype. Requested content revisions stay in Phase 1 unless advancement is also authorized.
