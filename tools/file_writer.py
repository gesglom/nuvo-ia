import os

from core.tool_policy import enforce_write_path


def write_file(file_path, content):
    enforce_write_path(file_path)
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f'✅ Archivo creado: {file_path}')
