# Professional Skills: audit and maintenance

One shared box shows four sections in a two-by-two desktop layout: **Languages, Libraries and Frameworks** (top left), **AWS Cloud Skills** (top right), **AI/ML Engineering** (bottom left), and **Agentic AI Engineering** (bottom right). Mobile stacks these sections in reading order. GitHub-style stacked bars, coloured dots, bold names and muted percentages share consistent typography, spacing and rules. The dark canvas and blue heading accents follow the LinkedIn Agent section.

The current snapshot is [skill-evidence.json](../config/skill-evidence.json). Every bar segment counts repositories containing verified source evidence for that skill. A repository may support several skills. Percentages divide a skill's repository count by the sum of all skill counts within its displayed section; they measure shares of evidence signals, not proficiency or GitHub Linguist language byte shares. The merged technology section preserves all language signals and features eight libraries: NumPy, pandas, scikit-learn, PyTorch, TensorFlow, React, Next.js and FastAPI. A grey **Others** segment includes every remaining library signal. The complete library list remains in the source snapshot. AWS Cloud Skills lists only the reviewed AWS service names individually; Docker, Docker Compose, Render, Vercel, Fly.io and Nixpacks are grouped into its grey Others entry. The complete cloud evidence remains intact in the raw snapshot, and grouping preserves its total signal count and percentage denominator. This measures project coverage, not ability, authorship, project quality or production reliability.

## What was audited

The full audit covers all accessible original repositories owned by this account, including private coursework and project repositories. Forks and the profile repository are excluded. Complete source trees establish language presence; implementation files and notebook code cells establish engineering topics. Build output, vendored dependencies, archive/snapshot copies, tests and prose claims do not establish implementation skills. Cloud coverage additionally includes manually reviewed technical AWS lab documents and substantive learning architecture designs, with that status recorded explicitly.

- **Programming Languages:** source file extensions plus inspected notebook code cells. PHP, SQL and notebook Python are included. JSP remains recorded as a server-page template in the source evidence. At the owner's request, its display label is Java, grouping the Java server-page template signal into the Java ecosystem. The artwork and tooltip state that Java includes JSP templates. This label change does not add .java implementation evidence or change any source counts. Actual .java or .pde evidence remains distinct in the collector.
- **Libraries and Frameworks:** external packages imported and actually used by inspected implementation code or notebook code cells. Python bindings must be referenced after import; unused imports, standard-library modules and dependency manifests do not qualify. JavaScript/TypeScript imports are checked for binding use, excluding type-only imports. Public proof retains exact file paths and blob SHAs; private proof retains only aggregate library names. The separate `library_audit` field records its date and bounded inspection scope.
- **Cloud Skills:** concrete provider integration, project deployment configuration, and manually inspected AWS lab and architecture learning evidence. Checked Docker builds, Compose service definitions, provider deployment manifests and AWS build configuration establish deployment tooling coverage. Technical case studies and lab documents qualify only after their actual contents have been reviewed and a service's role has been identified; their proofs are tagged `learning architecture` or `documented AWS lab`. These categories do not establish successful deployment or production operation. Bare service-name mentions, reference links, project titles, installed SDKs and uninspected binary documents do not count. The separate `cloud_audit` field records the inspection scope and limits. Subsequent collectors retain manually reviewed public learning evidence only while the same repository identity still contains the exact reviewed file path and blob SHA.
- **AI/ML Engineering:** implemented supervised and unsupervised learning, deep learning, reinforcement learning, NLP/transformers, time-series modelling, data preparation and model evaluation. Examples include classifiers/regressors, KMeans/PCA, neural layers, DQN/replay training, causal language models, ARIMA/LSTM and evaluation metrics. Package installation alone is insufficient.
- **Agentic AI Engineering:** restricted to the Agentic Core repository family and linkedin-agent-development-lab. It covers verified orchestration, tools, retrieval, state, approvals, guardrails, routing and agent evaluation. Unrelated web applications and README architecture claims do not contribute.

Python comments, docstrings, strings containing prompts/code examples and unimplemented stubs are removed before domain detection. Notebook markdown and output are excluded. The initial authenticated audit inspected a broad source sample across every repository; automatic collection inspects up to 36 prioritised implementation/notebook files per changed public repository. Unchanged public trees reuse previously verified evidence. Exact public files are listed in the snapshot. A bounded sample can miss a capability, so absence is not a claim that it has never been used.

## Private-source protection

Private source is read only for the authorised audit. The published snapshot contains only opaque per-repository identifiers and verified skill names for private projects. It contains no private repository names, paths, URLs, snippets, blob hashes, notebook text or raw API capture.

Public and private captures are separate. Public-only refresh preserves the private aggregate baseline and its capture date. If a private project becomes public, stable opaque identifiers prevent double counting.

## Keeping it current

Automatic monitoring is disabled at the owner's request. The scheduled GitHub workflow trigger and automatic refresh job have been removed, and the hourly skills task is paused. CI only rebuilds and validates the committed snapshot on pushes, pull requests and manual workflow runs.

An explicit manual authenticated audit can refresh the full accessible inventory, including private and new repositories. GitHub can cache profile images briefly after publication. A public-only capture cannot replace a full private audit.

A failed/truncated API response or a repository changing during capture aborts the update. Newly created empty repositories have no skills to count. No commit is created when the evidence is unchanged. Public/private snapshot dates record their last material captures; execution histories record subsequent successful checks.

## Rebuild commands

Manual public evidence capture (preserves the private baseline):

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
5. Commit only config/skill-evidence.json and the eight generated skill SVGs. Never commit the temporary API cache.
6. Recheck the current branch head before updating it to avoid overwriting concurrent work.

Generated assets: skills.svg, skills-mobile.svg, skills-programming.svg (the merged technology section), skills-cloud.svg, skills-aiml.svg and skills-agentic.svg. The historical skills-libraries.svg URL aliases the merged technology section, and skill-circles.svg aliases the combined panel. README image links follow the default branch so updates can appear without repinning a commit.

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


