# PROJECT_STATE.md — janishammer-document-center
> Version 1.2 — 2026-11-10
> Changes: cookie-notice added (sixth document); build-tool limits recorded (CC_SESSION_saycheer_cookie_v1b)
> Previous: Version 1.1 — 2026-11-03 (hosting fix — first deploy failed (Workers project, no static-assets config); wrangler.jsonc added). Earlier: Version 1.0 — 2026-11-03 (first state)

## Status
- CC_SESSION_saycheer_cookie_v1b — DONE (pending owner QA). NOT VERIFIED LIVE — owner QA steps 1–2 on this order's PR. Sixth document added: cookie notice (id `cookie-notice`, page /cookie-notice, PDF /pdf/cookie-notice.pdf, version 1.0-draft, 2026-11-10, business `saycheer` "SayCheer by Janishammer", group `website`), EN + TH, DRAFT. The five earlier documents, their PDFs, index.html and 404.html are byte-identical (hashed before and after). The SayCheer cookie bar (saycheer-website#9) links to this page.
- CC_SESSION_docs_center_v1 — DONE (pending owner QA). NOT VERIFIED LIVE — owner QA steps 1–5.
- Five documents (studio rules, safety consent, equipment care and damage, privacy notice, trainer pool basic agreement), all version 1.0-draft, all "on": true, DRAFT banner on every page and PDF.
- Hosting: a Cloudflare Workers project `janishammer-document-center` (the dashboard offers no Pages option), publishing the repo root as static assets via wrangler.jsonc. First deploy FAILED ("Could not detect a directory containing static files", read from the owner's screenshot) until wrangler.jsonc was added. Domain docs.janishammer.com to be connected by the owner. NOT VERIFIED LIVE.

## Open items
- LIMIT of the build tool (reported, not changed beyond one SEO line): the read page and the PDF header take the issuer line and the DRAFT banner from the global `entity` and `banner` in documents.json, which are written for I-Flex ("operating I-Flex Pilates"; "an agreement between the studio and the renter"). The cookie notice therefore shows those two lines, which do not fit a SayCheer cookie notice; its own text names the right issuer (Janis Hammer Co., Ltd, operating SayCheer). A later order should add a per-document or per-business issuer and banner. Also: the tool rebuilds all documents and PDFs on every run (PDF bytes change), so the new document was built alone with the tool's own functions; an `--only <id>` option is wanted.
- The notice text has blanks on purpose: cookie lifetime (confirm against Google's current documentation) and data retention (set in the Google Analytics property). Thai wording is Chat's draft; the owner checks it (saycheer-website#9 step 5).
- Central wording still says "Cloudflare Pages" for this site (KNOWLEDGE_MAP, DEP-3 context) — Chat decides whether to correct it.
- Check after deploy that .git is not served as a public file (404 expected on /.git/config).
- LOGO PENDING — the cat logo is not on the pages (no single confirmed Cloudinary address); og:image / twitter:image omitted (SEO debt).
- Legal check (last) — the DRAFT banner stays until the owner lifts it.
- Thai wording must be read once by a Thai speaker (Chat's wording; copied verbatim).
- Privacy Notice retention period is blank on purpose (owner to set).
- Old Pilates Studio Manual migration — later order, with a 301 (DEP-5).
