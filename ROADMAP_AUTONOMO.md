# Roadmap inmediato para fábrica de software autónoma

## Fases implementadas ✅
1. **Ejecución de tareas estructuradas**
   - `core/task_contract.py` define `TaskContract` con `id`, `owner_agent`, `input`, `expected_output`, `status`, `retries`, timestamps y trazas de salida/error.

2. **Persistencia de jobs**
   - `core/job_queue.py` implementa cola persistente (`memory/jobs.json`) con creación, consulta, selección de siguiente tarea y actualización de estado.
   - `agent_loop.py` ya ejecuta sobre jobs, no solo en memoria.

3. **Observabilidad**
   - `core/metrics_manager.py` registra latencia/estado/proveedor por ejecución y entrega resumen agregado.

4. **Automejora supervisada**
   - `core/self_improvement.py` guarda feedback de fallos y sugerencias de mejora para prompts/ejecución.

5. **Seguridad de herramientas**
   - `core/tool_policy.py` define política de paths y comandos bloqueados.
   - `tools/file_writer.py` aplica enforcement de escritura segura.

## Estado del ecosistema actual
- `BaseAgent` como contrato unificado.
- `agent_manifest` con esquema estricto y persistente.
- `context_manager` para contexto compartido entre agentes.
- Hot-loading de agentes dinámicos.
- `AgentCreatorAgent` con creación física de especialistas y logging de evolución.
- Router de proveedor por manifiesto + fallback chain (`core/provider_router.py`).
- Soporte de proveedor OpenAI-compatible para conectar IAs open source/comerciales bajo API estándar.

## Siguiente bloque (fase de escalado)
1. **Scheduler con prioridades y concurrencia por agente**.
2. **Ejecución distribuida (workers)** para pipelines largos.
3. **Métricas de coste real** por proveedor/modelo con presupuesto por job.
4. **Tests de regresión por rol de agente** antes de marcar tarea como `done`.
5. **Panel web de operaciones** para jobs/metrics/self-improvement en tiempo real.


## Evolución avanzada iniciada (memoria + evolución de agentes)
- Se añadió `core/memory_fabric.py` como capa unificada de memoria con modo `local` y modo `engram` (`NUVO_MEMORY_PROVIDER=engram` + `ENGRAM_API_URL`).
- El `agent_loop` ahora persiste episodios vía `store_episode()` para centralizar memoria operacional.
- Se añadió `core/agent_evolution.py` para generar ciclos de evolución basados en métricas + feedback y producir recomendaciones por agente (`memory/agent_evolution.json`).
