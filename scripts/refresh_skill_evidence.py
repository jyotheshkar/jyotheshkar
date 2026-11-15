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
import tomllib

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
TITLES = {'languages':'Languages', 'libraries':'Libraries and Frameworks', 'cloud':'Cloud Skills',
          'aiml':'AI/ML Engineering', 'agentic':'Agentic AI Engineering'}
LIBRARIES = {
    'numpy':'NumPy', 'pandas':'pandas', 'sklearn':'scikit-learn', 'torch':'PyTorch',
    'tensorflow':'TensorFlow', 'keras':'Keras', 'matplotlib':'Matplotlib',
    'seaborn':'Seaborn', 'scipy':'SciPy', 'statsmodels':'statsmodels',
    'pydantic':'Pydantic', 'fastapi':'FastAPI', 'flask':'Flask',
    'streamlit':'Streamlit', 'requests':'Requests', 'httpx':'HTTPX',
    'anthropic':'Anthropic SDK', 'openai':'OpenAI SDK', 'faiss':'FAISS',
    'sentence_transformers':'Sentence Transformers', 'transformers':'Transformers',
    'tiktoken':'tiktoken', 'langchain':'LangChain', 'langgraph':'LangGraph',
    'boto3':'Boto3', 'reportlab':'ReportLab', 'pygame':'Pygame', 'cv2':'OpenCV',
    'xgboost':'XGBoost', 'econml':'EconML', 'qdrant_client':'Qdrant',
    'fastembed':'FastEmbed', 'PIL':'Pillow', 'sympy':'SymPy',
    'react':'React', 'next':'Next.js', 'recharts':'Recharts', 'zod':'Zod',
    'lucide-react':'Lucide', 'framer-motion':'Motion', 'express':'Express',
    'pmdarima':'pmdarima', 'fuzzywuzzy':'FuzzyWuzzy', 'spacy':'spaCy',
    'speech_recognition':'SpeechRecognition', 'pyttsx3':'pyttsx3',
    'pyautogui':'PyAutoGUI', 'face_recognition':'face_recognition',
    'cryptography':'cryptography', 'dotenv':'python-dotenv',
    'psycopg':'Psycopg',
    'joblib':'joblib', 'lightgbm':'LightGBM',
}


def library_usage(body, path):
    """Require an imported external library and an executable use of its binding.

    Dependency manifests, comments, strings and unused imports are not evidence.
    Notebook callers pass code cells, never markdown or saved outputs.
    """
    if path.endswith(('.py', '.ipynb')):
        try:
            # Notebook shell/magic commands do not establish Python library use.
            body = '\n'.join(line for line in body.splitlines() if not line.lstrip().startswith(('%', '!')))
            tree = ast.parse(body)
        except SyntaxError:
            return set()
        imported = {}
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    root = alias.name.split('.')[0]
                    if root in LIBRARIES:
                        imported[alias.asname or root] = LIBRARIES[root]
            elif isinstance(node, ast.ImportFrom) and node.level == 0 and node.module:
                root = node.module.split('.')[0]
                if root in LIBRARIES:
                    for alias in node.names:
                        if alias.name != '*':
                            imported[alias.asname or alias.name] = LIBRARIES[root]
        used = set()
        for node in ast.walk(tree):
            values = []
            if isinstance(node, ast.Call):
                values.append(node.func)
                values.extend(node.args)
                values.extend(keyword.value for keyword in node.keywords)
            elif isinstance(node, ast.ClassDef):
                values.extend(node.bases)
            elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                values.extend(node.decorator_list)
            for value in values:
                for child in ast.walk(value):
                    if isinstance(child, ast.Name) and child.id in imported:
                        used.add(imported[child.id])
        return used
    if not path.endswith(('.js', '.jsx', '.ts', '.tsx', '.mjs', '.cjs')):
        return set()
    code = re.sub(r'/\*.*?\*/|//[^\n]*', '', body, flags=re.S)
    used = set()
    pattern = re.compile(r'^[ \t]*import\s+(?!type\b)(.*?)\s+from\s+[\x27\"]([^\x27\"]+)[\x27\"]\s*;?', re.S | re.M)
    declarations = list(pattern.finditer(code))
    executable = pattern.sub('', code)
    for match in declarations:
        root = match[2].split('/')[0]
        if root not in LIBRARIES:
            continue
        names = []
        for binding in match[1].replace('{', '').replace('}', '').split(','):
            binding = binding.strip()
            if not binding or binding.startswith('type '):
                continue
            name = re.split(r'\s+as\s+', binding)[-1].strip()
            if re.fullmatch(r'[A-Za-z_$][\w$]*', name):
                names.append(name)
        if any(re.search(r'(?:\b'+re.escape(name)+r'\s*(?:\(|\.)|<'+re.escape(name)+r'\b)', executable) for name in names):
            used.add(LIBRARIES[root])
    return used



