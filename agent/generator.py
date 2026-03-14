import requests
def generate_code(prompt: str):
    url = 'http://localhost:11434/api/generate'
    payload = {
        'model': 'qwen2.5-coder:7b',
        'prompt': f'Actúa como el desarrollador de Nuvo. Escribe solo código Python puro, sin markdown ni explicaciones: {prompt}',
        'stream': False
    }
    try:
        response = requests.post(url, json=payload)
        return response.json().get('response', '')
    except Exception as e:
        return f'Error: {str(e)}'
