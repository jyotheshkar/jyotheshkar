# LinkedIn Agent: installed workflow architecture

This diagram maps the **installed private LinkedIn plugin, version 1.3.19**, inspected on **15 November 2026**. It represents the actual ChatGPT-coordinated workflow package and its connected-service boundaries.

The package contains workflow instructions, a ReportLab CV renderer, PDF checks and Python evidence-validation helpers. Its app binding is Atlas. GitHub, Gmail, Google Drive/Sheets and browser capabilities are provided by the active ChatGPT runtime. This personal workflow is not affiliated with LinkedIn.

## Components and flow

| Diagram component | Source and observed responsibility |
| --- | --- |
| Owner request | Sets the batch objective, boundaries and action authority. |
| ChatGPT coordinator | Reads the installed workflow, routes available native tools, preserves batch state and resumes incomplete stages. |
| Policy + review | Uses current owner instructions, approved facts and recorded decisions; host controls remain in force. |
| LinkedIn | Discovers vacancies; verifies the live, individual official employer or ATS route. |
| GitHub | Retrieves current repository evidence and source versions to ground project claims. |
| Atlas | Supplies approved facts, project evidence, CV metadata, history and pending action intents. |
| Gmail history | Reads focused relevant conversations and native message receipts before duplicate decisions. |
| Match + prepare | Qualifies the vacancy, resolves stable identities, checks prior approaches and checkpoints action intent. |
| Tailored CV | Creates source-backed materials using the package's ReportLab renderer and PDF validation. |
| Google Drive | Stores the exact immutable CV version; verifies file metadata and bytes before dependent action. |
| Application | Uses the current vacancy's accepted employer/ATS or authorized alternative route; reads back actual acceptance evidence. |
| Gmail outreach | Sends the distinct, relevant outreach within the requested authority, using the same verified CV; reads back the real message receipt. |
| Atlas + Google Sheets | Stages records, prepares exact rows, writes native Sheets, reads the same row/version/hash back, then commits. Approval versions use the same synchronization path. |
| Atlas Dashboard | Receives only Atlas's approved safe projection and provides signed delivery/readback evidence. LinkedIn does not write the website directly. |
| Learn + recover | Persists sourced lessons and precise checkpoints; reconciles original provider outcomes and repairs only incomplete stages. |

The four source branches are independent reads and may run concurrently. Application and outreach are distinct provider effects; each reserves intent and persists its observed outcome separately. The convergence illustrates evidence gathering, not a requirement to delay recording until every branch succeeds. Source facts, artifacts and provider receipts retain their individual identities.

## Canonical data boundary

The installed handoff requires:

1. Read current approved Atlas knowledge and canonical history.
2. Reserve an external-effect intent before a Submit or Send.
3. Execute the authorized action once and inspect its actual provider result.
4. Stage the individual event, prepare the canonical row, perform the native Sheets write and exact readback, then call `atlas_commit_sheet_sync`.
5. Consume Atlas's automatic signed `dashboard_sync` receipt and verify the approved record's current projection membership.
6. Retain any pending stage and reconcile it without resubmitting or resending.

An application unit is complete only when its exact CV, application acceptance, distinct outreach, canonical Atlas commit and reporting-delivery gates are verified. Accepted applications and sent messages remain independently recorded when later stages are pending.

## Verified source package

Inspected installed sources:

- `plugin.json` and `.app.json`
- `skills/linkedin/SKILL.md`
- `skills/linkedin/references/atlas-only-handoff.md`
- `skills/linkedin/references/atlas-integration.md`
- `skills/linkedin/scripts/README.md`
- `workflow_state.py`, `five_gate_guard.py` and `atlas_sync_plan.py`

The last three are offline validators/planners operating on supplied observations. They do not call providers or independently establish provider receipt validity. Current Atlas tool schemas independently expose staging, review, prepare, canonical commit, approved record reads and signed dashboard projection functions.

| Inspected source | SHA-256 |
| --- | --- |
| `plugin.json` | `d83a3662a9764ea3a1db5f41160be9583180286159b6f3bcef6af83190281f7c` |
| `skills/linkedin/SKILL.md` | `fcf015854a8d889d53984d872f477e181a42c714dbaa280710ebda0aeecd554b` |
| `atlas-only-handoff.md` | `cdadcdcb0bdc887a4f12c3849cb6e6c7652c4686a7e5dfd8909f194201c83f5d` |
| `atlas_sync_plan.py` | `fdec9bc63fd16ba7d049656031f608e829851e62a9a84ce0de44d7f9d01f4d31` |

The separate LinkedIn Agent Development Lab is a learning implementation. LangGraph, Qdrant, FastEmbed and simulated employer effects belong to that lab and are not used to describe this installed plugin.

## Rendering

`scripts/network_section.py` exports desktop and mobile SVG fragments with the same major components. The design retains GitHub's dark canvas and blue connections. Original service logo colors identify native providers. Generic line icons identify workflow functions.

Blue packets animate along connection paths, split across parallel reads and converge at preparation and canonical recording. This is an architecture animation, not a live activity or health indicator. Reduced-motion preferences hide the animated packets. No credentials, CV bodies, email addresses, account IDs or private operational records are embedded.

