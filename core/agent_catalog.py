from typing import Iterable, List, Optional

# Canonical names aligned with modules in /agents.
CANONICAL_ALIASES = {
    "architect_agent": ["architect_agent", "arquitecto", "agente_arquitecto", "arquitecto_software"],
    "backend_engineer": ["backend_engineer", "ingeniero_backend", "backend", "desarrollador_backend"],
    "frontend_engineer": ["frontend_engineer", "ingeniero_frontend", "frontend", "desarrollador_frontend"],
    "security_auditor": ["security_auditor", "auditor_seguridad", "security", "auditor"],
    "agent_creator": ["agent_creator", "creador_agentes", "agente_creador", "creador_de_agentes"],
    "orchestrator_agent": ["orchestrator_agent", "orquestador", "agente_orquestador"],
    "planner_agent": ["planner_agent", "planificador", "agente_planificador"],
    "developer_agent": ["developer_agent", "desarrollador", "ingeniero_desarrollo"],
    "reviewer_agent": ["reviewer_agent", "revisor", "code_reviewer"],
    "tester_agent": ["tester_agent", "qa", "probador", "agente_qa"],
    "refactor_agent": ["refactor_agent", "refactor", "agente_refactor"],
    "git_agent": ["git_agent", "agente_git", "versionador"],
    "devops_agent": ["devops_agent", "devops", "agente_devops"],
    "monitoring_agent": ["monitoring_agent", "monitor", "agente_monitoreo"],
    "self_improvement_agent": ["self_improvement_agent", "auto_mejora", "agente_automejora"],
    "repository_engineer_agent": ["repository_engineer_agent", "ingeniero_repositorio", "repo_engineer"],
}

ALIAS_TO_CANONICAL = {
    alias.strip().lower(): canonical
    for canonical, aliases in CANONICAL_ALIASES.items()
    for alias in aliases
}


def canonical_agent_name(name: Optional[str]) -> Optional[str]:
    if not name:
        return None
    raw = str(name).strip().lower()
    if raw in CANONICAL_ALIASES:
        return raw
    return ALIAS_TO_CANONICAL.get(raw, raw)


def dedupe_agent_plan(agent_names: Iterable[str]) -> List[str]:
    seen = set()
    normalized: List[str] = []
    for name in agent_names:
        canonical = canonical_agent_name(name)
        if not canonical or canonical in seen:
            continue
        seen.add(canonical)
        normalized.append(canonical)
    return normalized
