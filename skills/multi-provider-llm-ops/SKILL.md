---
name: multi-provider-llm-ops
description: Opera proveedores LLM (open-source y pago), enruta por manifiesto y configura fallback con runbooks.
---

# Multi Provider LLM Ops

## Objetivo
Operar y endurecer conectividad con múltiples proveedores: Ollama/OpenAI/Anthropic/OpenAI-compatible.

## Flujo
1. Inspeccionar `/api/providers`.
2. Validar variables críticas (`.env`).
3. Ajustar `provider_preference` en manifests.
4. Configurar `NUVO_LLM_FALLBACKS` por criticidad.

## Runbook rápido
- Si proveedor cae, fallback automático.
- Si hay timeout recurrente, bajar temperatura/modelo y aumentar timeout.
