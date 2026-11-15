# Portfolio chart data and methodology

Source capture: **14 November 2026**. Curated: **15 November 2026**. Scope: **22 retained repository snapshots** from public, non-archived projects owned by jyotheshkar at capture time; excludes the profile repository and private repositories. Names and visibility describe the capture date, not the current GitHub inventory. This dated snapshot is not automatically refreshed.

The four doughnut charts preserve proportional data representation. Arc lengths directly encode values; labels show rounded shares. Animation changes only opacity and a decorative outer highlight, never the measured segment size. Original project and brand artwork above this section remains unchanged.

## What the charts measure

- **Language footprint:** unique source-file bytes, classified by extension and deduplicated across repositories by Git blob hash. Excludes notebooks, dependencies, builds, data/report exports, historical original-work copies, minified files, TypeScript declarations and an identified revision-baseline HTML snapshot. HTML and CSS are included as web source. This is not GitHub Linguist, commit share, authorship share or proficiency.
- **Engineering, AI and Agentic AI:** one repository-topic match per selected category using root README and dependency manifests. Containers and CI/CD additionally use Dockerfile/workflow filenames. Agentic topics are restricted to repositories whose root README mentions agentic, RAG, tool calling or LLM agents. A repository can match multiple topics. The denominator is the sum of category matches, not the number of projects. These describe documented coverage, including concepts and study, and do not establish implementation, mastery or a deployed system. Text can mention limitations or proposed work; matches should be read with the linked project context.

All per-file language bytes and topic evidence excerpts, paths and Git hashes are in [the evidence data](../config/portfolio-metrics.json). Category rules are in [the summarizer](../scripts/summarize_portfolio.py). This avoids invented skill percentages. Exact duplicate blobs contribute to language totals once; related but non-identical versions may still be represented.

## Language footprint

Total: 2,857,215 bytes.

| Category | Value | Share |
|---|---:|---:|
| Python | 2,310,492 | 80.9% |
| TypeScript | 401,827 | 14.1% |
| HTML | 98,695 | 3.5% |
| CSS | 24,315 | 0.9% |
| JavaScript | 15,496 | 0.5% |
| SQL | 6,390 | 0.2% |

## Engineering stack

Total: 44 matches.

| Category | Value | Share |
|---|---:|---:|
| CI / CD | 16 | 36.4% |
| Testing | 6 | 13.6% |
| SQL databases | 5 | 11.4% |
| AWS | 4 | 9.1% |
| Backend APIs | 4 | 9.1% |
| Node.js / npm | 3 | 6.8% |
| React | 3 | 6.8% |
| Containers | 3 | 6.8% |

## AI & machine learning

Total: 22 matches.

| Category | Value | Share |
|---|---:|---:|
| Model evaluation | 5 | 22.7% |
| Scikit-learn | 4 | 18.2% |
| PyTorch | 3 | 13.6% |
| Transformers | 3 | 13.6% |
| Embeddings | 3 | 13.6% |
| NLP | 2 | 9.1% |
| TensorFlow | 1 | 4.5% |
| Reinforcement learning | 1 | 4.5% |

## Agentic AI focus

Total: 13 matches.

| Category | Value | Share |
|---|---:|---:|
| Tracing / evals | 2 | 15.4% |
| Planning | 2 | 15.4% |
| Tool use | 2 | 15.4% |
| Memory / state | 2 | 15.4% |
| Orchestration | 2 | 15.4% |
| Guardrails | 1 | 7.7% |
| RAG / retrieval | 1 | 7.7% |
| Human review | 1 | 7.7% |

## Build and validation

`python scripts/build_skill_circles.py` rebuilds the SVG offline from the evidence data. `python scripts/validate_profile.py` checks the chart keys, legend labels, totals and each segment's proportional arc length against that data. CI checks deterministic output. SVG titles, descriptions, README alt text, this text table and a reduced-motion fallback support accessibility.

To update the snapshot, collect the current public repository recursive Git trees and root README/dependency manifests using GitHub, retaining tree and blob hashes. Supply a JSON object with `captured_at`, `scope`, `repositories` (repo, tree_sha, files with path/sha/size), and `evidence` (repo/path/sha/content) to `python scripts/summarize_portfolio.py snapshot.json`. Inspect classifications and exclusions, rebuild, validate and advance the README's immutable SVG revision after committing the verified asset. Do not include private repositories.

The old 3D calendar and snake remain historical files; their scheduled refresh workflow is removed. GitHub's native contribution section is unaffected.
