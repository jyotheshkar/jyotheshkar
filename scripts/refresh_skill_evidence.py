#!/usr/bin/env python3
"""Refresh skill evidence while publishing no private repository names or source."""
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import quote
from urllib.request import Request, urlopen
from urllib.error import HTTPError
import argparse
import ast
import base64
import hashlib
import json
import os
import re

ROOT = Path(__file__).resolve().parents[1]
OWNER = 'jyotheshkar'
EXTENSIONS = {
    '.py':'Python', '.js':'JavaScript', '.jsx':'JavaScript', '.mjs':'JavaScript',
    '.cjs':'JavaScript', '.ts':'TypeScript', '.tsx':'TypeScript', '.java':'Java',
    '.pde':'Java (Processing)', '.php':'PHP', '.jsp':'JSP', '.sql':'SQL',
    '.sh':'Shell', '.bash':'Shell', '.r':'R', '.c':'C', '.cpp':'C++',
    '.cc':'C++', '.cs':'C#', '.go':'Go', '.rs':'Rust',
}
EXCLUDE = re.compile(r'(^|/)(node_modules|vendor|dist|build|\.venv|venv|\.next|coverage|archives?|snapshots?|exports?|reports?)(/|$)|\.min\.(js|css)$|\.d\.ts$', re.I)
SOURCE_EXCLUDE = re.compile(r'(^|/)(tests?|fixtures?|docs?)(/|$)|(^|/)(test_|conftest)|\.test\.', re.I)
AIML = [
    ('Supervised learning', r'\b(?:DecisionTreeClassifier|RandomForestClassifier|RandomForestRegressor|DecisionTreeRegressor|LinearRegression|LogisticRegression|ElasticNetCV|GradientBoostingRegressor|SVC)\s*\('),
    ('Unsupervised learning', r'\b(?:KMeans|DBSCAN|PCA|AgglomerativeClustering)\s*\('),
    ('Deep learning', r'\b(?:nn\.(?:Linear|Conv2d|LSTM|Embedding)|Sequential|Dense|LSTM|Conv2D)\s*\('),
    ('Reinforcement learning', r'\b(?:class\s+\w*DQN\b|class\s+ReplayBuffer\b|def\s+train_dqn\b|def\s+step_reward\b|def\s+optimize_model\b)'),
    ('NLP and transformers', r'\b(?:class\s+(?:GPTLanguageModel|BigramLanguageModel|CausalAttention|DecoderBlock|MultiHeadAttention)\b|token_embedding_table\s*=|AutoTokenizer\.from_pretrained\s*\(|tiktoken\.get_encoding\s*\()'),
    ('Time-series modelling', r'\b(?:ARIMA|SARIMAX|ExponentialSmoothing|LSTM)\s*\('),
    ('Data preparation', r'\b(?:train_test_split|StandardScaler|MinMaxScaler|KNNImputer|SimpleImputer|OneHotEncoder)\s*\('),
    ('Model evaluation', r'\b(?:accuracy_score|confusion_matrix|mean_squared_error|mean_absolute_error|r2_score|classification_report|f1_score)\s*\(|\b(?:def\s+run_adversarial\b|class\s+\w*EvaluationPipeline\b)'),
]
AGENTIC = [
    ('Workflow orchestration', r'\b(?:def\s+(?:register_workflow|compile_workflow|start_run|advance|orchestrat\w*)|class\s+\w*(?:Orchestrator|Workflow)|StateGraph\s*\(|execution_graph\s*[=(])'),
    ('Tool execution', r'\b(?:def\s+(?:\w*dispatch\w*|execute_tool|register_tool|submit_receipt)|tool_calls?\s*[=.(]|function_call\s*[=(])'),
    ('Retrieval', r'\b(?:def\s+(?:_?retrieve\w*|search|build_index)|similarity_search\s*\(|faiss\.|retrieve_and_generate\s*\(|QdrantClient\s*\(|TextEmbedding\s*\()'),
    ('State and memory', r'\b(?:def\s+(?:resume|load_state|save_state|checkpoint)|class\s+\w*(?:State|Memory|Checkpoint)|sqlite3\.connect\s*\(|state_store\s*[=(])'),
    ('Human approval', r'\b(?:def\s+(?:approve|request_approval)|requires_approval\s*[:=]|approval_required\s*[:=]|approval_status\s*[:=])'),
    ('Guardrails', r'\b(?:def\s+(?:guardian\w*|redact\w*|check_safety|validate_policy)|class\s+\w*(?:Guardrail|Safety|Policy)|safety_check\s*\()'),
    ('Agent evaluation', r'\b(?:def\s+(?:run_adversarial|evaluate\w*|run_batch|score_response)|class\s+\w*(?:Evaluator|EvaluationPipeline)|evaluation_results\s*[=:])'),
    ('Task routing', r'\b(?:def\s+(?:route_task|route_request|select_agent)|class\s+\w*(?:Router|Planner)|routing_decision\s*[:=])'),
]
TITLES = {'languages':'Programming Languages', 'aiml':'AI/ML Engineering', 'agentic':'Agentic AI Engineering'}


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


