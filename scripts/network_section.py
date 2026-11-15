"""LinkedIn Agent architecture grounded in the inspected local-learning MVP."""
from html import escape

PROJECTS = ({
    "key": "linkedin", "icon": "python", "title": "LinkedIn Agent",
    "tools": (("python", "Python", "Application and workflow orchestration"),
              ("openai", "OpenAI", "Optional structured model adapter")),
},)
SOURCE_COMMIT = "65b2638d0bd094b5a7dd3b2885b175f3b01934c6"


def _text(x, y, text, size=20, color="#f0f6fc", weight=400, anchor="start", mono=False):
    family = "Consolas,monospace" if mono else "Arial,Helvetica,sans-serif"
    return (f'<text x="{x}" y="{y}" font-family="{family}" font-size="{size}" '
            f'font-weight="{weight}" fill="{color}" text-anchor="{anchor}">'
            f'{escape(text)}</text>')


def _glyph(kind, x, y, color="#79c0ff"):
    shapes = {
        "input": '<path d="M7 3h14l6 6v22H7zM21 3v7h6M12 16h10M12 21h10M12 26h6"/>',
        "search": '<circle cx="14" cy="14" r="9"/><path d="m21 21 9 9M9 14h10M14 9v10"/>',
        "agent": '<rect x="4" y="9" width="26" height="21" rx="6"/><path d="M17 3v6M1 16h3M30 16h3M11 23h12"/><circle cx="11" cy="16" r="1.3"/><circle cx="23" cy="16" r="1.3"/>',
        "review": '<circle cx="13" cy="10" r="6"/><path d="M3 30v-4a10 10 0 0 1 20 0M22 17l4 4 7-8"/>',
        "action": '<path d="m5 4 24 13L5 30zM5 17h14"/>',
        "store": '<ellipse cx="17" cy="7" rx="13" ry="5"/><path d="M4 7v20c0 7 26 7 26 0V7M4 17c0 7 26 7 26 0"/>',
        "ledger": '<rect x="5" y="3" width="24" height="29" rx="4"/><path d="m10 11 2 2 4-4M19 11h5m-14 9 2 2 4-4M19 20h5M10 27h14"/>',
    }
    return (f'<g transform="translate({x} {y})" fill="none" stroke="{color}" '
            f'stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">'
            f'{shapes[kind]}</g>')


