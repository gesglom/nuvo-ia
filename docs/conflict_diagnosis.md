# Diagnóstico de conflictos persistentes en PR

Si en GitHub siguen apareciendo conflictos aun cuando localmente no hay marcadores `<<<<<<<`, normalmente la causa es **divergencia con la rama target** (por ejemplo `main`) y no un conflicto sin resolver en el árbol local.

## Qué validar

1. No haya marcadores de conflicto en archivos críticos (`agent_loop.py`, `core/agent_evolution.py`, `core/job_queue.py`, `scripts/test_runtime.py`).
2. Qué archivos cambiaste desde el merge-base.
3. Qué archivos cambió la rama target desde ese mismo merge-base.
4. Intersección de ambos conjuntos (zona probable de conflicto en PR).

## Script agregado

- `scripts/diagnose_merge_conflicts.py`

Uso:

```bash
python scripts/diagnose_merge_conflicts.py
```

Opcional (rama target distinta):

```bash
NUVO_TARGET_BRANCH=master python scripts/diagnose_merge_conflicts.py
```

## Nota

Si la rama target no existe localmente, el script lo reporta y sugiere hacer fetch/rebase o merge con la rama remota antes de abrir/actualizar PR.
