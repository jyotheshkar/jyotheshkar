#!/usr/bin/env python3
"""Render three equally sized transparent skill cards from verified evidence."""
from html import escape
from pathlib import Path
import json
import math
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
PALETTE = ['#58a6ff','#d2a8ff','#7ee787','#ffa657','#f778ba','#39c5cf','#e3b341','#9ca8ff',
           '#68c8a0','#d8b99b','#a9c4d8','#c8a8c7']
FILES = {'languages':'skills-programming.svg','aiml':'skills-aiml.svg','agentic':'skills-agentic.svg'}


def text(x,y,label,size=18,fill='#c9d1d9',weight=400,anchor='start'):
    return f'<text x="{x}" y="{y}" fill="{fill}" font-size="{size}" font-weight="{weight}" text-anchor="{anchor}">{escape(str(label))}</text>'


def card(chart,height):
    cx,cy,radius = 220,214,100
    total = sum(item['value'] for item in chart['items'])
    assert total > 0 and all(item['value'] > 0 and item['evidence'] for item in chart['items'])
    out = [f'<g data-skill-circle="{chart["key"]}" data-total="{total}" data-center-x="{cx}" data-center-y="{cy}" aria-label="{escape(chart["title"])}">',
           f'<rect x="1" y="1" width="438" height="{height-2}" rx="20" fill="none" stroke="#30363d"/>',
           text(220,48,chart['title'],28,'#f0f6fc',600,'middle'),
           f'<circle cx="{cx}" cy="{cy}" r="{radius}" fill="none" stroke="#30363d" stroke-width="40"/>']
    circumference,offset = 2*math.pi*radius,0
    separators=[]
    for n,item in enumerate(chart['items']):
        color = PALETTE[n%len(PALETTE)]
        length = circumference*item['value']/total
        out.append(f'<circle data-segment="{escape(item["label"])}" data-value="{item["value"]}" cx="{cx}" cy="{cy}" r="{radius}" fill="none" stroke="{color}" stroke-width="40" stroke-dasharray="{length:.8f} {circumference-length:.8f}" stroke-dashoffset="{-offset:.8f}" transform="rotate(-90 {cx} {cy})"><title>{escape(item["label"])}</title></circle>')
        angle = offset/circumference*2*math.pi-math.pi/2
        x1,y1 = cx+79*math.cos(angle),cy+79*math.sin(angle)
        x2,y2 = cx+121*math.cos(angle),cy+121*math.sin(angle)
        separators.append(f'<path d="M{x1:.3f} {y1:.3f}L{x2:.3f} {y2:.3f}" stroke="#0d1117" stroke-width="3"/>')
        offset += length
    out += separators
    out.append(text(cx,cy+10,{'languages':'Code','aiml':'AI/ML','agentic':'Agents'}[chart['key']],34,'#f0f6fc',600,'middle'))
    for n,item in enumerate(chart['items']):
        color=PALETTE[n%len(PALETTE)]
        col,row = n%2,n//2
        x,y = 31+col*215,382+row*42
        width=176
        out += [f'<g data-skill-legend="{escape(item["label"])}">',
                f'<circle cx="{x}" cy="{y-6}" r="3.5" fill="{color}"/>',
                text(x+11,y,item['label'],16.5,'#d1d9e0'),
                f'<rect x="{x+11}" y="{y+9}" width="{width}" height="3.5" rx="1.75" fill="#30363d"/>',
                f'<rect data-evidence-bar="{escape(item["label"])}" x="{x+11}" y="{y+9}" width="{width*item["value"]/max(i["value"] for i in chart["items"]):.6f}" height="3.5" rx="1.75" fill="{color}"/>',
                '</g>']
    return '\n'.join(out+['</g>'])


def document(width,height,title,contents):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-label="{escape(title)}">
<title>{escape(title)}</title>
<desc>Repository evidence shown as segmented doughnuts. Names and unnumbered bars appear below each circle in two columns. Coverage is not a proficiency score. Transparent background.</desc>
<style>text{{font-family:Arial,Helvetica,sans-serif}}</style>
{contents}
</svg>
'''


def build():
    evidence=json.loads((ROOT/'config/skill-evidence.json').read_text(encoding='utf-8'))
    charts=evidence['charts']
    assert [c['key'] for c in charts]==['languages','aiml','agentic']
    height=max(580,382+math.ceil(max(len(c['items']) for c in charts)/2)*42+30)
    fragments=[card(chart,height) for chart in charts]
    assets=ROOT/'assets'
    for chart,fragment in zip(charts,fragments):
        svg=document(440,height,chart['title'],fragment)
        ET.fromstring(svg)
        (assets/FILES[chart['key']]).write_text(svg,encoding='utf-8',newline='\n')
    combined=text(25,54,'Professional Skills',38,'#f0f6fc',700)
    for n,fragment in enumerate(fragments):
        combined+=f'<g transform="translate({20+n*460} 90)">{fragment}</g>'
    (assets/'skill-circles.svg').write_text(document(1400,height+110,'Professional Skills',combined),encoding='utf-8',newline='\n')
    scale=1.5
    mobile=text(20,57,'Professional Skills',40,'#f0f6fc',700)
    for n,fragment in enumerate(fragments):
        mobile+=f'<g transform="translate(20 {90+n*(height*scale+25)}) scale({scale})">{fragment}</g>'
    (assets/'skills-mobile.svg').write_text(document(700,math.ceil(110+3*height*scale+50),'Professional Skills',mobile),encoding='utf-8',newline='\n')
    print('Built three equal transparent cards, a desktop row, and a stacked mobile view.')


if __name__=='__main__':
    build()

