"""Installed LinkedIn plugin architecture; source-grounded SVG workflow views.

These paths describe the coordinator and real provider boundaries, not an
execution-status feed. All animated packets are illustrative.
"""
from html import escape

WIDTH, HEIGHT = 1400, 1290
MOBILE_WIDTH, MOBILE_HEIGHT = 700, 1910
SOURCE_VERSION = "1.3.19"
PROJECTS = ({
    "key": "linkedin", "icon": "linkedin", "title": "LinkedIn Agent",
    "tools": (
        ("openai", "ChatGPT", "Workflow coordinator"),
        ("linkedin", "LinkedIn", "Vacancy discovery"),
        ("github", "GitHub", "Repository evidence"),
        ("gmail", "Gmail", "History, outreach and receipts"),
        ("googledrive", "Google Drive", "Exact versioned CV artifact"),
        ("googlesheets", "Google Sheets", "Atlas canonical records"),
    ),
},)

NODES = {
    "request": ("Owner request", ["Goals, scope and authority"], None, "user"),
    "coordinator": ("ChatGPT coordinator", ["LinkedIn workflow + tool routing"], "openai", "agent"),
    "policy": ("Policy + review", ["Owner-approved decisions"], None, "shield"),
    "linkedin": ("LinkedIn", ["Discover roles", "Verify employer / ATS"], "linkedin", None),
    "github": ("GitHub", ["Read repository evidence", "Ground project claims"], "github", None),
    "atlas": ("Atlas", ["Approved facts + history", "CV versions + action intents"], None, "database"),
    "history": ("Gmail", ["Relevant threads + receipts", "Check prior approaches"], "gmail", None),
    "prepare": ("Match + prepare", ["Qualify · deduplicate · checkpoint", "Source claims before creating materials"], None, "branch"),
    "cv": ("Tailored CV", ["ReportLab + PDF checks", "Evidence + exact byte hash"], None, "document"),
    "drive": ("Google Drive", ["Save immutable CV version", "Read back file + byte hash"], "googledrive", None),
    "apply": ("Application", ["Accepted employer route", "Submit + receipt readback"], None, "browser"),
    "outreach": ("Gmail outreach", ["Distinct relevant outreach", "Same CV + provider receipt"], "gmail", None),
    "canonical": ("Atlas + Google Sheets", ["Stage → native write → exact readback → commit", "Approved records · versions · provenance"], "googlesheets", None),
    "dashboard": ("Dashboard", ["Approved Atlas projection", "Signed delivery + readback"], None, "dashboard"),
    "learning": ("Learn + recover", ["Lessons + checkpoints", "Resume the missing stage"], None, "loop"),
}


def _text(x, y, text, size=20, color="#f0f6fc", weight=400, anchor="start", mono=False):
    family = "Consolas,monospace" if mono else "Arial,Helvetica,sans-serif"
    return (f'<text x="{x}" y="{y}" font-family="{family}" font-size="{size}" '
            f'font-weight="{weight}" fill="{color}" text-anchor="{anchor}">{escape(text)}</text>')


def _glyph(kind, x, y, scale=1):
    shapes = {
        "user": '<circle cx="20" cy="12" r="7"/><path d="M6 36v-4a14 14 0 0 1 28 0v4"/>',
        "agent": '<rect x="5" y="10" width="30" height="25" rx="7"/><path d="M20 3v7M12 26h16"/><circle cx="13" cy="18" r="2"/><circle cx="27" cy="18" r="2"/>',
        "shield": '<path d="M20 3 35 9v12c0 9-15 16-15 16S5 30 5 21V9zM12 20l6 6 11-12"/>',
        "database": '<ellipse cx="20" cy="8" rx="15" ry="6"/><path d="M5 8v23c0 8 30 8 30 0V8M5 19c0 8 30 8 30 0"/>',
        "branch": '<path d="M5 20h10c11 0 7-13 18-13M15 20c11 0 7 13 18 13M27 3l7 4-7 4M27 29l7 4-7 4"/>',
        "document": '<path d="M8 3h16l8 8v26H8zM24 3v9h8M13 18h13M13 24h13M13 30h9"/>',
        "browser": '<rect x="3" y="5" width="34" height="30" rx="5"/><path d="M3 14h34M10 9h1M16 9h1m-3 16 5 5 10-11"/>',
        "dashboard": '<rect x="3" y="4" width="34" height="31" rx="5"/><path d="M3 13h34M11 29v-7M20 29V18M29 29V16"/>',
        "loop": '<path d="M7 15a14 14 0 0 1 26-2M33 25A14 14 0 0 1 7 27M7 6v9h9M33 34v-9h-9"/>',
    }
    return (f'<g transform="translate({x} {y}) scale({scale})" fill="none" stroke="#f0f6fc" '
            f'stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">{shapes[kind]}</g>')


