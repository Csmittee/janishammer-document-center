# CLAUDE.md — janishammer-document-center
> Version 1.2 — 2026-11-10
> Changes: link constraint — WF-12 stable document addresses may be linked from a site named in an order (first: /cookie-notice from SayCheer); cookie-notice added to the stable URLs (CC_SESSION_saycheer_cookie_v1b)
> Previous: Version 1.1 — 2026-11-03 (hosting line — Cloudflare Workers static assets (wrangler.jsonc), not a Pages project). Earlier: Version 1.0 — 2026-11-03 (seed, CC_SESSION_docs_center_v1)

Project: Janishammer Document Center — https://docs.janishammer.com (Cloudflare Workers static assets, auto-deploy from main, no build command; config: wrangler.jsonc, .assetsignore).
Purpose: hidden reference site for business documents (rental rules, consent, privacy, agreements). Rules live in janishammer-central (START_HERE.md, RULES.md; house rule WF-12 in RULES-workflow.md).

House rules (only two here):
  1. ARCHIVE: before a document is changed, copy its current `src/<id>.md` and `pdf/<id>.pdf` to
     `archive/<id>/v<version>-<YYYY-MM-DD>/`, then change it. Archived files are never deleted or edited.
  2. HEADER REVISION: a changed document gets a new version (X.Y) and date in its header and in `documents.json`;
     status stays DRAFT until the owner lifts it; CC_CHAT_LOG says what changed.
  The issuer line always names Janishammer first, never a person.

Constraints:
  - Hidden: noindex, nofollow on every page (meta) and file (_headers); NO sitemap.xml; NO robots.txt; NO link from any other site, except the stable document addresses that a site must link under WF-12 (named in an order; first: /cookie-notice from saycheer.janishammer.com); NO injector.
  - The document URLs are STABLE (/studio-rules, /safety-consent, /equipment-care-damage, /privacy-notice, /trainer-pool-agreement, /cookie-notice). A move needs a `_redirects` 301 first (DEP-5).
  - Sources: `src/*.md` and `documents.json`. Built outputs: `*.html` (except index.html, 404.html) and `pdf/*.pdf` — never hand-edit; a CC order re-runs `tools/build_docs.py`.
  - `"on": false` in documents.json hides a document from the list but does NOT make it private: anyone with the exact file address can open it. documents.json is public. Nothing private goes in.
  - The DRAFT banner (documents.json `banner`) stays until the owner lifts it after the legal check.
  - No secrets. No image files committed (Cloudinary only, CONT-4). No bank details, no LINE links.
  - 404.html must exist; wrangler.jsonc has not_found_handling "404-page" so unknown addresses show it. Do not rename wrangler.jsonc or the project (WORKER CHANGE NOT REQUIRED, DEP-7).
