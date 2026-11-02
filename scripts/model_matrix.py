"""Checks for the declarative skill-routing v1 contract (not a runtime)."""

from __future__ import annotations

from collections.abc import Callable
import re


IDENTIFIER = re.compile(r"[a-z0-9]+(?:-[a-z0-9]+)*\Z")
ROOT_FIELDS = {
    "schema_version", "description", "recommendation_only", "path_base", "defaults",
    "skills", "agents", "routes", "council", "entrypoints", "capabilities",
}


def validate_matrix(
    data: dict,
    agents: set[str],
    skills: set[str],
    check_path: Callable[[str], bool],
) -> set[str]:
    rules: set[str] = set()

    def require(condition: bool, rule: str = "matrix-schema") -> None:
        if not condition:
            rules.add(rule)

    def text(value: object) -> bool:
        return isinstance(value, str) and bool(value.strip())

    def fields(value: object, names: set[str]) -> bool:
        valid = isinstance(value, dict) and set(value) == names
        require(valid)
        return valid

    def strings(value: object, *, nonempty: bool = False) -> bool:
        valid = isinstance(value, list) and (not nonempty or bool(value))
        valid = valid and all(text(item) for item in value)
        require(bool(valid))
        if valid:
            require(len(value) == len(set(value)), "matrix-duplicate-reference")
        return bool(valid)

    def references(value: object, known: set[str], rule: str, *, nonempty: bool = False) -> None:
        if strings(value, nonempty=nonempty):
            require(set(value) <= known, rule)

    def path(value: object, expected: str) -> None:
        if not isinstance(value, str):
            require(False)
            return
        safe = bool(value) and not (
            value.startswith(("/", "~")) or "\\" in value or ":" in value
            or any(part in {"", ".", ".."} for part in value.split("/"))
        )
        require(safe, "matrix-path-unsafe")
        require(value == expected, "matrix-path-mismatch")
        if safe:
            check_path(value)

    require(set(data) == ROOT_FIELDS)
    require(type(data.get("schema_version")) is int and data["schema_version"] == 1)
    require(text(data.get("description")))
    require(data.get("recommendation_only") is True)
    require(data.get("path_base") == "repository-root")
    defaults = data.get("defaults")
    if fields(defaults, {"effort", "max_parallel_agents", "max_correction_cycles"}):
        require(defaults["effort"] in ("high", "xhigh", "max", "ultra"))
        for key in ("max_parallel_agents", "max_correction_cycles"):
            require(type(defaults[key]) is int and 1 <= defaults[key] <= 3)

    for key, known, prefix, suffix, entry_fields in (
        ("skills", skills, ".agents/skills/", "/SKILL.md", {"path", "description"}),
        ("agents", agents, ".codex/agents/", ".toml", {"path", "description", "skills", "function"}),
    ):
        catalog = data.get(key)
        if not isinstance(catalog, dict):
            require(False)
            continue
        require(bool(catalog))
        require(set(catalog) == known, "matrix-" + key + "-coverage")
        for identifier, entry in catalog.items():
            require(bool(IDENTIFIER.fullmatch(identifier)), "matrix-id")
            if not fields(entry, entry_fields):
                continue
            require(text(entry["description"]))
            path(entry["path"], prefix + identifier + suffix)
            if key == "agents":
                require(text(entry["function"]))
                references(entry["skills"], skills, "matrix-skill-reference")

    routes = data.get("routes")
    if not isinstance(routes, list) or not routes:
        require(False)
    else:
        seen = set()
        for route in routes:
            if not fields(route, {"id", "description", "triggers", "agents", "skills", "mode", "external_approval_required"}):
                continue
            identifier = route["id"]
            if isinstance(identifier, str):
                require(bool(IDENTIFIER.fullmatch(identifier)), "matrix-id")
                require(identifier.casefold() not in seen, "matrix-duplicate-route-id")
                seen.add(identifier.casefold())
            else:
                require(False, "matrix-id")
            require(text(route["description"]))
            strings(route["triggers"], nonempty=True)
            references(route["agents"], agents, "matrix-agent-reference")
            references(route["skills"], skills, "matrix-skill-reference")
            require(route["mode"] in ("DIRECT", "DELEGATE", "READ_ONLY", "AUDIT", "GATED"))
            require(type(route["external_approval_required"]) is bool)

    council = data.get("council")
    if fields(council, {"agents", "financial_agent", "financial_when"}):
        references(council["agents"], agents, "matrix-agent-reference", nonempty=True)
        require(isinstance(council["financial_agent"], str) and council["financial_agent"] in agents, "matrix-agent-reference")
        require(text(council["financial_when"]))

    entrypoints = data.get("entrypoints")
    if not isinstance(entrypoints, dict) or not entrypoints:
        require(False)
    else:
        for identifier, entry in entrypoints.items():
            if fields(entry, {"skill", "description"}):
                require(identifier in skills and entry["skill"] == identifier, "matrix-entrypoint-reference")
                require(text(entry["description"]))

    capabilities = data.get("capabilities")
    if fields(capabilities, {"included", "adapted", "optional_dependencies", "excluded"}):
        for value in capabilities.values():
            strings(value)
    return rules
