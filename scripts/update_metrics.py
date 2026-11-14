#!/usr/bin/env python3
"""Render GitHub-only public repository telemetry. Python standard library only."""

import argparse
from collections import Counter
from datetime import datetime, timezone
from html import escape
import json
import os
from pathlib import Path
import tempfile
from urllib.request import Request, urlopen
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
PALETTE = ["#4493F8", "#79C0FF", "#A5A5FF", "#D2A8FF", "#F78166", "#FFA657", "#9198A1"]
FIELDS = ("id", "name", "full_name", "private", "fork", "archived", "stargazers_count", "forks_count", "language", "pushed_at", "html_url")


def utc_now():
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def api_get(url):
    headers = {"Accept": "application/vnd.github+json", "User-Agent": "jyotheshkar-profile-metrics", "X-GitHub-Api-Version": "2022-11-28"}
    # The user-repositories endpoint returns public repositories only. The workflow
    # token increases the rate limit; no private-repository endpoint is queried.
    token = os.environ.get("GITHUB_TOKEN")
    if token:
        headers["Authorization"] = "Bearer " + token
    with urlopen(Request(url, headers=headers), timeout=30) as response:
        return json.load(response)


def collect(user):
    rows, page = [], 1
    while True:
        batch = api_get(f"https://api.github.com/users/{user}/repos?type=owner&per_page=100&page={page}")
        if not isinstance(batch, list):
            raise ValueError("GitHub returned an invalid repository page")
        rows.extend(batch)
        if len(batch) < 100:
            break
        page += 1
        if page > 100:
            raise ValueError("Unexpectedly large repository pagination")
    safe = []
    for repo in rows:
        if repo.get("private") is not False or repo.get("owner", {}).get("login", "").lower() != user.lower():
            raise ValueError("Unexpected repository visibility or owner")
        safe.append({**{key: repo[key] for key in FIELDS}, "owner": {"login": repo["owner"]["login"]}})
    return {"user": user, "captured_at": utc_now(), "complete": True, "source": "GitHub public repository REST metadata; public repositories only.", "repositories": safe}


def parse_date(value):
    parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if parsed.tzinfo is None:
        raise ValueError("Timestamp must include a timezone")
    return parsed


def validate_snapshot(data, user):
    if data.get("user", "").lower() != user.lower() or data.get("complete") is not True:
        raise ValueError("Snapshot must identify its owner and complete public inventory")
    parse_date(data["captured_at"])
    repos = data["repositories"]
    if not isinstance(repos, list) or not repos:
        raise ValueError("Snapshot has no repository list")
    seen = set()
    for r in repos:
        if set(FIELDS) - r.keys():
            raise ValueError("Repository metadata is incomplete")
        if r["id"] in seen:
            raise ValueError("Duplicate repository in snapshot")
        seen.add(r["id"])
        if r["private"] is not False or r.get("owner", {}).get("login", "").lower() != user.lower():
            raise ValueError("Snapshot contains a non-public or foreign repository")
        for field in ("stargazers_count", "forks_count"):
            if not isinstance(r[field], int) or r[field] < 0:
                raise ValueError("Invalid repository count")
        if not isinstance(r["fork"], bool) or not isinstance(r["archived"], bool):
            raise ValueError("Repository classification missing")
        if r["pushed_at"]:
            parse_date(r["pushed_at"])
    return repos


def text(x, y, value, size=14, fill="#F0F6FC", weight=400, extra=""):
    return f'<text x="{x}" y="{y}" fill="{fill}" font-size="{size}" font-weight="{weight}" {extra}>{escape(str(value))}</text>'


def frame(title, subtitle, height):
    return [f'<svg xmlns="http://www.w3.org/2000/svg" width="1000" height="{height}" viewBox="0 0 1000 {height}" role="img" aria-labelledby="title desc">', f'<title id="title">{escape(title)}</title><desc id="desc">{escape(subtitle)}</desc>', '<defs><pattern id="grid" width="32" height="32" patternUnits="userSpaceOnUse"><path d="M32 0H0V32" fill="none" stroke="#3D444D" stroke-width=".5"/></pattern></defs>', f'<rect width="1000" height="{height}" rx="14" fill="#0D1117"/><rect x="1" y="1" width="998" height="{height-2}" rx="13" fill="url(#grid)" stroke="#3D444D"/>', '<g font-family="Consolas,DejaVu Sans Mono,monospace">', '<path d="M28 44H42M35 37V51" stroke="#4493F8" stroke-width="2"/>', text(54, 50, title, 20, "#4493F8", 700), text(30, 78, subtitle, 12, "#9198A1")]


