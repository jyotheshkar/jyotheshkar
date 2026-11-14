"""Connected agent ecosystem illustration for a GitHub profile SVG.

No browser script or external resources are emitted. All logos are local symbols.
"""

from html import escape


ICON_KEYS = (
    'openai', 'github', 'gmail', 'youtube', 'binance', 'bitcoin',
    'ethereum', 'solana', 'spacex', 'tesla', 'anthropic', 'nvidia',
    'microsoft', 'google', 'gemini', 'googleaistudio', 'googleflow',
    'googledrive',
)


def render_network(icons=None):
    """Return a fragment fitting x=0..1400, y=200..1050.

    The enclosing SVG must define authentic logos as symbols named brand-{key}.
    If a product-specific mark is unavailable, its real parent brand is used.
    """
    if icons is None:
        icons = {key: {} for key in ICON_KEYS}

    aliases = {
        'googleaistudio': ('google-ai-studio', 'googlegemini', 'gemini', 'google'),
        'googleflow': ('google-flow', 'flow', 'google'),
        'googledrive': ('google-drive', 'drive', 'google'),
        'gmail': ('email', 'mail'),
        'openai': ('chatgpt',),
        'spacex': ('space-x',),
    }

    def icon(key, x, y, size=30):
        actual = key if key in icons else next((a for a in aliases.get(key, ()) if a in icons), None)
        if actual is None:
            raise KeyError('Missing authentic icon: ' + key)
        return f'<use href="#brand-{escape(actual)}" x="{x}" y="{y}" width="{size}" height="{size}"/>'

    svg = ['''
<defs>
  <linearGradient id="nw-route"><stop stop-color="#4493f8" stop-opacity=".12"/><stop offset=".55" stop-color="#79c0ff" stop-opacity=".7"/><stop offset="1" stop-color="#4493f8" stop-opacity=".28"/></linearGradient>
  <radialGradient id="nw-core"><stop stop-color="#4493f8" stop-opacity=".12"/><stop offset="1" stop-color="#0d1117" stop-opacity="0"/></radialGradient>
  <filter id="nw-glow" x="-200%" y="-200%" width="500%" height="500%"><feGaussianBlur stdDeviation="3"/></filter>
  <style>
    .nw-label{font-family:Arial,Helvetica,sans-serif}.nw-mono{font-family:Consolas,"Liberation Mono",monospace}
    .nw-flow{stroke-dasharray:3 15;animation:nw-flow 5s linear infinite}
    .nw-phase{animation:nw-phase 10s ease-in-out infinite}.nw-p2{animation-delay:2.5s}.nw-p3{animation-delay:5s}.nw-p4{animation-delay:7.5s}
    .nw-halo{animation:nw-halo 5s ease-in-out infinite;transform-origin:560px 535px}
    @keyframes nw-flow{to{stroke-dashoffset:-108}}
    @keyframes nw-phase{0%,100%{opacity:.35}10%,20%{opacity:1}35%{opacity:.35}}
    @keyframes nw-halo{0%,100%{opacity:.25}50%{opacity:.7}}
    @media(prefers-reduced-motion:reduce){.nw-flow,.nw-phase,.nw-halo{animation:none}.nw-packet{display:none}}
  </style>
</defs>
<g class="nw-label">
  <text x="40" y="218" fill="#9198a1" font-size="16" letter-spacing="2.6" class="nw-mono">CONNECTED INTELLIGENCE</text>
  <text x="40" y="246" fill="#9198a1" font-size="14" class="nw-mono">CONCEPT / TOOLS + KNOWLEDGE + REVIEW</text>
</g>
<circle cx="560" cy="535" r="230" fill="url(#nw-core)"/>
''']

    def route(d, index, secondary=False):
        color = '#4493f8' if not secondary else '#9198a1'
        opacity = '.5' if not secondary else '.35'
        svg.append(f'<path d="{d}" fill="none" stroke="#3d444d" stroke-width="1.5" stroke-opacity=".7"/>')
        svg.append(f'<path class="nw-flow" d="{d}" fill="none" stroke="{color}" stroke-width="1.4" stroke-opacity="{opacity}" style="animation-delay:-{index % 5}s"/>')
        # Native SVG motion is decorative; reduced-motion users retain the paths.
        svg.append(f'<g class="nw-packet"><circle r="3.6" fill="#79c0ff"><animateMotion dur="{5.5 + index % 4}s" begin="-{index * .67:.2f}s" repeatCount="indefinite" path="{d}"/></circle></g>')

    # Agent to five capability domains, laid out before all node surfaces.
    route('M438 490C383 490 377 310 335 310', 0)
    route('M438 535C388 535 379 520 335 520', 1)
    route('M438 582C384 582 399 760 382 760', 2)
    route('M682 492C748 492 792 390 930 390', 3)
    route('M682 585C764 585 786 735 930 735', 4)

    # Binance -> Bitcoin / Ethereum / Solana.
    route('M280 802V845C280 876 110 870 110 914', 5, True)
    route('M280 802V855C280 878 330 882 330 914', 6, True)
    route('M280 802V845C280 876 550 870 550 914', 7, True)

    # YouTube / Google -> six genuine ecosystem products.
    top = [(800, 'youtube', 'YouTube', 'Data API'),
           (1040, 'google', 'Google', 'Search'),
           (1280, 'gemini', 'Gemini', 'Models')]
    bottom = [(800, 'googleaistudio', 'Google', 'AI Studio'),
              (1040, 'googleflow', 'Google Flow', 'Creative tools'),
              (1280, 'googledrive', 'Google', 'Drive')]
    for j, (x, _, _, _) in enumerate(top):
        route(f'M1040 348C1040 308 {x} 319 {x} 280', 8+j, True)
    for j, (x, _, _, _) in enumerate(bottom):
        route(f'M1040 432C1040 470 {x} 466 {x} 502', 11+j, True)

    # Company research is a neutral watchlist, including private companies.
    route('M1040 777C1040 806 800 790 800 832', 14, True)
    route('M1040 777V832', 15, True)
    route('M1040 777C1040 806 1280 790 1280 832', 16, True)
    route('M930 735H684V990H825', 17, True)
    route('M1150 735H1390V990H1255', 18, True)

    def app_node(x, y, key, label, sub, width=210, height=82, small=False):
        left, top_y = x-width/2, y-height/2
        svg.append(f'<g class="nw-label"><rect x="{left}" y="{top_y}" width="{width}" height="{height}" rx="13" fill="#151b23" fill-opacity=".68" stroke="#3d444d" stroke-opacity=".9"/>')
        svg.append(f'<path d="M{left+15} {top_y}h34" stroke="#4493f8" stroke-opacity=".7" stroke-width="1.5"/>')
        size = 30 if small else 34
        svg.append(icon(key, left+18, y-size/2, size))
        tx = left+61 if small else left+68
        svg.append(f'<text x="{tx}" y="{y-4}" fill="#f0f6fc" font-size="{19 if small else 22}" font-weight="600">{escape(label)}</text>')
        svg.append(f'<text x="{tx}" y="{y+20}" fill="#9198a1" font-size="{16 if small else 17}">{escape(sub)}</text></g>')

    app_node(230, 310, 'github', 'GitHub', 'Code + versioning')
    app_node(230, 520, 'gmail', 'Email', 'Gmail + outreach')
    app_node(280, 760, 'binance', 'Binance', 'Crypto research', width=204)
    app_node(1040, 390, 'youtube', 'YouTube', 'Google ecosystem', width=220, height=84)

    # Custom market parent, a semantic graph/market icon rather than a brand.
    svg.append('''<g class="nw-label">
      <rect x="930" y="693" width="220" height="84" rx="13" fill="#151b23" fill-opacity=".68" stroke="#3d444d"/>
      <path d="M945 693h34" stroke="#4493f8" stroke-opacity=".7" stroke-width="1.5"/>
      <g transform="translate(947 717)" fill="none" stroke="#79c0ff" stroke-width="2"><path d="M0 26V0M0 26H34M5 20l8-7 7 3L32 3"/><path d="M24 3h8v8"/></g>
      <text x="997" y="731" fill="#f0f6fc" font-size="22" font-weight="600">Markets</text>
      <text x="997" y="755" fill="#9198a1" font-size="17">Company research</text>
    </g>''')

    for x, key, label, sub in top:
        app_node(x, 242, key, label, sub, 190, 76, True)
    for x, key, label, sub in bottom:
        app_node(x, 540, key, label, sub, 190, 76, True)
    for x, key, name, ticker in [(110, 'bitcoin', 'Bitcoin', 'BTC'), (330, 'ethereum', 'Ethereum', 'ETH'), (550, 'solana', 'Solana', 'SOL')]:
        app_node(x, 952, key, name, ticker, 178, 76, True)
    for x, y, key, name, sub in [(800, 870, 'spacex', 'SpaceX', 'IPO watch'),
                                (1040, 870, 'tesla', 'Tesla', 'Watchlist'),
                                (1280, 870, 'anthropic', 'Anthropic', 'IPO watch'),
                                (920, 990, 'nvidia', 'NVIDIA', 'Watchlist'),
                                (1160, 990, 'microsoft', 'Microsoft', 'Watchlist')]:
        app_node(x, y, key, name, sub, 190, 76, True)

    # Central orchestration surface. A logo, not an orb or a claim of a live agent.
    svg.append('''<g class="nw-label">
      <rect class="nw-halo" x="430" y="438" width="260" height="194" rx="27" fill="none" stroke="#4493f8" stroke-width="8" stroke-opacity=".12" filter="url(#nw-glow)"/>
      <rect x="438" y="446" width="244" height="178" rx="21" fill="#151b23" fill-opacity=".74" stroke="#4493f8" stroke-opacity=".62" stroke-width="1.5"/>
      <path d="M462 446h54M606 624h52" fill="none" stroke="#79c0ff" stroke-width="2"/>
    ''')
    svg.append(icon('openai', 528, 464, 64))
    svg.append('''
      <text x="560" y="565" text-anchor="middle" fill="#f0f6fc" font-size="26" font-weight="700" letter-spacing="1">AGENTIC AI</text>
      <text x="560" y="595" text-anchor="middle" fill="#9198a1" font-size="17">Plan · act · verify</text>
      <text x="560" y="665" text-anchor="middle" fill="#9198a1" font-size="15">HUMAN REVIEW IN THE LOOP</text>
      <g fill="#79c0ff">
        <circle class="nw-phase" cx="475" cy="416" r="3"/><circle class="nw-phase nw-p2" cx="530" cy="416" r="3"/><circle class="nw-phase nw-p3" cx="585" cy="416" r="3"/><circle class="nw-phase nw-p4" cx="640" cy="416" r="3"/>
      </g>
    </g>
<text x="40" y="1042" fill="#9198a1" font-size="14" class="nw-mono">Illustrative ecosystem · animated routes show concepts, not connected accounts or investment holdings.</text>
''')
    return '\n'.join(svg)


if __name__ == '__main__':
    import xml.etree.ElementTree as ET
    fragment = render_network()
    ET.fromstring('<svg xmlns="http://www.w3.org/2000/svg">' + fragment + '</svg>')
    print('Network fragment validated:', len(fragment), 'characters')
