"""Career and Keele education overlays for the GitHub profile SVG.

Source: approved Atlas Candidate_Facts, read 14 November 2026.
The caller supplies the continuous background and optional authentic logo symbols.
"""

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
            f'width="{width}" height="{height}" color="#f0f6fc"/>')


def render_career(icons):
    """Return a self-contained 1400×660 SVG fragment, without a background.

    Optional icon keys: ``amazon`` and ``keele``. Missing institution logos are
    omitted; names remain visible and no substitute emblem is fabricated.
    """
    out = [
        '<g id="career-education" aria-labelledby="career-title">',
        '<title id="career-title">Professional experience and Keele University education</title>',
        '<desc>Amazon AGI Data Services evaluation experience, three earlier roles, '
        'and an MSc Computer Science with Distinction from Keele University.</desc>',
        '<defs><linearGradient id="career-topline"><stop stop-color="#4493f8" '
        'stop-opacity=".7"/><stop offset="1" stop-color="#4493f8" '
        'stop-opacity="0"/></linearGradient></defs>',
    ]

    # The translucent surfaces let the shared page grid remain visible.
    for x in (24, 714):
        out += [
            f'<rect x="{x}" y="24" width="662" height="612" rx="18" '
            'fill="#151b23" fill-opacity=".55" stroke="#3d444d" stroke-opacity=".82"/>',
            f'<path d="M{x+22} 24H{x+250}" fill="none" '
            'stroke="url(#career-topline)" stroke-width="1.4"/>',
        ]

    # Experience: the current role has prominence; prior roles retain dates.
    out += [
        _text(56, 66, "PROFESSIONAL EXPERIENCE", 18, "#9198a1", mono=True, tracking=1.5),
        _brand(icons, "amazon", 600, 44, 50, 42),
        _text(56, 120, "Amazon AGI Data Services", 27, weight=700),
        _text(56, 156, "Machine Learning Data Associate II", 23, weight=600),
        _text(56, 190, "JUN 2025 — PRESENT  /  LONDON", 19, "#9198a1", mono=True),
    ]
    for y, label in (
        (238, "Structured foundation-model evaluation"),
        (270, "Multimodal red / blue-team review"),
        (302, "Peer verification since February 2026"),
    ):
        out += [f'<circle cx="62" cy="{y-7}" r="3" fill="#4493f8"/>',
                _text(78, y, label, 21, "#c9d1d9")]
    out += [
        '<path d="M56 338H654" stroke="#3d444d" stroke-opacity=".65"/>',
        _text(56, 375, "EARLIER EXPERIENCE", 18, "#9198a1", mono=True, tracking=1.5),
    ]
    for y, employer, role, date in (
        (416, "Flione IT", "Associate Web Developer", "OCT 2022 — JUL 2023"),
        (482, "Thrive and Shine", "Web Developer Intern", "SEP 2024 — DEC 2024"),
        (548, "Edu Lettings", "Recreational Assistant · part-time", "APR 2024 — JUN 2025"),
    ):
        out += [
            _text(56, y, employer, 23, weight=600),
            _text(654, y, date, 18, "#9198a1", anchor="end", mono=True),
            _text(56, y+28, role, 20, "#9198a1"),
        ]

    # Degree and award form a complementary panel, not a résumé paragraph.
    out += [
        _text(746, 66, "EDUCATION", 18, "#9198a1", mono=True, tracking=1.5),
        _brand(icons, "keele", 1228, 38, 118, 60),
        _text(746, 120, "Keele University", 32, weight=700),
        _text(746, 158, "MSc Computer Science", 27, weight=600),
        _text(746, 191, "SEP 2023 — SEP 2024", 19, "#9198a1", mono=True),
        '<rect x="746" y="219" width="194" height="42" rx="8" fill="#4493f8" '
        'fill-opacity=".08" stroke="#4493f8" stroke-opacity=".5"/>',
        _text(843, 247, "DISTINCTION", 20, "#79c0ff", 700, "middle", True, 1.2),
        _text(746, 310, "Best Performance Award", 25, weight=700),
        _text(746, 346, "School of Mathematics", 21, "#c9d1d9"),
        _text(746, 376, "and Computer Science", 21, "#c9d1d9"),
        '<path d="M746 410H1344" stroke="#3d444d" stroke-opacity=".65"/>',
        _text(746, 450, "RESEARCH FOCUS", 18, "#9198a1", mono=True, tracking=1.5),
        _text(746, 491, "Time-series neural networks", 25, weight=600),
        _text(746, 530, "LSTM regression and classification", 21, "#c9d1d9"),
        _text(746, 563, "Dairy-herd activity + temperature data", 20, "#9198a1"),
        '</g>',
    ]
    return "\n".join(out)
