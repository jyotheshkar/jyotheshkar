#!/usr/bin/env python3
"""Build four qualitative skill maps. Ring geometry never encodes proficiency."""
from pathlib import Path
from html import escape
import hashlib
import json
import math
import re
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
GROUPS = [
    ('languages', 'Language', 'Foundations', 'CODE / QUERY / EXPRESS', [
        ('Python', 'python'), ('JavaScript', 'javascript'), ('TypeScript', 'typescript'),
        ('Java', 'java'), ('SQL', 'database'), ('HTML', 'code'), ('CSS', 'layers'), ('Bash', 'terminal')]),
    ('engineering', 'Software', 'Engineering', 'BUILD / CONNECT / DELIVER', [
        ('React', 'react'), ('Node.js', 'nodejs'), ('Backend APIs', 'code'),
        ('PostgreSQL', 'postgresql'), ('Docker', 'docker'), ('GitHub Actions', 'github'),
        ('AWS', 'cloud'), ('System design', 'layers')]),
    ('ai', 'AI & Machine', 'Learning', 'LEARN / MODEL / EVALUATE', [
        ('PyTorch', 'pytorch'), ('TensorFlow', 'tensorflow'), ('Reinforcement|learning', 'loop'),
        ('Transformers', 'network'), ('NLP', 'text'), ('Embeddings', 'layers'),
        ('Model evaluation', 'chart'), ('RLHF', 'human')]),
    ('agentic', 'Agentic', 'AI', 'PLAN / ACT / VERIFY', [
        ('Planning', 'plan'), ('Tool calling', 'tools'), ('RAG', 'search'),
        ('Memory', 'database'), ('Workflows', 'network'), ('Guardrails', 'shield'),
        ('Tracing & evals', 'chart'), ('Human review', 'human')]),
]

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


