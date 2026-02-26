import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
import os

def generate_synthetic_flights(n_flights=50000):
    """
    Genera datos sintéticos de vuelos para desarrollo
    """
    np.random.seed(42)  # Para que los datos sean reproducibles
    
    # Aeropuertos españoles principales
    airports = {
        'MAD': {'lat': 40.4936, 'lon': -3.5668, 'city': 'Madrid'},
        'BCN': {'lat': 41.2971, 'lon': 2.0785, 'city': 'Barcelona'},
        'AGP': {'lat': 36.6749, 'lon': -4.4991, 'city': 'Málaga'},
        'PMI': {'lat': 39.5536, 'lon': 2.7278, 'city': 'Palma'},
        'LPA': {'lat': 27.9319, 'lon': -15.3866, 'city': 'Gran Canaria'},
        'TFN': {'lat': 28.4827, 'lon': -16.3415, 'city': 'Tenerife Norte'},
        'ALC': {'lat': 38.2822, 'lon': -0.5582, 'city': 'Alicante'},
        'SVQ': {'lat': 37.4180, 'lon': -5.8931, 'city': 'Sevilla'},
        'VLC': {'lat': 39.4893, 'lon': -0.4816, 'city': 'Valencia'},
        'BIO': {'lat': 43.3011, 'lon': -2.9106, 'city': 'Bilbao'}
    }
    
    # Generar fechas (últimos 30 días)
    end_date = datetime.now()
    start_date = end_date - timedelta(days=30)
    dates = pd.date_range(start_date, end_date, periods=n_flights)
    
    flights = []
    airlines = ['IBE', 'RYR', 'VLG', 'ANE', 'QTR', 'DLH', 'AFR']
    
    for i in range(n_flights):
        # Seleccionar origen y destino (diferentes)
        origin = random.choice(list(airports.keys()))
        dest = random.choice([a for a in airports.keys() if a != origin])
        
        # Hora de salida (con preferencia por horas pico) - AHORA SUMAN 1
        hour_probs = [
            0.02, 0.01, 0.01, 0.01, 0.02, 0.03,  # 0-5: 0.10
            0.05, 0.06, 0.07, 0.06, 0.05, 0.04,  # 6-11: 0.33
            0.05, 0.06, 0.07, 0.07, 0.06, 0.05,  # 12-17: 0.36
            0.04, 0.03, 0.02, 0.02, 0.01, 0.01   # 18-23: 0.13
        ]  # Total: 0.10 + 0.33 + 0.36 + 0.13 = 0.92? ¡Vamos a verificar!
        
        # Verificar y corregir la suma
        total = sum(hour_probs)
        if abs(total - 1.0) > 0.0001:
            print(f"Corrigiendo probabilidades: suma era {total}")
            # Ajustar para que sumen exactamente 1
            hour_probs = [p/total for p in hour_probs]
        
        hour = np.random.choice(range(24), p=hour_probs)
        
        scheduled_time = dates[i].replace(hour=int(hour))
        
        # Retraso (distribución realista)
        if np.random.random() < 0.2:  # 20% de vuelos con retraso significativo
            delay = np.random.exponential(30)  # Media 30 min
        else:
            delay = np.random.normal(0, 3)  # Pequeños adelantos/retrasos
        delay = max(-15, min(180, int(delay)))  # Limitar entre -15 y 180 min
        
        # Duración del vuelo (minutos) basada en distancia aleatoria
        distance = np.random.normal(500, 200)  # Distancia en km
        duration = max(30, int(distance / 800 * 60 + np.random.normal(0, 10)))
        
        # Determinar estado del vuelo basado en retraso
        if delay > 15:
            status = 'delayed'
        elif delay >= -5:
            status = 'on_time'
        else:
            status = 'early'
        
        flight = {
            'flight_id': f"{random.choice(airlines)}{random.randint(100, 999)}",
            'airline': random.choice(airlines),
            'origin': origin,
            'origin_lat': airports[origin]['lat'],
            'origin_lon': airports[origin]['lon'],
            'destination': dest,
            'dest_lat': airports[dest]['lat'],
            'dest_lon': airports[dest]['lon'],
            'scheduled_departure': scheduled_time,
            'actual_departure': scheduled_time + timedelta(minutes=delay),
            'delay_minutes': delay,
            'scheduled_arrival': scheduled_time + timedelta(minutes=duration),
            'flight_duration_minutes': duration,
            'status': status,
            'passengers': np.random.randint(50, 200),
            'weather_conditions': np.random.choice(['good', 'fair', 'poor'], 
                                                  p=[0.7, 0.2, 0.1])
        }
        flights.append(flight)
    
    df = pd.DataFrame(flights)
    return df

if __name__ == "__main__":
    print("🛫 Generando datos sintéticos de vuelos...")
    print("⏱️  Esto puede tomar unos segundos...")
    
    # Generar datos
    df = generate_synthetic_flights(50000)
    
    # Crear carpeta data/raw si no existe
    os.makedirs('data/raw', exist_ok=True)
    
    # Guardar en CSV
    output_file = 'data/raw/synthetic_flights.csv'
    df.to_csv(output_file, index=False)
    
    # Mostrar resultados
    print(f"✅ ¡Completado! Se generaron {len(df):,} vuelos")
    print(f"📁 Archivo guardado en: {output_file}")
    print("\n📋 Primeros 5 registros:")
    print(df.head())
    print("\n📊 Estadísticas básicas:")
    print(df[['delay_minutes', 'flight_duration_minutes', 'passengers']].describe())
    print(f"\n📅 Rango de fechas: {df['scheduled_departure'].min()} a {df['scheduled_departure'].max()}")
    
    # Mostrar distribución por aerolínea
    print("\n✈️  Vuelos por aerolínea:")
    print(df['airline'].value_counts())
    
    # Mostrar distribución por estado
    print("\n📊 Estado de los vuelos:")
    print(df['status'].value_counts(normalize=True).mul(100).round(1).astype(str) + '%')
