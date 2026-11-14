#!/usr/bin/env python3
"""Validate generated contribution SVGs and add accessible, reduced-motion metadata."""

import argparse
from datetime import datetime, timezone
from pathlib import Path
import re
import xml.etree.ElementTree as ET

NS = "http://www.w3.org/2000/svg"
ET.register_namespace("", NS)
ET.register_namespace("xlink", "http://www.w3.org/1999/xlink")


def validate_local_css(value):
    if re.search(r"@import", value, re.I):
        raise ValueError("External SVG styles are not permitted")
    for match in re.finditer(r"url\s*\((.*?)\)", value, re.I | re.S):
        target = match.group(1).strip()
        if target.startswith(("'", '"')):
            if len(target) < 2 or target[-1] != target[0]:
                raise ValueError("Malformed SVG CSS resource")
            target = target[1:-1].strip()
        if not target.startswith("#") or len(target) == 1:
            raise ValueError("Only local SVG CSS references are permitted")


def prepare(path, kind, captured):
    raw = path.read_text(encoding="utf-8")
    if len(raw.encode("utf-8")) > 2_000_000 or re.search(r"<!DOCTYPE|<!ENTITY", raw, re.I):
        raise ValueError("Unexpected SVG size or document declaration")
    root = ET.fromstring(raw)
    if root.tag != f"{{{NS}}}svg":
        raise ValueError("Expected an SVG document")
    dimensions = [float(v) for v in root.get("viewBox", "").replace(",", " ").split()]
    if len(dimensions) != 4 or not (0 < dimensions[2] < 10000 and 0 < dimensions[3] < 10000):
        raise ValueError("Invalid SVG viewBox")
    ids = set()
    for element in root.iter():
        local_tag = element.tag.split("}")[-1]
        if local_tag in ("script", "foreignObject", "iframe", "audio", "video"):
            raise ValueError("Active content is not permitted")
        identifier = element.get("id")
        if identifier:
            if identifier in ids:
                raise ValueError("Duplicate SVG identifier")
            ids.add(identifier)
        for key, value in element.attrib.items():
            if key.lower().startswith("on"):
                raise ValueError("Event handlers are not permitted")
            if key.split("}")[-1] in ("href", "src") and not value.startswith("#"):
                raise ValueError("External SVG resources are not permitted")
            validate_local_css(value)
        if local_tag == "style":
            validate_local_css(element.text or "")
    title_id, desc_id = f"contribution-{kind}-title", f"contribution-{kind}-description"
    if title_id in ids or desc_id in ids:
        raise ValueError("Reserved accessibility identifiers already exist")
    title = ET.Element(f"{{{NS}}}title", {"id": title_id})
    description = ET.Element(f"{{{NS}}}desc", {"id": desc_id})
    if kind == "3d":
        title.text = "Jyothesh Karnam's GitHub contribution landscape"
        description.text = (
            "3D contribution calendar, contribution-type radar and language share from GitHub's "
            "public profile data over the past year. Language share describes attributed commit "
            "contributions, not skill level. Generated " + captured + "."
        )
    else:
        title.text = "Jyothesh Karnam's animated GitHub contribution trail"
        description.text = (
            "A decorative snake traverses GitHub's contribution calendar over the past year. "
            "This is an animation of recorded activity, not a productivity score or contribution "
            "streak. Reduced-motion preferences show a static frame. Generated " + captured + "."
        )
        style = ET.Element(f"{{{NS}}}style")
        style.text = "@media (prefers-reduced-motion: reduce) { * { animation: none !important; } }"
        root.append(style)
    root.set("role", "img")
    root.set("aria-labelledby", title_id + " " + desc_id)
    root.insert(0, description)
    root.insert(0, title)
    return ET.tostring(root, encoding="unicode") + "\n"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--calendar", type=Path, default=Path("profile-3d-contrib/contribution-3d.svg"))
    parser.add_argument("--snake", type=Path, default=Path("dist/contributions/contribution-snake.svg"))
    parser.add_argument("--output-dir", type=Path, default=Path("dist/contributions"))
    args = parser.parse_args()
    captured = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    rendered = {
        "contribution-3d.svg": prepare(args.calendar, "3d", captured),
        "contribution-snake.svg": prepare(args.snake, "snake", captured),
    }
    args.output_dir.mkdir(parents=True, exist_ok=True)
    for filename, svg in rendered.items():
        (args.output_dir / filename).write_text(svg, encoding="utf-8", newline="\n")
    print("Validated two GitHub contribution SVGs; accessibility metadata added.")


if __name__ == "__main__":
    main()
