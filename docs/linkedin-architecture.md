# LinkedIn Agent architecture

The overview diagram presents the implemented local learning MVP in a workflow-editor layout. It uses the profile's existing GitHub dark colors and a single LinkedIn Agent system. Animated connector dots indicate diagram direction only.

Source inspected on **15 November 2026**: [LinkedIn Agent Development Lab](https://github.com/jyotheshkar/linkedin-agent-development-lab), commit `65b2638d0bd094b5a7dd3b2885b175f3b01934c6`. The source repository is private; access is required to follow its code links.

## Node-to-code mapping

| Diagram node | Inspected source | Observed responsibility |
| --- | --- | --- |
| Job + goal | `contracts.py`, `application.py`, repository README | Validates the supplied job and goal; the CLI and FastAPI console share the application service. |
| Retrieve evidence | `service.py`, `retrieval.py` | Retrieves filtered, ranked evidence from Qdrant local. The default hash embedding is a nonsemantic test double; FastEmbed is the optional semantic mode. |
| Plan + draft | `application.py`, `workflow.py`, `planner.py`, `materials.py` | Creates persisted application and outreach drafts, binds a bounded plan to exact artifact bytes, and executes validated tool calls through LangGraph. |
| Human review | `application.py`, `workflow.py`, `materials.py` | Approval binds the reviewed plan and artifact hashes. A revision requires renewed review. |
| Simulate actions | `application.py`, `workflow.py` | Runs simulated application/outreach effects through a provider, with independent receipts and completion gates. |
| Atlas knowledge | `application.py`, `service.py` | Loads versioned, isolated Atlas Lab snapshots. Operational Atlas is not synchronized. |
| Model adapter | `openai_adapter.py`, `service.py` | Optional structured planning/generation with OpenAI; offline fixtures are the default. Live generation accepts synthetic evidence only. |
| Durable evidence | `application.py`, `workflow.py`, `materials.py` | Stores artifacts, approvals, local SQLite provider receipts and workflow journals; resumes uncertain effects by reconciliation. |
| Engineering footer | `observability.py`, `grounding.py`, repository README | Local OpenTelemetry spans, structural grounding validation, evaluation and recovery checks. |

The preparation sequence is summarized for readability; `ApplicationService` coordinates the stages. Dashed connections show dependencies and the review revision path. Solid connections show the principal workflow and stored output evidence.

## Scope

- The current effects remain **simulation**. The lab has no live employer, LinkedIn or Gmail writer.
- The default planner and generator are deterministic offline adapters. Their optional model counterparts do not grant executor permissions.
- Grounding checks validate citation IDs, exact quotes, output shape and known source conflicts. They do not prove semantic entailment.
- Vercel delivery is prepared but not deployed, so the diagram does not show a hosted production service.
- The diagram is an implementation map; it makes no claim about independent authorship, proficiency, employer usage or hiring outcomes.

The SVG fragment is maintained in `scripts/network_section.py` and embedded by `scripts/build_profile.py`.

