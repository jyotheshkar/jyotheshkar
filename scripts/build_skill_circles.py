#!/usr/bin/env python3
"""Render one GitHub-style skills panel with four evidence-backed sections."""
from html import escape
from pathlib import Path
import json
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
KEYS = ['languages', 'libraries', 'aiml', 'agentic']
TITLES = {'languages': 'Languages', 'libraries': 'Libraries and Frameworks',
          'aiml': 'AI/ML Engineering', 'agentic': 'Agentic AI Engineering'}
FILES = {'languages': 'skills-programming.svg', 'libraries': 'skills-libraries.svg',
         'aiml': 'skills-aiml.svg', 'agentic': 'skills-agentic.svg'}
PALETTE = ['#3572a5', '#3178c6', '#e34c26', '#f1e05a', '#563d7c', '#89e051',
           '#da5b0b', '#4f5d95', '#b07219', '#2b7489', '#e16737', '#c6538c',
           '#178600', '#00add8', '#dea584', '#a9b8c9']
LANGUAGE_COLORS = {'Python': '#3572a5', 'TypeScript': '#3178c6', 'JavaScript': '#f1e05a',
                   'HTML': '#e34c26', 'CSS': '#563d7c', 'Shell': '#89e051',
                   'PHP': '#4f5d95', 'Java': '#b07219', 'Java (Processing)': '#0096d8',
                   'JSP': '#2a6277', 'SQL': '#e38c00', 'C': '#555555', 'C++': '#f34b7d',
                   'Other': '#8b949e'}
BAR_WIDTH = 596


def display_chart(chart):
    """Show all evidence; group the JSP template signal under owner label Java."""
    items = [dict(item) for item in chart['items']]
    if chart['key'] == 'languages':
        for item in items:
            if item['label'] == 'JSP':
                item.update(label='Java', source_label='JSP')
    return {**chart, 'items': items}


def text(x, y, label, size=22, fill='#f0f6fc', weight=400, mono=False):
    family = 'Consolas,monospace' if mono else 'Arial,Helvetica,sans-serif'
    return (f'<text x="{x}" y="{y}" fill="{fill}" font-family="{family}" '
            f'font-size="{size}" font-weight="{weight}">{escape(str(label))}</text>')


def text_width(label, size=21):
    # Conservative Arial widths used only to wrap the native-style inline legend.
    widths = {'i': .23, 'l': .23, 'I': .28, 'j': .23, 't': .3, 'f': .31,
              'r': .36, 'm': .86, 'w': .8, 'M': .86, 'W': .95, ' ': .29}
    return sum(widths.get(c, .66 if c.isupper() else .56) for c in label) * size


