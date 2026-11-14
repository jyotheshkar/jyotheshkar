# Four circles of skills and exploration

The README replaces the 3D contribution calendar, radar, language-share chart and snake with a single self-contained SVG containing four circular maps. The original profile canvas above it is unchanged.

1. **Language Foundations:** Python, JavaScript, TypeScript, Java, SQL, HTML, CSS and Bash.
2. **Software Engineering:** React, Node.js, backend APIs, PostgreSQL, Docker, GitHub Actions, AWS and system design.
3. **AI & Machine Learning:** PyTorch, TensorFlow, reinforcement learning, transformers, NLP, embeddings, model evaluation and RLHF.
4. **Agentic AI:** planning, tool calling, RAG, memory, workflows, guardrails, tracing and evaluation, and human review.

These are qualitative portfolio focus and learning areas. Equal ring segments, node placement and decorative animation are not measured proficiency, language proportions, contribution activity or assertions of deployed integrations. React, Node.js and TensorFlow were requested as focus areas; this graphic does not assert production experience with them. Python, PyTorch, transformer and reinforcement-learning study are supported by the public LLM-from-scratch and reinforcement-learning repositories. The public Agentic Core excerpt supports bounded workflows, state, approvals and validation, while its broader deployment remains a proposed design. AWS architecture work is a documented lab. No private repository content was published.

## Rebuild

Run `python scripts/build_skill_circles.py` followed by `python scripts/validate_profile.py`. CI rebuilds the SVG and rejects stale output. The builder uses only the Python standard library and local artwork. Devicon source SVGs are retained with their exact Git blob hashes and pinned source URLs in `assets/brands/skills-originals.json`; hashes are checked before embedding. The existing Devicon MIT license is retained in `assets/brands/DEVICON_LICENSE.txt`. Python, PostgreSQL and GitHub use the existing attributed local registry. Brand colors are unchanged; generic concepts use custom blue line glyphs rather than invented brand marks.

The design matches the main canvas (#0d1117 background, subtle grid, blue connections), with four readable stationary hubs in a two-by-two arrangement. Only the orbit highlights and connection trails move. Reduced-motion preferences disable animations. An SVG title/description and a detailed README alt text provide accessible labels. No scripts, external SVG dependencies, tokens or third-party stats service are used.

The former contribution-refresh workflow is removed; historical source and generated contributions remain in the repository for reference. GitHub's native contribution calendar is unaffected. Updating these maps is an editorial change, not a daily activity generator.
