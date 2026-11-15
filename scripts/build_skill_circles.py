#!/usr/bin/env python3
"""Three measured orbital charts, restoring the original circle design."""
from pathlib import Path
from html import escape
import hashlib
import json
import math
import re
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]

GLYPHS = {
    'code': '<path d="m8 5-6 7 6 7m16-14 6 7-6 7M19 3l-6 18"/>',
    'terminal': '<rect x="1" y="2" width="30" height="22" rx="4"/><path d="m7 8 5 5-5 5m10 0h8"/>',
    'database': '<ellipse cx="16" cy="5" rx="12" ry="4"/><path d="M4 5v17c0 6 24 6 24 0V5M4 13c0 6 24 6 24 0"/>',
    'layers': '<path d="m16 2 14 7-14 7L2 9Zm-14 13 14 7 14-7M2 21l14 7 14-7"/>',
    'cloud': '<path d="M8 24h17a6 6 0 0 0 1-12A10 10 0 0 0 7 10a7 7 0 0 0 1 14Z"/>',
    'loop': '<path d="M27 12A12 12 0 0 0 6 6l-3 4m0-8v8h8M5 20a12 12 0 0 0 21 6l3-4m0 8v-8h-8"/>',
    'network': '<path d="m6 7 20 9L6 25V7l20 9"/><circle cx="6" cy="7" r="4"/><circle cx="26" cy="16" r="4"/><circle cx="6" cy="25" r="4"/>',
    'text': '<path d="M3 4h26M16 4v22M10 26h12M3 4v5m26-5v5"/>',
    'chart': '<path d="M3 3v25h26M8 21l6-8 6 3 8-12m-7 0h7v7"/>',
    'human': '<circle cx="16" cy="8" r="5"/><path d="M5 29v-5a11 11 0 0 1 22 0v5M9 22v7m14-7v7"/>',
    'plan': '<circle cx="5" cy="5" r="3"/><circle cx="27" cy="27" r="3"/><path d="M8 5h12a6 6 0 0 1 0 12h-8a5 5 0 0 0 0 10h12"/>',
    'tools': '<path d="m11 3-7 8 7 8m10-16 7 8-7 8M18 2l-4 21m-5 5h14"/>',
    'search': '<circle cx="13" cy="13" r="10"/><path d="m20 20 9 9M8 13h10m-5-5v10"/>',
    'shield': '<path d="M16 2 29 7v9c0 7-8 12-13 15C11 28 3 23 3 16V7ZM9 15l5 5 10-10"/>',
}


def point(cx, cy, radius, angle):
    a = math.radians(angle)
    return cx + radius * math.cos(a), cy + radius * math.sin(a)


PALETTE = ['#79c0ff', '#58a6ff', '#a5a0ff', '#65d6ce', '#e3b86c', '#c995e8', '#8bd49c', '#a1b5ca']
ICONS = {
    'Python':'python', 'TypeScript':'typescript', 'JavaScript':'javascript',
    'HTML':'code', 'CSS':'layers', 'SQL':'database',
    'Model evaluation':'chart', 'Scikit-learn':'network', 'PyTorch':'pytorch',
    'Transformers':'network', 'Embeddings':'layers', 'NLP':'text',
    'TensorFlow':'tensorflow', 'Reinforcement learning':'loop',
    'CI / CD':'github', 'Testing':'chart', 'SQL databases':'postgresql',
    'AWS':'cloud', 'Backend APIs':'code', 'Node.js / npm':'nodejs', 'React':'react',
    'Containers':'docker', 'Tracing / evals':'chart', 'Planning':'plan',
    'Tool use':'tools', 'Memory / state':'database', 'Orchestration':'network',
    'Guardrails':'shield', 'RAG / retrieval':'search', 'Human review':'human',
}
COLORS = {'Python':'#79b8ff', 'TypeScript':'#3178c6', 'JavaScript':'#f0db4f',
          'HTML':'#e34f26', 'CSS':'#a5a0ff', 'SQL':'#65d6ce',
          'Scikit-learn':'#f7931e', 'PyTorch':'#ee4c2c', 'TensorFlow':'#ff6f00',
          'React':'#61dafb', 'Node.js / npm':'#83cd29', 'Containers':'#2496ed',
          'AWS':'#ff9900', 'CI / CD':'#e6edf3'}


def text(x, y, value, size=20, fill='#d1d9e0', anchor='start', weight='400', extra=''):
    return f'<text x="{x}" y="{y}" fill="{fill}" font-size="{size}" text-anchor="{anchor}" font-weight="{weight}" {extra}>{escape(str(value))}</text>'


