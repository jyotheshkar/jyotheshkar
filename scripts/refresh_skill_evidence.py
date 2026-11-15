#!/usr/bin/env python3
"""Refresh public repository evidence; no private sources, README claims or skill scores."""
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import quote
from urllib.request import Request, urlopen
from urllib.error import HTTPError
import argparse
import base64
import json
import os
import re

ROOT = Path(__file__).resolve().parents[1]
OWNER = 'jyotheshkar'
EXTENSIONS = {'.py':'Python', '.js':'JavaScript', '.jsx':'JavaScript', '.mjs':'JavaScript',
              '.cjs':'JavaScript', '.ts':'TypeScript', '.tsx':'TypeScript', '.java':'Java',
              '.sql':'SQL', '.sh':'Shell', '.bash':'Shell', '.r':'R', '.c':'C',
              '.cpp':'C++', '.cc':'C++', '.cs':'C#', '.go':'Go', '.rs':'Rust'}
EXCLUDE = re.compile(r'(^|/)(node_modules|vendor|dist|build|\.venv|venv|\.next|coverage|archives?|snapshots?|data|exports?|reports?)(/|$)|\.min\.(js|css)$|\.d\.ts$', re.I)
SOURCE_EXCLUDE = re.compile(r'(^|/)(tests?|fixtures?|examples?|docs?)(/|$)|(^|/)(test_|conftest)|\.test\.', re.I)
MANIFEST = re.compile(r'(^|/)(package\.json|requirements[^/]*\.txt|pyproject\.toml|setup\.py|Pipfile)$', re.I)
LIBRARIES = [
    ('NumPy', 'numpy'), ('pandas', 'pandas'), ('scikit-learn', 'sklearn|scikit-learn'),
    ('PyTorch', 'torch'), ('TensorFlow', 'tensorflow'), ('Keras', 'keras'),
    ('Transformers', 'transformers'), ('Matplotlib', 'matplotlib'), ('SciPy', 'scipy'),
    ('FastAPI', 'fastapi'), ('Flask', 'flask'), ('Pydantic', 'pydantic'),
    ('React', 'react'), ('Next.js', 'next'), ('LangChain', 'langchain(?:[-_]core|[-_]community)?'),
    ('FAISS', 'faiss(?:-cpu|-gpu)?'), ('Streamlit', 'streamlit'),
    ('LangGraph', 'langgraph'), ('FastEmbed', 'fastembed'),
    ('Qdrant', 'qdrant[-_]client|@qdrant/js-client-rest'), ('OpenAI SDK', 'openai'),
]
# Match implementation symbols/calls, never prose mentions in a README.
AGENTIC = [
    ('Workflow orchestration', r'\b(?:def\s+(?:register_workflow|compile_workflow|start_run|advance|orchestrat\w*)|class\s+\w*(?:Orchestrator|Workflow)|StateGraph\s*\(|execution_graph\s*[=(])'),
    ('Tool execution', r'\b(?:def\s+(?:\w*dispatch\w*|execute_tool|register_tool|submit_receipt)|tool_calls?\s*[=.(]|function_call\s*[=(])'),
    ('Retrieval', r'\b(?:def\s+(?:_?retrieve\w*|search|build_index)|similarity_search\s*\(|faiss\.|retrieve_and_generate\s*\()'),
    ('State and memory', r'\b(?:def\s+(?:resume|load_state|save_state|checkpoint)|class\s+\w*(?:State|Memory|Checkpoint)|sqlite3\.connect\s*\(|state_store\s*[=(])'),
    ('Human approval', r'\b(?:def\s+(?:approve|request_approval)|requires_approval\s*[:=]|approval_required\s*[:=]|approval_status\s*[:=])'),
    ('Guardrails', r'\b(?:def\s+(?:guardian\w*|redact\w*|check_safety|validate_policy)|class\s+\w*(?:Guardrail|Safety|Policy)|safety_check\s*\()'),
    ('Evaluation', r'\b(?:def\s+(?:run_adversarial|evaluate\w*|run_batch|score_response)|class\s+\w*(?:Evaluator|EvaluationPipeline)|evaluation_results\s*[=:])'),
    ('Task routing', r'\b(?:def\s+(?:route_task|route_request|select_agent)|class\s+\w*(?:Router|Planner)|routing_decision\s*[:=])'),
]


class API:
    def __init__(self, cache=None):
        self.cache = json.loads(Path(cache).read_text(encoding='utf-8-sig')) if cache else None

    def get(self, path):
        if self.cache is not None:
            if path not in self.cache:
                raise RuntimeError('Missing captured API response: ' + path)
            return self.cache[path]
        headers = {'Accept':'application/vnd.github+json', 'User-Agent':'jyotheshkar-profile-evidence',
                   'X-GitHub-Api-Version':'2022-11-28'}
        if os.getenv('GITHUB_TOKEN'):
            headers['Authorization'] = 'Bearer ' + os.environ['GITHUB_TOKEN']
        with urlopen(Request('https://api.github.com' + path, headers=headers), timeout=40) as response:
            return json.load(response)


