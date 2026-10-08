"""
SISTEMA DE APRENDIZAJE NO SUPERVISADO - TRANSPORTE MASIVO
Modelo: Técnicas de Agrupamiento / K-Means (Capítulo 16 - Palma Méndez, 2008)
"""

import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import os

# =====================================================================
# 1. GENERACIÓN DEL DATASET HISTÓRICO SIN ETIQUETAS (Punto 3 de la guía)
# =====================================================================
def generar_dataset_agrupamiento(filename="datos_agrupamiento.csv", num_muestras=500):
    """Genera datos históricos sin etiquetas para descubrir patrones ocultos."""
    np.random.seed(42)
    
    # Variables continuas: Tiempo de viaje e Intensidad de flujo de pasajeros
    tiempo_viaje = np.random.normal(loc=25, scale=10, size=num_muestras).clip(5, 60)
    pasajeros_flujo = np.random.normal(loc=150, scale=60, size=num_muestras).clip(10, 300)
    
    df = pd.DataFrame({
        'Tiempo_Viaje_Min': np.round(tiempo_viaje, 1),
        'Flujo_Pasajeros_Min': np.round(pasajeros_flujo, 0).astype(int)
    })
    
    df.to_csv(filename, index=False)
    print(f"[Info] Dataset de agrupamiento generado exitosamente como '{filename}'.")

# =====================================================================
# 2. ENTRENAMIENTO DEL MODELO - K-MEANS CLUSTERING (Punto 4 de la guía)
# =====================================================================
def entrenar_clustering(filename="datos_agrupamiento.csv"):
    if not os.path.exists(filename):
        generar_dataset_agrupamiento(filename)
        
    df = pd.read_csv(filename)
    
    # En clustering es indispensable estandarizar las magnitudes de escala
    escalador = StandardScaler()
    datos_escalados = escalador.fit_transform(df)
    
    # Instanciar K-Means para segmentar en 3 estados operativos de tráfico
    kmeans = KMeans(n_clusters=3, random_state=42, n_init=10)
    df['Cluster_Estado'] = kmeans.fit_predict(datos_escalados)
    
    print("\n" + "="*50)
    print("   RESULTADOS DEL CLUSTERING (MÉTODO NO SUPERVISADO)")
    print("="*50)
    
    # Extracción de centroides para interpretar el significado de cada grupo
    resumen = df.groupby('Cluster_Estado').mean()
    print("Centroides de los clústeres calculados por distancia Euclidea:")
    print(resumen)
    print("\nInterpretación sugerida de los grupos:")
    print(" -> Tráfico Fluido  (Bajo tiempo, pocos pasajeros)")
    print(" -> Tráfico Moderado (Tiempos y pasajeros en rangos medios)")
    print(" -> Tráfico Crítico  (Tiempos elevados y alta densidad de usuarios)")
    print("="*50)
    
    # Exportar el resultado segmentado de la base de datos
    df.to_csv("datos_segmentados.csv", index=False)
    return kmeans, escalador

# =====================================================================
# 3. INTERFAZ INTERACTIVA DE PRUEBA EN VIVO
# =====================================================================
if __name__ == "__main__":
    modelo, escalador_sistema = entrenar_clustering()
    
    print("\n" + "*"*40)
    print("  PRUEBA OPERATIVA EN VIVO - NO SUPERVISADA")
    print("*"*40)
    print("Ingrese métricas actuales para agrupar el estado del tramo:")
    
    try:
        t_viaje = float(input("Tiempo actual detectado en el tramo (minutos): "))
        p_flujo = int(input("Cantidad de pasajeros ingresando por minuto: "))
        
        # Predicción del clúster más cercano
        nuevo_dato = escalador_sistema.transform([[t_viaje, p_flujo]])
        grupo_asignado = modelo.predict(nuevo_dato)
        
        print("\n" + "-"*40)
        print(f"📍 El algoritmo K-Means asignó esta muestra al CLUSTER: {grupo_asignado[0]}")
        print("👉 Inferencia: La situación ha sido agrupada según la similitud geométrica")
        print("   con los patrones históricos analizados.")
        print("-"*40)
    except ValueError:
        print("[Error] Ingrese valores numéricos válidos en la consola.")

        input("\n[Pausa del Sistema] Presione ENTER para salir...")
