"""
SISTEMA DE APRENDIZAJE SUPERVISADO - TRANSPORTE MASIVO
Modelo: Árboles de Decisión y Reglas de Decisión (Palma Méndez, 2008)
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier, export_text
from sklearn.metrics import accuracy_score, classification_report
import os

# =====================================================================
# 1. IDENTIFICACIÓN Y GENERACIÓN DEL DATASET (Punto 1 de la guía)
# =====================================================================
def generar_dataset_sintetico(filename="datos_transporte.csv", num_muestras=1000):
    """Genera una muestra histórica de datos de transporte masivo."""
    np.random.seed(42)
    
    hora_pico = np.random.choice([0, 1], size=num_muestras, p=[0.6, 0.4])
    dia_semana = np.random.randint(0, 7, size=num_muestras)
    clima = np.random.choice([0, 1], size=num_muestras, p=[0.7, 0.3]) # 1 = Lluvia
    estado_via = np.random.choice([0, 1], size=num_muestras, p=[0.85, 0.15]) # 1 = Bloqueo
    pasajeros = np.random.choice([0, 1, 2], size=num_muestras, p=[0.3, 0.5, 0.2]) # Ocupación
    
    # Regla lógica subyacente que el árbol debe aprender de los datos:
    # Habrá retraso alto si hay bloqueo, o si combina hora pico con lluvia u ocupación alta.
    retraso_alto = []
    for i in range(num_muestras):
        if estado_via[i] == 1:
            retraso_alto.append(1)
        elif hora_pico[i] == 1 and (clima[i] == 1 or pasajeros[i] == 2):
            retraso_alto.append(1)
        else:
            retraso_alto.append(0)
            
    df = pd.DataFrame({
        'Hora_Pico': hora_pico,
        'Dia_Semana': dia_semana,
        'Clima_Lluvia': clima,
        'Bloqueo_Via': estado_via,
        'Ocupacion_Estacion': pasajeros,
        'Retraso_Alto': retraso_alto
    })
    
    df.to_csv(filename, index=False)
    print(f"[Info] Dataset generado exitosamente y guardado como '{filename}'.")

# =====================================================================
# 2. ENTRENAMIENTO DEL MODELO DE APRENDIZAJE AUTOMÁTICO (Punto 2)
# =====================================================================
def entrenar_arbol_decision(filename="datos_transporte.csv"):
    if not os.path.exists(filename):
        generar_dataset_sintetico(filename)
        
    # Cargar datos
    df = pd.read_csv(filename)
    
    # Separar características (X) y etiqueta objetivo (y)
    X = df.drop(columns=['Retraso_Alto'])
    y = df['Retraso_Alto']
    
    # División en entrenamiento (80%) y prueba (20%)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Crear y entrenar el clasificador de Árbol de Decisión (Palma Méndez, 2008)
    # Limitamos la profundidad (max_depth) para extraer reglas legibles y evitar sobreajuste
    clf = DecisionTreeClassifier(max_depth=4, random_state=42, criterion='entropy')
    clf.fit(X_train, y_train)
    
    # Predicciones y Evaluación
    y_pred = clf.predict(X_test)
    exactitud = accuracy_score(y_test, y_pred)
    
    print("\n" + "="*50)
    print("      RESULTADOS DEL MODELO (MÉTODO SUPERVISADO)")
    print("="*50)
    print(f"Exactitud Global (Accuracy): {exactitud * 100:.2f}%\n")
    print("Reporte de Clasificación:")
    print(classification_report(y_test, y_pred, target_names=['A Tiempo (0)', 'Retraso Alto (1)']))
    
    # EXTRAER REGLAS DE DECISIÓN (Capítulo 17 de Palma Méndez)
    print("="*50)
    print("  REGLAS DE DECISIÓN LOGRADAS POR EL ÁRBOL")
    print("="*50)
    reglas_texto = export_text(clf, feature_names=list(X.columns))
    print(reglas_texto)
    
    return clf

# =====================================================================
# 3. INTERFAZ DE PRUEBA EN VIVO (Componente de pruebas)
# =====================================================================
if __name__ == "__main__":
    # Instalar dependencias si no existen: pip install pandas scikit-learn numpy
    modelo = entrenar_arbol_decision()
    
    print("\n" + "*"*40)
    print("   SISTEMA PREDICTIVO EN VIVO")
    print("*"*40)
    print("Ingrese las condiciones actuales de la red para predecir retrasos:")
    
    try:
        hp = int(input("¿Es hora pico? (1=Sí, 0=No): "))
        cl = int(input("¿Está lloviendo? (1=Sí, 0=No): "))
        bv = int(input("¿Hay algún bloqueo en la vía? (1=Sí, 0=No): "))
        oc = int(input("Nivel de pasajeros en estación (0=Baja, 1=Media, 2=Alta): "))
        
        # Muestra de test manual (Día de semana por defecto 1 = Martes)
        prediccion = modelo.predict([[hp, 1, cl, bv, oc]])
        
        print("\n" + "-"*40)
        if prediccion[0] == 1:
            print("🚨 ALERTA: El modelo supervisado infiere un RETRASO ALTO.")
            print("👉 Acción recomendada: Desviar articulados y sugerir rutas alternas.")
        else:
            print("✅ SISTEMA NORMAL: Flujo dentro del itinerario estándar.")
        print("-"*40)
    except ValueError:
        print("[Error] Ingrese solo valores numéricos válidos configurados en el sistema.")