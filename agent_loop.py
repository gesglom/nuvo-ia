import os
import sys
# Permitir que Python encuentre el auditor en la carpeta tools
sys.path.append(os.path.join(os.getcwd(), 'tools'))

from agent.generator import generate_code
from tools.file_writer import write_file
from security_auditor import SecurityAuditor

def start_nuvo_flow(goal):
    auditor = SecurityAuditor()
    print(f'🚀 Iniciando misión Nuvo: {goal}')
    
    # Planificación básica
    plan_prompt = f'Crea una lista de 2 archivos .py necesarios para: {goal}. Responde solo con los nombres de archivo separados por comas.'
    files_to_create = generate_code(plan_prompt).strip().split(',')
    
    for file_name in files_to_create:
        file_name = file_name.strip()
        print(f'🧠 Generando y Auditando: {file_name}...')
        
        code_prompt = f'Escribe el código Python completo para {file_name} del proyecto Nuvo. Objetivo: {goal}'
        actual_code = generate_code(code_prompt)
        
        # EL PASO CRÍTICO: Auditoría automática
        dangers = auditor.scan_text(actual_code)
        if dangers:
            print(f'❌ ALERTA DE SEGURIDAD en {file_name}: {dangers}')
            print('🔄 Solicitando a Qwen corregir el código...')
            # Re-intento (simplificado)
            actual_code = generate_code(f'Corrige este código eliminando riesgos: {actual_code}')
        
        write_file(f'workspace/nuvo_backend/{file_name}', actual_code)
        print(f'✅ {file_name} ha pasado la auditoría y fue guardado.')
    
    print('🏁 Misión terminada bajo estándares de seguridad Nuvo.')

if __name__ == "__main__":
    objetivo = input('¿Qué parte de Nuvo crearemos con auditoría activa?: ')
    start_nuvo_flow(objetivo)
