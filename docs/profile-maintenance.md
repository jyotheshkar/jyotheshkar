# Connected GitHub profile

The README uses a repository-hosted animated SVG canvas followed by four animated skill circles. The continuous grid, conceptual agent network and translucent career panels are drawn in one image so the page does not depend on README CSS or scripts in Markdown. Contact links are in the GitHub sidebar. The closing slogan, opportunity text, action buttons and repository-year note were removed from the displayed profile.

The main canvas is referenced by its verified commit revision to avoid stale branch-image caching. When changing it, advance the README image revision after the new SVG has been committed and validated.

## Rebuild and validation

```sh
python scripts/import_brand_icons.py
python scripts/build_profile.py
python scripts/build_skill_circles.py
python scripts/validate_profile.py
```

The builder uses only Python's standard library and the local brand registry. The network section provides animated tool-routing paths and a reduced-motion fallback. The career section contains ordinary professional facts approved in Atlas: Amazon AGI Data Services and three prior roles, plus the Keele MSc, Distinction, award and dissertation.

## Meaning of the network

The heading is "Current Agentic AI Projects I Am Working On". It branches to two concept projects, each with exactly eight tool nodes. The YouTube Agent Concept includes Gemini, Google Search, Gmail, Google Drive, AI Studio, Google Cloud, Python and GitHub. The Crypto Agent Concept includes Binance, Bitcoin, Ethereum, Solana, Python, PostgreSQL, OpenAI and Redis. The Google tools support discovery, planning and review; the crypto tools illustrate research, analysis, model reasoning and evidence storage.

Routes are decorative. They do not establish connected accounts, implemented adapters, trading automation, investment holdings or endorsements. Both projects are explicitly labelled concepts, with human review in the loop. The experience and education section remains separate from these independent project ideas.

## Brand provenance

`assets/brands/color-originals.json` retains the upstream color SVG source and exact Git blob hashes. `scripts/import_brand_icons.py` verifies those hashes offline and regenerates the matching entries in `assets/brands/icons.json`. Internal gradient and mask IDs are prefixed per brand to prevent collisions. Optional `--download` retrieves the exact pinned Git blobs and verifies their hashes before replacing the local originals. Normal builds use no network access.

Upstream multicolor fills and gradients are preserved, including Gmail, Google Drive, Gemini, Python and Solana. OpenAI, GitHub and AI Studio retain their white dark-background variants. Binance uses official gold. A light backing badge makes Ethereum's original gray facets legible. `assets/profile-icon-sources.json` is generated from the current project definitions and records the 8+8 node lists and icon provenance. `docs/brand-sources.json` records attribution and source/license details. Simple Icons, Lobe Icons, Devicon and SVG Logos license files are retained beside the registry. Logos identify ecosystem services; respective owners retain their trademarks.

Validation checks all local SVGs and README links, rejects active or external embedded resources, and checks the live canvas for duplicate IDs, unresolved local symbol/gradient references and exactly eight tool nodes per concept. CI also rebuilds the generated profile assets to detect stale output.

The Keele white logo is the unmodified transparent PNG from the university's official logo ZIP:
https://www.keele.ac.uk/media/keeleuniversity/brand/logos/keele-logo.zip
The profile builder embeds it locally; no remote asset is loaded when the profile is viewed.

## Retained history

Earlier orb, diagram, project-gallery, action-button and telemetry assets remain as historical source; the current README does not display them. Automatic repository telemetry refresh is disabled. The profile validation workflow has read-only access; the old contribution refresh workflow has been removed. The qualitative circles are documented in [skill-circles.md](skill-circles.md). The profile does not claim an Amazon affiliation for independent projects or a production deployment.