def _defs():
    return '''<defs>
<pattern id="nw-dots" width="25" height="25" patternUnits="userSpaceOnUse"><circle cx="1" cy="1" r=".7" fill="#3d444d" opacity=".45"/></pattern>
<linearGradient id="nw-focus" x1="0" y1="0" x2="1" y2="1"><stop stop-color="#132c47"/><stop offset="1" stop-color="#111820"/></linearGradient>
<linearGradient id="nw-rule"><stop stop-color="#4493f8" stop-opacity=".8"/><stop offset="1" stop-color="#4493f8" stop-opacity=".05"/></linearGradient>
<radialGradient id="nw-aura"><stop stop-color="#4493f8" stop-opacity=".07"/><stop offset="1" stop-color="#0d1117" stop-opacity="0"/></radialGradient>
<filter id="nw-packet-glow" x="-300%" y="-300%" width="700%" height="700%"><feGaussianBlur stdDeviation="2"/></filter>
<style>.nw-packet{fill:#79c0ff}.nw-soft{fill:#4493f8;opacity:.65}
@media(prefers-reduced-motion:reduce){.nw-packet,.nw-soft{display:none}}</style>
</defs>'''


def _route(path, delay=0, secondary=False, period=9):
    stroke = "#395a7c" if secondary else "#4b7097"
    dash = ' stroke-dasharray="5 7"' if secondary else ""
    # Shared start times on fan-out paths make one packet become several; equal
    # arrival timings at merge paths make the parallel branches converge.
    parts = [f'<path d="{path}" fill="none" stroke="{stroke}" stroke-width="1.6"{dash}/>']
    for extra in (0, period/2):
        for cls, radius, filter_attr in (("nw-soft", 5, ' filter="url(#nw-packet-glow)"'), ("nw-packet", 3, "")):
            parts.append(f'<circle class="{cls}" r="{radius}"{filter_attr}><animateMotion dur="{period}s" '
                         f'begin="{delay-extra-period}s" repeatCount="indefinite" calcMode="linear" path="{path}"/></circle>')
    return "".join(parts)


def _port(x, y):
    return f'<circle cx="{x}" cy="{y}" r="4.5" fill="#0d1117" stroke="#6c92b9" stroke-width="1.7"/>'


def _node(key, x, y, w, h, icons, compact=False, mobile=False, body_lines=None):
    title, lines, brand, glyph = NODES[key]
    lines = lines if body_lines is None else body_lines
    primary = key in {"coordinator", "prepare", "canonical"}
    fill = "url(#nw-focus)" if primary else "#111820"
    stroke = "#3b6f9f" if primary else "#334253"
    title_size = 24 if mobile else 22
    line_size = 19 if mobile else 17.5
    padding, icon_gap = 24, 14
    parts = [f'<g id="linkedin-{key}"><rect x="{x}" y="{y}" width="{w}" height="{h}" rx="15" fill="{fill}" stroke="{stroke}" stroke-width="1.35"/>',
             f'<path d="M{x+20} {y}h42" stroke="#4493f8" stroke-width="2" opacity=".8"/>']
    if compact:
        icon_size = 32 if mobile else 30
        ix, iy = x+padding, y+18
        tx, ty = ix+icon_size+icon_gap, y+(40 if mobile else 39)
        body_y, line_height = y+(70 if mobile else 69), 25
    else:
        icon_size = 36 if mobile else 32
        ix, iy = x+padding, y+20
        tx, ty = ix+icon_size+icon_gap, y+(45 if mobile else 44)
        body_y, line_height = (y+76, 25) if h<=120 else (y+82, 27)
    if brand and brand in icons:
        parts.append(f'<use href="#brand-{brand}" x="{ix}" y="{iy}" width="{icon_size}" height="{icon_size}"/>')
    else:
        parts.append(_glyph(glyph or "agent", ix, iy, icon_size/40))
    parts.append(_text(tx, ty, title, title_size, weight=600))
    for i, line in enumerate(lines):
        parts.append(_text(x+padding, body_y+i*line_height, line, line_size, "#a9b8c9"))
    parts.append("</g>")
    return "".join(parts)