def load_icons():
    icons = json.loads((ROOT/'assets/brands/icons.json').read_text(encoding='utf-8'))
    for item in json.loads((ROOT/'assets/brands/skills-originals.json').read_text(encoding='utf-8')):
        raw = item['svg'].encode()
        assert hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest() == item['sha']
        svg = ET.fromstring(item['svg'])
        inner = re.sub(r'^.*?<svg\b[^>]*>|</svg>\s*$', '', item['svg'], flags=re.S)
        identifiers = {ident:'circle-'+item['key']+'-'+ident for ident in re.findall(r'\bid="([^"]+)"', inner)}
        inner = re.sub(r'\bid="([^"]+)"', lambda match:'id="'+identifiers[match[1]]+'"', inner)
        inner = re.sub(r'url\(#([^)]+)\)', lambda match:'url(#'+identifiers.get(match[1],match[1])+')', inner)
        inner = re.sub(r'((?:href|xlink:href)="#)([^"]+)(")', lambda match:match[1]+identifiers.get(match[2],match[2])+match[3], inner)
        icons[item['key']] = {'viewBox':svg.get('viewBox'), 'inner':inner}
    return icons


def build():
    data = json.loads((ROOT/'config/portfolio-metrics.json').read_text(encoding='utf-8'))
    source = {chart['key']:chart for chart in data['charts']}
    charts = [
        {**source['languages'], 'title':'Languages', 'subtitle':'Unique source-file bytes'},
        {**source['ai'], 'title':'AI & Machine Learning', 'subtitle':'Documented model and learning topics'},
        {**source['agentic'], 'title':'Agentic AI Engineering',
         'subtitle':'Engineering stack + agent workflows',
         'items':[*source['engineering']['items'], *source['agentic']['items']]},
    ]
    icons = load_icons()
    symbols = ''.join(f'<symbol id="circle-brand-{key}" viewBox="{icons[key]["viewBox"]}">{icons[key]["inner"]}</symbol>'
                      for key in sorted(set(ICONS.values()) & icons.keys()))
    out = ['''<svg xmlns="http://www.w3.org/2000/svg" width="1400" height="930" viewBox="0 0 1400 930" role="img" aria-labelledby="skills-title skills-desc" color="#f0f6fc">
<title id="skills-title">Three connected worlds: languages, AI and Agentic AI Engineering</title>
<desc id="skills-desc">Three horizontal orbital charts with measured source-byte and repository-topic arcs. Labels show raw bytes or repository counts, without percentage labels. Engineering stack and agentic workflow categories are combined, retaining all sixteen topics. Counts describe documented portfolio evidence, not proficiency. Source capture: 14 November 2026; curated: 15 November 2026. Orbit highlights and dotted routes are decorative; reduced motion is supported.</desc>
<defs>
<pattern id="circle-grid" width="40" height="40" patternUnits="userSpaceOnUse"><path d="M40 0H0V40" fill="none" stroke="#3d444d" stroke-opacity=".16" stroke-width=".65"/></pattern>
<radialGradient id="circle-aura"><stop stop-color="#4493f8" stop-opacity=".16"/><stop offset="1" stop-color="#0d1117" stop-opacity="0"/></radialGradient>
<radialGradient id="circle-hub"><stop stop-color="#1b2b42"/><stop offset="1" stop-color="#101720"/></radialGradient>
<linearGradient id="circle-trail"><stop stop-color="#4493f8" stop-opacity=".06"/><stop offset="1" stop-color="#a5d6ff"/></linearGradient>
<style>
text{font-family:Arial,Helvetica,sans-serif}.mono{font-family:Consolas,monospace}
.orbit{animation:orbit 32s linear infinite;transform-box:fill-box;transform-origin:center}.reverse{animation-direction:reverse;animation-duration:44s}
.route{stroke-dasharray:3 13;animation:flow 9s linear infinite}.pulse{animation:pulse 6s ease-in-out infinite}
@keyframes orbit{to{transform:rotate(360deg)}}@keyframes flow{to{stroke-dashoffset:-96}}@keyframes pulse{50%{opacity:.4}}
@media(prefers-reduced-motion:reduce){.orbit,.route,.pulse{animation:none!important}}
</style>
''' + symbols + '''</defs>
<rect width="1400" height="930" fill="#0d1117"/><rect width="1400" height="930" fill="url(#circle-grid)"/>
''']
    out += [text(30,32,'ENGINEERING CONSTELLATION',14,'#9198a1',extra='class="mono" letter-spacing="2.5"'),
            text(30,80,'Three connected worlds.',36,'#f0f6fc',weight='700'),
            text(1370,77,f'{data["repo_count"]} snapshots / 14 NOV 2026',17,'#9198a1','end'),
            '<path d="M467 115V870M933 115V870" stroke="#3d444d" stroke-opacity=".28"/>']
    summaries = []
    for index, chart in enumerate(charts):
        cx, cy = (235,700,1165)[index], 355
        x = cx-205
        items = chart['items']
        total = sum(item['value'] for item in items)
        assert total > 0 and all(item['value'] >= 0 for item in items)
        for item in items:
            expected = sum(e['size'] for e in item['evidence']) if chart['unit']=='bytes' else len(item['evidence'])
            assert item['value'] == expected
        out.append(f'<g data-skill-circle="{chart["key"]}" data-total="{total}" data-center-x="{cx}" data-center-y="{cy}" aria-label="{escape(chart["title"])}">')
        out += [text(cx,124,chart['title'],26,'#f0f6fc','middle','600'),
                text(cx,147,chart['subtitle'],17,'#9198a1','middle'),
                f'<circle cx="{cx}" cy="{cy}" r="208" fill="url(#circle-aura)"/>']
        for radius in (132,170):
            out.append(f'<circle cx="{cx}" cy="{cy}" r="{radius}" fill="none" stroke="#4493f8" stroke-opacity=".2"/>')
        radius = 110
        circumference = 2*math.pi*radius
        offset = 0
        for n, item in enumerate(items):
            color = COLORS.get(item['label'],PALETTE[n % len(PALETTE)])
            length = circumference*item['value']/total
            if item['value']:
                out.append(f'<circle data-segment="{escape(item["label"])}" data-value="{item["value"]}" cx="{cx}" cy="{cy}" r="{radius}" fill="none" stroke="{color}" stroke-opacity=".9" stroke-width="11" stroke-dasharray="{length:.8f} {circumference-length:.8f}" stroke-dashoffset="{-offset:.8f}" transform="rotate(-90 {cx} {cy})"><title>{escape(item["label"])}: {item["value"]:,} {chart["unit"]}</title></circle>')
            offset += length
            angle = -90+360*n/len(items)
            nx,ny = point(cx,cy,170,angle)
            sx,sy = point(cx,cy,121,angle)
            ex,ey = point(cx,cy,147,angle)
            out.append(f'<path d="M{sx:.2f} {sy:.2f}L{ex:.2f} {ey:.2f}" stroke="#3d444d"/><path class="route" d="M{sx:.2f} {sy:.2f}L{ex:.2f} {ey:.2f}" stroke="{color}" stroke-opacity=".6" style="animation-delay:-{n}s"/>')
            out.append(f'<g data-skill-node="{escape(item["label"])}"><title>{escape(item["label"])}: {item["value"]:,} {chart["unit"]}</title><circle cx="{nx:.2f}" cy="{ny:.2f}" r="23" fill="#151b23" stroke="#3b5574"/>')
            icon = ICONS[item['label']]
            if icon in icons:
                out.append(f'<use href="#circle-brand-{icon}" x="{nx-14:.2f}" y="{ny-14:.2f}" width="28" height="28"/>')
            else:
                out.append(f'<g transform="translate({nx-12:.2f} {ny-12:.2f}) scale(.75)" fill="none" stroke="{color}" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round">{GLYPHS[icon]}</g>')
            out.append('</g>')
        out.append(f'<g transform="translate({cx} {cy})"><g class="orbit {"reverse" if index % 2 else ""}"><circle r="132" fill="none" stroke="transparent"/><circle r="132" fill="none" stroke="url(#circle-trail)" stroke-width="1.8" stroke-dasharray="95 734.38046"/><circle cx="132" cy="0" r="3" fill="#a5d6ff"/></g></g>')
        out += [f'<circle cx="{cx}" cy="{cy}" r="91" fill="url(#circle-hub)" stroke="#4493f8" stroke-opacity=".65"/>',
                f'<circle cx="{cx}" cy="{cy}" r="85" fill="none" stroke="#79c0ff" stroke-opacity=".09"/>',
                text(cx,cy-35,f'0{index+1}',13,'#79c0ff','middle',extra='class="mono" letter-spacing="3"'),
                text(cx,cy+15,f'{total/1_000_000:.2f}' if chart['unit']=='bytes' else str(total),46,'#f0f6fc','middle','600'),
                text(cx,cy+42,'MB OF SOURCE' if chart['unit']=='bytes' else 'TOPIC MATCHES',12,'#9198a1','middle',extra='class="mono" letter-spacing="1"')]
        columns = 2 if len(items)>8 else 1
        out.append(text(x+5,582,'SOURCE BYTES' if chart['unit']=='bytes' else 'REPOSITORIES PER TOPIC',12,'#7d8590',extra='class="mono" letter-spacing="1"'))
        for n, item in enumerate(items):
            column = n//8 if columns==2 else 0
            row = n % 8 if columns==2 else n
            lx,yy = x+column*212, 618+row*34
            color = COLORS.get(item['label'],PALETTE[n % len(PALETTE)])
            out.append(f'<g data-skill-legend="{escape(item["label"])}"><circle cx="{lx+7}" cy="{yy-6}" r="4" fill="{color}"/>')
            out.append(text(lx+19,yy,item['label'],16 if columns==2 else 20))
            out.append(text(lx+(202 if columns==2 else 410),yy,f'{item["value"]:,}',17 if columns==2 else 20,'#f0f6fc','end','500'))
            out.append('</g>')
        out.append('</g>')
        summaries.append(f'{chart["title"]}: {len(items)} categories; {total:,} {chart["unit"]}.')
    out += [text(30,901,'Arcs show source bytes or documented topic matches. A repository can appear in several topics.',16,'#9198a1'),'</svg>']
    svg = '\n'.join(out)+'\n'
    ET.fromstring(svg)
    (ROOT/'assets/skill-circles.svg').write_text(svg,encoding='utf-8',newline='\n')
    print('Built three orbital evidence circles in one row, without percentage labels.')
    print('\n'.join(summaries))


if __name__ == '__main__':
    build()
