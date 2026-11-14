#!/usr/bin/env python3
"""Summarize a captured public GitHub tree/README/manifest snapshot."""
from pathlib import Path
from collections import defaultdict
import json
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
EXTENSIONS = {'.py':'Python','.js':'JavaScript','.jsx':'JavaScript','.mjs':'JavaScript','.cjs':'JavaScript','.ts':'TypeScript','.tsx':'TypeScript','.java':'Java','.sql':'SQL','.html':'HTML','.htm':'HTML','.css':'CSS','.scss':'CSS','.sh':'Shell','.bash':'Shell'}
EXCLUDE = re.compile(r'(^|/)(node_modules|vendor|dist|build|\.venv|venv|\.next|coverage|original-work|archives?|snapshots?|data|exports?|reports?)(/|$)|\.min\.(js|css)$|\.d\.ts$|(^|/)revision-baseline\.html$',re.I)
RULES = {
 'engineering': [('React',r'\breact\b'),('Node.js / npm',r'\bnode(?:\.js)?\b|\bnpm\b|@types/node'),('Backend APIs',r'\bfastapi\b|\bflask\b|\bdjango\b|\bexpress\b'),('SQL databases',r'\bsqlite\b|\bpostgres(?:ql)?\b|\bmysql\b'),('Containers',r'\bdocker\b|\bcontainers?\b'),('CI / CD',r'github actions|\bCI/CD\b|continuous integration'),('AWS',r'\bAWS\b|Amazon (?:S3|Bedrock|Lambda|DynamoDB)'),('Testing',r'\bpytest\b|\bunittest\b|\bjest\b|automated tests')],
 'ai': [('PyTorch',r'\bpytorch\b|\btorch\b'),('TensorFlow',r'\btensorflow\b'),('Reinforcement learning',r'reinforcement learning|\bDQN\b'),('Transformers',r'\btransformers?\b|multihead attention'),('NLP',r'\bNLP\b|natural language processing|\btokeniz(?:ed|er|ation)\b|\btokenis(?:ed|er|ation)\b'),('Scikit-learn',r'\bscikit-learn\b|\bsklearn\b'),('Model evaluation',r'LLM eval|model eval|AI eval|\bbenchmark|\bRLHF\b'),('Embeddings',r'\bembeddings?\b')],
 'agentic': [('Planning',r'\bplanning\b|\bplan proposals\b|\bplanner\b'),('Tool use',r'\btool(?:s|ing)?\b|tool.call'),('RAG / retrieval',r'\bRAG\b|\bretrieval\b|retrieval.augmented'),('Memory / state',r'\bmemory\b|\bcheckpoints?\b|\bstate\b'),('Orchestration',r'\borchestrat\w*|\bworkflow\b'),('Guardrails',r'\bguardrails?\b|\bpermission rules\b|\bbounded\b'),('Tracing / evals',r'\btracing\b|\btraces?\b|\bevaluation\b|\bverification\b'),('Human review',r'human.review|human.in.the.loop|\bapprovals?\b|\bHITL\b')]
}


def summarize(source):
    rows = json.loads(source.read_text(encoding='utf-8'))
    repos = rows['repositories']
    evidence = [e for e in rows['evidence'] if not EXCLUDE.search(e['path'])]
    by_repo = defaultdict(list)
    for e in evidence:
        by_repo[e['repo']].append(e)
    sizes = defaultdict(int)
    files = defaultdict(list)
    seen = set()
    for repo in repos:
        for f in repo['files']:
            lang = EXTENSIONS.get(Path(f['path']).suffix.lower())
            if not lang or EXCLUDE.search(f['path']) or f['sha'] in seen:
                continue
            seen.add(f['sha'])
            sizes[lang] += f['size']
            files[lang].append({'repo':repo['repo'],**f})
    charts = [{'key':'languages','title':'Language footprint','subtitle':'Share of unique source-file bytes','unit':'bytes','items':[{'label':k,'value':v,'evidence':files[k]} for k,v in sorted(sizes.items(),key=lambda kv:-kv[1])]}]
    for key, rules in RULES.items():
        items = []
        for label, pattern in rules:
            matches=[]
            for repo in repos:
                if key == 'agentic':
                    readme = '\n'.join(e['content'] for e in by_repo[repo['repo']] if e['path'].lower() == 'readme.md')
                    if not re.search(r'\bagentic\b|\bRAG\b|tool.call|LLM.{0,30}agent', readme, re.I):
                        continue
                for e in by_repo[repo['repo']]:
                    hit = re.search(pattern,e['content'],re.I)
                    if hit:
                        line=e['content'][max(0,e['content'].rfind('\n',0,hit.start())+1):e['content'].find('\n',hit.end()) if '\n' in e['content'][hit.end():] else len(e['content'])]
                        matches.append({'repo':repo['repo'],'path':e['path'],'sha':e['sha'],'excerpt':line[:450]})
                        break
                else:
                    # Filenames are direct evidence for these infrastructure categories.
                    path_pattern = r'(^|/)Dockerfile$|(^|/)docker-compose' if label=='Containers' else r'^\.github/workflows/.*\.ya?ml$' if label=='CI / CD' else None
                    if path_pattern:
                        file=next((f for f in repo['files'] if re.search(path_pattern,f['path'])),None)
                        if file:
                            matches.append({'repo':repo['repo'],'path':file['path'],'sha':file['sha'],'excerpt':'Repository file exists.'})
            items.append({'label':label,'value':len(matches),'evidence':matches,'pattern':pattern})
        charts.append({'key':key,'title':{'engineering':'Engineering stack','ai':'AI & machine learning','agentic':'Agentic AI focus'}[key],'subtitle':'Documented repository-topic matches','unit':'matches','items':sorted(items,key=lambda x:-x['value'])})
    report={'captured_at':rows['captured_at'],'repo_count':len(repos),'scope':rows['scope'],'repositories':[{'repo':r['repo'],'tree_sha':r['tree_sha']} for r in repos], 'methodology':{'languages':'Extension-classified source bytes; deduplicated by Git blob SHA across repositories. Excludes notebooks, dependencies, builds, vendored and original-work copies, minified files, TS declarations, data/report exports and the revision-baseline HTML snapshot. This is not GitHub Linguist or authored-line share.', 'topics':'One match per repository per selected category in root README or dependency manifests; Docker/CI additionally use filenames. Agentic categories are scoped to READMEs mentioning agentic, RAG, tool calling or LLM agents. Counts describe documentation and dependency coverage, including concepts and labs, not implementation or proficiency. A repository may match multiple categories. Percentages use the sum of category matches, not all repositories. Zero means no match in this bounded sample.'},'charts':charts}
    dest=ROOT/'config/portfolio-metrics.json'
    dest.write_text(json.dumps(report,indent=2,ensure_ascii=False)+'\n',encoding='utf-8',newline='\n')
    for c in charts: print(c['key'], [(x['label'],x['value']) for x in c['items']])


if __name__=='__main__':
    summarize(Path(sys.argv[1]))