# Cloud coverage describes implemented integrations and deployment configuration,
# never a claim that a service is live or that deployment has succeeded.
AWS_SERVICES = {
    's3':'Amazon S3', 'ec2':'Amazon EC2', 'rds':'Amazon RDS',
    'lambda':'AWS Lambda', 'dynamodb':'Amazon DynamoDB',
    'bedrock':'Amazon Bedrock', 'bedrock-runtime':'Amazon Bedrock',
    'bedrock-agent':'Amazon Bedrock', 'bedrock-agent-runtime':'Amazon Bedrock',
    'cloudwatch':'Amazon CloudWatch', 'logs':'Amazon CloudWatch',
    'ecs':'Amazon ECS', 'ecr':'Amazon ECR', 'sqs':'Amazon SQS',
    'sns':'Amazon SNS', 'secretsmanager':'AWS Secrets Manager',
    'sts':'AWS STS', 'iam':'AWS IAM',
}
CLOUD_RESOURCES = {
    'aws_s3_bucket':'Amazon S3', 'aws_instance':'Amazon EC2',
    'aws_db_instance':'Amazon RDS', 'aws_lambda_function':'AWS Lambda',
    'aws_dynamodb_table':'Amazon DynamoDB', 'aws_ecs_service':'Amazon ECS',
    'aws_ecs_cluster':'Amazon ECS', 'aws_ecr_repository':'Amazon ECR',
    'aws_cloudwatch_log_group':'Amazon CloudWatch',
    'aws_bedrockagent_agent':'Amazon Bedrock',
    'AWS::S3::Bucket':'Amazon S3', 'AWS::EC2::Instance':'Amazon EC2',
    'AWS::RDS::DBInstance':'Amazon RDS', 'AWS::Lambda::Function':'AWS Lambda',
    'AWS::DynamoDB::Table':'Amazon DynamoDB', 'AWS::ECS::Service':'Amazon ECS',
    'AWS::ECR::Repository':'Amazon ECR', 'AWS::Logs::LogGroup':'Amazon CloudWatch',
    'AWS::Bedrock::Agent':'Amazon Bedrock',
    'google_storage_bucket':'Google Cloud Storage',
    'google_cloud_run_v2_service':'Google Cloud Run',
    'google_bigquery_dataset':'Google BigQuery',
    'azurerm_storage_account':'Azure Storage',
    'azurerm_linux_web_app':'Azure App Service',
    'azurerm_container_app':'Azure Container Apps',
}
CLOUD_EXCLUDE = re.compile(
    r'(^|/)(examples?|samples?|tests?|fixtures?|docs?)(/|$)|'
    r'(^|/)[^/]*(?:[.-](?:example|sample|template))[.-]', re.I)


def cloud_config_candidate(path):
    """Only actual, conventionally named deployment files enter this sample."""
    if CLOUD_EXCLUDE.search(path) or SOURCE_EXCLUDE.search(path):
        return False
    name = Path(path).name.lower()
    return (name in {'dockerfile', 'vercel.json', 'render.yaml', 'render.yml',
                     'fly.toml', 'nixpacks.toml', 'serverless.yml', 'serverless.yaml',
                     'buildspec.yml', 'buildspec.yaml',
                     'template.yml', 'template.yaml', 'cloudformation.json',
                     'cloudformation.yml', 'cloudformation.yaml',
                     'compose.yml', 'compose.yaml', 'docker-compose.yml',
                     'docker-compose.yaml'}
            or name.startswith('dockerfile.') or name.endswith('.tf'))


