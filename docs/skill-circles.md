# Portfolio chart data and methodology

Snapshot: **14 November 2026**. Scope: **23 public, non-archived project repositories** owned by jyotheshkar; excludes the profile repository and all private repositories. This dated snapshot is not automatically refreshed.

The four doughnut charts preserve proportional data representation. Arc lengths directly encode values; labels show rounded shares. Animation changes only opacity and a decorative outer highlight, never the measured segment size. Original project and brand artwork above this section remains unchanged.

## What the charts measure

- **Language footprint:** unique source-file bytes, classified by extension and deduplicated across repositories by Git blob hash. Excludes notebooks, dependencies, builds, data/report exports, historical original-work copies, minified files, TypeScript declarations and an identified revision-baseline HTML snapshot. HTML and CSS are included as web source. This is not GitHub Linguist, commit share, authorship share or proficiency.
- **Engineering, AI and Agentic AI:** one repository-topic match per selected category using root README and dependency manifests. Containers and CI/CD additionally use Dockerfile/workflow filenames. Agentic topics are restricted to repositories whose root README mentions agentic, RAG, tool calling or LLM agents. A repository can match multiple topics. The denominator is the sum of category matches, not the number of projects. These describe documented coverage, including concepts and study, and do not establish implementation, mastery or a deployed system. Text can mention limitations or proposed work; matches should be read with the linked project context.

All per-file language bytes and topic evidence excerpts, paths and Git hashes are in [the evidence data](../config/portfolio-metrics.json). Category rules are in [the summarizer](../scripts/summarize_portfolio.py). This avoids invented skill percentages. Exact duplicate blobs contribute to language totals once; related but non-identical versions may still be represented.

## Language footprint

Total: 3,181,753 bytes.

| Category | Value | Share |
|---|---:|---:|
| Python | 2,504,469 | 78.7% |
| TypeScript | 401,827 | 12.6% |
| JavaScript | 146,057 | 4.6% |
| HTML | 98,695 | 3.1% |
| CSS | 24,315 | 0.8% |
| SQL | 6,390 | 0.2% |

## Engineering stack

Total: 47 matches.

| Category | Value | Share |
|---|---:|---:|
| CI / CD | 17 | 36.2% |
| Testing | 6 | 12.8% |
| SQL databases | 5 | 10.6% |
| AWS | 5 | 10.6% |
| Node.js / npm | 4 | 8.5% |
| Backend APIs | 4 | 8.5% |
| React | 3 | 6.4% |
| Containers | 3 | 6.4% |

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

Total: 15 matches.

| Category | Value | Share |
|---|---:|---:|
| Tracing / evals | 3 | 20.0% |
| Planning | 2 | 13.3% |
| Tool use | 2 | 13.3% |
| Memory / state | 2 | 13.3% |
| Orchestration | 2 | 13.3% |
| Guardrails | 2 | 13.3% |
| RAG / retrieval | 1 | 6.7% |
| Human review | 1 | 6.7% |

## Build and validation

`python scripts/build_skill_circles.py` rebuilds the SVG offline from the evidence data. `python scripts/validate_profile.py` checks the chart keys, legend labels, totals and each segment's proportional arc length against that data. CI checks deterministic output. SVG titles, descriptions, README alt text, this text table and a reduced-motion fallback support accessibility.

To update the snapshot, collect the current public repository recursive Git trees and root README/dependency manifests using GitHub, retaining tree and blob hashes. Supply a JSON object with `captured_at`, `scope`, `repositories` (repo, tree_sha, files with path/sha/size), and `evidence` (repo/path/sha/content) to `python scripts/summarize_portfolio.py snapshot.json`. Inspect classifications and exclusions, rebuild, validate and advance the README's immutable SVG revision after committing the verified asset. Do not include private repositories.

The old 3D calendar and snake remain historical files; their scheduled refresh workflow is removed. GitHub's native contribution section is unaffected.
