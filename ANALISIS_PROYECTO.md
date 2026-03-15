# Revisión del proyecto Nuvo IA

## Estado actual

El proyecto ya tiene una base funcional de orquestación por agentes, pero estaba acoplado principalmente a Ollama en varios archivos.

## Mejoras aplicadas

1. **Cliente LLM unificado (`core/llm_client.py`)**
   - Soporte para múltiples proveedores:
     - `ollama`
     - `openai`
     - `anthropic`
   - Selección por variable de entorno `NUVO_LLM_PROVIDER`.
   - Manejo consistente de errores de red y configuración.

2. **Desacople de proveedor en agentes/orquestador**
   - `nuvo_orchestrator.py`, `agents/backend_engineer.py`, `agents/agent_creator.py` ahora usan `ask_llm()` común.

3. **Compatibilidad hacia atrás**
   - `core/ollama_client.py` se mantiene como wrapper de `ask_llm`.

4. **Corrección de carga de agentes**
   - `frontend_engineer.py` ahora expone `FrontendEngineerAgent` con método `execute`.
   - `security_auditor.py` ahora expone `SecurityAuditorAgent` (antes no lo detectaba `agent_loader`).

5. **Corrección de flujo de auditoría**
   - `agent_loop.py` importaba `security_auditor` desde una ruta inválida.
   - Ahora importa desde `agents.security_auditor`.

## Recomendaciones siguientes

1. Crear una capa de **router por tarea** para escoger proveedor por tipo de trabajo (arquitectura, código, QA).
2. Agregar **fallback automático** (ej.: OpenAI -> Ollama local) ante timeout o cuota.
3. Incluir **trazabilidad por proveedor** en memoria (`coste`, `latencia`, `éxito`).
4. Añadir pruebas unitarias para:
   - `core/llm_client.py`
   - `core/agent_loader.py`
   - contratos de `execute()` por agente.
5. Incorporar un archivo `.env.example` documentando variables de cada proveedor.

## Variables de entorno recomendadas

- `NUVO_LLM_PROVIDER=ollama|openai|anthropic`
- `NUVO_LLM_TIMEOUT=120`
- `OLLAMA_URL=http://localhost:11434/api/generate`
- `OLLAMA_MODEL=qwen2.5-coder:7b`
- `OPENAI_API_KEY=...`
- `OPENAI_MODEL=gpt-4o-mini`
- `OPENAI_BASE_URL=https://api.openai.com/v1`
- `ANTHROPIC_API_KEY=...`
- `ANTHROPIC_MODEL=claude-3-5-haiku-latest`