def source_id(repo):
    return hashlib.sha256(('profile-evidence:' + str(repo['id'])).encode()).hexdigest()[:16]


def decode(payload):
    value = payload.get('content', '')
    return base64.b64decode(value).decode('utf-8', errors='replace') if payload.get('encoding') == 'base64' else value


def notebook_code(body):
    notebook = json.loads(body)
    cells = [''.join(cell.get('source', [])) for cell in notebook.get('cells', []) if cell.get('cell_type') == 'code']
    metadata = notebook.get('metadata', {})
    language = metadata.get('language_info', {}).get('name') or metadata.get('kernelspec', {}).get('language')
    return '\n'.join(cells), language


def implementation(body):
    """Remove Python comments/docstrings and unimplemented stubs before detection."""
    try:
        tree = ast.parse(body)
    except SyntaxError:
        return '\n'.join(line for line in body.splitlines() if not line.lstrip().startswith(('#', '//')))
    class Clean(ast.NodeTransformer):
        def visit_Constant(self, node):
            # Strings may contain prompts or code examples; they are not implementations.
            return ast.Constant(value='') if isinstance(node.value, str) else node
        def visit_Module(self, node):
            node = self.generic_visit(node)
            node.body = [s for s in node.body if not (isinstance(s, ast.Expr) and isinstance(s.value, ast.Constant) and isinstance(s.value.value, str))]
            return node
        def clean_body(self, node):
            node = self.generic_visit(node)
            node.body = [s for s in node.body if not (isinstance(s, ast.Expr) and isinstance(s.value, ast.Constant) and isinstance(s.value.value, str))]
            stub = all(isinstance(s, ast.Pass) or (isinstance(s, ast.Raise) and 'NotImplemented' in ast.unparse(s)) for s in node.body)
            return None if stub else node
        visit_FunctionDef = clean_body
        visit_AsyncFunctionDef = clean_body
        visit_ClassDef = clean_body
    return ast.unparse(Clean().visit(tree))


def select_sources(files):
    candidates = [f for f in files if not SOURCE_EXCLUDE.search(f['path'])
                  and (Path(f['path']).suffix.lower() in EXTENSIONS or f['path'].endswith('.ipynb'))
                  and f.get('size', 0) <= 1_000_000]
    def priority(file):
        path = file['path'].lower()
        score = sum(term in path for term in ('engine', 'agent', 'runtime', 'safety', 'contract',
                    'retriev', 'evaluat', 'routing', 'pipeline', 'model', 'train', 'notebook', 'dqn'))
        return (not path.endswith('.ipynb'), -score, path.count('/'), path)
    return sorted(candidates, key=priority)[:36]


