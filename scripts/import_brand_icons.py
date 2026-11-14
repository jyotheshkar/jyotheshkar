#!/usr/bin/env python3
"""Import pinned, locally retained upstream color artwork into the SVG registry.

Offline by default. --download retrieves the exact recorded Git blob through
GitHub's public API and verifies its content hash before replacing local source.
"""

import argparse
import base64
import hashlib
import json
from pathlib import Path
import re
import urllib.request
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'assets/brands/color-originals.json'


def symbol_content(key, source):
    root = ET.fromstring(source)
    ids = {el.get('id'): f'brand-{key}-{el.get("id")}'
           for el in root.iter() if el.get('id')}
    for element in root.iter():
        element.tag = element.tag.split('}')[-1]
        for attr, value in list(element.attrib.items()):
            new_attr = attr.split('}')[-1]
            if new_attr == 'id':
                value = ids[value]
            elif new_attr == 'href' and value.startswith('#'):
                value = '#' + ids[value[1:]]
            else:
                value = re.sub(r'url\(#([^)]+)\)', lambda m: f'url(#{ids[m[1]]})', value)
            del element.attrib[attr]
            element.set(new_attr, value)
        if element.text and element.tag == 'style':
            for old, new in ids.items():
                element.text = element.text.replace('#' + old, '#' + new)
    attrs = {k: v for k, v in root.attrib.items()
             if k not in ('viewBox', 'width', 'height', 'version', 'id')}
    group = ET.Element('g', attrs)
    group.extend(list(root))
    return {'viewBox': root.attrib['viewBox'],
            'inner': ET.tostring(group, encoding='unicode', short_empty_elements=True)}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--download', action='store_true')
    args = parser.parse_args()
    original = json.loads(SOURCE.read_text(encoding='utf-8'))
    if args.download:
        for entry in original['entries'].values():
            owner, repo = entry['source'].split('/')[3:5]
            url = f'https://api.github.com/repos/{owner}/{repo}/git/blobs/{entry["upstream_blob_sha"]}'
            request = urllib.request.Request(url, headers={'User-Agent': 'github-profile-brand-importer'})
            with urllib.request.urlopen(request, timeout=30) as response:
                blob = json.load(response)
            data = base64.b64decode(blob['content'])
            actual = hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()
            if actual != entry['upstream_blob_sha']:
                raise ValueError('Upstream SVG content hash mismatch: ' + entry['source'])
            entry['svg'] = data.decode('utf-8')
        SOURCE.write_text(json.dumps(original, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    registry_path = ROOT / 'assets/brands/icons.json'
    registry = json.loads(registry_path.read_text(encoding='utf-8'))
    for key, entry in original['entries'].items():
        data = entry['svg'].encode('utf-8')
        actual = hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()
        if actual != entry['upstream_blob_sha']:
            raise ValueError('Retained SVG content hash mismatch: ' + entry['source'])
        registry[key] = {**symbol_content(key, entry['svg']),
                         **{k: v for k, v in entry.items() if k != 'svg'}}
    # Binance's authentic single-color mark uses its official gold.
    registry['binance']['inner'] = registry['binance']['inner'].replace('currentColor', '#F0B90B')
    registry_path.write_text(json.dumps(registry, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(f'Imported {len(original["entries"])} pinned color brand assets; local IDs are namespaced.')


if __name__ == '__main__':
    main()
