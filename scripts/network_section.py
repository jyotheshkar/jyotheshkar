"""Two illustrative agent projects, with eight tool nodes per concept.

All resources are embedded local SVG symbols. Routes are decorative, with a
reduced-motion fallback; they do not imply deployed or connected integrations.
"""

from html import escape


PROJECTS = (
    {
        'key': 'youtube', 'x': 350, 'icon': 'youtube',
        'title': 'YouTube Agent Concept', 'line1': 'YouTube Agent',
        'subtitle': 'Research / plan / review',
        'tools': (
            ('gemini', 'Gemini', 'Planning + models'),
            ('google', 'Google Search', 'Discovery'),
            ('gmail', 'Gmail', 'Review digests'),
            ('googledrive', 'Google Drive', 'Knowledge files'),
            ('googleaistudio', 'AI Studio', 'Prompt experiments'),
            ('googlecloud', 'Google Cloud', 'Runtime + APIs'),
            ('python', 'Python', 'Tool adapters'),
            ('github', 'GitHub', 'Code + evaluation'),
        ),
    },
    {
        'key': 'crypto', 'x': 1050, 'icon': 'binance',
        'title': 'Crypto Agent Concept', 'line1': 'Crypto Agent',
        'subtitle': 'Observe / analyse / review',
        'tools': (
            ('binance', 'Binance', 'Market-data API'),
            ('bitcoin', 'Bitcoin', 'BTC research'),
            ('ethereum', 'Ethereum', 'ETH research'),
            ('solana', 'Solana', 'SOL research'),
            ('python', 'Python', 'Analysis tools'),
            ('postgresql', 'PostgreSQL', 'Evidence store'),
            ('openai', 'OpenAI', 'Research + tools'),
            ('redis', 'Redis', 'Cache + queues'),
        ),
    },
)

# Clockwise pairs around each hub. The 180 x 74 cards fit entirely within their
# 640-pixel-wide concept region, with clear gutters around the centre surface.
TOOL_POSITIONS = ((-100, 485), (100, 485), (220, 630), (220, 805),
                  (100, 950), (-100, 950), (-220, 805), (-220, 630))


