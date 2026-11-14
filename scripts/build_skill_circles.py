#!/usr/bin/env python3
"""Four measured doughnut charts. Segment angles are proportional to evidence."""
from pathlib import Path
from html import escape
import json
import math
import xml.etree.ElementTree as ET

ROOT=Path(__file__).resolve().parents[1]
PALETTE=['#79c0ff','#58a6ff','#a5a0ff','#65d6ce','#e3b86c','#c995e8','#8bd49c','#a1b5ca']


def text(x,y,value,size=20,fill='#d1d9e0',anchor='start',weight='400',extra=''):
    return f'<text x="{x}" y="{y}" fill="{fill}" font-size="{size}" text-anchor="{anchor}" font-weight="{weight}" {extra}>{escape(str(value))}</text>'


def build():
    data=json.loads((ROOT/'config/portfolio-metrics.json').read_text(encoding='utf-8'))
    out=['''<svg xmlns="http://www.w3.org/2000/svg" width="1400" height="1250" viewBox="0 0 1400 1250" role="img" aria-labelledby="chart-title chart-desc">
<title id="chart-title">Portfolio composition: languages, engineering stack, AI and Agentic AI</title>
<desc id="chart-desc">Four proportional doughnut charts with values and legends. Language percentages measure unique source-file bytes. Other percentages measure the share of selected documented repository-topic matches. Repositories can appear in multiple categories. These are evidence counts, not skill scores. Snapshot of 23 public project repositories, 14 November 2026.</desc>
<defs>
<pattern id="grid" width="40" height="40" patternUnits="userSpaceOnUse"><path d="M40 0H0V40" fill="none" stroke="#3d444d" stroke-opacity=".16" stroke-width=".65"/></pattern>
<linearGradient id="surface" x2=".9" y2="1"><stop stop-color="#131d2b"/><stop offset="1" stop-color="#0f151d"/></linearGradient>
<radialGradient id="halo"><stop stop-color="#4493f8" stop-opacity=".1"/><stop offset="1" stop-color="#0d1117" stop-opacity="0"/></radialGradient>
<linearGradient id="rule"><stop stop-color="#79c0ff" stop-opacity=".7"/><stop offset="1" stop-color="#79c0ff" stop-opacity="0"/></linearGradient>
<style>
text{font-family:Arial,Helvetica,sans-serif}.mono{font-family:Consolas,monospace}
.segments{animation:reveal 1.2s ease-out both}.shimmer{animation:shimmer 8s ease-in-out infinite}
@keyframes reveal{from{opacity:0}to{opacity:1}}@keyframes shimmer{50%{opacity:.25}}
@media(prefers-reduced-motion:reduce){.segments,.shimmer{animation:none!important}}
</style></defs>
<rect width="1400" height="1250" fill="#0d1117"/><rect width="1400" height="1250" fill="url(#grid)"/>
''']
    out += [text(40,45,'PORTFOLIO / IN FOCUS',15,'#9198a1',extra='class="mono" letter-spacing="3"'),text(40,96,'The shape of my work.',38,'#f0f6fc',weight='700'),text(1360,92,f'{data["repo_count"]} public projects  /  14 NOV 2026',17,'#9198a1','end')]
    summaries=[]
    for i,chart in enumerate(data['charts']):
        x,y=(30 if i%2==0 else 720),(137 if i<2 else 654)
        cx,cy=x+164,y+260
        items=chart['items']; total=sum(v['value'] for v in items)
        assert total>0 and all(v['value']>=0 for v in items)
        assert all(v['value']==(sum(e['size'] for e in v['evidence']) if chart['unit']=='bytes' else len(v['evidence'])) for v in items)
        out.append(f'<g data-skill-circle="{chart["key"]}" data-total="{total}" aria-label="{escape(chart["title"])}">')
        out.append(f'<rect x="{x}" y="{y}" width="650" height="485" rx="22" fill="url(#surface)" stroke="#303b4c" stroke-opacity=".7"/>')
        out.append(f'<path d="M{x+23} {y}h200" stroke="url(#rule)"/>')
        out.append(text(x+28,y+41,f'0{i+1}',15,'#79c0ff',extra='class="mono"'))
        out.append(text(x+70,y+43,chart['title'],25,'#f0f6fc',weight='600'))
        out.append(text(x+28,y+76,chart['subtitle'],17,'#9198a1'))
        out.append(f'<circle cx="{cx}" cy="{cy}" r="158" fill="url(#halo)"/>')
        out.append(f'<circle cx="{cx}" cy="{cy}" r="133" fill="none" stroke="#79c0ff" stroke-opacity=".1"/>')
        out.append(f'<circle cx="{cx}" cy="{cy}" r="112" fill="none" stroke="#253144" stroke-width="26"/>')
        radius=112; circumference=2*math.pi*radius; offset=0
        out.append('<g class="segments">')
        for n,item in enumerate(items):
            value=item['value']; length=circumference*value/total
            if value:
                out.append(f'<circle data-segment="{escape(item["label"])}" data-value="{value}" cx="{cx}" cy="{cy}" r="{radius}" fill="none" stroke="{PALETTE[n]}" stroke-width="26" stroke-dasharray="{length:.8f} {circumference-length:.8f}" stroke-dashoffset="{-offset:.8f}" transform="rotate(-90 {cx} {cy})"><title>{escape(item["label"])}: {value:,} {chart["unit"]}, {100*value/total:.1f}%</title></circle>')
            offset+=length
        out.append('</g>')
        out.append(f'<path class="shimmer" d="M{cx-94} {cy-94}A133 133 0 0 1 {cx+94} {cy-94}" fill="none" stroke="#a5d6ff" stroke-opacity=".45" stroke-width="1.2"/>')
        center=f'{total/1000000:.2f}' if chart['unit']=='bytes' else str(total)
        out.append(text(cx,cy+2,center,49,'#f0f6fc','middle','600'))
        out.append(text(cx,cy+31,'MB OF SOURCE' if chart['unit']=='bytes' else 'TOPIC MATCHES',12,'#9198a1','middle',extra='class="mono" letter-spacing="1.5"'))
        out.append(text(cx,cy+177,'PROPORTION OF TOTAL',12,'#7d8590','middle',extra='class="mono" letter-spacing="1.2"'))
        lx=x+324; row_y=y+128
        out.append(text(lx,y+105,'LANGUAGE' if chart['unit']=='bytes' else 'TOPIC',11,'#7d8590',extra='class="mono" letter-spacing="1"'))
        out.append(text(x+622,y+105,'SHARE',11,'#7d8590','end',extra='class="mono" letter-spacing="1"'))
        for n,item in enumerate(items):
            yy=row_y+n*37; label=item['label']
            out.append(f'<g data-skill-node="{escape(label)}"><circle cx="{lx+4}" cy="{yy-6}" r="4" fill="{PALETTE[n]}"/>')
            out.append(text(lx+17,yy,label,15.5 if len(label)>20 else 17,'#d1d9e0'))
            out.append(text(x+622,yy,f'{100*item["value"]/total:.1f}%',18,'#f0f6fc','end','500'))
            if chart['unit']!='bytes':
                out.append(text(lx+17,yy+14,f'{item["value"]} repos',10.5,'#7d8590'))
            out.append('</g>')
        out.append(f'<path d="M{x+26} {y+432}h598" stroke="#303b4c" stroke-opacity=".65"/>')
        note='Deduplicated source bytes · excludes notebook/data exports' if chart['unit']=='bytes' else 'Share of topic matches · a repository can match multiple topics'
        out.append(text(x+28,y+460,note,14,'#9198a1'))
        out.append('</g>')
        summaries.append(chart['title']+': '+', '.join(f'{v["label"]} {100*v["value"]/total:.1f}%' for v in items))
    out += [text(40,1182,'Evidence, not proficiency scores.',17,'#d1d9e0',weight='500'),text(40,1212,'Topics reflect README and dependency evidence, including learning projects and concept designs.',16,'#9198a1'),'</svg>']
    svg='\n'.join(out)+'\n'; ET.fromstring(svg)
    (ROOT/'assets/skill-circles.svg').write_text(svg,encoding='utf-8',newline='\n')
    print('Built four proportional doughnut charts from the repository evidence snapshot.')
    print('\n'.join(summaries))


if __name__=='__main__':
    build()