def render_metrics(data, repos):
    active = [r for r in repos if not r["fork"] and not r["archived"]]
    counts = [("PUBLIC REPOS", len(repos)), ("ACTIVE SOURCE", len(active)), ("REPO STARS", sum(r["stargazers_count"] for r in repos)), ("REPO FORKS", sum(r["forks_count"] for r in repos))]
    dated = parse_date(data["captured_at"]).strftime("%d %b %Y %H:%M UTC")
    svg = frame("ENGINEERING TELEMETRY", f"PUBLIC GITHUB SNAPSHOT / {dated}", 480)
    for i, (label, count) in enumerate(counts):
        x = 30 + 240 * i
        svg += [f'<rect x="{x}" y="102" width="220" height="108" rx="8" fill="#151B23" stroke="#3D444D"/>', text(x+18, 132, label, 12, "#9198A1"), text(x+18, 183, count, 42, "#F0F6FC", 700), f'<path d="M{x+175} 178h23v-20" fill="none" stroke="#4493F8" stroke-width="2"/>']
    language_counts = Counter(r["language"] for r in active if r["language"])
    ordered = language_counts.most_common(6)
    rest = sum(language_counts.values()) - sum(v for _, v in ordered)
    if rest:
        ordered.append(("Other", rest))
    total = sum(language_counts.values())
    svg += [text(30, 251, "LANGUAGE FOOTPRINT", 16, "#4493F8", 700), text(30, 277, "Primary language by active source repository", 13, "#9198A1")]
    offset = 0
    if total:
        for i, (_, count) in enumerate(ordered):
            width = 940 * count / total
            svg.append(f'<rect x="{30+offset:.2f}" y="300" width="{width:.2f}" height="18" fill="{PALETTE[i]}"/>')
            offset += width
    else:
        svg.append('<rect x="30" y="300" width="940" height="18" fill="#3D444D"/>')
    for i, (lang, count) in enumerate(ordered):
        col, row = i % 4, i // 4
        x, y = 30 + col*240, 352 + row*32
        svg += [f'<rect x="{x}" y="{y-10}" width="9" height="9" fill="{PALETTE[i]}"/>', text(x+18, y, f"{lang}  {count}", 12)]
    no_language = len(active) - total
    svg += [text(30, 433, f"Counts are repositories, not skill scores. Unclassified active source repos: {no_language}.", 11, "#9198A1"), text(30, 456, "Active source = owned, public, non-fork, non-archived. Stars/forks span all public repos.", 10, "#9198A1"), '</g></svg>']
    return "\n".join(svg)


def render_activity(data, repos, user):
    captured = parse_date(data["captured_at"])
    recent = sorted((r for r in repos if not r["fork"] and not r["archived"] and r["name"].lower() != user.lower() and r["pushed_at"]), key=lambda r: r["pushed_at"], reverse=True)[:6]
    svg = frame("PUBLIC BUILD SIGNAL", "LAST PUSH BY REPOSITORY / 90-DAY RECENCY WINDOW", 480)
    start, end = 460, 935
    for days in (90, 60, 30, 0):
        x = end - days/90*(end-start)
        svg += [f'<path d="M{x:.1f} 116V399" stroke="#3D444D" stroke-dasharray="3 5"/>', text(x, 105, "Today" if not days else f"-{days}d", 10, "#9198A1", extra='text-anchor="middle"')]
    for i, r in enumerate(recent):
        y = 140+i*45
        age = max(0, (captured-parse_date(r["pushed_at"])).total_seconds()/86400)
        x = end-min(90,age)/90*(end-start)
        name = r["name"] if len(r["name"]) <= 39 else r["name"][:36]+"..."
        date = parse_date(r["pushed_at"]).strftime("%d %b %Y")
        svg += [text(30, y, name, 13, "#F0F6FC", 600), text(30, y+17, date, 10, "#9198A1"), f'<path d="M{start} {y-3}H{end}" stroke="#3D444D" stroke-width="3"/>', f'<path d="M{start} {y-3}H{x:.1f}" stroke="#4493F8" stroke-opacity=".32" stroke-width="3"/>', f'<circle cx="{x:.1f}" cy="{y-3}" r="8" fill="#4493F8" opacity=".13"/><circle cx="{x:.1f}" cy="{y-3}" r="3" fill="#4493F8"/>']
    svg += [text(30, 432, "Source: public repository pushed_at metadata. A push can include any contributor.", 11, "#9198A1"), text(30, 454, "This is repository recency, not a commit count or contribution streak. Profile repo excluded.", 10, "#9198A1"), '</g></svg>']
    return "\n".join(svg)


def atomic_write(path, content):
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile("w", encoding="utf-8", dir=path.parent, delete=False, suffix=".tmp") as handle:
        handle.write(content)
        temporary = Path(handle.name)
    temporary.replace(path)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--user", default="jyotheshkar")
    parser.add_argument("--snapshot", type=Path, help="Use a complete sanitized public metadata snapshot offline")
    parser.add_argument("--output-dir", type=Path, default=ROOT / "assets")
    args = parser.parse_args()
    if not args.user or any(c not in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-" for c in args.user):
        parser.error("Invalid GitHub username")
    try:
        data = json.loads(args.snapshot.read_text(encoding="utf-8")) if args.snapshot else collect(args.user)
        repos = validate_snapshot(data, args.user)
        outputs = {"metrics.svg": render_metrics(data, repos), "activity.svg": render_activity(data, repos, args.user)}
        for rendered in outputs.values():
            ET.fromstring(rendered)
        # Collection, validation and rendering finish before any existing output is replaced.
        for name, rendered in outputs.items():
            atomic_write(args.output_dir / name, rendered + "\n")
        if not args.snapshot:
            atomic_write(args.output_dir / "data" / "public-repos.json", json.dumps(data, indent=2) + "\n")
        print(f"Rendered two SVGs from {len(repos)} public repositories; snapshot {data['captured_at']}.")
    except Exception as exc:
        # Avoid request objects or headers: credentials must never enter logs.
        raise SystemExit(f"Public metrics refresh failed ({type(exc).__name__}); no metrics are rendered from incomplete data.") from None


if __name__ == "__main__":
    main()
