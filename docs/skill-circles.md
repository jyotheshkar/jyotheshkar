# Professional Skills: audit and maintenance

Three equally sized cards show **Programming Languages**, **AI/ML Engineering** and **Agentic AI Engineering**. Each has a centred doughnut and a two-column list of names with unnumbered bars below. Backgrounds are transparent. Desktop artwork presents a row; mobile artwork stacks the same cards. No percentages, calculations or proficiency scores appear in the artwork.

The current snapshot is [skill-evidence.json](../config/skill-evidence.json). Every slice and bar counts repositories containing verified source evidence for that category. A repository may support several categories. This measures project coverage, not ability, authorship, project quality or production reliability.

## What was audited

The full audit covers all accessible original repositories owned by this account, including private coursework and project repositories. Forks and the profile repository are excluded. Complete source trees establish language presence; implementation files and notebook code cells establish engineering topics. Build output, vendored dependencies, archive/snapshot copies, tests and prose documentation do not establish skills.

- **Programming Languages:** source file extensions plus inspected notebook code cells. PHP, SQL and notebook Python are included. JSP is recorded as a server-page template. The current JSP web project has Maven WAR packaging and an HTML-only JSP; this does **not** establish Java implementation. Java or Java (Processing) will appear only when actual .java or .pde source is present.
- **AI/ML Engineering:** implemented supervised and unsupervised learning, deep learning, reinforcement learning, NLP/transformers, time-series modelling, data preparation and model evaluation. Examples include classifiers/regressors, KMeans/PCA, neural layers, DQN/replay training, causal language models, ARIMA/LSTM and evaluation metrics. Package installation alone is insufficient.
- **Agentic AI Engineering:** restricted to the Agentic Core repository family and linkedin-agent-development-lab. It covers verified orchestration, tools, retrieval, state, approvals, guardrails, routing and agent evaluation. Unrelated web applications and README architecture claims do not contribute.

Python comments, docstrings, strings containing prompts/code examples and unimplemented stubs are removed before domain detection. Notebook markdown and output are excluded. The initial authenticated audit inspected a broad source sample across every repository; automatic collection inspects up to 36 prioritised implementation/notebook files per changed public repository. Unchanged public trees reuse previously verified evidence. Exact public files are listed in the snapshot. A bounded sample can miss a capability, so absence is not a claim that it has never been used.

## Private-source protection

Private source is read only for the authorised audit. The published snapshot contains only opaque per-repository identifiers and verified skill names for private projects. It contains no private repository names, paths, URLs, snippets, blob hashes, notebook text or raw API capture.

Public and private captures are separate. Public-only refresh preserves the private aggregate baseline and its capture date. If a private project becomes public, stable opaque identifiers prevent double counting.

## Keeping it current

The GitHub Actions workflow checks public repositories every 15 minutes, on profile source changes, and through **Run workflow**. An hourly authenticated connected-GitHub audit refreshes the full accessible inventory, including private repositories and new repositories.

These are scheduled checks, not universal GitHub push webhooks. GitHub can delay scheduled Actions and cache profile images. The workflow's own token cannot read other private repositories, so it must not replace a full private audit with a public-only scan.

A failed/truncated API response or a repository changing during capture aborts the update. Newly created empty repositories have no skills to count. No commit is created when the evidence is unchanged. Public/private snapshot dates record their last material captures; execution histories record subsequent successful checks.

## Rebuild commands

Public automatic refresh:

~~~bash
python scripts/refresh_skill_evidence.py --scope public
python scripts/build_skill_circles.py
python scripts/validate_profile.py
~~~

Authenticated all-repository capture through the connected GitHub tools:

1. Retrieve the current owned repository inventory, including accessible private repositories.
2. Capture metadata and recursive trees, then implementation files/notebooks into a temporary API cache. The inventory cache key is /users/jyotheshkar/repos?per_page=100&page=1 (subsequent pages as needed), but its contents must come from the authenticated full inventory. Include exact file SHAs and UTF-8 or base64 contents.
3. Run the collector with --api-cache /temporary/capture.json --scope accessible.
4. Rebuild and validate the artwork. Check that private_snapshot and private chart entries contain only allowed aggregate fields before publication.
5. Commit only config/skill-evidence.json and the five generated skill SVGs. Never commit the temporary API cache.
6. Recheck the current branch head before updating it to avoid overwriting concurrent work.

Generated assets: skill-circles.svg, skills-mobile.svg, skills-programming.svg, skills-aiml.svg and skills-agentic.svg. README image links follow the default branch so new rendered evidence can appear without repinning a commit.

### Temporary API cache contract

The cache is one JSON object keyed by API path. Parse connector JSON responses rather than storing their tool-result wrappers. Required shapes:

~~~json
{
  "/users/jyotheshkar/repos?per_page=100&page=1": [
    {"id": 123, "name": "example", "full_name": "jyotheshkar/example", "owner": {"login": "jyotheshkar"}, "default_branch": "main", "private": true, "fork": false, "size": 10}
  ],
  "/repos/jyotheshkar/example/git/trees/main?recursive=1": {
    "sha": "EXACT_TREE_SHA", "truncated": false,
    "tree": [{"path": "src/example.py", "type": "blob", "sha": "EXACT_BLOB_SHA", "size": 100}]
  },
  "/repos/jyotheshkar/example/contents/src/example.py?ref=main": {
    "path": "src/example.py", "sha": "EXACT_BLOB_SHA", "encoding": "utf-8", "content": "ACTUAL_FILE_CONTENT"
  }
}
~~~

If an inventory page contains 100 repositories, include successive pages and the final short/empty page. Capture a complete tree for every included repository. Content keys may percent-encode path characters while retaining slashes; raw paths are also accepted for connector captures. Base64 encoding is accepted instead of UTF-8. Notebook content must be the original JSON so the collector can inspect code cells and kernel language. Select actual implementation files across each repository, especially every available notebook and runtime/agent/model/training source. Missing cached content is treated as a bounded sample, while missing trees or a truncated tree fail the capture. Never put this temporary cache into the public repository.