def assemble(public, private, captured_at):
    public_ids = {s['source_id'] for s in public['sources']}
    # If a previously private project becomes public, never count it twice.
    private = {**private, 'sources':[s for s in private.get('sources', []) if s['source_id'] not in public_ids]}
    groups = {key:defaultdict(list) for key in TITLES}
    for source in public['sources'] + private['sources']:
        for key in TITLES:
            for label, proof in source['skills'][key].items():
                item = {'source_id':source['source_id'], 'visibility':source['visibility']}
                if source['visibility'] == 'public':
                    item.update({'repo':source['repo'], **proof})
                groups[key][label].append(item)
    charts = [{'key':key,'title':title,'unit':'repositories',
               'items':[{'label':label,'value':len(proof),'evidence':proof}
                        for label,proof in sorted(groups[key].items(), key=lambda item:(-len(item[1]), item[0].lower()))]}
              for key,title in TITLES.items()]
    return {
        'schema_version':2, 'captured_at':captured_at,
        'public_snapshot':public, 'private_snapshot':private,
        'methodology':{
            'measure':'One repository per evidenced language or engineering domain. Counts describe source presence, never proficiency or authorship.',
            'languages':'Complete source trees plus inspected notebook code cells. PHP and JSP included. Java requires .java or Processing implementation; a Maven WAR or pure-HTML JSP does not establish Java source. HTML/CSS styling and dependencies/builds are excluded.',
            'aiml':'Executable implementations of learning domains; dependencies and README claims do not qualify. Notebook markdown/outputs and unimplemented Python stubs are excluded.',
            'agentic':'Only Agentic Core family repositories and linkedin-agent-development-lab. Source implementation symbols, not other web apps or architecture prose.',
            'privacy':'Private evidence publishes only opaque per-repository IDs and skill names. No private names, filenames, snippets, blob hashes, URLs or notebook contents are published.',
            'refresh':'Public snapshot can refresh through GitHub Actions. Full authenticated connector audits refresh private aggregates. Public-only refresh preserves the private baseline and its separate capture date.',
        },
        'charts':charts,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--api-cache')
    parser.add_argument('--scope', choices=['public','accessible'], default='public')
    parser.add_argument('--captured-at')
    args = parser.parse_args()
    api = API(args.api_cache)
    date = args.captured_at or datetime.now(timezone.utc).isoformat(timespec='seconds')
    output = ROOT / 'config/skill-evidence.json'
    previous = json.loads(output.read_text(encoding='utf-8')) if output.exists() else {}
    prior_public = {s['source_id']:s for s in previous.get('public_snapshot', {}).get('sources', [])}
    repos = []
    for page in range(1, 21):
        endpoint = f'/users/{OWNER}/repos?per_page=100&page={page}'
        if args.scope == 'accessible' and api.cache is None:
            endpoint = f'/user/repos?affiliation=owner&per_page=100&page={page}'
        chunk = api.get(endpoint)
        repos.extend(chunk)
        if len(chunk) < 100:
            break
    else:
        raise RuntimeError('Repository pagination exceeded the explicit safety limit')
    repos = sorted([r for r in repos if not r.get('fork') and r['name'] != OWNER
                    and r.get('owner', {}).get('login', OWNER).lower() == OWNER
                    and (args.scope == 'accessible' or not r.get('private'))],
                   key=lambda r:r.get('full_name', OWNER+'/'+r['name']).lower())
    sources = []
    for repo in repos:
        name = repo.get('full_name', OWNER+'/'+repo['name'])
        branch = repo['default_branch']
        prefix = '/repos/' + name
        rid = source_id(repo)
        try:
            tree = api.get(prefix+'/git/trees/'+quote(branch, safe='')+'?recursive=1')
        except HTTPError as error:
            if error.code == 409 and repo.get('size') == 0:
                continue
            raise
        if tree.get('truncated'):
            raise RuntimeError('Truncated repository tree: '+name)
        prior = prior_public.get(rid)
        if api.cache is None and prior and not repo.get('private') and prior['tree_sha'] == tree['sha']:
            sources.append({**prior, 'repo':name})
            continue
        files = [f for f in tree['tree'] if f['type']=='blob' and not EXCLUDE.search(f['path'])]
        skills = {key:{} for key in TITLES}
        def proof(file, kind='implementation'):
            return {'path':file['path'],'sha':file['sha'],'kind':kind}
        for file in files:
            lang = EXTENSIONS.get(Path(file['path']).suffix.lower())
            if lang and file.get('size') and not SOURCE_EXCLUDE.search(file['path']):
                skills['languages'].setdefault(lang, proof(file, 'template' if lang=='JSP' else 'source'))
        selected = {f['path']:f for f in select_sources(files)}
        if api.cache is not None:
            selected = {}
            for file in files:
                path = file['path']
                if SOURCE_EXCLUDE.search(path) or (Path(path).suffix.lower() not in EXTENSIONS and not path.endswith('.ipynb')):
                    continue
                keys = [prefix+'/contents/'+quote(path, safe='/')+'?ref='+quote(branch,safe=''),
                        prefix+'/contents/'+path+'?ref='+branch]
                if any(key in api.cache for key in keys):
                    selected[path] = file
        scanned = []
        agent_scope = bool(re.search(r'agentic[-_ ]core', repo['name'], re.I) or repo['name']=='linkedin-agent-development-lab')
        for path,file in sorted(selected.items()):
            request_path = prefix+'/contents/'+quote(path,safe='/')+'?ref='+quote(branch,safe='')
            if api.cache is not None and request_path not in api.cache:
                request_path = prefix+'/contents/'+path+'?ref='+branch
            payload = api.get(request_path)
            if payload.get('sha') and payload['sha'] != file['sha']:
                raise RuntimeError('Repository changed during capture: '+name)
            body = decode(payload)
            scanned.append({'path':path,'sha':file['sha']})
            if path.endswith('.ipynb'):
                body, language = notebook_code(body)
                if body.strip() and language and language.lower() in ('python','python3'):
                    skills['languages'].setdefault('Python', proof(file,'notebook code cells'))
            code = implementation(body)
            for label,pattern in AIML:
                if re.search(pattern,code,re.I):
                    skills['aiml'].setdefault(label,proof(file))
            if agent_scope:
                for label,pattern in AGENTIC:
                    if re.search(pattern,code,re.I):
                        skills['agentic'].setdefault(label,proof(file))
        if repo.get('private'):
            sources.append({'source_id':rid,'visibility':'private',
                            'skills':{key:{label:{'kind':'verified source'} for label in matches} for key,matches in skills.items()}})
        else:
            sources.append({'source_id':rid,'visibility':'public','repo':name,'tree_sha':tree['sha'],
                            'scanned_files':scanned,'skills':skills})
    public = {'captured_at':date,'sources':[s for s in sources if s['visibility']=='public']}
    private = {'captured_at':date,'sources':[s for s in sources if s['visibility']=='private']} if args.scope=='accessible' else previous.get('private_snapshot',{'captured_at':None,'sources':[]})
    if public['sources'] == previous.get('public_snapshot', {}).get('sources'):
        public['captured_at'] = previous['public_snapshot']['captured_at']
    if private['sources'] == previous.get('private_snapshot', {}).get('sources'):
        private['captured_at'] = previous['private_snapshot']['captured_at']
    result = assemble(public,private,date)
    if {k:v for k,v in result.items() if k!='captured_at'} == {k:v for k,v in previous.items() if k!='captured_at'}:
        print('Evidence verified; no material source change.')
        return
    output.write_text(json.dumps(result,indent=2,ensure_ascii=False)+'\n',encoding='utf-8',newline='\n')
    for group in result['charts']:
        print(group['title']+': '+', '.join(item['label'] for item in group['items']))


if __name__ == '__main__':
    main()
