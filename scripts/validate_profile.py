#!/usr/bin/env python3
"""Validate local profile images and README references without network access."""

from pathlib import Path
import re
import sys
from urllib.parse import unquote, urlsplit
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]


def main():
    errors = []
    svgs = list((ROOT / "assets").rglob("*.svg"))
    if not svgs:
        errors.append("No local SVG assets found")
    for path in svgs:
        try:
            doc = ET.fromstring(path.read_text(encoding="utf-8"))
            if doc.tag.split("}")[-1] != "svg" or not doc.get("viewBox"):
                errors.append(f"{path.relative_to(ROOT)}: missing SVG viewBox")
            try:
                viewbox = [float(v) for v in doc.get("viewBox", "").replace(",", " ").split()]
                if len(viewbox) != 4 or viewbox[2] <= 0 or viewbox[3] <= 0:
                    raise ValueError
            except ValueError:
                errors.append(f"{path.relative_to(ROOT)}: invalid SVG dimensions")
            for element in doc.iter():
                if element.tag.split("}")[-1] in ("script", "foreignObject", "iframe"):
                    errors.append(f"{path.relative_to(ROOT)}: active embedded content")
                for key, value in element.attrib.items():
                    if key.lower().startswith("on") or (key.split("}")[-1] == "href" and re.match(r"\s*(javascript:|https?://)", value, re.I)):
                        errors.append(f"{path.relative_to(ROOT)}: script or external resource")
        except (ET.ParseError, OSError) as exc:
            errors.append(f"{path.relative_to(ROOT)}: {type(exc).__name__}")
    readme = ROOT / "README.md"
    if not readme.exists():
        errors.append("README.md missing")
    else:
        content = readme.read_text(encoding="utf-8")
        refs = re.findall(r'(?:src|href)=[\"\x27]([^\"\x27]+)[\"\x27]', content)
        refs += re.findall(r'\]\(([^\s)]+)\)', content)
        for ref in refs:
            uri = urlsplit(ref)
            if uri.scheme or ref.startswith("#"):
                continue
            local = (ROOT / unquote(uri.path)).resolve()
            if not local.is_relative_to(ROOT) or not local.exists():
                errors.append(f"README.md: missing or out-of-root reference {ref}")
        if re.search(r"<script|<iframe|\bstyle=|\bonclick=", content, re.I):
            errors.append("README contains HTML GitHub will strip")
        if "linkedin.com/in/jyotheshkarnam" not in content:
            errors.append("README lacks verified LinkedIn contact")
    if errors:
        print("\n".join(errors), file=sys.stderr)
        raise SystemExit(1)
    print(f"Validated {len(svgs)} SVGs and all local README references.")


if __name__ == "__main__":
    main()
