# PROJECT_STATE.md — janishammer-document-center
> Version 1.1 — 2026-11-03
> Changes: hosting fix — first deploy failed (Workers project, no static-assets config); wrangler.jsonc added
> Previous: Version 1.0 — 2026-11-03 (first state)

## Status
- CC_SESSION_docs_center_v1 — DONE (pending owner QA). NOT VERIFIED LIVE — owner QA steps 1–5.
- Five documents (studio rules, safety consent, equipment care and damage, privacy notice, trainer pool basic agreement), all version 1.0-draft, all "on": true, DRAFT banner on every page and PDF.
- Hosting: a Cloudflare Workers project `janishammer-document-center` (the dashboard offers no Pages option), publishing the repo root as static assets via wrangler.jsonc. First deploy FAILED ("Could not detect a directory containing static files", read from the owner's screenshot) until wrangler.jsonc was added. Domain docs.janishammer.com to be connected by the owner. NOT VERIFIED LIVE.

## Open items
- Central wording still says "Cloudflare Pages" for this site (KNOWLEDGE_MAP, DEP-3 context) — Chat decides whether to correct it.
- Check after deploy that .git is not served as a public file (404 expected on /.git/config).
- LOGO PENDING — the cat logo is not on the pages (no single confirmed Cloudinary address); og:image / twitter:image omitted (SEO debt).
- Legal check (last) — the DRAFT banner stays until the owner lifts it.
- Thai wording must be read once by a Thai speaker (Chat's wording; copied verbatim).
- Privacy Notice retention period is blank on purpose (owner to set).
- Old Pilates Studio Manual migration — later order, with a 301 (DEP-5).
