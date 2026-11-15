"""Career and university cards; wording approved by the owner on 15 November 2026."""

from html import escape

WIDTH = 1400
HEIGHT = 660
MOBILE_WIDTH = 700
MOBILE_HEIGHT = 1320


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
        '<desc>Model evaluation on Alexa and Nova research models. '
        'Red teaming on Amazon Nova multimodal research models. Quality '
        'and verification for red-teaming workflows across London, Cambridge, Boston, '
        'and Amsterdam. MSc Computer Science with Distinction and Best Performance '
        'Award. THESIS: DHMS, Dairy Herd Monitoring System.</desc>',
    ]
    for x in (24, 714):
        out += [
            f'<rect x="{x}" y="24" width="662" height="612" rx="15" '
            'fill="#111820" stroke="#334253" stroke-width="1.35"/>',
            f'<path d="M{x+20} 24h42" stroke="#4493f8" stroke-width="2" opacity=".8"/>',
        ]

    # Original Amazon artwork sits on an opaque light plate for readable contrast.
    out += [
        '<rect x="50" y="55" width="104" height="100" rx="12" fill="#ffffff"/>',
        _brand(icons, "amazon", 58, 89, 88, 32),
        _text(170, 83, "Amazon AGI Data Services", 27, weight=700),
        _text(170, 122, "Machine Learning Data Associate II", 22, weight=600),
        _text(170, 157, "JUN 2025 — PRESENT  /  LONDON", 17, "#9198a1", mono=True),
    ]
    bullets = (
        (218, ("Model evaluation on Alexa and Nova research models",)),
        (261, ("Red teaming on Amazon Nova multimodal research models",)),
        (304, ("Quality and verification for red-teaming workflows across",
               "London, Cambridge, Boston, and Amsterdam")),
    )
    for y, lines in bullets:
        out.append(f'<circle cx="62" cy="{y-7}" r="3" fill="#4493f8"/>')
        for i, line in enumerate(lines):
            out.append(_text(78, y+i*26, line, 21, "#c9d1d9"))
    out += [
        '<path d="M56 374H654" stroke="#3d444d" stroke-opacity=".65"/>',
        _text(56, 420, "EARLIER EXPERIENCE", 17, "#9198a1", mono=True, tracking=1.5),
    ]
    for y, employer, role, date in (
        (464, "Flione IT", "Associate Web Developer", "OCT 2022 — JUL 2023"),
        (530, "Thrive and Shine", "Web Developer Intern", "SEP 2024 — DEC 2024"),
        (596, "Edu Lettings", "Recreational Assistant · part-time", "APR 2024 — JUN 2025"),
    ):
        out += [
            _text(56, y, employer, 22, weight=600),
            _text(654, y, date, 16, "#9198a1", anchor="end", mono=True),
            _text(56, y+23, role, 18, "#9198a1"),
        ]

    out += [
        _brand(icons, "keele", 746, 55, 130, 100),
        _text(900, 83, "Keele University", 32, weight=700),
        _text(900, 123, "MSc Computer Science", 27, weight=600),
        _text(900, 157, "SEP 2023 — SEP 2024", 17, "#9198a1", mono=True),
        _text(746, 218, "Awarded Distinction", 29, "#79c0ff", 600),
        _text(746, 267, "Received Best Performance Award", 27, weight=700),
        _text(746, 309, "Keele University Department of", 21, "#c9d1d9"),
        _text(746, 338, "Mathematics and Computer Science", 21, "#c9d1d9"),
        '<path d="M746 374H1344" stroke="#3d444d" stroke-opacity=".65"/>',
        _text(746, 420, "THESIS", 18, "#91a9c3", mono=True, tracking=1.2),
        _text(746, 464, "DHMS: Dairy Herd Monitoring System", 26, weight=600),
        _text(746, 512, "Time-series neural networks", 22, "#c9d1d9"),
        _text(746, 550, "LSTM regression and classification", 21, "#c9d1d9"),
        _text(746, 588, "Dairy-herd activity and temperature data", 20, "#9198a1"),
        '</g>',
    ]
    return "\n".join(out)


def render_career_mobile(icons):
    """Stack the exact two desktop cards in a 700 by 1320 SVG fragment.

    A shared definition keeps the copy and original-colour symbols identical.
    Each nested viewport selects one card without reducing the font size.
    The caller supplies the outer SVG, background, and institution symbols.
    """
    return (
        '<defs><g id="career-mobile-layout">' + render_career(icons) + '</g></defs>'
        '<svg x="0" y="0" width="700" height="660" viewBox="0 0 700 660" '
        'overflow="hidden"><use href="#career-mobile-layout"/></svg>'
        '<svg x="0" y="660" width="700" height="660" viewBox="690 0 700 660" '
        'overflow="hidden"><use href="#career-mobile-layout"/></svg>'
    )

