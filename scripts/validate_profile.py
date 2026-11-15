#!/usr/bin/env python3
"""Validate self-contained profile artwork, source totals and private-data boundaries."""
from pathlib import Path
from urllib.parse import unquote, urlsplit
import json
import math
import re
import sys
import xml.etree.ElementTree as ET

ROOT=Path(__file__).resolve().parents[1]
CHART_FILES={'skills-programming.svg':'languages','skills-aiml.svg':'aiml','skills-agentic.svg':'agentic'}


def main():
    errors=[]
    documents={}
    for path in (ROOT/'assets').rglob('*.svg'):
        name=path.relative_to(ROOT).as_posix()
        try:
            svg=ET.fromstring(path.read_text(encoding='utf-8'))
            documents[path.name]=svg
            box=[float(v) for v in svg.get('viewBox','').replace(',',' ').split()]
            if len(box)!=4 or box[2]<=0 or box[3]<=0:
                raise ValueError('Invalid viewBox')
            ids=[e.get('id') for e in svg.iter() if e.get('id')]
            if len(ids)!=len(set(ids)):
                errors.append(name+': duplicate IDs')
            for e in svg.iter():
                if e.tag.split('}')[-1] in ('script','foreignObject','iframe'):
                    errors.append(name+': active embedded content')
                for key,value in e.attrib.items():
                    if key.lower().startswith('on') or (key.split('}')[-1]=='href' and re.match(r'\s*(javascript:|https?://)',value,re.I)):
                        errors.append(name+': external/active resource')
                    refs=re.findall(r'url\(#([^)]+)\)',value)
                    if key.split('}')[-1]=='href' and value.startswith('#'):
                        refs.append(value[1:])
                    for ref in refs:
                        if ref not in ids:
                            errors.append(name+': unresolved local reference '+ref)
        except (ET.ParseError,OSError,ValueError) as error:
            errors.append(name+': '+type(error).__name__)
    if not documents:
        errors.append('No SVG documents found')
    profile=documents.get('profile.svg')
    if profile is None or not any(e.get('id')=='linkedin-architecture' for e in profile.iter()):
        errors.append('profile.svg: LinkedIn architecture missing')
    if profile is not None and any(e.get('data-concept') in ('youtube','crypto') for e in profile.iter()):
        errors.append('profile.svg: retired concept remains')

    metrics=json.loads((ROOT/'config/skill-evidence.json').read_text(encoding='utf-8'))
    charts={chart['key']:chart for chart in metrics['charts']}
    if set(charts)!={'languages','aiml','agentic'}:
        errors.append('Skill evidence must have the three requested categories')
    public=metrics['public_snapshot']['sources']
    private=metrics['private_snapshot']['sources']
    sources=public+private
    source_ids={source['source_id'] for source in sources}
    if len(source_ids)!=len(sources):
        errors.append('Evidence sources are counted twice')
    # Private aggregate shapes deliberately have no fields capable of publishing raw evidence.
    for source in private:
        if set(source)!={'source_id','visibility','skills'} or source['visibility']!='private' or not re.fullmatch(r'[0-9a-f]{16}',source['source_id']):
            errors.append('Private source has an unexpected field or identifier')
        if set(source['skills'])!={'languages','aiml','agentic'}:
            errors.append('Private source has an unexpected skills group')
        for skills in source['skills'].values():
            if any(proof!={'kind':'verified source'} for proof in skills.values()):
                errors.append('Private source contains more than an aggregate skill')
    for source in public:
        if source['skills']['agentic'] and not (re.search(r'agentic[-_ ]core',source['repo'],re.I) or source['repo'].endswith('/linkedin-agent-development-lab')):
            errors.append('Agentic evidence includes an unrelated repository')
    for key,chart in charts.items():
        expected={}
        for source in sources:
            for label in source['skills'][key]:
                expected.setdefault(label,set()).add(source['source_id'])
        if {i['label'] for i in chart['items']}!=set(expected):
            errors.append(key+': chart categories do not match source partitions')
        for item in chart['items']:
            ids={e['source_id'] for e in item['evidence']}
            if item['value']!=len(item['evidence']) or item['value']!=len(ids) or ids!=expected.get(item['label'],set()):
                errors.append(key+': incorrect evidence count')
            for proof in item['evidence']:
                if proof['visibility']=='private' and set(proof)!={'source_id','visibility'}:
                    errors.append('Private chart evidence has a disallowed field')

    canonical={}
    sizes=set()
    for filename,key in CHART_FILES.items():
        if filename not in documents:
            errors.append(filename+': missing individual card')
            continue
        doc=documents[filename]
        sizes.add((doc.get('width'),doc.get('height'),doc.get('viewBox')))
        groups=[e for e in doc.iter() if e.get('data-skill-circle')]
        if len(groups)!=1 or groups[0].get('data-skill-circle')!=key:
            errors.append(filename+': unexpected skill group')
            continue
        canonical[key]=ET.tostring(groups[0]).strip()
    if len(sizes)!=1:
        errors.append('The individual skill cards must have identical dimensions')
    expected_files={**CHART_FILES,'skill-circles.svg':None,'skills-mobile.svg':None}
    for filename,key in expected_files.items():
        if filename not in documents:
            errors.append(filename+': missing skill artwork')
            continue
        doc=documents[filename]
        groups=[e for e in doc.iter() if e.get('data-skill-circle')]
        required={key} if key else set(charts)
        if {e.get('data-skill-circle') for e in groups}!=required or len(groups)!=len(required):
            errors.append(filename+': incorrect group coverage')
        labels=[e.text or '' for e in doc.iter() if e.tag.split('}')[-1] in ('text','title')]
        if any(re.search(r'\d',label) for label in labels):
            errors.append(filename+': numeric display label')
        for group in groups:
            group_key=group.get('data-skill-circle')
            if ET.tostring(group).strip()!=canonical.get(group_key):
                errors.append(filename+': card diverges from its individual artwork')
            values={i['label']:i['value'] for i in charts[group_key]['items']}
            total=sum(values.values())
            if int(group.get('data-total'))!=total:
                errors.append(filename+': incorrect total')
            legends=[e for e in group.iter() if e.get('data-skill-legend')]
            if {e.get('data-skill-legend') for e in legends}!=set(values):
                errors.append(filename+': missing name legend')
            for legend in legends:
                texts=[e for e in legend if e.tag.split('}')[-1]=='text']
                if any(float(t.get('y'))<=334 for t in texts):
                    errors.append(filename+': legend is not below the circle')
            segments=[e for e in group.iter() if e.get('data-segment')]
            if {e.get('data-segment') for e in segments}!=set(values):
                errors.append(filename+': missing segments')
            for segment in segments:
                value=values[segment.get('data-segment')]
                actual=float(segment.get('stroke-dasharray').split()[0])
                correct=2*math.pi*float(segment.get('r'))*value/total
                if int(segment.get('data-value'))!=value or abs(actual-correct)>1e-6:
                    errors.append(filename+': non-proportional segment')
            bars=[e for e in group.iter() if e.get('data-evidence-bar')]
            if {e.get('data-evidence-bar') for e in bars}!=set(values):
                errors.append(filename+': missing bars')
            for bar in bars:
                if abs(float(bar.get('width'))-176*values[bar.get('data-evidence-bar')]/max(values.values()))>1e-5:
                    errors.append(filename+': non-proportional bar')

    readme=ROOT/'README.md'
    if not readme.exists():
        errors.append('README.md missing')
    else:
        body=readme.read_text(encoding='utf-8')
        refs=re.findall(r'(?:src|href|srcset)=["\x27]([^"\x27]+)["\x27]',body)
        refs+=re.findall(r'\]\(([^\s)]+)\)',body)
        for ref in refs:
            uri=urlsplit(ref)
            if uri.scheme or ref.startswith('#'):
                continue
            local=(ROOT/unquote(uri.path)).resolve()
            if not local.is_relative_to(ROOT) or not local.exists():
                errors.append('README.md: missing or out-of-root reference '+ref)
        if re.search(r'<script|<iframe|\bstyle=|\bonclick=',body,re.I):
            errors.append('README contains unsupported active HTML')
        if 'assets/profile.svg' not in body:
            errors.append('README lacks profile artwork')
    if errors:
        print('\n'.join(errors),file=sys.stderr)
        raise SystemExit(1)
    print(f'Validated {len(documents)} SVGs, all skill proportions, private-data boundaries and README references.')


if __name__=='__main__':
    main()