def _shell(width, height, mobile=False):
    parts = ['<g id="linkedin-architecture" aria-labelledby="linkedin-architecture-title">',
        '<title id="linkedin-architecture-title">LinkedIn Agent — Agentic AI System Engineering</title>',
        '<desc>The installed private LinkedIn workflow coordinates ChatGPT, LinkedIn vacancy research, GitHub project evidence, Gmail history and outreach, Google Drive CV storage, and canonical Atlas records in Google Sheets. Verified receipts converge in Atlas; Atlas alone delivers the approved dashboard projection. Blue packet animation illustrates the architecture, not live activity.</desc>',
        _defs(),
        f'<rect width="{width}" height="{height}" fill="#0d1117"/>',
        f'<rect width="{width}" height="{height}" fill="url(#nw-dots)"/>',
        f'<ellipse cx="{width/2}" cy="{height/2}" rx="{width*.55}" ry="{height*.48}" fill="url(#nw-aura)"/>']
    if mobile:
        parts += [_text(36, 48, "AGENTIC AI SYSTEM ENGINEERING", 21, "#91a9c3", mono=True),
                  _text(36, 106, "LinkedIn Agent", 38, weight=700),
                  _text(36, 145, "One workflow. Connected evidence.", 25, "#a9b8c9"),
                  _text(36, 179, "Source-verified architecture · v"+SOURCE_VERSION, 20, "#7d92aa"),
                  '<path d="M36 209H664" stroke="url(#nw-rule)"/>']
    else:
        parts += [_text(40, 49, "AGENTIC AI SYSTEM ENGINEERING", 18, "#91a9c3", mono=True),
                  _text(40, 110, "LinkedIn Agent", 42, weight=700),
                  _text(40, 150, "One workflow. Connected evidence. Verified outcomes.", 25, "#a9b8c9"),
                  _text(1360, 53, "INSTALLED WORKFLOW  /  v"+SOURCE_VERSION, 16, "#7d92aa", anchor="end", mono=True),
                  '<path d="M40 178H1360" stroke="url(#nw-rule)"/>']
    return parts


def render_network(icons):
    """Desktop view, origin 0,0; embedded by build_profile.py."""
    out = _shell(WIDTH, HEIGHT)
    # Request + policy connect to the coordinator, whose read branches split.
    out += [_route("M340 269H510", 0),
            _route("M1060 269H890", 0, True),
            _route("M700 310V359", 1),
            _route("M700 359H225Q205 359 205 379V420", 2),
            _route("M700 359H555Q535 359 535 379V420", 2),
            _route("M700 359H845Q865 359 865 379V420", 2),
            _route("M700 359H1175Q1195 359 1195 379V420", 2)]
    # Independent source responses converge before drafting or action.
    for x in (205, 535, 865, 1195):
        bend = "680" if x < 700 else "720"
        out.append(_route(f"M{x} 550V565Q{x} 585 {x+20 if x<700 else x-20} 585H{bend}Q700 585 700 605V625", 3))
    out += [
        _route("M700 755V757Q700 777 680 777H225Q205 777 205 797V820", 4),
        _route("M340 877H400", 5),
        _route("M670 877H730", 6),
        _route("M670 877H686Q706 877 706 857V795Q706 775 726 775H1175Q1195 775 1195 795V820", 6),
        _route("M535 950V976Q535 996 555 996H680Q700 996 700 1016V1035", 7),
        _route("M865 950V976Q865 996 845 996H720Q700 996 700 1016V1035", 7),
        _route("M1195 950V976Q1195 996 1175 996H720Q700 996 700 1016V1035", 7),
        _route("M1000 1098H1060", 8),
        _route("M400 1098H340", 8, True),
    ]
    for x,y in ((700,359),(700,585),(706,877),(700,996)):
        out.append(f'<circle cx="{x}" cy="{y}" r="4" fill="#79c0ff"/>')
    for key,x,y,w,h,compact in [
        ("request",70,220,270,90,True),("coordinator",510,220,380,90,True),
        ("policy",1060,220,270,90,True),
        ("linkedin",70,420,270,130,False),("github",400,420,270,130,False),
        ("atlas",730,420,270,130,False),("history",1060,420,270,130,False),
        ("prepare",510,625,380,130,False),
        ("cv",70,820,270,130,False),("drive",400,820,270,130,False),
        ("apply",730,820,270,130,False),("outreach",1060,820,270,130,False),
        ("learning",70,1035,270,130,False),("canonical",400,1035,600,130,False),
        ("dashboard",1060,1035,270,130,False),
    ]:
        out.append(_node(key,x,y,w,h,icons,compact))
    for x,y in [(340,269),(510,269),(890,269),(1060,269),(700,310),
                (700,625),(700,755),(340,877),(400,877),(670,877),(730,877),
                (1195,820),(205,820),(700,1035),(400,1098),(340,1098),(1000,1098),(1060,1098)]:
        out.append(_port(x,y))
    for x in (205,535,865,1195):
        for y in (420,550):
            out.append(_port(x,y))
    for x in (535,865,1195):
        out.append(_port(x,950))
    out += [_text(40, 394, "PARALLEL SOURCE READS", 15, "#7188a0", mono=True),
            _text(40, 798, "MATERIALS + AUTHORISED ACTIONS", 15, "#7188a0", mono=True),
            '<path d="M40 1208H1360" stroke="#3d444d" stroke-opacity=".7"/>',
            _text(40,1243,"Stable identities · exact artifacts · provider receipts · recoverable checkpoints",19,"#91a9c3"),
            _text(1360,1271,"Architecture animation · source-verified workflow",14,"#7188a0",anchor="end"),
            "</g>"]
    return "\n".join(out)