def build():
    icons = json.loads((ROOT / 'assets/brands/icons.json').read_text(encoding='utf-8'))
    for item in json.loads((ROOT / 'assets/brands/skills-originals.json').read_text(encoding='utf-8')):
        raw = item['svg'].encode()
        assert hashlib.sha1(b'blob ' + str(len(raw)).encode() + b'\0' + raw).hexdigest() == item['sha'], item['key']
        svg = ET.fromstring(item['svg'])
        inner = re.sub(r'^.*?<svg\b[^>]*>|</svg>\s*$', '', item['svg'], flags=re.S)
        # Namespace upstream gradient IDs independently from all other marks.
        for ident in re.findall(r'\bid="([^"]+)"', inner):
            inner = inner.replace('"'+ident+'"', '"skill-'+item['key']+'-'+ident+'"').replace('#'+ident, '#skill-'+item['key']+'-'+ident)
        icons[item['key']] = {'viewBox': svg.get('viewBox'), 'inner': inner}
    used = {icon for group in GROUPS for _, icon in group[4] if icon in icons}
    symbols = ''.join(f'<symbol id="brand-{k}" viewBox="{icons[k]["viewBox"]}">{icons[k]["inner"]}</symbol>' for k in sorted(used))
    out = ['''<svg xmlns="http://www.w3.org/2000/svg" width="1400" height="1450" viewBox="0 0 1400 1450" role="img" aria-labelledby="skills-title skills-desc" color="#f0f6fc">
<title id="skills-title">Engineering constellation: four circles of skills and exploration</title>
<desc id="skills-desc">Language Foundations, Software Engineering, AI and Machine Learning, and Agentic AI. These qualitative maps show technologies and learning areas, not contribution percentages or proficiency scores. All labels stay still while decorative orbit trails move; reduced motion is supported.</desc>
<defs>
<pattern id="grid" width="40" height="40" patternUnits="userSpaceOnUse"><path d="M40 0H0V40" fill="none" stroke="#3d444d" stroke-opacity=".22" stroke-width=".65"/></pattern>
<radialGradient id="aura"><stop stop-color="#4493f8" stop-opacity=".13"/><stop offset="1" stop-color="#0d1117" stop-opacity="0"/></radialGradient>
<radialGradient id="hub"><stop stop-color="#1b2b42"/><stop offset="1" stop-color="#101720"/></radialGradient>
<linearGradient id="arc"><stop stop-color="#4493f8" stop-opacity=".06"/><stop offset="1" stop-color="#a5d6ff"/></linearGradient>
<style>
text{font-family:Arial,Helvetica,sans-serif} .mono{font-family:Consolas,monospace}
.orbit{animation:orbit 32s linear infinite;transform-box:fill-box;transform-origin:center}.reverse{animation-direction:reverse;animation-duration:44s}
.route{stroke-dasharray:3 13;animation:flow 9s linear infinite}.pulse{animation:pulse 6s ease-in-out infinite}
@keyframes orbit{to{transform:rotate(360deg)}} @keyframes flow{to{stroke-dashoffset:-96}} @keyframes pulse{50%{opacity:.4}}
@media(prefers-reduced-motion:reduce){.orbit,.route,.pulse{animation:none!important}}
</style>
''' + symbols + '''</defs>
<rect width="1400" height="1450" fill="#0d1117"/><rect width="1400" height="1450" fill="url(#grid)"/>
<text x="40" y="52" fill="#9198a1" font-size="16" letter-spacing="3" class="mono">ENGINEERING CONSTELLATION</text>
<text x="40" y="100" fill="#f0f6fc" font-size="35" font-weight="700" letter-spacing="-.7">Four connected worlds.</text>
<text x="1360" y="98" text-anchor="end" fill="#9198a1" font-size="17">Skills &amp; exploration</text>
<path d="M700 165v1180M40 755h1320" stroke="#3d444d" stroke-opacity=".35"/>
''']
    for i, (key, title1, title2, subtitle, nodes) in enumerate(GROUPS):
        cx, cy = (350 if i % 2 == 0 else 1050), (430 if i < 2 else 1090)
        out.append(f'<g data-skill-circle="{key}" aria-label="{escape(title1+" "+title2)}">')
        out.append(f'<circle cx="{cx}" cy="{cy}" r="290" fill="url(#aura)"/>')
        for radius in (145, 218):
            out.append(f'<circle cx="{cx}" cy="{cy}" r="{radius}" fill="none" stroke="#4493f8" stroke-opacity=".19" stroke-width="1"/>')
        for n, (label, icon) in enumerate(nodes):
            angle = -90 + n * 45
            x,y = point(cx,cy,218,angle)
            sx,sy = point(cx,cy,115,angle)
            ex,ey = point(cx,cy,190,angle)
            out.append(f'<path d="M{sx:.2f} {sy:.2f}L{ex:.2f} {ey:.2f}" stroke="#3d444d"/><path class="route" d="M{sx:.2f} {sy:.2f}L{ex:.2f} {ey:.2f}" stroke="#79c0ff" stroke-opacity=".5" style="animation-delay:-{n}s"/>')
            # Equal decorative arcs keep the language ring non-quantitative.
            ax,ay=point(cx,cy,131,angle-16); bx,by=point(cx,cy,131,angle+16)
            out.append(f'<path d="M{ax:.2f} {ay:.2f}A131 131 0 0 1 {bx:.2f} {by:.2f}" fill="none" stroke="#4493f8" stroke-opacity="{.3+(n%3)*.2}" stroke-width="3" stroke-linecap="round"/>')
            out.append(f'<g data-skill-node="{escape(label.replace(chr(124), " "))}"><circle cx="{x:.2f}" cy="{y:.2f}" r="29" fill="#151b23" stroke="#3b5574"/>')
            if icon in icons:
                out.append(f'<use href="#brand-{icon}" x="{x-16:.2f}" y="{y-16:.2f}" width="32" height="32"/>')
            else:
                out.append(f'<g transform="translate({x-15:.2f} {y-15:.2f})" fill="none" stroke="#79c0ff" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round">{GLYPHS[icon]}</g>')
            for j,line in enumerate(label.split('|')):
                out.append(f'<text x="{x:.2f}" y="{y+49+j*22:.2f}" text-anchor="middle" fill="#d1d9e0" font-size="20" font-weight="500">{escape(line)}</text>')
            out.append('</g>')
        out.append(f'<g transform="translate({cx} {cy})"><g class="orbit {"reverse" if i%2 else ""}"><circle r="153" fill="none" stroke="transparent"/><circle r="153" fill="none" stroke="url(#arc)" stroke-width="2" stroke-dasharray="100 861"/><circle cx="153" cy="0" r="3.5" fill="#a5d6ff"/></g></g>')
        out.append(f'<circle cx="{cx}" cy="{cy}" r="111" fill="url(#hub)" stroke="#4493f8" stroke-opacity=".6"/>')
        out.append(f'<circle cx="{cx}" cy="{cy}" r="105" fill="none" stroke="#79c0ff" stroke-opacity=".08"/>')
        out.append(f'<text x="{cx}" y="{cy-48}" text-anchor="middle" fill="#79c0ff" font-size="14" class="mono" letter-spacing="3">0{i+1}</text>')
        for j,title in enumerate((title1,title2)):
            out.append(f'<text x="{cx}" y="{cy-7+j*30}" text-anchor="middle" fill="#f0f6fc" font-size="25" font-weight="700">{escape(title)}</text>')
        out.append(f'<path d="M{cx-22} {cy+46}h44" stroke="#79c0ff" stroke-width="2" class="pulse"/>')
        out.append(f'<text x="{cx}" y="{cy+303}" text-anchor="middle" fill="#9198a1" font-size="14" class="mono" letter-spacing="1.5">{escape(subtitle)}</text></g>')
    out.append('</svg>')
    text = '\n'.join(out) + '\n'
    ET.fromstring(text)
    (ROOT/'assets/skill-circles.svg').write_text(text, encoding='utf-8', newline='\n')
    print(f'Built four skill circles, 32 nodes, {len(text.encode()):,} bytes.')


if __name__ == '__main__':
    build()
