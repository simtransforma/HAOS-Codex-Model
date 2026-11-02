"""The local-file subset of Markdown links; no network or full Markdown parser."""

from __future__ import annotations

import re


def prose(text: str) -> str:
    lines = []
    fence = None
    for line in text.splitlines():
        match = re.match(r"^\s{0,3}(`{3,}|~{3,})", line)
        if match:
            marker = match[1]
            if fence is None:
                fence = marker
            elif marker[0] == fence[0] and len(marker) >= len(fence):
                fence = None
            continue
        if fence is None:
            lines.append(line)
    return "\n".join(lines)


def destination(text: str, start: int) -> str:
    while start < len(text) and text[start].isspace():
        start += 1
    if start == len(text):
        return ""
    angle = text[start] == "<"
    if angle:
        start += 1
    depth = 0
    output = []
    while start < len(text):
        char = text[start]
        if char == "\\" and start + 1 < len(text) and text[start + 1] in r"()<>\ ":
            output.append(text[start + 1])
            start += 2
            continue
        if angle:
            if char == ">":
                break
        else:
            if char.isspace() or (char == ")" and depth == 0):
                break
            if char == "(":
                depth += 1
            elif char == ")":
                depth -= 1
        output.append(char)
        start += 1
    return "".join(output)


def local_targets(text: str) -> tuple[list[str], bool]:
    # Links shown as inline code are examples; explicit code paths are checked
    # separately by the caller. Fenced examples have already been removed.
    markup = re.sub(r"(`+)(.*?)\1", "", text)
    targets = [destination(markup, match.end()) for match in re.finditer(
        r"(?<!\\)!?\[(?:\\.|[^\]\n])*\]\(", markup
    )]

    def label(value: str) -> str:
        return " ".join(value.split()).casefold()

    definitions = {}
    for match in re.finditer(r"^\s{0,3}\[([^\]]+)\]:\s*", markup, re.M):
        target = destination(markup, match.end())
        definitions[label(match[1])] = target
        targets.append(target)
    missing = any(
        label(reference or title) not in definitions
        for title, reference in re.findall(r"(?<!\\)!?\[([^\]]+)\]\[([^\]]*)\]", markup)
    )
    return targets, missing