def _python_cloud_usage(body):
    """Require imported SDK bindings, client construction and a client method."""
    try:
        body = '\n'.join(line for line in body.splitlines()
                         if not line.lstrip().startswith(('%', '!')))
        tree = ast.parse(body)
    except SyntaxError:
        return set()
    sdk_modules, constructors = set(), {}
    class_services = {
        ('azure.storage.blob', 'BlobServiceClient'):'Azure Blob Storage',
        ('azure.storage.blob', 'ContainerClient'):'Azure Blob Storage',
        ('azure.cosmos', 'CosmosClient'):'Azure Cosmos DB',
        ('azure.keyvault.secrets', 'SecretClient'):'Azure Key Vault',
        ('google.cloud', 'storage'):'Google Cloud Storage',
        ('google.cloud', 'bigquery'):'Google BigQuery',
        ('google.cloud', 'pubsub_v1'):'Google Cloud Pub/Sub',
        ('google.cloud.storage', 'Client'):'Google Cloud Storage',
        ('google.cloud.bigquery', 'Client'):'Google BigQuery',
        ('google.cloud.pubsub_v1', 'PublisherClient'):'Google Cloud Pub/Sub',
        ('google.cloud.pubsub_v1', 'SubscriberClient'):'Google Cloud Pub/Sub',
    }
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                if alias.name == 'boto3':
                    sdk_modules.add(alias.asname or 'boto3')
        elif isinstance(node, ast.ImportFrom) and node.level == 0:
            for alias in node.names:
                label = class_services.get((node.module, alias.name))
                if label:
                    constructors[alias.asname or alias.name] = label
    sessions, clients = set(), {}
    def root_name(value):
        while isinstance(value, ast.Attribute):
            value = value.value
        return value.id if isinstance(value, ast.Name) else None
    def service_of(call):
        if not isinstance(call, ast.Call):
            return None
        fn = call.func
        if isinstance(fn, ast.Attribute) and fn.attr in ('client', 'resource'):
            owner = root_name(fn.value)
            if owner in sdk_modules or owner in sessions:
                service = call.args[0] if call.args else next(
                    (k.value for k in call.keywords if k.arg == 'service_name'), None)
                if isinstance(service, ast.Constant) and isinstance(service.value, str):
                    return AWS_SERVICES.get(service.value)
        owner = root_name(fn)
        if owner in constructors:
            return constructors[owner]
        return None
    # In normal source the SDK binding precedes the operation. A few passes also
    # handle function definitions whose AST walk ordering differs from line order.
    for _ in range(3):
        for node in ast.walk(tree):
            if not isinstance(node, (ast.Assign, ast.AnnAssign)):
                continue
            value = node.value
            targets = node.targets if isinstance(node, ast.Assign) else [node.target]
            names = [target.id for target in targets if isinstance(target, ast.Name)]
            if isinstance(value, ast.Call) and isinstance(value.func, ast.Attribute):
                if value.func.attr == 'Session' and root_name(value.func.value) in sdk_modules:
                    sessions.update(names)
            label = service_of(value)
            if label:
                clients.update({name:label for name in names})
    found = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute):
            owner = root_name(node.func.value)
            if owner in clients and node.func.attr not in ('client', 'resource'):
                found.add(clients[owner])
            direct = service_of(node.func.value)
            if direct:
                found.add(direct)
    return found


