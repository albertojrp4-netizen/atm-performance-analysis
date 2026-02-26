import json
import pandas as pd

# Intentar leer el notebook dañado
try:
    with open('notebooks/01_analisis_exploratorio.ipynb', 'r', encoding='utf-8') as f:
        notebook = json.load(f)
    
    print("📝 Código recuperado del notebook:")
    print("="*50)
    
    for i, cell in enumerate(notebook['cells']):
        if cell['cell_type'] == 'code':
            print(f"\n--- Celda {i+1} ---")
            print(''.join(cell['source']))
            
except Exception as e:
    print(f"Error al leer: {e}")
    print("\n📝 Aquí tienes el código que deberías tener:")