def render_network(icons):
    """Return a workflow-editor canvas within x=24..1376, y=215..1052."""
    out = ['''<g id="linkedin-architecture" aria-labelledby="linkedin-architecture-title">
<title id="linkedin-architecture-title">LinkedIn Agent — Agentic AI System Engineering</title>
<desc>A local learning system: job and goal input, evidence retrieval, bounded planning and drafting,
exact-material human approval, and simulated application and outreach. Versioned Atlas Lab knowledge,
an optional OpenAI model adapter, and durable SQLite receipts support the workflow.
The diagram shows implemented code structure, not live LinkedIn integrations.</desc>
<defs>
<pattern id="nw-dots" width="22" height="22" patternUnits="userSpaceOnUse"><circle cx="1" cy="1" r=".8" fill="#3d444d" opacity=".44"/></pattern>
<linearGradient id="nw-focus" x1="0" y1="0" x2="1" y2="1"><stop stop-color="#142941"/><stop offset="1" stop-color="#151b23"/></linearGradient>
<marker id="nw-arrow" markerWidth="7" markerHeight="7" refX="6" refY="3.5" orient="auto"><path d="m1 1 4 2.5L1 6" fill="none" stroke="#79c0ff" stroke-width="1.2"/></marker>
<style>.nw-flow{stroke-dasharray:2 12;animation:nw-travel 16s linear infinite}
@keyframes nw-travel{to{stroke-dashoffset:-140}}
@media(prefers-reduced-motion:reduce){.nw-flow{animation:none}}</style>
</defs>''']
    out += [
        _text(40, 231, "AGENTIC AI SYSTEM ENGINEERING", 17, "#9198a1", mono=True),
        _text(40, 291, "LinkedIn Agent", 43, weight=700),
        _text(40, 327, "Evidence-led workflows. Human-reviewed actions. Recoverable execution.", 22, "#9198a1"),
        '<circle cx="1120" cy="280" r="4" fill="#59c3c3"/>',
        _text(1135, 286, "LOCAL LEARNING LAB", 16, "#a3c7d9", mono=True),
        '<rect x="24" y="359" width="1352" height="686" rx="18" fill="#0d1117" stroke="#3d444d"/>',
        '<rect x="25" y="360" width="1350" height="684" rx="17" fill="url(#nw-dots)"/>',
        '<path d="M24 415H1376" stroke="#3d444d" stroke-opacity=".65"/>',
        '<circle cx="50" cy="387" r="4" fill="#4493f8"/>',
        _text(65, 394, "linkedin-agent / application workflow", 17, "#c9d1d9", mono=True),
        _text(1346, 394, "Python · FastAPI · LangGraph", 17, "#9198a1", anchor="end"),
    ]

    def route(path, support=False, animated=False):
        dash = ' stroke-dasharray="5 7"' if support else ""
        color = "#4c657e" if support else "#79c0ff"
        out.append(f'<path d="{path}" fill="none" stroke="{color}" stroke-width="1.8"{dash} marker-end="url(#nw-arrow)"/>')
        if animated:
            out.append(f'<path class="nw-flow" d="{path}" fill="none" stroke="#b6dcff" stroke-width="2.4" opacity=".6"/>')

    # Solid connections carry workflow; dashed connections are dependencies.
    for path in ("M284 565H323", "M544 565H583", "M816 565H855", "M1076 565H1115"):
        route(path, animated=True)
    route("M966 492V461Q966 443 948 443H718Q700 443 700 461V492", support=True)
    out.append(_text(833, 436, "Revise", 16, "#9198a1", anchor="middle"))
    route("M434 796V638", support=True)
    route("M700 796V638", support=True)
    route("M1226 638V796")
    out.append(_text(1095, 481, "Approve", 14, "#9198a1", anchor="middle"))

    def port(x, y, accent=False):
        color = "#79c0ff" if accent else "#64788e"
        out.append(f'<circle cx="{x}" cy="{y}" r="5" fill="#0d1117" stroke="{color}" stroke-width="1.8"/>')

    def card(key, x, y, w, title, subtitle, module, glyph, accent=False):
        fill = "url(#nw-focus)" if accent else "#151b23"
        stroke = "#4493f8" if accent else "#3d444d"
        out.append(f'<g id="linkedin-node-{key}"><rect x="{x}" y="{y}" width="{w}" height="142" rx="14" fill="{fill}" stroke="{stroke}" stroke-width="1.5"/>')
        out.append(f'<rect x="{x+16}" y="{y+16}" width="44" height="44" rx="11" fill="#0d1117" stroke="#3d444d"/>')
        out.append(_glyph(glyph, x+21, y+21))
        number = "0" + str(["input", "retrieval", "agent", "review", "effects"].index(key)+1)
        out.append(_text(x+w-16, y+43, number, 16, "#64788e", anchor="end", mono=True))
        out.extend([_text(x+16, y+84, title, 22, weight=600),
                    _text(x+16, y+110, subtitle, 17, "#a4b2c2"),
                    _text(x+16, y+131, module, 14, "#7d8b9b", mono=True),
                    "</g>"])
        if key != "input":
            port(x, y+71, accent)
        if key != "effects":
            port(x+w, y+71, accent)

    card("input", 64, 494, 220, "Job + goal", "FastAPI / CLI", "contracts.py", "input")
    card("retrieval", 324, 494, 220, "Retrieve evidence", "Qdrant + FastEmbed", "retrieval.py", "search")
    card("agent", 584, 494, 232, "Plan + draft", "Bounded tool execution", "workflow.py", "agent", True)
    card("review", 856, 494, 220, "Human review", "Exact plan + draft hash", "materials.py", "review")
    card("effects", 1116, 494, 220, "Simulate actions", "Application + outreach", "provider.py", "action")
    for x, y in ((966, 494), (700, 494), (434, 636), (700, 636), (1226, 636)):
        port(x, y, x == 700)

    def support(key, x, w, title, sub, footer, glyph=None, brand=None):
        y = 798
        out.append(f'<g id="linkedin-support-{key}"><rect x="{x}" y="{y}" width="{w}" height="134" rx="14" fill="#111820" stroke="#344354"/>')
        if brand and brand in icons:
            out.append(f'<use href="#brand-{brand}" x="{x+18}" y="{y+18}" width="30" height="30"/>')
        else:
            out.append(_glyph(glyph, x+16, y+16))
        out.extend([_text(x+62, y+39, title, 20, weight=600),
                    _text(x+18, y+78, sub, 17, "#a4b2c2"),
                    _text(x+18, y+105, footer, 15, "#7d8b9b"), "</g>"])
        port(x+w/2, y)

    support("knowledge", 314, 240, "Atlas knowledge", "Versioned local snapshots", "knowledge.py / atlas_lab.py", "store")
    support("model", 580, 240, "Model adapter", "Offline / optional OpenAI", "Structured plan + generation", brand="openai")
    support("state", 1090, 270, "Durable evidence", "SQLite · artifacts · receipts", "Resume / reconcile / project", "ledger")
    out.append('<path d="M64 975H1336" stroke="#3d444d" stroke-opacity=".65"/>')
    out += [
        _text(64, 1008, "OpenTelemetry traces", 17, "#a4b2c2"),
        _text(419, 1008, "Grounding + evaluation", 17, "#a4b2c2"),
        _text(792, 1008, "Effects remain simulated", 17, "#a4b2c2"),
        _text(1336, 1008, "MVP", 17, "#79c0ff", anchor="end", mono=True),
        "</g>",
    ]
    return "\n".join(out)

