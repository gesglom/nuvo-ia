# Software Factory Architecture (Incremental Evolution Plan)

## Architectural Principles

1. Build on existing Nuvo modules (no rewrite).
2. Keep runtime backward-compatible.
3. Separate control-plane abstractions from agent implementations.
4. Standardize memory/event/task interfaces.
5. Keep agents plugin-compatible and dynamically registerable.

## Target Core System

### 1) Agent Registry
- Dynamic registration and lookup by capability tags.
- Supports built-in and plugin agents.
- Source of truth for orchestrator routing decisions.

### 2) Tool Registry
- Tool discovery and capability declaration.
- Policy checks before execution.
- Unified invocation protocol.

### 3) Task Queue
- Unified API abstracting current file queue and future distributed queue.
- Priority-aware dispatch and lifecycle transitions.

### 4) Event Bus
- Publish/subscribe for lifecycle signals:
  - `goal.received`
  - `task.created`
  - `task.started`
  - `task.completed`
  - `task.failed`
  - `improvement.proposed`

### 5) Execution Manager
- Coordinates agent execution, retries, timeout, and event emission.
- Integrates memory adapter and metrics.

### 6) Git Integration
- Standardized git tools for status/add/commit/push/branch info.
- Enables agent-driven commits and PR preparation.

### 7) Plugin System
- Drop-in agents/tools loaded dynamically.
- Capability metadata in manifests.

## Agent Topology

- **Orchestrator Agent**: end-to-end SDLC control loop.
- **Planner Agent**: decomposes goals into executable tasks.
- **Developer Agent**: implements features/fixes.
- **Reviewer Agent**: reviews diffs and design consistency.
- **Tester Agent**: test strategy + execution recommendations.
- **Refactor Agent**: improves structure/maintainability.
- **Git Agent**: stages, commits, branch/push operations.
- **DevOps Agent**: deployment and rollback procedures.
- **Monitoring Agent**: runtime health and anomalies.
- **Self-Improvement Agent**: system-level optimization proposals.
- **Repository Engineer Agent**: repository intelligence + issue-driven execution.

## Memory Architecture (Engram-centric)

All memory operations go through `core/memory_adapter.py`.

Typed operations:
- `store_agent_knowledge`
- `retrieve_relevant_memories`
- `save_architectural_decision`
- `persist_system_improvement`
- `store_repository_insight`

Provider strategy:
- Primary: Engram provider (configured via `ENGRAM_*` env vars).
- Safe fallback: local memory fabric adapter (non-breaking continuity).

## Autonomous Development Loop

`goal -> planning -> implementation -> testing -> review -> commit -> deployment -> monitoring -> improvement`

Execution strategy:
1. Orchestrator creates loop plan.
2. Task queue stores atomic tasks.
3. Event bus emits lifecycle events.
4. Specialized agents execute by phase.
5. Memory adapter records outcomes and decisions.
6. Git agent commits approved changes.
7. Self-improvement agent proposes next optimizations.

## Repository Intelligence

`tools/repo_analyzer.py` provides:
- project structure map,
- dependency hints,
- module inventory,
- test gap detection,
- technical debt signals.

`tools/repo_knowledge_ingestion.py` provides:
- external repository ingestion,
- architecture/component extraction,
- memory persistence of reusable insights.

## Incremental Rollout

- **Phase 1 (implemented in this change set)**: core framework abstractions, memory adapter, new agent set, tooling foundations.
- **Phase 2**: route existing `agent_loop` through execution manager + event bus.
- **Phase 3**: optional distributed queue backend.
- **Phase 4**: policy engine and deeper deployment automation.
