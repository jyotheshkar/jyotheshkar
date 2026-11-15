# GitHub profile maintenance

The overview opens with the installed LinkedIn Agent workflow in GitHub's dark palette. Architecture nodes use consistent internal padding, separated icon/title and body rows, and white generic symbols; authentic provider logos retain their original colours. Experience, education and skills share its dark canvas, subtle borders, blue heading rules and reduced heading sizes. Both experience and education cards and the shared skills panel have transparent backgrounds, while the Amazon logo retains its opaque white plate. The employer heading is Amazon. The institution headers use matching logo slots, text offsets and typography. Awarded Distinction is white; Received Best Performance Award uses the blue accent. Each work role displays its city and full country name, taken from owner-approved employment records. Each section has desktop and mobile artwork selected by README picture elements. Skills use one box with four sections, GitHub-style stacked bars and inline dot legends. The overview ends with the skills artwork and has no evidence or architecture footer links.

## Rebuild

```sh
python scripts/import_brand_icons.py
python scripts/build_profile.py
python scripts/build_skill_circles.py
python scripts/validate_profile.py
```

All rendering uses Python's standard library and local assets. The profile builder embeds authentic institution logos; no remote resources or JavaScript are required to view the profile.

## Architecture and evidence

The [LinkedIn architecture](linkedin-architecture.md) maps the installed ChatGPT-coordinated plugin: connected source reads, evidence-based preparation, exact Drive artifacts, separate application/outreach paths, canonical Atlas records, dashboard delivery and recovery. Blue packet animation illustrates topology, not real-time execution.

The [skills methodology](skill-circles.md) explains the combined Languages, Libraries and Frameworks section, AWS Cloud Skills, AI/ML Engineering and Agentic AI Engineering. The technology section highlights eight key libraries and groups the rest under grey Others; AWS entries come from checked repository configuration and reviewed technical AWS lab or learning architecture materials. Non-AWS cloud platforms and deployment tools are grouped under grey Others. Learning/design evidence is labelled in source proofs and does not claim live infrastructure. Automatic monitoring is disabled at the owner's request. Evidence collection is available for explicit manual audits. GitHub Actions only rebuild and validate the committed snapshot on pushes, pull requests or manual runs. Private code, names and file paths are never published by the collector.

README images follow the main branch. GitHub may cache images briefly after a commit.

## Validation

Validation parses generated SVGs, rejects external resources and active content, checks local references and unique IDs, confirms the LinkedIn panel, and verifies the four-section desktop arrangement, mobile reading order, percentages and proportional segments against the evidence. CI rebuilds outputs and checks they are committed. Institution logo provenance is documented in [logo-sources.md](logo-sources.md).


