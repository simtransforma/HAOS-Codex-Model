"""Conservative, offline publication checks. Diagnostics never contain matches."""

from __future__ import annotations

import re


def placeholder(value: str) -> bool:
    value = value.strip().strip("\"'`").lower()
    return bool(
        re.fullmatch(r"<[^<>]+>|\$\{[^{}]+\}|\{\{[^{}]+\}\}", value)
        or re.fullmatch(
            r"(?:your|seu|sua|example|sample|dummy|fake|test|demo|replace|change[_-]?me|redacted|"
            r"placeholder)(?:[-_ ][a-z0-9_-]+)?", value
        )
        or re.fullmatch(r"(?:password|token|api_key|secret)[_-](?:here|placeholder)", value)
        or re.fullmatch(r"not[-_]a[-_](?:real[-_])?(?:secret|token|key|password)", value)
        or re.fullmatch(r"(?:x{3,}|0{3,}|1{3,}|\*{3,})", value)
    )


EMAIL = re.compile(
    r"(?<![\w.+-])[\w.+-]{1,64}@"
    r"(?=[a-z0-9.-]{1,253}(?![\w.-]))"
    r"([a-z0-9.-]{1,250}\.[a-z]{2,63})(?![\w.-])", re.I
)
WINDOWS_PATH = re.compile(r"\b(?:[a-z]:[/\\]+Users[/\\]+|H:[/\\]+)([^\s\"'`/\\]+)", re.I)
PHONE = re.compile(r"(?<![\w\d])\+[1-9](?:[ .()-]*\d){7,14}(?!\d)|\(\d{2}\)\s*9?\d{4}[- .]\d{4}(?!\d)")
LABELED_PHONE = re.compile(
    r"\b(?:phone|telefone|whatsapp|celular)\s*[:=]\s*[\"']?([+\d][\d .()-]{7,22})", re.I
)
PRODUCTION_ID = re.compile(
    r"\b(?:act_\d{8,}|GTM-[A-Z0-9]{6,}|G-[A-Z0-9]{8,}|AW-\d{8,}|UA-\d{6,}-\d+)\b"
    r"|\b\d{8,}(?:-\d+)?@(?:g\.us|s\.whatsapp\.net)\b"
)
LABELED_ID = re.compile(
    r"\b(?:prod(?:uction)?|account|campaign|pixel|waba|phone_number|business|tenant|project|workflow)"
    r"[_ -]?id[\"']?\s*[:=]\s*[\"']?([a-z0-9_-]{6,})", re.I
)
SECRET_PATTERNS = (
    re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH |DSA |ENCRYPTED )?PRIVATE KEY-----\s+[A-Za-z0-9+/=]{32,}"),
    re.compile(r"\b(?:gh[pousr]_[A-Za-z0-9]{30,}|github_pat_[A-Za-z0-9_]{30,})\b"),
    re.compile(r"\bsk-(?:proj-|ant-)?[A-Za-z0-9_-]{20,}\b"),
    re.compile(r"\b(?:AKIA|ASIA)[A-Z0-9]{16}\b"),
    re.compile(r"\bxox[baprs]-[A-Za-z0-9-]{20,}\b"),
    re.compile(r"\beyJ[A-Za-z0-9_-]{16,}\.[A-Za-z0-9_-]{16,}\.[A-Za-z0-9_-]{16,}\b"),
    re.compile(r"(?<![a-z0-9+.-])[a-z][a-z0-9+.-]*://[^\s/:]+:[^\s/@]{4,}@", re.I),
)
SECRET_ASSIGNMENT = re.compile(
    r"\b(?:api[_-]?key|access[_-]?token|refresh[_-]?token|client[_-]?secret|"
    r"password|passwd|secret|token)[\"']?\s*[:=]\s*[\"']?([A-Za-z0-9_+/.=-]{12,})", re.I
)


def obvious_placeholder(match: str) -> bool:
    payload = re.sub(
        r"^(?:gh[pousr]_|github_pat_|sk-(?:proj-|ant-)?|AKIA|ASIA|xox[baprs]-|"
        r"act_|GTM-|G-|AW-|UA-)", "", match
    )
    if "://" in payload:
        payload = payload.split("://", 1)[1].split(":", 1)[-1].rstrip("@")
    return placeholder(payload)


def sensitive_rules(text: str) -> set[str]:
    rules: set[str] = set()
    if any(not placeholder(match[1]) for match in WINDOWS_PATH.finditer(text)):
        rules.add("private-environment-path")
    for match in EMAIL.finditer(text) if "@" in text else ():
        domain = match[1].lower()
        if not any(domain == safe or domain.endswith("." + safe) for safe in (
            "example.com", "example.net", "example.org", "example.invalid", "example.test"
        )) and not domain.endswith((".invalid", ".test", ".example")):
            rules.add("personal-email")
    for match in PHONE.finditer(text):
        digits = re.sub(r"\D", "", match[0])
        if not placeholder(digits):
            rules.add("phone-number")
    for match in LABELED_PHONE.finditer(text):
        digits = re.sub(r"\D", "", match[1])
        if 8 <= len(digits) <= 15 and not placeholder(digits):
            rules.add("phone-number")
    if any(not obvious_placeholder(match[0]) for match in PRODUCTION_ID.finditer(text)):
        rules.add("production-id")
    for match in LABELED_ID.finditer(text):
        value = match[1]
        if re.search(r"\d", value) and not placeholder(value):
            rules.add("production-id")
    candidates = SECRET_PATTERNS if "://" in text and "@" in text else SECRET_PATTERNS[:-1]
    if any(not obvious_placeholder(match[0]) for pattern in candidates for match in pattern.finditer(text)):
        rules.add("secret-pattern")
    if any(not placeholder(match[1]) for match in SECRET_ASSIGNMENT.finditer(text)):
        rules.add("secret-assignment")
    return rules
