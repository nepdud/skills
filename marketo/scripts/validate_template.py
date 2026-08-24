#!/usr/bin/env python3
"""
Validate a Marketo Design Studio template file before pasting it into
Design Studio. Catches the mechanical issues that cause vague "Invalid
tags" validation failures: smart quotes, zero-width characters, duplicate
ids, missing mktoName, and unbalanced tags.

Usage:
    python validate_template.py path/to/template.html

Exit code 0 if clean, 1 if any issues were found.
"""

import re
import sys
from pathlib import Path

BAD_CHARS = {
    "\u2018": "left single quote (')",
    "\u2019": "right single quote (')",
    "\u201c": "left double quote (\u201c)",
    "\u201d": "right double quote (\u201d)",
    "\u200b": "zero-width space",
}

MKTO_CLASSES = ("Text", "Img", "Video", "Form", "Color", "Boolean", "String")


def check_unicode(text):
    issues = []
    for ch, name in BAD_CHARS.items():
        count = text.count(ch)
        if count:
            issues.append(f"Found {count}x {name} -- replace with a straight quote / delete")
    return issues


def check_tag_balance(text, tag):
    # Naive but effective for well-formed templates: count open vs close.
    # Ignores matches inside HTML comments to avoid false positives from
    # documentation text mentioning a tag name.
    without_comments = re.sub(r"<!--.*?-->", "", text, flags=re.DOTALL)
    opens = len(re.findall(rf"<{tag}\b", without_comments))
    closes = len(re.findall(rf"</{tag}>", without_comments))
    if opens != closes:
        return [f"<{tag}> imbalance: {opens} opening vs {closes} closing tags"]
    return []


def check_unique_ids(text):
    ids = re.findall(r'id=["\']([^"\']+)["\']', text)
    seen = {}
    for i in ids:
        seen[i] = seen.get(i, 0) + 1
    dupes = [i for i, c in seen.items() if c > 1]
    if dupes:
        return [f"Duplicate id '{i}' used {seen[i]}x" for i in dupes]
    return []


def check_mkto_name(text):
    pattern = r'<[^>]*class=["\'][^"\']*mkto(?:' + "|".join(MKTO_CLASSES) + r')[^"\']*["\'][^>]*>'
    tags = re.findall(pattern, text)
    missing = [t for t in tags if "mktoName" not in t]
    return [f"Missing mktoName: {t.strip()[:100]}" for t in missing]


def check_mkto_content(text):
    if "mktoContent" not in text:
        return [
            "No mktoContent div found. Required for Free-Form templates "
            "(not required for Guided -- ignore if this is a Guided template)."
        ]
    return []


def validate(path):
    text = Path(path).read_text(encoding="utf-8")

    all_issues = []
    all_issues += check_unicode(text)
    for tag in ("div", "section", "script", "style", "head", "body", "html"):
        all_issues += check_tag_balance(text, tag)
    all_issues += check_unique_ids(text)
    all_issues += check_mkto_name(text)
    mkto_content_issues = check_mkto_content(text)  # informational, not a hard failure

    print(f"Validating {path}\n")

    if all_issues:
        print(f"FOUND {len(all_issues)} ISSUE(S):\n")
        for issue in all_issues:
            print(f"  - {issue}")
    else:
        print("No structural issues found.")

    if mkto_content_issues:
        print("\nNOTE:")
        for note in mkto_content_issues:
            print(f"  - {note}")

    print()
    return len(all_issues) == 0


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python validate_template.py path/to/template.html")
        sys.exit(2)

    ok = validate(sys.argv[1])
    sys.exit(0 if ok else 1)