def cloud_usage(body, path):
    """Recognise explicit SDK calls and valid deployment/resource declarations.

    This intentionally misses unrecognised providers and indirect wrappers.
    Manifests or credentials alone never establish a cloud skill.
    """
    if CLOUD_EXCLUDE.search(path) or SOURCE_EXCLUDE.search(path):
        return set()
    suffix, name = Path(path).suffix.lower(), Path(path).name.lower()
    if suffix in ('.py', '.ipynb'):
        return _python_cloud_usage(body)
    found = set()
    if suffix in ('.js', '.jsx', '.ts', '.tsx', '.mjs', '.cjs'):
        # Provider packages must be imported and their constructed binding used.
        code = re.sub(r'/\*.*?\*/|//[^\n]*', '', body, flags=re.S | re.M)
        executable = re.sub(r'"(?:\\.|[^"\\])*"|\x27(?:\\.|[^\x27\\])*\x27|`(?:\\.|[^`\\])*`',
                            '""', code, flags=re.S)
        providers = {
            '@aws-sdk/client-s3':('S3Client', 'Amazon S3'),
            '@aws-sdk/client-ec2':('EC2Client', 'Amazon EC2'),
            '@aws-sdk/client-bedrock-runtime':('BedrockRuntimeClient', 'Amazon Bedrock'),
            '@aws-sdk/client-lambda':('LambdaClient', 'AWS Lambda'),
            '@aws-sdk/client-dynamodb':('DynamoDBClient', 'Amazon DynamoDB'),
            '@azure/storage-blob':('BlobServiceClient', 'Azure Blob Storage'),
            '@azure/cosmos':('CosmosClient', 'Azure Cosmos DB'),
            '@google-cloud/storage':('Storage', 'Google Cloud Storage'),
            '@google-cloud/bigquery':('BigQuery', 'Google BigQuery'),
        }
        for package, (klass, label) in providers.items():
            match = re.search(r'import\s*\{([^}]+)\}\s*from\s*[\x27"]'
                              + re.escape(package) + r'[\x27"]', code)
            if not match:
                continue
            binding = re.search(r'\b'+klass+r'(?:\s+as\s+(\w+))?\b', match[1])
            if not binding:
                continue
            alias = binding[1] or klass
            assigned = re.search(r'\b(?:const|let|var)\s+(\w+)\s*=\s*new\s+'
                                 + re.escape(alias) + r'\s*\(', executable)
            if assigned and re.search(r'\b'+re.escape(assigned[1])+r'\.\w+\s*\(', executable):
                found.add(label)
        return found
    if not cloud_config_candidate(path):
        return found
    code = '\n'.join(line for line in body.splitlines()
                     if not line.lstrip().startswith(('#', '//')))
    code = re.sub(r'/\*.*?\*/', '', code, flags=re.S)
    if suffix == '.tf':
        code = re.sub(r'<<-?([A-Za-z_]\w*)[^\n]*\n.*?^\s*\1\s*$',
                      '', code, flags=re.S | re.M)
    if name.startswith('dockerfile'):
        if (re.search(r'^\s*FROM\s+(?:--platform=\S+\s+)?[A-Za-z0-9_$][^\s]*',
                      code, re.I | re.M)
                and re.search(r'^\s*(?:COPY|ADD|RUN)\s+\S', code, re.I | re.M)
                and re.search(r'^\s*(?:CMD|ENTRYPOINT|EXPOSE)\s+\S', code, re.I | re.M)):
            found.add('Docker')
    elif name == 'vercel.json':
        try:
            config = json.loads(body)
            meaningful = {'framework','buildCommand','outputDirectory','functions',
                          'rewrites','routes','builds','headers','redirects'}
            if isinstance(config, dict) and any(config.get(key) for key in meaningful):
                found.add('Vercel')
        except (ValueError, TypeError):
            pass
    elif name in ('fly.toml', 'nixpacks.toml'):
        try:
            config = tomllib.loads(body)
            if (name == 'fly.toml' and isinstance(config.get('app'), str)
                    and any(config.get(key) for key in ('http_service', 'services', 'build'))):
                found.add('Fly.io')
            if name == 'nixpacks.toml' and any(config.get(key) for key in ('phases', 'start')):
                found.add('Nixpacks')
        except (tomllib.TOMLDecodeError, TypeError):
            pass
    elif name in ('render.yaml', 'render.yml'):
        if (re.search(r'^services:\s*$', code, re.M)
                and re.search(r'^\s*-\s*type:\s*(?:web|worker|cron|pserv|redis)\s*$', code, re.M)
                and re.search(r'^\s*(?:startCommand|dockerfilePath|runtime|env):\s*\S', code, re.M)):
            found.add('Render')
    elif name in ('compose.yml','compose.yaml','docker-compose.yml','docker-compose.yaml'):
        if (re.search(r'^services:\s*$', code, re.M)
                and re.search(r'^\s{2,}[\w.-]+:\s*$', code, re.M)
                and re.search(r'^\s+(?:image|build):\s*\S', code, re.M)):
            found.add('Docker Compose')
    elif name in ('buildspec.yml', 'buildspec.yaml'):
        if (re.search(r'^version:\s*[\x27\"]?0\.[12][\x27\"]?\s*$', code, re.M)
                and re.search(r'^phases:\s*$', code, re.M)
                and re.search(r'^\s+(?:build|install|pre_build|post_build):\s*$', code, re.M)
                and re.search(r'^\s+commands:\s*$', code, re.M)
                and re.search(r'^\s+-\s+\S', code, re.M)):
            found.add('AWS CodeBuild')
    # Declarations count only in provider resource blocks, never variables,
    # installed providers or a list of service names.
    if suffix == '.tf':
        for resource in re.findall(r'^\s*resource\s+"([^"]+)"\s+"[^"]+"\s*\{', code, re.M):
            if resource in CLOUD_RESOURCES:
                found.add(CLOUD_RESOURCES[resource])
    elif suffix == '.json':
        try:
            config = json.loads(body)
            resources = config.get('Resources', config.get('resources', {}).get('Resources', {}))
            if isinstance(resources, dict):
                for resource in resources.values():
                    if isinstance(resource, dict) and resource.get('Type') in CLOUD_RESOURCES:
                        found.add(CLOUD_RESOURCES[resource['Type']])
        except (ValueError, TypeError, AttributeError):
            pass
    elif suffix in ('.yaml', '.yml') and re.search(r'^\s*Resources:\s*$', code, re.M):
        for resource in re.findall(r'^\s*["\x27]?Type["\x27]?\s*:\s*["\x27]?([A-Za-z0-9:]+)', code, re.M):
            if resource in CLOUD_RESOURCES:
                found.add(CLOUD_RESOURCES[resource])
    return found


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
    deployment = sorted([f for f in files if cloud_config_candidate(f['path'])
                         and f.get('size', 0) <= 250_000], key=lambda f:f['path'])[:20]
    return sorted(candidates, key=priority)[:36] + deployment


