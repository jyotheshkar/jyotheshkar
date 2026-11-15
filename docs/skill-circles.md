# Professional Skills: repository evidence

The three charts are **Programming Languages**, **Libraries and Frameworks**, and **Agentic AI Engineering**. Each is a segmented doughnut with skill names and proportional bars to its right. The GitHub dark palette matches the overview. The artwork prints no percentages, counts, calculations or proficiency scores.

The current evidence, source paths, exact Git blob hashes and scan coverage are in [skill-evidence.json](../config/skill-evidence.json). It replaces the historical portfolio snapshot as the source of the displayed skills.

## What the charts measure

- **Programming Languages:** extension-classified source bytes in current public repositories. Identical Git blobs are counted once across repositories. Notebooks, HTML/CSS markup, data/report exports, dependency folders, generated builds and archived snapshots are excluded. This is a repository source footprint, not authorship or ability.
- **Libraries and Frameworks:** repositories with a verified runtime dependency or implementation import from a selected library catalog. Development dependencies are excluded. Long Python environment freezes are not accepted without implementation imports. A dependency establishes use within a repository, not mastery.
- **Agentic AI Engineering:** implementation symbols or executable configuration for orchestration, tool execution, retrieval, state, approvals, guardrails, evaluation and routing. Matches are restricted to agent, RAG or Rufus repositories. README claims, documentation and tests do not qualify as implementation evidence. Presence does not imply that a workflow is deployed or operationally reliable.

A repository can support several skill categories. Doughnut slices divide each group's total evidence. Bars compare each item with the largest item in its group. They are not personal skill ratings. Zero-evidence categories are omitted rather than invented.

## Scope and refresh

Every refresh retrieves the current public repository inventory for `jyotheshkar`. Private, forked and archived repositories and the profile repository are excluded. Deleted repositories disappear from the next successful capture.

The collector inspects complete recursive trees and a bounded sample of up to six dependency manifests and twelve implementation files per repository. Previously verified source files are retained while they exist; remaining slots prioritize runtime, agent, engine, retrieval, evaluation and model code. The initial connector-assisted capture may include additional verified implementation files. Exact scanned files are recorded. This is a bounded evidence sample, so absence does not prove a skill is missing.

The [profile workflow](../.github/workflows/profile-metrics.yml) refreshes **hourly at minute 17**, on changes to the profile source and through **Run workflow**. GitHub may delay scheduled runs. A repository change is reflected after the next successful scan and GitHub image cache refresh; a README cannot perform real-time browser API requests.

A failed or truncated API response aborts the refresh instead of publishing an incomplete scan. A newly created, zero-size repository returning GitHub's empty-tree response is skipped because it contains no source evidence. Changes made to a repository during capture are detected using blob hashes. The workflow publishes only the chart and its evidence JSON, and creates no new commit when the evidence is unchanged. The evidence timestamp records the last material snapshot; workflow run history records subsequent checks.

## Rebuild

```bash
python scripts/refresh_skill_evidence.py
python scripts/build_skill_circles.py
python scripts/validate_profile.py
```

Online refresh uses Python's standard library and GitHub's public REST API. `GITHUB_TOKEN` raises the rate limit in GitHub Actions. The same renderer can be rebuilt offline from the checked-in evidence JSON. An optional `--api-cache` argument supports reproducing a captured API response set.

README image links follow the current default branch, so updates to the generated chart are visible without changing a commit-pinned image URL.

