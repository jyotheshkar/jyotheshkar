# GitHub profile maintenance

The overview opens with the installed LinkedIn Agent workflow in GitHub's dark palette. Separate transparent career and skill sections follow. Each section has desktop and mobile artwork selected by README picture elements. Skills use centred doughnuts with names and evidence bars beneath them in two columns.

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

The [skills methodology](skill-circles.md) explains Programming Languages, AI/ML Engineering and Agentic AI Engineering evidence across accessible repositories. GitHub Actions refresh public evidence every fifteen minutes, on profile pushes, and on manual runs. An owner-authorized hourly connector task refreshes the complete accessible scope, including sanitized private aggregates. It commits only changed evidence and generated chart files. Private code, names and file paths are never published by the collector.

README images follow the main branch so future refreshes appear. GitHub caches images and schedules can be delayed; this is automatic refresh rather than a real-time browser dashboard.

## Validation

Validation parses generated SVGs, rejects external resources and active content, checks local references and unique IDs, confirms the LinkedIn panel, and verifies that all three skills charts and legends match their evidence source proportionally. CI rebuilds outputs and checks they are committed. Institution logo provenance is documented in [logo-sources.md](logo-sources.md).

