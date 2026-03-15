---
name: autonomous-factory-architect
description: Diseña y evoluciona la arquitectura de fábrica autónoma (task runtime, planner, workers, fallback y auto-mejora).
---

# Autonomous Factory Architect

## Objetivo
Definir arquitectura de referencia para una fábrica de software multi-agente, agnóstica a proveedor y con mejora continua.

## Checklist
1. Definir `TaskContract` y ciclo de estados.
2. Validar `job_queue` persistente y estrategia de retries.
3. Verificar recuperación autónoma mediante agente especialista.
4. Proponer siguiente fase (scheduler, workers, budgeting).

## Entregables
- Diagrama lógico (texto) de componentes.
- Plan por fases (MVP -> Escala).
