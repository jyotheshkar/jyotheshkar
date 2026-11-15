# Portfolio chart data and methodology

Source capture: **14 November 2026**. Curated: **15 November 2026**. Scope: **22 retained repository snapshots**, captured from public, non-archived projects. Names and visibility describe the capture date, rather than today's GitHub inventory. Private projects and the profile repository are excluded.

The three circles occupy one horizontal row: **Languages**, **AI & Machine Learning**, and **Agentic AI Engineering**. The presentation restores the original [orbital design](https://github.com/jyotheshkar/jyotheshkar/commit/59a6df4e4a41091c96c61f827f84c4efeb45c964): dark grid, blue halos, concentric rings, colored tool nodes and decorative moving routes. Original brand artwork retains its source colors.

The measured arcs retain the evidence proportions. Labels and tooltips show raw bytes or repository counts; no percentage labels or proficiency scores are displayed. Nodes and legends remain still; moving orbit highlights and dotted routes are decorative. Reduced motion is supported.

## What the data measures

- **Languages:** source-file bytes classified by extension and deduplicated across repositories by Git blob hash. Notebook/data/report exports, dependencies, build output, historical original-work copies, minified source, TypeScript declarations and an identified HTML revision baseline are excluded. This is source coverage, rather than GitHub Linguist, contribution share or authorship.
- **AI and engineering topics:** one repository match per selected category based on captured README and dependency evidence. CI/CD and container categories also use workflow/Dockerfile names. A repository can appear in several categories, so the sum counts topic matches rather than distinct repositories. Text may describe study, concepts, limitations or proposed work; a match alone does not establish a deployed capability.
- **Merged engineering circle:** preserves all eight Engineering Stack categories and all eight Agentic AI categories as sixteen distinct topics. The total is **44 + 13 = 57 topic matches**. Software-stack categories retain their original portfolio-wide scope; they are not relabeled as evidence that every project is an agent.

The immutable captured values, paths, repository names and Git hashes remain in [portfolio-metrics.json](../config/portfolio-metrics.json). The original four source groups remain intact; the builder combines two only for display. No source evidence was added or recounted for this styling change.

## Languages

Total: **2,857,215 bytes**.

| Category | Source bytes |
| --- | ---: |
| Python | 2,310,492 |
| TypeScript | 401,827 |
| HTML | 98,695 |
| CSS | 24,315 |
| JavaScript | 15,496 |
| SQL | 6,390 |

## AI & Machine Learning

Total: **22 topic matches**.

| Category | Repositories |
| --- | ---: |
| Model evaluation | 5 |
| Scikit-learn | 4 |
| PyTorch | 3 |
| Transformers | 3 |
| Embeddings | 3 |
| NLP | 2 |
| TensorFlow | 1 |
| Reinforcement learning | 1 |

## Agentic AI Engineering

Total: **57 topic matches**.

| Category | Repositories |
| --- | ---: |
| CI / CD | 16 |
| Testing | 6 |
| SQL databases | 5 |
| AWS | 4 |
| Backend APIs | 4 |
| Node.js / npm | 3 |
| React | 3 |
| Containers | 3 |
| Tracing / evals | 2 |
| Planning | 2 |
| Tool use | 2 |
| Memory / state | 2 |
| Orchestration | 2 |
| Guardrails | 1 |
| RAG / retrieval | 1 |
| Human review | 1 |

## Build and validation

Run `python scripts/build_skill_circles.py`, then `python scripts/validate_profile.py`. Validation checks the three-circle row, both source groups in the merged circle, legend/node coverage, exact totals, proportional arc lengths, local icon references and absence of numeric percentage labels. CI also checks deterministic SVG output.

The profile README pins the chart SVG to its verified asset commit. The YouTube/Crypto Agent artwork above it is unchanged.
