"""Career and university cards; wording approved by the owner on 15 November 2026."""

from html import escape

WIDTH = 1400
HEIGHT = 660


def _text(x, y, value, size=22, fill="#f0f6fc", weight=400,
          anchor="start", mono=False, tracking=None):
    family = "ui-monospace,Consolas,monospace" if mono else "Arial,Helvetica,sans-serif"
    letter = f' letter-spacing="{tracking}"' if tracking is not None else ""
    return (f'<text x="{x}" y="{y}" fill="{fill}" font-family="{family}" '
            f'font-size="{size}" font-weight="{weight}" text-anchor="{anchor}"'
            f'{letter}>{escape(value)}</text>')


def _brand(icons, key, x, y, width=48, height=48):
    if key not in icons:
        return ""
    return (f'<use href="#brand-{escape(key)}" x="{x}" y="{y}" '
            f'width="{width}" height="{height}"/>')


def render_career(icons):
    """Return a 1400 by 660 fragment with original-colour institution symbols."""
    out = [
        '<g id="career-education" aria-labelledby="career-title">',
        '<title id="career-title">Amazon experience and Keele University education</title>',
        '<desc>Model evaluation experience on Alexa and Nova research models. '
        'Red teaming on Amazon Nova multimodal research models. Quality assurance '
        'and verification for red-teaming workflows across London, Cambridge, Boston, '
        'and Amsterdam. MSc Computer Science with Distinction and Best Performance '
        'Award. Research: DHMS, Dairy Herd Monitoring System.</desc>',
        '<defs><linearGradient id="career-topline"><stop stop-color="#4493f8" '
        'stop-opacity=".7"/><stop offset="1" stop-color="#4493f8" '
        'stop-opacity="0"/></linearGradient></defs>',
    ]
    for x in (24, 714):
        out += [
            f'<rect x="{x}" y="24" width="662" height="612" rx="18" '
            'fill="#151b23" fill-opacity=".55" stroke="#3d444d" stroke-opacity=".82"/>',
            f'<path d="M{x+22} 24H{x+250}" fill="none" '
            'stroke="url(#career-topline)" stroke-width="1.4"/>',
        ]

    # Pale mounts preserve the original dark wordmarks and their real colours.
    out += [
        '<rect x="523" y="49" width="131" height="52" rx="7" fill="#f0f3f6"/>',
        _brand(icons, "amazon", 536, 59, 105, 33),
        _text(56, 83, "Amazon AGI Data Services", 27, weight=700),
        _text(56, 122, "Machine Learning Data Associate II", 23, weight=600),
        _text(56, 157, "JUN 2025 — PRESENT  /  LONDON", 18, "#9198a1", mono=True),
    ]
    bullets = (
        (203, ("Model evaluation experience on Alexa", "and Nova research models")),
        (270, ("Red teaming on Amazon Nova", "multimodal research models")),
        (337, ("Quality assurance and verification for", "red-teaming workflows across London,", "Cambridge, Boston, and Amsterdam")),
    )
    for y, lines in bullets:
        out.append(f'<circle cx="62" cy="{y-7}" r="3" fill="#4493f8"/>')
        for i, line in enumerate(lines):
            out.append(_text(78, y+i*26, line, 21, "#c9d1d9"))
    out += [
        '<path d="M56 419H654" stroke="#3d444d" stroke-opacity=".65"/>',
        _text(56, 450, "EARLIER EXPERIENCE", 17, "#9198a1", mono=True, tracking=1.5),
    ]
    for y, employer, role, date in (
        (482, "Flione IT", "Associate Web Developer", "OCT 2022 — JUL 2023"),
        (537, "Thrive and Shine", "Web Developer Intern", "SEP 2024 — DEC 2024"),
        (592, "Edu Lettings", "Recreational Assistant · part-time", "APR 2024 — JUN 2025"),
    ):
        out += [
            _text(56, y, employer, 22, weight=600),
            _text(654, y, date, 16, "#9198a1", anchor="end", mono=True),
            _text(56, y+23, role, 18, "#9198a1"),
        ]

    out += [
        _text(746, 83, "Keele University", 32, weight=700),
        _text(746, 123, "MSc Computer Science", 27, weight=600),
        _text(746, 157, "SEP 2023 — SEP 2024", 18, "#9198a1", mono=True),
        '<path d="M746 184V232" stroke="#79c0ff" stroke-width="3"/>',
        _text(765, 215, "Distinction", 30, "#79c0ff", 600),
        '<rect x="746" y="270" width="214" height="90" rx="8" fill="#f0f3f6"/>',
        _brand(icons, "keele", 760, 290, 186, 49),
        _text(984, 288, "Best Performance Award", 24, weight=700),
        _text(984, 322, "School of Mathematics", 20, "#c9d1d9"),
        _text(984, 350, "and Computer Science", 20, "#c9d1d9"),
        '<path d="M746 400H1344" stroke="#3d444d" stroke-opacity=".65"/>',
        _text(746, 435, "RESEARCH FOCUS", 17, "#9198a1", mono=True, tracking=1.5),
        _text(746, 475, "DHMS", 29, weight=700),
        _text(746, 508, "Dairy Herd Monitoring System", 24, weight=600),
        _text(746, 548, "Time-series neural networks", 22, "#c9d1d9"),
        _text(746, 578, "LSTM regression and classification", 20, "#c9d1d9"),
        _text(746, 607, "Dairy-herd activity and temperature data", 19, "#9198a1"),
        '</g>',
    ]
    return "\n".join(out)
