#!/usr/bin/env python3
"""Build the repository-local animated agent orb. Python standard library only."""

from pathlib import Path
import math
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
CX, CY, R = 916, 257, 157
FRAMES = 17
TAU = math.tau


def project(point, angle):
    x, y, z = point
    xx = x * math.cos(angle) + z * math.sin(angle)
    zz = -x * math.sin(angle) + z * math.cos(angle)
    tilt = -.24
    yy = y * math.cos(tilt) - zz * math.sin(tilt)
    zz = y * math.sin(tilt) + zz * math.cos(tilt)
    scale = 900 / (900 - zz)
    return CX + xx * scale, CY + yy * scale, zz


def path(points, angle):
    coords = [project(p, angle) for p in points]
    return 'M' + 'L'.join(f'{x:.1f},{y:.1f}' for x, y, _ in coords)


def animate(name, values, duration='22s'):
    return f'<animate attributeName="{name}" dur="{duration}" repeatCount="indefinite" values="{";".join(values)}"/>'


def build():
    svg = ['''<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="540" viewBox="0 0 1200 540" role="img" aria-labelledby="title desc">
<title id="title">Jyothesh Karnam — Developing Agentic AI Systems</title>
<desc id="desc">London-based developer focused on Python, orchestration, retrieval and evaluation. A luminous three-dimensional particle orb rotates through a conceptual agent cognition loop: context, reasoning, tools and verification. Decorative animation makes no live system or performance claim.</desc>
<defs>
  <radialGradient id="aura"><stop stop-color="#4493f8" stop-opacity=".16"/><stop offset=".45" stop-color="#4493f8" stop-opacity=".06"/><stop offset="1" stop-color="#0d1117" stop-opacity="0"/></radialGradient>
  <radialGradient id="sphere" cx="35%" cy="30%" r="72%"><stop stop-color="#79c0ff" stop-opacity=".09"/><stop offset=".55" stop-color="#4493f8" stop-opacity=".035"/><stop offset="1" stop-color="#0d1117" stop-opacity=".02"/></radialGradient>
  <radialGradient id="inner"><stop stop-color="#f0f6fc" stop-opacity=".22"/><stop offset=".12" stop-color="#79c0ff" stop-opacity=".15"/><stop offset=".5" stop-color="#4493f8" stop-opacity=".035"/><stop offset="1" stop-color="#4493f8" stop-opacity="0"/></radialGradient>
  <linearGradient id="rule"><stop stop-color="#4493f8" stop-opacity=".6"/><stop offset=".72" stop-color="#3d444d" stop-opacity=".25"/><stop offset="1" stop-color="#0d1117" stop-opacity="0"/></linearGradient>
  <linearGradient id="orbit"><stop stop-color="#79c0ff" stop-opacity="0"/><stop offset=".52" stop-color="#79c0ff" stop-opacity=".08"/><stop offset="1" stop-color="#79c0ff" stop-opacity=".9"/></linearGradient>
  <filter id="soft" x="-100%" y="-100%" width="300%" height="300%"><feGaussianBlur stdDeviation="5"/></filter>
  <filter id="pin" x="-150%" y="-150%" width="400%" height="400%"><feGaussianBlur stdDeviation="1.8"/></filter>
  <style>
    text{font-family:Arial,Helvetica,sans-serif}.mono{font-family:ui-monospace,Consolas,"Liberation Mono",monospace}
    .breathe{transform-origin:916px 257px;animation:breathe 5s ease-in-out infinite}
    .orbitA{transform-origin:916px 257px;animation:turn 18s linear infinite}
    .orbitB{transform-origin:916px 257px;animation:turn 27s linear infinite reverse}
    .trace{stroke-dasharray:3 11;animation:trace 8s linear infinite}
    .thought{animation:thought 8s ease-in-out infinite}.p2{animation-delay:2s}.p3{animation-delay:4s}.p4{animation-delay:6s}
    .shimmer{animation:shimmer 6s ease-in-out infinite}.still{display:none}
    @keyframes turn{to{transform:rotate(360deg)}}
    @keyframes breathe{0%,100%{opacity:.55;transform:scale(.97)}50%{opacity:1;transform:scale(1.04)}}
    @keyframes trace{to{stroke-dashoffset:-112}}
    @keyframes thought{0%,18%,100%{opacity:.28}7%,11%{opacity:1}}
    @keyframes shimmer{0%,100%{opacity:.3}50%{opacity:.75}}
    @media(prefers-reduced-motion:reduce){.moving{display:none}.still{display:inline}.breathe,.orbitA,.orbitB,.trace,.thought,.shimmer{animation:none}}
  </style>
</defs>
<rect width="1200" height="540" fill="#0d1117"/>
<circle cx="916" cy="257" r="270" fill="url(#aura)"/>
<g fill="none" stroke="#3d444d" stroke-opacity=".2">
  <path d="M645 114h87l26 26M1196 379h-73l-30-30M695 441h66l21-21"/>
  <path d="M1180 92h-45M1165 77v30M694 382h-22M683 371v22"/>
</g>
<g>
  <text x="28" y="59" class="mono" fill="#9198a1" font-size="11" letter-spacing="3">JYOTHESH KARNAM / ENGINEERING</text>
  <path d="M28 79H95" stroke="#4493f8" stroke-width="2"/>
  <text x="25" y="155" fill="#f0f6fc" font-size="57" font-weight="700" letter-spacing="-2">Jyothesh Karnam.</text>
  <text x="28" y="204" fill="#9198a1" font-size="21">Developing</text>
  <text x="25" y="262" fill="#f0f6fc" font-size="52" font-weight="700" letter-spacing="-1.8">Agentic AI systems.</text>
  <text x="28" y="315" fill="#9198a1" font-size="17">From model evaluation to deliberate action.</text>
  <path d="M28 343H610" stroke="url(#rule)"/>
  <g class="mono" fill="#9198a1" font-size="12">
    <text x="28" y="376">PYTHON</text><text x="108" y="376" fill="#3d444d">/</text>
    <text x="128" y="376">ORCHESTRATION</text><text x="262" y="376" fill="#3d444d">/</text>
    <text x="282" y="376">RETRIEVAL</text><text x="382" y="376" fill="#3d444d">/</text>
    <text x="402" y="376">EVALUATION</text>
  </g>
  <g transform="translate(28 422)" fill="none" stroke="#9198a1" stroke-width="1.4"><path d="M5 0a5 5 0 0 0-5 5c0 4 5 9 5 9s5-5 5-9a5 5 0 0 0-5-5Z"/><circle cx="5" cy="5" r="1.5"/></g>
  <text x="51" y="434" class="mono" fill="#9198a1" font-size="12" letter-spacing=".7">LONDON, UK</text>
  <text x="216" y="434" class="mono" fill="#9198a1" font-size="11">BUILD. EVALUATE. ITERATE.</text>
</g>
<circle cx="916" cy="257" r="157" fill="url(#sphere)"/>
<circle class="breathe" cx="916" cy="257" r="163" fill="none" stroke="#4493f8" stroke-opacity=".1" stroke-width="7" filter="url(#soft)"/>
<circle class="breathe" cx="916" cy="257" r="133" fill="url(#inner)"/>
<g fill="none" stroke="#4493f8">
  <circle cx="916" cy="257" r="170" stroke-opacity=".12"/>
  <circle cx="916" cy="257" r="190" stroke-opacity=".08" stroke-dasharray="1 9"/>
</g>
''']
    curves = []
    for i in range(11):
        lon = i * math.pi / 11
        curves.append([(R*math.cos(t)*math.sin(lon), R*math.sin(t), R*math.cos(t)*math.cos(lon)) for t in [j*TAU/32 for j in range(33)]])
    for i in range(1, 12):
        lat = -math.pi/2 + i*math.pi/12
        curves.append([(R*math.cos(lat)*math.sin(t), R*math.sin(lat), R*math.cos(lat)*math.cos(t)) for t in [j*TAU/40 for j in range(41)]])
    svg.append('<g class="moving" fill="none" stroke="#79c0ff" stroke-width=".65" stroke-opacity=".22">')
    for c in curves:
        values = [path(c, j*TAU/(FRAMES-1)) for j in range(FRAMES)]
        svg.append(f'<path d="{values[0]}">{animate("d",values)}</path>')
    svg.append('</g><g class="still" fill="none" stroke="#79c0ff" stroke-width=".65" stroke-opacity=".22">')
    for c in curves:
        svg.append(f'<path d="{path(c,0)}"/>')
    svg.append('</g>')
    particles = []
    for i in range(112):
        y = 1 - (i+.5)/112*2
        rr = math.sqrt(1-y*y)
        a = i*math.pi*(3-math.sqrt(5))
        point = (R*rr*math.cos(a), R*y, R*rr*math.sin(a))
        coords = [project(point,j*TAU/(FRAMES-1)) for j in range(FRAMES)]
        particles.append(coords[0])
        svg.append(f'<circle class="moving" cx="{coords[0][0]:.1f}" cy="{coords[0][1]:.1f}" r="1.2" fill="#d6e9ff">')
        svg.append(animate('cx',[f'{x:.1f}' for x,y,z in coords]))
        svg.append(animate('cy',[f'{y:.1f}' for x,y,z in coords]))
        svg.append(animate('r',[f'{.6+1.35*(z/R+1)/2:.2f}' for x,y,z in coords]))
        svg.append(animate('opacity',[f'{.1+.85*(z/R+1)/2:.2f}' for x,y,z in coords]))
        svg.append('</circle>')
    svg.append('<g class="still" fill="#d6e9ff">')
    for x,y,z in particles:
        svg.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{.6+1.35*(z/R+1)/2:.2f}" opacity="{.1+.85*(z/R+1)/2:.2f}"/>')
    svg.append('''</g>
<g class="orbitA" fill="none">
  <ellipse cx="916" cy="257" rx="217" ry="58" transform="rotate(-27 916 257)" stroke="url(#orbit)" stroke-width="1.1"/>
  <circle cx="1109" cy="159" r="7" fill="#4493f8" opacity=".45" filter="url(#pin)"/>
  <circle cx="1109" cy="159" r="2.4" fill="#f0f6fc"/>
</g>
<g class="orbitB" fill="none">
  <ellipse cx="916" cy="257" rx="204" ry="87" transform="rotate(47 916 257)" stroke="#4493f8" stroke-opacity=".28" stroke-width=".7"/>
  <circle cx="1055" cy="405" r="2" fill="#79c0ff"/>
</g>
<g fill="none" stroke="#4493f8" stroke-opacity=".45" stroke-width=".8">
  <path class="trace" d="M721 150H693L662 119H631"/>
  <path class="trace" d="M1117 333h25l24 24h32"/>
</g>
<g class="mono" font-size="10" fill="#9198a1" letter-spacing="1.8">
  <g class="thought"><circle cx="757" cy="74" r="2" fill="#79c0ff"/><text x="770" y="78">CONTEXT</text></g>
  <g class="thought p2"><circle cx="1033" cy="74" r="2" fill="#79c0ff"/><text x="1046" y="78">REASON</text></g>
  <g class="thought p3"><circle cx="1033" cy="448" r="2" fill="#79c0ff"/><text x="1046" y="452">TOOLS</text></g>
  <g class="thought p4"><circle cx="757" cy="448" r="2" fill="#79c0ff"/><text x="770" y="452">VERIFY</text></g>
</g>
<path d="M28 488H1172" stroke="#3d444d" stroke-opacity=".35"/>
<text x="28" y="515" class="mono" fill="#9198a1" font-size="10" letter-spacing="1.8">HUMAN JUDGEMENT. BOUNDED AUTONOMY. VERIFIABLE OUTPUT.</text>
<text x="1172" y="515" text-anchor="end" class="mono" fill="#9198a1" font-size="10" letter-spacing="1.8">AGENTIC AI / DEVELOPMENT</text>
</svg>''')
    result = '\n'.join(svg) + '\n'
    ET.fromstring(result)
    target = ROOT/'assets/hero.svg'
    target.write_text(result,encoding='utf-8',newline='\n')
    print(f'Built {target}: {len(result.encode())} bytes; animated 3D mesh and 112 depth-aware particles.')


if __name__ == '__main__':
    build()
