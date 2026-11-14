#!/usr/bin/env python3
"""Build the GitHub-native connected profile canvas from local brand assets."""

from pathlib import Path
from html import escape
import base64
import json
import xml.etree.ElementTree as ET
from network_section import PROJECTS, render_network
from career_section import render_career

ROOT = Path(__file__).resolve().parents[1]


def build():
    icons = json.loads((ROOT / 'assets/brands/icons.json').read_text(encoding='utf-8'))
    keele = ROOT / 'assets/brands/keele-white.png'
    if keele.exists():
        encoded = base64.b64encode(keele.read_bytes()).decode('ascii')
        icons['keele'] = {'viewBox': '0 0 3260 1656', 'inner': f'<image width="3260" height="1656" href="data:image/png;base64,{encoded}"/>'}
    symbols = []
    for key, icon in icons.items():
        symbols.append(f'<symbol id="brand-{escape(key)}" viewBox="{escape(icon["viewBox"])}">{icon["inner"]}</symbol>')
    svg = '''<svg xmlns="http://www.w3.org/2000/svg" width="1400" height="1780" viewBox="0 0 1400 1780" role="img" aria-labelledby="profile-title profile-desc" color="#f0f6fc">
<title id="profile-title">Jyothesh Karnam - Developing Agentic AI systems</title>
<desc id="profile-desc">Current Agentic AI Projects I Am Working On: YouTube Agent Concept and Crypto Agent Concept, each with eight proposed tool nodes. Original brand-colored logos identify the Google ecosystem, development tools and crypto research services. Animated routes are illustrative and human review remains in the loop. Below: verified Amazon and earlier experience; MSc Computer Science with Distinction and Best Performance Award at Keele University. No live account connections or automated trading are asserted.</desc>
<defs>
  <pattern id="page-grid" width="40" height="40" patternUnits="userSpaceOnUse"><path d="M40 0H0V40" fill="none" stroke="#3d444d" stroke-opacity=".22" stroke-width=".65"/></pattern>
  <radialGradient id="network-aura"><stop stop-color="#4493f8" stop-opacity=".055"/><stop offset="1" stop-color="#0d1117" stop-opacity="0"/></radialGradient>
  <linearGradient id="section-rule"><stop stop-color="#4493f8" stop-opacity=".5"/><stop offset="1" stop-color="#3d444d" stop-opacity=".16"/></linearGradient>
  <style>text{font-family:Arial,Helvetica,sans-serif}.mono{font-family:ui-monospace,Consolas,monospace}</style>
''' + '\n'.join(symbols) + '''
</defs>
<rect width="1400" height="1780" fill="#0d1117"/>
<rect width="1400" height="1780" fill="url(#page-grid)"/>
<ellipse cx="590" cy="535" rx="580" ry="490" fill="url(#network-aura)"/>
<text x="40" y="52" class="mono" fill="#9198a1" font-size="17" letter-spacing="3">DEVELOPING AGENTIC AI SYSTEMS</text>
<text x="36" y="120" fill="#f0f6fc" font-size="64" font-weight="700" letter-spacing="-1.6">Jyothesh Karnam.</text>
<text x="40" y="162" fill="#9198a1" font-size="22">Python / tool orchestration / retrieval / evaluation</text>
<text x="1360" y="56" text-anchor="end" class="mono" fill="#9198a1" font-size="17">LONDON, UK</text>
<path d="M40 188H1360" stroke="url(#section-rule)"/>
'''
    svg += render_network(icons)
    svg += '''<text x="40" y="1090" class="mono" fill="#9198a1" font-size="18" letter-spacing="2">EXPERIENCE / EDUCATION</text>
<g transform="translate(0 1110)">'''
    svg += render_career(icons)
    svg += '</g>\n</svg>'
    ET.fromstring(svg)
    (ROOT / 'assets/profile.svg').write_text(svg, encoding='utf-8', newline='\n')
    used_keys = {'openai'} | {p['icon'] for p in PROJECTS} | {t[0] for p in PROJECTS for t in p['tools']}
    manifest = {
        'purpose': 'Current portfolio concept graph; original brand colors and local embedded SVG resources.',
        'node_counts': {p['key']: len(p['tools']) for p in PROJECTS},
        'concept_tools': {p['title']: [t[1] for t in p['tools']] for p in PROJECTS},
        'icon_sources': [{'icon': key, **{k: v for k, v in icons[key].items() if k not in ('inner', 'viewBox')}} for key in sorted(used_keys)],
        'color_treatment': 'Upstream multicolor fills and gradients retained. OpenAI, GitHub and AI Studio use their white dark-background marks. Binance uses official gold #F0B90B.',
        'source_rebuild': 'python scripts/import_brand_icons.py (offline); python scripts/build_profile.py',
    }
    (ROOT / 'assets/profile-icon-sources.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    for key, label in [('linkedin','Connect on LinkedIn'),('projects','Explore GitHub projects'),('email','Email Jyothesh')]:
        button = f'''<svg xmlns="http://www.w3.org/2000/svg" width="330" height="64" viewBox="0 0 330 64" role="img" aria-label="{label}"><rect x=".5" y=".5" width="329" height="63" rx="10" fill="#151b23" fill-opacity=".45" stroke="#3d444d"/><text x="22" y="39" fill="#f0f6fc" font-family="Arial,Helvetica,sans-serif" font-size="21" font-weight="600">{label}</text><path d="M294 39l13-13m-12 0h12v12" fill="none" stroke="#4493f8" stroke-width="1.8"/></svg>'''
        (ROOT / f'assets/{key}-link.svg').write_text(button,encoding='utf-8',newline='\n')
    print(f'Built continuous profile canvas: {len(svg.encode("utf-8")):,} bytes, {len(icons)} authentic brand symbols.')


if __name__ == '__main__':
    build()
