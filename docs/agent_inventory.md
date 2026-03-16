# Agent Inventory and Duplicate-Alias Review

## Existing canonical agents in repository

- `agent_creator`
- `architect_agent`
- `backend_engineer`
- `frontend_engineer`
- `security_auditor`
- `orchestrator_agent`
- `planner_agent`
- `developer_agent`
- `reviewer_agent`
- `tester_agent`
- `refactor_agent`
- `git_agent`
- `devops_agent`
- `monitoring_agent`
- `self_improvement_agent`
- `repository_engineer_agent`

## Duplicate risk identified

There is naming risk between Spanish and English variants (for example `arquitecto` vs `architect_agent`, `qa` vs `tester_agent`, `desarrollador` vs `developer_agent`).

Even when not duplicated as files, the planner can produce aliases that cause semantic repetition in execution plans.

## Mitigation implemented

- Added `core/agent_catalog.py` with canonical alias mapping.
- Added `canonical_agent_name()` and `dedupe_agent_plan()`.
- Integrated plan normalization/deduplication in `agent_loop._build_tasks()` and filtered to currently loaded agents.

This prevents repeated execution of equivalent roles and avoids unknown alias names becoming runnable tasks.
