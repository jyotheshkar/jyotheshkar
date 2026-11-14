# Profile visual maintenance

The profile is a GitHub README and repository-local image assets. It does not require a portfolio website, external image service, JavaScript in Markdown, or a paid API.

## Retained telemetry assets

`scripts/update_metrics.py` uses Python's standard library and GitHub's public user-repository REST endpoint, following pagination until the final page. It sanitizes the output to public repository metadata before saving `assets/data/public-repos.json`. An optional `GITHUB_TOKEN` increases the API rate limit; tokens and request headers are never logged. The script never queries private repository endpoints or exports private source.

The panels show:

- **Public repos:** all owned public repositories, including archived repositories and forks.
- **Active source:** owned public repositories that are neither forks nor archived.
- **Repo stars/forks:** aggregate GitHub repository counters across all owned public repositories.
- **Language footprint:** each active source repository contributes one count for its GitHub primary language. This is neither language bytes nor a proficiency score. Unclassified repositories are counted separately.
- **Public build signal:** latest `pushed_at` dates for six active source repositories, excluding this profile repository. Dates can reflect any contributor's push. The plot is recency within a 90-day window, not commit volume, contribution history, or a streak.

The visible snapshot date is taken from the actual retrieval, including when a saved snapshot is rendered offline. No date is presented as current merely because a renderer ran. API errors, incomplete metadata, duplicate IDs or invalid visibility fail the refresh before existing metrics are replaced.

Refresh from GitHub:

```sh
python scripts/update_metrics.py
python scripts/validate_profile.py
```

Reproduce the saved panels without network access:

```sh
python scripts/update_metrics.py --snapshot assets/data/public-repos.json
python scripts/validate_profile.py
```

The project gallery, toolkit and telemetry section were removed from the profile at the owner's request. Their source assets remain in the repository for history and optional manual reuse. The workflow now validates profile images and links with read-only repository access; automatic telemetry refresh is disabled. Repository activity naturally changes when source projects are updated; this README makes no production usage or model-quality claims.

## Content maintenance

Update project descriptions when their public implementation or maturity changes. Preserve the distinction between working local code, synthetic evaluation, architecture proposals and hosted demonstrations. The professional biography states the current employment title separately from independent Agentic AI development.

SVGs contain their own GitHub dark backgrounds, neutral text and blue accents because GitHub sanitizes README HTML. GitHub's surrounding navigation, sidebar and contribution calendar retain GitHub's own theme. Animation is decorative; essential professional text and project descriptions remain readable without motion.
