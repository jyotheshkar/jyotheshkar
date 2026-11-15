# GitHub profile maintenance

The overview keeps its dark GitHub palette and shared grid. A generated SVG holds the LinkedIn Agent workflow and the two career cards. A separate generated SVG displays three Professional Skills doughnuts, with names and small evidence bars to their right.

## Rebuild

```sh
python scripts/import_brand_icons.py
python scripts/build_profile.py
python scripts/build_skill_circles.py
python scripts/validate_profile.py
```

All rendering uses Python's standard library and local assets. The profile builder embeds authentic institution logos; no remote resources or JavaScript are required to view the profile.

## Architecture and evidence

The [LinkedIn architecture](linkedin-architecture.md) maps the local learning implementation: retrieval, planning, exact-material human approval, simulated effects, and durable receipts. It does not claim live LinkedIn integrations.

The [skills methodology](skill-circles.md) explains public repository language, dependency and code evidence. Run `python scripts/refresh_skill_evidence.py` to collect fresh evidence before rebuilding the skills graphic. The GitHub workflow validates pushed changes and refreshes evidence hourly, on profile pushes, and on manual runs. It commits only changed evidence and chart files.

README images follow the main branch so future refreshes appear. GitHub caches images and schedules can be delayed; this is automatic refresh rather than a real-time browser dashboard.

## Validation

Validation parses generated SVGs, rejects external resources and active content, checks local references and unique IDs, confirms the LinkedIn panel, and verifies that all three skills charts and legends match their evidence source proportionally. CI rebuilds outputs and checks they are committed. Institution logo provenance is documented in [logo-sources.md](logo-sources.md).

