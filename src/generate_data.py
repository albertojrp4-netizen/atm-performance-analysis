import pandas as pd
import random
from datetime import datetime, timedelta
import os

print("🛫 Generando datos de vuelos...")

# Aeropuertos españoles
airports = ['MAD', 'BCN', 'AGP', 'PMI', 'LPA', 'TFN', 'ALC', 'SVQ', 'VLC', 'BIO']
airlines = ['IBE', 'RYR', 'VLG', 'ANE', 'DLH']

# Coordenadas
coords = {
    'MAD': (40.49, -3.57), 'BCN': (41.30, 2.08), 'AGP': (36.67, -4.50),
    'PMI': (39.55, 2.73), 'LPA': (27.93, -15.39), 'TFN': (28.48, -16.34),
    'ALC': (38.28, -0.56), 'SVQ': (37.42, -5.89), 'VLC': (39.49, -0.48),
    'BIO': (43.30, -2.91)
}

# Generar 50000 vuelos
flights = []
fecha_fin = datetime.now()
fecha_ini = fecha_fin - timedelta(days=30)

for i in range(50000):
    if i % 10000 == 0:
        print(f"  Procesados {i} vuelos...")
    
    origen = random.choice(airports)
    destino = random.choice([a for a in airports if a != origen])
    
    # Fecha aleatoria
    dias = random.randint(0, 30)
    hora = random.randint(0, 23)
    minuto = random.randint(0, 59)
    fecha_salida = fecha_fin - timedelta(days=dias)
    fecha_salida = fecha_salida.replace(hour=hora, minute=minuto, second=0)
    
    # Retraso
    if random.random() < 0.25:
        retraso = random.randint(15, 120)
    elif random.random() < 0.35:
        retraso = random.randint(-15, -1)
    else:
        retraso = random.randint(-5, 14)
    
    duracion = random.randint(45, 150)
    
    vuelo = {
        'vuelo_id': f"{random.choice(airlines)}{random.randint(100,999)}",
        'aerolinea': random.choice(airlines),
        'origen': origen,
        'origen_lat': coords[origen][0],
        'origen_lon': coords[origen][1],
        'destino': destino,
        'destino_lat': coords[destino][0],
        'destino_lon': coords[destino][1],
        'fecha_salida': fecha_salida,
        'retraso_min': retraso,
        'duracion_min': duracion,
        'pasajeros': random.randint(50, 200)
    }
    flights.append(vuelo)

# Crear DataFrame
df = pd.DataFrame(flights)

# Guardar
os.makedirs('data/raw', exist_ok=True)
df.to_csv('data/raw/vuelos.csv', index=False)

print(f"\n✅ Generados {len(df)} vuelos")
print(f"📁 Guardado en: data/raw/vuelos.csv")
print("\n📊 Primeros 5 registros:")
print(df.head())