def render_network(icons):
    """Return a local-symbol SVG fragment fitting x=0..1400, y=200..1050."""
    def icon(key, x, y, size=34):
        if key not in icons:
            raise KeyError('Missing authentic icon: ' + key)
        return (f'<use href="#brand-{escape(key)}" x="{x}" y="{y}" '
                f'width="{size}" height="{size}"/>')

    out = ['''
<defs>
  <linearGradient id="nw-route"><stop stop-color="#4493f8" stop-opacity=".2"/><stop offset=".5" stop-color="#79c0ff" stop-opacity=".7"/><stop offset="1" stop-color="#4493f8" stop-opacity=".2"/></linearGradient>
  <radialGradient id="nw-core"><stop stop-color="#4493f8" stop-opacity=".1"/><stop offset="1" stop-color="#0d1117" stop-opacity="0"/></radialGradient>
  <filter id="nw-glow" x="-30%" y="-60%" width="160%" height="220%"><feGaussianBlur stdDeviation="5"/></filter>
  <style>
    .nw-label{font-family:Arial,Helvetica,sans-serif}.nw-mono{font-family:Consolas,"Liberation Mono",monospace}
    .nw-flow{stroke-dasharray:3 16;animation:nw-flow 7s linear infinite}
    .nw-phase{animation:nw-phase 8s ease-in-out infinite}.nw-p2{animation-delay:2s}.nw-p3{animation-delay:4s}.nw-p4{animation-delay:6s}
    @keyframes nw-flow{to{stroke-dashoffset:-114}}
    @keyframes nw-phase{0%,100%{opacity:.3}20%,35%{opacity:1}}
    @media(prefers-reduced-motion:reduce){.nw-flow,.nw-phase{animation:none}.nw-packet{display:none}}
  </style>
</defs>
<text x="40" y="228" fill="#9198a1" font-size="16" letter-spacing="2.6" class="nw-mono">CONNECTED INTELLIGENCE</text>
<text x="1360" y="228" text-anchor="end" fill="#9198a1" font-size="14" class="nw-mono">TOOLS + KNOWLEDGE + HUMAN REVIEW</text>
<g id="current-agentic-projects" class="nw-label" aria-labelledby="current-projects-title">
  <title id="current-projects-title">Current Agentic AI Projects I Am Working On</title>
  <rect x="444" y="256" width="512" height="138" rx="23" fill="none" stroke="#4493f8" stroke-opacity=".15" stroke-width="8" filter="url(#nw-glow)"/>
  <rect x="450" y="262" width="500" height="126" rx="18" fill="#151b23" stroke="#4493f8" stroke-opacity=".7" stroke-width="1.5"/>
  <path d="M474 262h52M874 388h52" stroke="#79c0ff" stroke-width="2"/>
''', icon('openai', 479, 292, 64), '''
  <text x="570" y="311" fill="#f0f6fc" font-size="24" font-weight="700">Current Agentic AI Projects</text>
  <text x="570" y="345" fill="#f0f6fc" font-size="24" font-weight="700">I Am Working On</text>
</g>
''']

    def route(path, index, main=False):
        out.append(f'<path d="{path}" fill="none" stroke="#3d444d" stroke-width="1.4" stroke-opacity=".8"/>')
        out.append(f'<path class="nw-flow" d="{path}" fill="none" stroke="url(#nw-route)" stroke-width="1.5" style="animation-delay:-{index % 7}s"/>')
        if main:
            out.append(f'<g class="nw-packet"><circle r="3.5" fill="#79c0ff"><animateMotion dur="8s" begin="-{index * 2}s" repeatCount="indefinite" path="{path}"/></circle></g>')

    # One shared heading branches to both concepts; all edges are behind cards.
    route('M700 388V418C700 550 350 530 350 653', 0, True)
    route('M700 388V418C700 550 1050 530 1050 653', 1, True)
    out.append('<circle cx="700" cy="418" r="3.5" fill="#79c0ff"/>')

    for project in PROJECTS:
        key, cx, cy = project['key'], project['x'], 710
        out.append(f'<g id="{key}-concept" aria-labelledby="{key}-concept-title">')
        out.append(f'<title id="{key}-concept-title">{project["title"]}: eight proposed tool integrations</title>')
        out.append(f'<ellipse cx="{cx}" cy="{cy}" rx="300" ry="285" fill="url(#nw-core)"/>')
        out.append(f'<ellipse cx="{cx}" cy="{cy}" rx="222" ry="225" fill="none" stroke="#4493f8" stroke-width=".9" stroke-opacity=".12" stroke-dasharray="2 10"/>')
        for index, ((dx, y), tool) in enumerate(zip(TOOL_POSITIONS, project['tools'])):
            x = cx + dx
            if abs(dx) == 220:
                start_x, start_y = cx + (120 if dx > 0 else -120), cy
                end_x = x + (-90 if dx > 0 else 90)
                path = f'M{start_x} {start_y}C{(start_x + end_x)/2} {start_y} {(start_x + end_x)/2} {y} {end_x} {y}'
            else:
                start_x, start_y = cx, cy + (57 if y > cy else -57)
                end_y = y + (-37 if y > cy else 37)
                path = f'M{start_x} {start_y}C{start_x} {(start_y + end_y)/2} {x} {(start_y + end_y)/2} {x} {end_y}'
            route(path, index + 2)
        out.append(f'<g class="nw-label"><rect x="{cx-120}" y="653" width="240" height="114" rx="18" fill="#151b23" stroke="#4493f8" stroke-opacity=".7" stroke-width="1.5"/>')
        out.append(icon(project['icon'], cx-20, 669, 40))
        out.append(f'<text x="{cx}" y="734" text-anchor="middle" fill="#f0f6fc" font-size="22" font-weight="700">{project["line1"]}</text>')
        out.append(f'<text x="{cx}" y="755" text-anchor="middle" fill="#9198a1" font-size="16">Concept</text></g>')
        for (dx, y), (tool_key, label, sub) in zip(TOOL_POSITIONS, project['tools']):
            x, left, top = cx + dx, cx + dx - 90, y - 37
            out.append(f'<g id="{key}-tool-{tool_key}" class="nw-tool nw-label" data-concept="{key}"><title>{escape(label)} / {escape(sub)}</title>')
            out.append(f'<rect x="{left}" y="{top}" width="180" height="74" rx="12" fill="#151b23" fill-opacity=".9" stroke="#3d444d"/>')
            out.append(f'<path d="M{left+14} {top}h26" stroke="#4493f8" stroke-opacity=".6"/>')
            if tool_key == 'ethereum':
                out.append(f'<circle cx="{left+30}" cy="{y}" r="20" fill="#f0f6fc"/>')
            out.append(icon(tool_key, left+14, y-16, 32))
            out.append(f'<text x="{left+58}" y="{y-3}" fill="#f0f6fc" font-size="17" font-weight="600">{escape(label)}</text>')
            out.append(f'<text x="{left+58}" y="{y+18}" fill="#9198a1" font-size="13">{escape(sub)}</text></g>')
        out.append(f'<text x="{cx}" y="1009" text-anchor="middle" fill="#9198a1" font-size="15" class="nw-mono">{escape(project["subtitle"])}</text></g>')
    out.append('''<text x="700" y="1044" text-anchor="middle" fill="#9198a1" font-size="14" class="nw-mono">Concept integrations / human review in the loop / no connected accounts or automated trading implied.</text>''')
    return '\n'.join(out)
