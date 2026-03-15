# Metodología moderna para la fábrica de software autónoma

## Framework recomendado
- **Product Discovery continuo** (outcome-driven).
- **Trunk-Based Development** con feature flags.
- **CI/CD + Quality Gates** (lint, tests, smoke e2e de agentes).
- **Arquitectura evolutiva con ADRs** (Architecture Decision Records).
- **SRE-lite** con SLOs y error budgets para jobs/agentes.

## Flujo operativo
1. Definir objetivo de negocio y KPIs.
2. Traducir objetivo a `TaskContract` por job.
3. Ejecutar en runtime con retries/timeouts/fallback.
4. Medir (`metrics`) y aprender (`self_improvement`).
5. Ajustar prompts/manifiestos/providers en iteraciones cortas.

## Estándares técnicos
- Todo agente hereda de `BaseAgent`.
- Toda invocación LLM pasa por router multi-proveedor.
- Todo cambio incluye prueba de humo de agentes y runtime.
- Seguridad por policy para tools (rutas/comandos).

## Definition of Done
- Job ejecutable end-to-end desde frontend/API.
- Métricas registradas.
- Logs de fallos y sugerencias de mejora.
- Riesgos de seguridad verificados.