def eligible(path):
    return not EXCLUDE.search(path)


def select_sources(files):
    source = [f for f in files if eligible(f['path']) and not SOURCE_EXCLUDE.search(f['path']) and f.get('size', 0) <= 200000
              and Path(f['path']).suffix.lower() in ('.py', '.ts', '.tsx', '.js', '.jsx')]
    def priority(file):
        path = file['path'].lower()
        score = sum(term in path for term in ('engine', 'agent', 'runtime', 'safety', 'contract',
                     'retriev', 'evaluat', 'routing', 'pipeline', 'model', 'train', 'app'))
        return (-score, path.count('/'), path)
    return sorted(source, key=priority)[:12]


def content(payload):
    value = payload.get('content', '')
    if payload.get('encoding') == 'base64':
        return base64.b64decode(value).decode('utf-8', errors='replace')
    return value


def dependency_hit(label_pattern, path, body):
    if path.endswith('package.json'):
        try:
            value = json.loads(body)
        except ValueError:
            return None
        # Runtime dependencies only; build/dev tools do not masquerade as framework experience.
        for name in value.get('dependencies', {}):
            if re.fullmatch(label_pattern, name, re.I):
                return name
        return None
    if 'requirements' in Path(path).name.lower():
        lines = [line.strip() for line in body.splitlines() if line.strip() and not line.startswith('#')]
        if len(lines) > 80:  # Broad environment freezes require corroboration from actual imports.
            return None
        return next((line for line in lines if re.match(r'^(?:' + label_pattern + r')(?:\[|\s|[=<>~!;]|$)', line, re.I)), None)
    if MANIFEST.search(path):
        return next((line.strip() for line in body.splitlines() if re.search(r'["\x27](?:' + label_pattern + r')(?:[=<>~!\[\s]|["\x27])', line, re.I)), None)
    # Python imports and JS/TS imports/requires only, not arbitrary identifier substrings.
    rx = r'(?:^\s*(?:from|import)\s+(?:' + label_pattern + r')(?:\.|\s|,|$)|\bfrom\s+["\x27](?:' + label_pattern + r')(?:/|["\x27])|\brequire\(["\x27](?:' + label_pattern + r')["\x27]\))'
    return next((line.strip() for line in body.splitlines() if re.search(rx, line, re.I)), None)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--api-cache')
    parser.add_argument('--captured-at')
    args = parser.parse_args()
    api = API(args.api_cache)
    repos = []
    for page in range(1, 21):
        chunk = api.get(f'/users/{OWNER}/repos?per_page=100&page={page}')
        repos.extend(chunk)
        if len(chunk) < 100:
            break
    else:
        raise RuntimeError('Repository pagination exceeded the explicit safety limit')
    repos = sorted([r for r in repos if not r.get('private') and not r.get('fork') and not r.get('archived')
                    and r['name'] != OWNER and r.get('owner', {}).get('login', OWNER).lower() == OWNER],
                   key=lambda r: r.get('full_name', OWNER + '/' + r['name']).lower())
    languages, libraries, agentic = defaultdict(list), defaultdict(list), defaultdict(list)
    seen_blobs = set()
    provenance = []
    output = ROOT / 'config/skill-evidence.json'
    previous = json.loads(output.read_text(encoding='utf-8')) if output.exists() else {}
    previous_sources = {r['repo']:[f['path'] for f in r['scanned_files']]
                        for r in previous.get('repositories', [])}
    for repo in repos:
        name = repo.get('full_name', OWNER + '/' + repo['name'])
        branch = repo['default_branch']
        prefix = '/repos/' + name
        try:
            tree = api.get(prefix + '/git/trees/' + quote(branch, safe='') + '?recursive=1')
        except HTTPError as error:
            if error.code == 409 and repo.get('size') == 0:
                # A new repository without a commit has no tree or evidence yet.
                print('Skipping empty repository without a Git tree:', name)
                continue
            raise
        if tree.get('truncated'):
            raise RuntimeError('Truncated repository tree: ' + name)
        files = [f for f in tree['tree'] if f['type'] == 'blob' and eligible(f['path'])]
        for file in files:
            label = EXTENSIONS.get(Path(file['path']).suffix.lower())
            if not label or file['sha'] in seen_blobs or not file.get('size'):
                continue
            seen_blobs.add(file['sha'])
            languages[label].append({'repo':name, 'path':file['path'], 'sha':file['sha'], 'size':file['size']})
        manifests = sorted([f for f in files if MANIFEST.search(f['path'])], key=lambda f:(f['path'].count('/'),f['path']))[:6]
        previous_files = [f for f in files if f['path'] in previous_sources.get(name, [])
                          and not MANIFEST.search(f['path']) and not SOURCE_EXCLUDE.search(f['path'])]
        # Retain verified implementation samples while they exist, then add new candidates.
        source_candidates = {f['path']:f for f in previous_files + select_sources(files)}
        selected = {f['path']:f for f in manifests + list(source_candidates.values())[:12]}
        if api.cache is not None:
            # Initial connector capture may include a different bounded source sample.
            for key, payload in api.cache.items():
                if key.startswith(prefix + '/contents/'):
                    path = payload.get('path')
                    match = next((f for f in files if f['path'] == path), None)
                    if match and (MANIFEST.search(path) or (not SOURCE_EXCLUDE.search(path)
                        and Path(path).suffix.lower() in ('.py', '.ts', '.tsx', '.js', '.jsx'))):
                        selected[path] = match
            selected = {path:file for path,file in selected.items()
                        if prefix + '/contents/' + quote(path, safe='/') + '?ref=' + quote(branch, safe='') in api.cache
                        or prefix + '/contents/' + path + '?ref=' + branch in api.cache}
        lib_hits, agent_hits = {}, {}
        scanned = []
        for path, file in sorted(selected.items()):
            api_path = prefix + '/contents/' + quote(path, safe='/') + '?ref=' + quote(branch, safe='')
            if api.cache is not None and api_path not in api.cache:
                api_path = prefix + '/contents/' + path + '?ref=' + branch
            payload = api.get(api_path)
            if payload.get('sha') and payload['sha'] != file['sha']:
                raise RuntimeError('Repository changed during capture: ' + name + '/' + path)
            body = content(payload)
            scanned.append({'path':path,'sha':file['sha']})
            for label, pattern in LIBRARIES:
                hit = dependency_hit(pattern, path, body)
                if hit and label not in lib_hits:
                    lib_hits[label] = {'repo':name,'path':path,'sha':file['sha'],'excerpt':hit[:280]}
            if not MANIFEST.search(path) and re.search(r'agent|rag|rufus', name, re.I):
                for label, pattern in AGENTIC:
                    hit = re.search(pattern, body, re.I)
                    if hit and label not in agent_hits:
                        line = body.count('\n', 0, hit.start()) + 1
                        agent_hits[label] = {'repo':name,'path':path,'sha':file['sha'],'line':line,
                                             'excerpt':body.splitlines()[line-1].strip()[:280]}
        for label,evidence in lib_hits.items():
            libraries[label].append(evidence)
        for label,evidence in agent_hits.items():
            agentic[label].append(evidence)
        provenance.append({'repo':name,'default_branch':branch,'tree_sha':tree['sha'],'scanned_files':scanned})
    def chart(key,title,unit,entries):
        items = [{'label':label,'value':sum(e['size'] for e in evidence) if unit == 'bytes' else len(evidence),
                  'evidence':evidence} for label,evidence in entries.items()]
        return {'key':key,'title':title,'unit':unit,'items':sorted(items,key=lambda i:(-i['value'],i['label'].lower()))}
    result = {
        'schema_version':1,
        'captured_at':args.captured_at or datetime.now(timezone.utc).isoformat(timespec='seconds'),
        'scope':'Current public, owned, nonfork, unarchived repositories; profile excluded.',
        'repositories':provenance,
        'methodology':{
            'languages':'Extension-classified source bytes, deduplicated globally by Git blob SHA; excludes notebooks, markup/stylesheets, data, reports, archives, vendor, dependencies and build output. Repository content is not an authorship or proficiency score.',
            'libraries':'One evidence match per repository from runtime dependencies or implementation imports. Long environment freezes need corroborating imports. Bounded sample: up to six manifests and twelve prioritised source files per repository; initial capture may contain additional source verification.',
            'agentic':'One implementation-symbol or executable configuration match per repository and category, only in agent/RAG/Rufus repositories. README prose, tests and documentation are excluded. Source evidence establishes implementation presence, not operational reliability or production use.',
            'visual':'Doughnut slices divide the category evidence total. Right-side bars are relative to the largest item in that group. No proficiency scores, percentages or counts are printed.',
        },
        'charts':[chart('languages','Programming Languages','bytes',languages),
                  chart('libraries','Libraries and Frameworks','repositories',libraries),
                  chart('agentic','Agentic AI Engineering','repositories',agentic)],
    }
    if output.exists():
        if {k:v for k,v in result.items() if k != 'captured_at'} == {k:v for k,v in previous.items() if k != 'captured_at'}:
            print('Evidence verified; no source change, so no new commit is needed.')
            return
    output.write_text(json.dumps(result, indent=2, ensure_ascii=False) + '\n',encoding='utf-8',newline='\n')
    print('Refreshed evidence from',len(repos),'public repositories.')
    for group in result['charts']:
        print(group['title'] + ': ' + ', '.join(i['label'] for i in group['items']))


if __name__ == '__main__':
    main()