def render_network_mobile(icons):
    """Mobile art direction retains all major nodes with larger type."""
    out = _shell(MOBILE_WIDTH, MOBILE_HEIGHT, True)
    # Mobile routes form a readable top-down sequence with two-column branches.
    out += [_route("M185 330V355Q185 375 205 375H330Q350 375 350 395V410",0),
            _route("M515 330V355Q515 375 495 375H370Q350 375 350 395V410",0,True),
            _route("M350 510V550",1),
            _route("M350 550H205Q185 550 185 570V590",2),
            _route("M350 550H495Q515 550 515 570V590",2),
            _route("M350 550V740H205Q185 740 185 760V780",2),
            _route("M350 550V740H495Q515 740 515 760V780",2),
            _route("M185 720H20V945Q20 965 40 965H330Q350 965 350 985V1005",3),
            _route("M515 720H680V945Q680 965 660 965H370Q350 965 350 985V1005",3),
            _route("M185 910V945Q185 965 205 965H330Q350 965 350 985V1005",3),
            _route("M515 910V945Q515 965 495 965H370Q350 965 350 985V1005",3),
            _route("M350 1125V1145Q350 1165 330 1165H205Q185 1165 185 1185V1205",4),
            _route("M330 1270H370",5),
            _route("M515 1335V1370H205Q185 1370 185 1390V1410",6),
            _route("M515 1335V1410",6),
            _route("M185 1540V1560Q185 1580 205 1580H330Q350 1580 350 1600V1620",7),
            _route("M515 1540V1560Q515 1580 495 1580H370Q350 1580 350 1600V1620",7),
            _route("M350 1740V1765H205Q185 1765 185 1785V1800",8,True),
            _route("M350 1740V1765H495Q515 1765 515 1785V1800",8)]
    layouts = [
        ("request",40,240,290,90,True),("policy",370,240,290,90,True),
        ("coordinator",160,410,380,100,True),
        ("linkedin",40,590,290,130,False),("github",370,590,290,130,False),
        ("atlas",40,780,290,130,False),("history",370,780,290,130,False),
        ("prepare",140,1005,420,120,False),
        ("cv",40,1205,290,130,False),("drive",370,1205,290,130,False),
        ("apply",40,1410,290,130,False),("outreach",370,1410,290,130,False),
        ("canonical",40,1620,620,120,False),
    ]
    for key,x,y,w,h,compact in layouts:
        out.append(_node(key,x,y,w,h,icons,compact,mobile=True))
    # Footer outcomes use two concise cards to stay within the mobile viewport.
    for key,x in (("learning",40),("dashboard",370)):
        summary = "Saved checkpoints" if key=="learning" else "Signed Atlas projection"
        out.append(_node(key,x,1800,290,90,icons,compact=True,mobile=True,
                         body_lines=[summary]))
    for x,y in ((350,550),(350,965),(515,1370),(350,1580),(350,1765)):
        out.append(f'<circle cx="{x}" cy="{y}" r="4" fill="#79c0ff"/>')
    out.append("</g>")
    return "\n".join(out)


