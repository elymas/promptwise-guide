# FRAME / NOTES

An independent Korean directing guide and attributed PromptWise reference library, with newly generated Claire educational examples published as 480p drafts.

Site: https://elymas.github.io/promptwise-guide/

## Development

Requires Node.js 22.12+ and pnpm 9.

```sh
pnpm install --frozen-lockfile
pnpm dev
pnpm build
pnpm preview
```

Astro static output. The GitHub Pages project base is `/promptwise-guide/`. `main` publishes through `.github/workflows/deploy.yml`; workflow setup follows the existing `elymas.github.io` hub's Astro/Actions conventions. No backend or generation credentials are used by this site.

## Content

- 2026-11-18 scan: numbered source pages 1–500, 29 HTTP 200, 471 HTTP 404, zero request errors.
- 29 archived HTML pages, 28 unique base pages; duplicate 002/014 omitted from catalog.
- 29 content versions and 270 copy blocks after including the separate 025 replacement.
- PW-106 added on 2026-11-18. PW-087 differs only in newline transport, not normalized text.
- Counts include templates, short instructions and examples; they do not count completed videos.
- `src/data/catalog.json` and `public/data/catalog.json` contain the same attributed public catalog.
- `src/data/media.json` is the source of truth for generated examples. Planned, draft and reviewed media are distinct; a schematic diagram is never presented as a generated result.

Source project: `/Users/masterp/orca/projects/fanvue-initiate/library/prompts/` (local authoring reference; not required for builds). Source audit and export scripts live in that project's `tools/prompts/`.

For updates: run the source scan, review changes, ingest, update the Korean guide, run the catalog exporter, synchronize the two public catalog copies, then build. Source snapshots and generated private job receipts stay outside this repository. Never add API keys, signed generation download URLs or account details.

## Attribution

Original reference text: PromptWise (`https://promptwise-free.vercel.app/`). Individual blocks link to their source and retain content hashes. The 025 archive differs from the current remote page; both versions are labeled. Third-party reference text/assets are not relicensed as open source. This is not an official PromptWise, IDALL or Tein site.

## Example production

New examples feature the adult fictional Claire Yoon (27). Eight approximately 6-second silent 16:9 examples are published as 480p drafts, with per-clip observations. The story example illustrates a midpoint performance, not an entire five-step story. Prior Fanvue videos are not reused. Generation and publication status are recorded in the media manifest. The provider returns 864×496 H.264 drafts; public copies are fit and padded to 854×480 without stretching or adding audio. 720p final production remains subject to draft review and its separate budget.
