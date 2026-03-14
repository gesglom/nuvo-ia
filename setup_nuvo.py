import os
folders = ['agent', 'tools', 'memory', 'project_index', 'workspace/nuvo_backend', 'api']
for f in folders: 
    os.makedirs(f, exist_ok=True)
files = {'memory/agent_memory.json': '{}', 'memory/task_history.json': '{\"history\": []}'}
for p, c in files.items():
    if not os.path.exists(p):
        with open(p, 'w') as f: f.write(c)
print('🚀 Infraestructura de Nuvo lista.')
