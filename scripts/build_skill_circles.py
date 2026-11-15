#!/usr/bin/env python3
"""Render three proportional evidence doughnuts with name-only legends."""
from html import escape
from pathlib import Path
import json
import math
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
PALETTE = ['#79c0ff', '#58a6ff', '#388bfd', '#65d6ce', '#46a6ab', '#9baeff',
           '#a5d6ff', '#5198b5', '#7795ce', '#7cc9be', '#c4d8ef', '#56778f']


def text(x, y, value, size=18, fill='#c9d1d9', weight=400, anchor='start', extra=''):
    return (f'<text x="{x}" y="{y}" fill="{fill}" font-size="{size}" '
            f'font-weight="{weight}" text-anchor="{anchor}" {extra}>{escape(str(value))}</text>')


def build():
    data = json.loads((ROOT / 'config/skill-evidence.json').read_text(encoding='utf-8'))
    charts = data['charts']
    assert [c['key'] for c in charts] == ['languages', 'libraries', 'agentic']
    longest = max(len(c['items']) for c in charts)
    height = max(570, 183 + longest * 37 + 58)
    center_y = 327
    out = [f'''<svg xmlns="http://www.w3.org/2000/svg" width="1400" height="{height}" viewBox="0 0 1400 {height}" role="img" aria-labelledby="skills-title skills-desc">
<title id="skills-title">Professional Skills</title>
<desc id="skills-desc">Programming Languages, Libraries and Frameworks, and Agentic AI Engineering. Segments and bars show repository evidence coverage, not proficiency. Skill names appear to the right of each circle, with no numeric labels. Evidence is automatically refreshed from public repositories.</desc>
<defs>
<pattern id="skill-grid" width="40" height="40" patternUnits="userSpaceOnUse"><path d="M40 0H0V40" fill="none" stroke="#3d444d" stroke-opacity=".16" stroke-width=".65"/></pattern>
<radialGradient id="skill-center"><stop stop-color="#172a40"/><stop offset="1" stop-color="#101720"/></radialGradient>
<style>text{{font-family:Arial,Helvetica,sans-serif}}.mono{{font-family:Consolas,monospace}}</style>
</defs>
<rect width="1400" height="{height}" fill="#0d1117"/><rect width="1400" height="{height}" fill="url(#skill-grid)"/>
''', text(38, 57, 'Professional Skills', 37, '#f0f6fc', 700),
           text(40, 92, 'Built through projects. Grounded in repository evidence.', 19, '#9198a1')]
    for index, chart in enumerate(charts):
        left = 24 + index * 464
        cx = left + 106
        items = chart['items']
        total = sum(item['value'] for item in items)
        assert all(item['value'] > 0 and item['evidence'] for item in items)
        out += [f'<g data-skill-circle="{chart["key"]}" data-total="{total}" data-center-x="{cx}" data-center-y="{center_y}" aria-label="{escape(chart["title"])}">',
                f'<rect x="{left}" y="123" width="448" height="{height-160}" rx="18" fill="#151b23" fill-opacity=".48" stroke="#30363d"/>',
                text(left + 22, 164, chart['title'], 22, '#f0f6fc', 600),
                f'<circle cx="{cx}" cy="{center_y}" r="82" fill="none" stroke="#263241" stroke-width="34"/>']
        radius = 82
        circumference = 2 * math.pi * radius
        offset = 0
        for n, item in enumerate(items):
            color = PALETTE[n % len(PALETTE)]
            length = circumference * item['value'] / total
            out.append(f'<circle data-segment="{escape(item["label"])}" data-value="{item["value"]}" cx="{cx}" cy="{center_y}" r="{radius}" fill="none" stroke="{color}" stroke-width="34" stroke-dasharray="{length:.8f} {circumference-length:.8f}" stroke-dashoffset="{-offset:.8f}" transform="rotate(-90 {cx} {center_y})"><title>{escape(item["label"])}</title></circle>')
            angle = offset / circumference * 2 * math.pi - math.pi / 2
            x1, y1 = cx + 64 * math.cos(angle), center_y + 64 * math.sin(angle)
            x2, y2 = cx + 100 * math.cos(angle), center_y + 100 * math.sin(angle)
            out.append(f'<path d="M{x1:.3f} {y1:.3f}L{x2:.3f} {y2:.3f}" stroke="#0d1117" stroke-width="2.2"/>')
            offset += length
            lx, ly = left + 229, 208 + n * 37
            out += [f'<g data-skill-legend="{escape(item["label"])}">',
                    f'<circle cx="{lx-11}" cy="{ly-6}" r="3.5" fill="{color}"/>',
                    text(lx, ly, item['label'], 17, '#d1d9e0'),
                    f'<rect x="{lx}" y="{ly+7}" width="185" height="3" rx="1.5" fill="#25303d"/>',
                    f'<rect data-evidence-bar="{escape(item["label"])}" x="{lx}" y="{ly+7}" width="{185*item["value"]/max(i["value"] for i in items):.5f}" height="3" rx="1.5" fill="{color}"/>',
                    '</g>']
        out += [f'<circle cx="{cx}" cy="{center_y}" r="61" fill="url(#skill-center)" stroke="#303f51"/>']
        center_label = {'languages': ('Code', 'LANGUAGES'), 'libraries': ('Build', 'FRAMEWORKS'), 'agentic': ('Agentic', 'ENGINEERING')}[chart['key']]
        out += [text(cx, center_y+1, center_label[0], 26, '#f0f6fc', 600, 'middle'),
                text(cx, center_y+24, center_label[1], 10, '#8ea9c6', anchor='middle', extra='class="mono" letter-spacing="1.2"')]
        if not items:
            out.append(text(left+229, 220, 'No verified evidence yet', 16, '#9198a1'))
        out.append('</g>')
    out += [text(40, height-12, 'Repository evidence · Automatically refreshed', 15, '#7d8590'), '</svg>']
    svg = '\n'.join(out) + '\n'
    ET.fromstring(svg)
    (ROOT / 'assets/skill-circles.svg').write_text(svg, encoding='utf-8', newline='\n')
    print('Built three evidence-based doughnut charts with names and unnumbered bars.')


if __name__ == '__main__':
    build()

