#!/usr/bin/env python3
"""Build self-contained desktop/mobile GitHub profile images."""
from pathlib import Path
from html import escape
import base64
import json
import xml.etree.ElementTree as ET
import network_section as network
import career_section as career
from import_brand_icons import symbol_content

ROOT = Path(__file__).resolve().parents[1]


def load_icons():
    icons = json.loads((ROOT / 'assets/brands/icons.json').read_text(encoding='utf-8'))
    for key in ('linkedin', 'googlesheets'):
        original = ET.fromstring((ROOT / f'assets/brands/{key}-original.svg').read_text(encoding='utf-8'))
        if not original.get('viewBox'):
            original.set('viewBox', f'0 0 {original.get("width")} {original.get("height")}')
        icons[key] = symbol_content(key, ET.tostring(original, encoding='unicode'))
    amazon = base64.b64encode((ROOT / 'assets/brands/amazon-original.png').read_bytes()).decode('ascii')
    icons['amazon'] = {'viewBox': '0 0 6110 2047', 'inner': f'<image width="6110" height="2047" href="data:image/png;base64,{amazon}"/>'}
    keele = base64.b64encode((ROOT / 'assets/brands/keele-selected.png').read_bytes()).decode('ascii')
    # Display original image bytes inside the crest silhouette, retaining internal white heraldry.
    icons['keele'] = {'viewBox': '110 70 292 405', 'inner': '<defs><clipPath id="keele-crest-outline"><path d="M112 72H399V408L256 473L112 408Z"/></clipPath></defs>' + f'<image width="512" height="512" href="data:image/png;base64,{keele}" clip-path="url(#keele-crest-outline)"/>'}
    return icons


def document(width, height, title, body, icons, keys):
    symbols = ''.join(f'<symbol id="brand-{escape(key)}" viewBox="{escape(icons[key]["viewBox"])}">{icons[key]["inner"]}</symbol>' for key in sorted(keys))
    svg = f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-labelledby="image-title" color="#f0f6fc"><title id="image-title">{escape(title)}</title><defs>{symbols}</defs>{body}</svg>\n'
    ET.fromstring(svg)
    return svg


def heading(mobile=False):
    size, end = (44, 660) if mobile else (48, 1360)
    return ('<text x="40" y="49" fill="#91a9c3" font-family="Consolas,monospace" font-size="18">EXPERIENCE AND EDUCATION</text>'
            f'<text x="40" y="110" fill="#f0f6fc" font-family="Arial,Helvetica,sans-serif" font-size="{size}" font-weight="700">Experience / Education</text>'
            '<text x="40" y="150" fill="#a9b8c9" font-family="Arial,Helvetica,sans-serif" font-size="23">Professional experience. Academic achievement.</text>'
            f'<path d="M40 178H{end}" stroke="url(#career-rule)"/>')


def career_shell(width, height):
    """Share the LinkedIn architecture's dark canvas and restrained blue rule."""
    return ('<defs><pattern id="career-dots" width="25" height="25" patternUnits="userSpaceOnUse">'
            '<circle cx="1" cy="1" r=".7" fill="#3d444d" opacity=".45"/></pattern>'
            '<linearGradient id="career-rule"><stop stop-color="#4493f8" stop-opacity=".8"/>'
            '<stop offset="1" stop-color="#4493f8" stop-opacity=".05"/></linearGradient></defs>'
            f'<rect width="{width}" height="{height}" fill="#0d1117"/>'
            f'<rect width="{width}" height="{height}" fill="url(#career-dots)"/>')


def build():
    icons = load_icons()
    network_keys = {'openai', 'linkedin', 'github', 'gmail', 'googledrive', 'googlesheets'}
    outputs = {
        'profile.svg': document(network.WIDTH, network.HEIGHT, 'LinkedIn Agent — Agentic AI System Engineering', network.render_network(icons), icons, network_keys),
        'profile-mobile.svg': document(network.MOBILE_WIDTH, network.MOBILE_HEIGHT, 'LinkedIn Agent — connected workflow architecture', network.render_network_mobile(icons), icons, network_keys),
        'career.svg': document(career.WIDTH, career.HEIGHT + 194, 'Experience / Education', career_shell(career.WIDTH, career.HEIGHT + 194) + heading() + '<g transform="translate(0 194)">' + career.render_career(icons) + '</g>', icons, {'amazon', 'keele'}),
        'career-mobile.svg': document(career.MOBILE_WIDTH, career.MOBILE_HEIGHT + 194, 'Experience / Education', career_shell(career.MOBILE_WIDTH, career.MOBILE_HEIGHT + 194) + heading(True) + '<g transform="translate(0 194)">' + career.render_career_mobile(icons) + '</g>', icons, {'amazon', 'keele'}),
    }
    for name, content in outputs.items():
        (ROOT / 'assets' / name).write_text(content, encoding='utf-8', newline='\n')
    manifest = {
        'purpose': 'Installed LinkedIn plugin architecture, with illustrative branch-and-converge motion.',
        'architecture_source_version': network.SOURCE_VERSION,
        'providers': sorted(network_keys),
        'responsive_assets': list(outputs),
        'icon_sources': {
            'linkedin': 'https://github.com/devicons/devicon/blob/master/icons/linkedin/linkedin-original.svg',
            'googlesheets': 'https://github.com/walkxcode/dashboard-icons/blob/main/svg/google-sheets.svg',
            'keele': 'https://keelegreece.gr/wp-content/uploads/2025/08/ICON-NPPE2025-LOGO-KEELE-512x512-1.png',
            'amazon': 'https://assets.aboutamazon.com/2e/d7/ac71f1f344c39f8949f48fc89e71/amazon-logo-squid-ink-smile-orange.png',
        },
        'color_treatment': 'Original provider logo colours. Transparent career and skills card backgrounds with subtle borders and blue accents on a shared dark canvas. Opaque white Amazon logo plate.',
        'motion': 'Illustrative SVG motion only; not live execution status. Reduced-motion preference supported.',
        'source_rebuild': 'python scripts/import_brand_icons.py; python scripts/build_profile.py',
    }
    (ROOT / 'assets/profile-icon-sources.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + '\n', encoding='utf-8', newline='\n')
    print('Built desktop/mobile architecture and matching dark career artwork.')


if __name__ == '__main__':
    build()