def assemble(public, private, captured_at):
    public_ids = {s['source_id'] for s in public['sources']}
    # If a previously private project becomes public, never count it twice.
    private = {**private, 'sources':[s for s in private.get('sources', []) if s['source_id'] not in public_ids]}
    groups = {key:defaultdict(list) for key in TITLES}
    for source in public['sources'] + private['sources']:
        for key in TITLES:
            for label, proof in source['skills'].get(key, {}).items():
                item = {'source_id':source['source_id'], 'visibility':source['visibility']}
                if source['visibility'] == 'public':
                    item.update({'repo':source['repo'], **proof})
                groups[key][label].append(item)
    charts = [{'key':key,'title':title,'unit':'repositories',
               'items':[{'label':label,'value':len(proof),'evidence':proof}
                        for label,proof in sorted(groups[key].items(), key=lambda item:(-len(item[1]), item[0].lower()))]}
              for key,title in TITLES.items()]
    return {
        'schema_version':4, 'captured_at':captured_at,
        'public_snapshot':public, 'private_snapshot':private,
        'methodology':{
            'measure':'One repository per evidenced language or engineering domain. Counts describe source presence, never proficiency or authorship.',
            'languages':'Complete source trees plus inspected notebook code cells. PHP and JSP included. Java requires .java or Processing implementation; a Maven WAR or pure-HTML JSP does not establish Java source. HTML/CSS styling and dependencies/builds are excluded.',
            'libraries':'External libraries/frameworks imported and used in inspected implementation or notebook code cells. Dependency manifests, unused imports, prose and standard-library modules do not qualify. Each repository contributes once per library; this is source coverage, not execution verification.',
            'cloud':'Explicit provider SDK client operations or recognised infrastructure/deployment configuration. Docker and Docker Compose describe container build/deployment tooling. Vercel, Render, Fly.io, Nixpacks and AWS CodeBuild describe configured targets/builds, not verified live infrastructure. Prose, PDFs, credentials, dependency lists and unused client imports do not qualify. The bounded detector can miss indirect wrappers and unrecognised services.',
            'aiml':'Executable implementations of learning domains; dependencies and README claims do not qualify. Notebook markdown/outputs and unimplemented Python stubs are excluded.',
            'agentic':'Only Agentic Core family repositories and linkedin-agent-development-lab. Source implementation symbols, not other web apps or architecture prose.',
            'privacy':'Private evidence publishes only opaque per-repository IDs and skill names. No private names, filenames, snippets, blob hashes, URLs or notebook contents are published.',
            'refresh':'Evidence is captured on demand. A public-only capture preserves the sanitized private baseline and its separate capture date; a full authenticated audit can update both partitions.',
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
        if (api.cache is None and prior and not repo.get('private')
                and prior['tree_sha'] == tree['sha'] and set(prior['skills']) == set(TITLES)):
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
                if SOURCE_EXCLUDE.search(path) or (Path(path).suffix.lower() not in EXTENSIONS
                        and not path.endswith('.ipynb') and not cloud_config_candidate(path)):
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
            for label in cloud_usage(body, path):
                kind = 'deployment configuration' if cloud_config_candidate(path) else 'SDK client operation'
                skills['cloud'].setdefault(label, proof(file, kind))
            if cloud_config_candidate(path):
                continue
            code = implementation(body)
            for label in library_usage(body, path):
                skills['libraries'].setdefault(label, proof(file, 'import and usage'))
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

