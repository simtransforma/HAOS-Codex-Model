"""Rebuild the declarative catalog from real frontmatters; never run a skill."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import re

try:
    from .model_frontmatter import frontmatter
except ImportError:
    from model_frontmatter import frontmatter


# Domain-specific assignments precede broader terms. Every imported skill has
# at least one accountable specialist, not a broadcast to all agents.
SPECIALTIES = (
    (r"security|seguran|ticketing|ffuf|privacy|credentials", ("security-reviewer", "compliance-officer")),
    (r"test|quality|claim-verification|auditor|review", ("qa-reviewer", "auditor-confianca")),
    (r"cashflow|economics|margem|receita|cfo|orcamento|finance|bling|yampi", ("cfo",)),
    (r"meta-ads|tiktok-ads|google-ads|ads-copy|ad-creative|ads$|traffic", ("media-buyer", "traffic-master")),
    (r"tracking|capi|gtm|ga4|analytics", ("tracking-engineer", "data-analyst")),
    (r"tiktok-bi|data-|dash|metrics|saga|schema", ("data-analyst", "bi-engineer")),
    (r"email|mautic", ("email-marketer", "automation-engineer")),
    (r"clint|prospect|churn|crm|lia-api|evolution|whatsapp|contatos", ("crm-specialist",)),
    (r"n8n|typebot|flow|automati|curseduca", ("automation-engineer",)),
    (r"backup|cloudflare|google-cloud|deploy|vercel|openclaw|runtimes|manutencao", ("devops",)),
    (r"react|frontend|composition|mobile", ("dev-frontend",)),
    (r"fullstack|software|api|supabase|openapi", ("dev-backend",)),
    (r"design|impeccable|hero-visual|vibe", ("designer", "dev-frontend")),
    (r"video|youtube|transcre|interpretar", ("videomaker", "content-strategist")),
    (r"instagram|carousel|social|trend|outlier|community", ("sm-social", "relacionamento-editorial")),
    (r"copy|escrita|lisa|prompt|ralph", ("copy-specialist",)),
    (r"funnel|cro|landing|lead-magnet|page-analyst", ("funnel-architect", "ux-researcher")),
    (r"product|prd|customer-research|feedback", ("product-manager", "ux-researcher")),
    (r"marketing|launch|amazon|tiktok-shop|seo", ("cmo", "content-strategist")),
    (r"memory|mem|obsidian|brain|json-canvas|mega", ("oraculo", "pesquisador")),
    (r"research|source|query|rag|pdf|last30|second-opinion|benchmark", ("pesquisador",)),
    (r"session|handoff|dump|artifact|project|sprint|long-running|token", ("project-manager",)),
    (r"haos-|skill-|find-skills|incorporador", ("estrategista-chefe", "project-manager")),
)


def rebuild(root: Path) -> tuple[dict, dict[str, str]]:
    path = root / ".codex/skill-routing.json"
    data = json.loads(path.read_text(encoding="utf-8-sig"))
    catalog = {}
    for skill in sorted((root / ".agents/skills").iterdir()):
        if not skill.is_dir():
            continue
        metadata = frontmatter((skill / "SKILL.md").read_text(encoding="utf-8-sig"))
        if metadata["name"] != skill.name or not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", skill.name):
            raise ValueError("skill-folder-name")
        catalog[skill.name] = {"path": f".agents/skills/{skill.name}/SKILL.md", "description": metadata["description"]}
    previous = set(data["skills"])
    if not previous <= set(catalog):
        raise ValueError("routing-existing-skill-removed")
    data["skills"] = catalog
    agents = data["agents"]
    for identifier in sorted(catalog):
        if identifier in previous:
            continue
        owners = next((roles for pattern, roles in SPECIALTIES if re.search(pattern, identifier)), ("pesquisador",))
        for owner in owners:
            if owner not in agents:
                raise ValueError("routing-agent-missing")
            agents[owner]["skills"] = sorted(set(agents[owner]["skills"]) | {identifier})
    # Keep existing intent routes and add a bounded specialist entry per role.
    routes = [r for r in data["routes"] if not r["id"].startswith("specialist-")]
    output_agents = {}
    for identifier, entry in sorted(agents.items()):
        entry["skills"] = sorted(set(entry["skills"]))
        routes.append({"id": "specialist-" + identifier, "description": entry["description"],
                       "triggers": [identifier, entry["function"]], "agents": [identifier],
                       "skills": entry["skills"], "mode": "DELEGATE", "external_approval_required": False})
        agent_path = root / entry["path"]
        text = agent_path.read_text(encoding="utf-8-sig")
        start = text.index("Rotas relativas a raiz do repositorio:\n")
        end = text.index("A matriz declara capacidades;", start)
        text = text[:start] + "Rotas relativas a raiz do repositorio:\n" + "".join(
            "- " + catalog[skill]["path"] + "\n" for skill in entry["skills"]
        ) + text[end:]
        output_agents[entry["path"]] = text
    data["routes"] = routes
    return data, output_agents


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parent.parent)
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--search", help="Read compact metadata only; do not load procedure bodies")
    parser.add_argument("--limit", type=int, default=20)
    args = parser.parse_args()
    if args.search is not None:
        index = json.loads((args.root / "docs/skill-index.json").read_text(encoding="utf-8"))
        query = args.search.casefold()
        matches = [entry for entry in index["skills"] if query in (entry["name"] + " " + entry["description"]).casefold()]
        print(json.dumps({"total_matches": len(matches), "skills": matches[:max(1, args.limit)]}, ensure_ascii=True))
        return
    data, agents = rebuild(args.root)
    index = {"schema_version": 1, "skills": [{"name": name, **entry} for name, entry in data["skills"].items()]}
    files = {".codex/skill-routing.json": json.dumps(data, ensure_ascii=True, indent=2) + "\n",
             "docs/skill-index.json": json.dumps(index, ensure_ascii=True, separators=(",", ":")) + "\n", **agents}
    stale = []
    for name, text in files.items():
        path = args.root / name
        if not path.is_file() or path.read_text(encoding="utf-8-sig") != text:
            stale.append(name)
            if args.write:
                path.write_text(text, encoding="utf-8", newline="\n")
    if stale and not args.write:
        raise SystemExit("FAIL: routing-stale")
    print(f"PASS: {len(data['skills'])} real frontmatters; {len(agents)} specialist profiles; {len(stale)} changed")


if __name__ == "__main__":
    main()