def legend_layout(chart):
    total = sum(i['value'] for i in chart['items'])
    result, x, row = [], 0, 0
    for n, item in enumerate(chart['items']):
        percent = f"{100 * item['value'] / total:.1f}%"
        if chart['key'] == 'libraries':
            result.append((n, item, percent, (n % 2) * 300, n // 2, 0))
            row = n // 2
            continue
        label_width = text_width(item['label']) * 1.15
        width = 20 + label_width + 12 + text_width(percent, 20) * 1.1 + 30
        if x and x + width > BAR_WIDTH:
            x, row = 0, row + 1
        if width > BAR_WIDTH:
            raise ValueError('Skill label exceeds the section width: ' + item['label'])
        result.append((n, item, percent, x, row, label_width))
        x += width
    return result, row + 1


def section(chart):
    key, items = chart['key'], chart['items']
    total = sum(i['value'] for i in items)
    assert total > 0 and all(i['value'] > 0 and i['evidence'] for i in items)
    out = [f'<g data-skill-section="{key}" data-total="{total}" aria-label="{escape(TITLES[key])}">',
           text(0, 30, TITLES[key], 30, weight=700),
           f'<clipPath id="bar-{key}"><rect y="60" width="{BAR_WIDTH}" height="14" rx="7"/></clipPath>',
           f'<g clip-path="url(#bar-{key})">']
    offset = 0
    for n, item in enumerate(items):
        color = LANGUAGE_COLORS.get(item['label'], PALETTE[n % len(PALETTE)])
        width = BAR_WIDTH * item['value'] / total
        out.append(f'<rect data-segment="{escape(item["label"])}" data-value="{item["value"]}" '
                   f'x="{offset:.8f}" y="60" width="{width:.8f}" height="14" fill="{color}">'
                   f'<title>{escape(item["label"])}</title></rect>')
        if n:
            out.append(f'<path d="M{offset:.8f} 60v14" stroke="#0d1117" stroke-width="2"/>')
        offset += width
    out.append('</g>')
    layout, rows = legend_layout(chart)
    for n, item, percent, x, row, label_width in layout:
        color = LANGUAGE_COLORS.get(item['label'], PALETTE[n % len(PALETTE)])
        y = 116 + row * (34 if key == 'libraries' else 38)
        label_size = 19 if key == 'libraries' else 21
        percent_size = 18 if key == 'libraries' else 20
        detail = 'JSP template evidence grouped under Java.' if item.get('source_label') == 'JSP' else item['label']
        out += [f'<g data-skill-legend="{escape(item["label"])}">',
                f'<title>{escape(detail)}</title>',
                f'<circle cx="{x+6:.2f}" cy="{y-7}" r="6" fill="{color}"/>',
                f'<text x="{x+20:.2f}" y="{y}" fill="#f0f6fc" font-family="Arial,Helvetica,sans-serif" font-size="{label_size}" font-weight="600">'
                f'<tspan>{escape(item["label"])}</tspan><tspan dx="10" fill="#9198a1" font-size="{percent_size}" font-weight="400">{percent}</tspan></text>', '</g>']
    return '\n'.join(out + ['</g>']), 116 + (rows-1)*(34 if key == 'libraries' else 38) + 32


def document(width, height, title, contents):
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
           f'viewBox="0 0 {width} {height}" role="img" aria-labelledby="skills-title">'
           f'<title id="skills-title">{escape(title)}</title>'
           '<desc>Combined repository evidence. Each stacked bar and percentage shows a category share '
           'of verified repository evidence, not language byte totals or proficiency. '
           'One repository can support several categories. Java includes JSP template evidence.</desc>' + contents + '</svg>\n')
    ET.fromstring(svg)
    return svg


def shell(width, height, mobile=False):
    size = 44 if mobile else 48
    return ('<defs><pattern id="skills-dots" width="25" height="25" patternUnits="userSpaceOnUse">'
            '<circle cx="1" cy="1" r=".7" fill="#3d444d" opacity=".45"/></pattern>'
            '<linearGradient id="skills-rule"><stop stop-color="#4493f8" stop-opacity=".8"/>'
            '<stop offset="1" stop-color="#4493f8" stop-opacity=".05"/></linearGradient></defs>'
            f'<rect width="{width}" height="{height}" fill="#0d1117"/>'
            f'<rect width="{width}" height="{height}" fill="url(#skills-dots)"/>'
            + text(40, 49, 'REPOSITORY ENGINEERING', 18, '#91a9c3', mono=True)
            + text(40, 110, 'Professional Skills', size, weight=700)
            + text(40, 150, 'Combined evidence across all repositories.', 23, '#a9b8c9')
            + f'<path d="M40 178H{width-40}" stroke="url(#skills-rule)"/>')


def build():
    evidence = json.loads((ROOT/'config/skill-evidence.json').read_text(encoding='utf-8'))
    charts = {c['key']: display_chart(c) for c in evidence['charts']}
    assert set(charts) == set(KEYS)
    sections = {k: section(charts[k]) for k in KEYS}
    row_heights = [max(sections[k][1] for k in KEYS[i:i+2]) + 52 for i in (0, 2)]
    panel_y, row_y = 218, 250
    height = panel_y + sum(row_heights) + 64
    desktop = shell(1400, height)
    desktop += f'<rect data-skills-panel="true" x="24" y="{panel_y}" width="1352" height="{sum(row_heights)}" rx="15" fill="#0d1117" stroke="#334253" stroke-width="1.35"/>'
    desktop += f'<path d="M700 {panel_y+28}V{panel_y+sum(row_heights)-28}" stroke="#30363d"/>'
    desktop += f'<path d="M56 {panel_y+row_heights[0]}H1344" stroke="#30363d"/>'
    for n, key in enumerate(KEYS):
        x = 56 if n % 2 == 0 else 748
        y = row_y if n < 2 else row_y + row_heights[0]
        desktop += f'<g data-position="{key}" transform="translate({x} {y})">{sections[key][0]}</g>'
    desktop += text(40, height-25, 'Percentages show repository evidence share within each section. Java includes JSP templates.', 18, '#7d92aa')
    assets = ROOT/'assets'
    (assets/'skills.svg').write_text(document(1400, height, 'Professional Skills', desktop), encoding='utf-8', newline='\n')
    mobile_height = 218 + sum(sections[k][1]+52 for k in KEYS) + 84
    mobile = shell(700, mobile_height, True)
    mobile += f'<rect data-skills-panel="true" x="24" y="218" width="652" height="{mobile_height-302}" rx="15" fill="#0d1117" stroke="#334253" stroke-width="1.35"/>'
    y = 250
    for n, key in enumerate(KEYS):
        mobile += f'<g data-position="{key}" transform="translate(52 {y})">{sections[key][0]}</g>'
        y += sections[key][1]+52
        if n < 3:
            mobile += f'<path d="M52 {y-32}H648" stroke="#30363d"/>'
    mobile += text(40, mobile_height-45, 'Percentages show repository evidence share', 20, '#7d92aa')
    mobile += text(40, mobile_height-17, 'within each section. Java includes JSP templates.', 20, '#7d92aa')
    (assets/'skills-mobile.svg').write_text(document(700, mobile_height, 'Professional Skills', mobile), encoding='utf-8', newline='\n')
    for key in KEYS:
        fragment, section_height = sections[key]
        body = f'<rect width="660" height="{section_height+56}" fill="#0d1117"/><g transform="translate(32 28)">{fragment}</g>'
        (assets/FILES[key]).write_text(document(660, section_height+56, TITLES[key], body), encoding='utf-8', newline='\n')
    # Retain the historical asset URL as an alias, with no old circle UI.
    (assets/'skill-circles.svg').write_bytes((assets/'skills.svg').read_bytes())
    print('Built one GitHub-style panel with four sections and a stacked mobile view.')


if __name__ == '__main__':
    build()

