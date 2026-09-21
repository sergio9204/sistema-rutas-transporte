# -*- coding: utf-8 -*-
"""
base_conocimiento.py
====================

BASE DE CONOCIMIENTO del sistema inteligente de rutas de transporte masivo.

Este modulo aplica los conceptos del CAPITULO 2 (Lógica y representación del
conocimiento) del libro de Benítez (2014): el conocimiento del dominio se
representa mediante HECHOS y REGLAS LÓGICAS, no mediante código imperativo.

Idea central
------------
En lugar de "programar" el mapa, lo DECLARAMOS como conocimiento:

    Hecho:  estacion("Centro", 0, 6)          -> existe una estación llamada Centro
    Hecho:  tramo("Centro", "Prado", "L1", 3) -> hay un tramo directo de 3 minutos

El resto del sistema (motor de inferencia + búsqueda) razona SOBRE estos hechos.
Si mañana cambia la red de transporte, solo se edita este archivo.

La red es FICTICIA (genérica) para que sea fácil de explicar. Está inspirada en
un sistema de transporte masivo con tres troncales (líneas) que se cruzan en
estaciones de transbordo.
"""

# ---------------------------------------------------------------------------
# HECHOS 1: estaciones
# ---------------------------------------------------------------------------
# Cada estación es un hecho:  estacion(nombre, x, y)
# Las coordenadas (x, y) son puntos en un plano y sirven para dos cosas:
#   1) representar geográficamente la red,
#   2) calcular la HEURÍSTICA de la búsqueda A* (capítulo 9).
#
# Aquí se guardan como un diccionario {nombre: (x, y)} por comodidad, pero
# conceptualmente cada entrada es un hecho lógico "estacion(N, X, Y)".

ESTACIONES = {
    # --- Línea 1 (L1): troncal Norte - Sur (vertical) ---
    "Norte":       (0, 10),
    "Prado":       (0, 8),
    "Centro":      (0, 6),   # transbordo L1 <-> L2
    "Mercado":     (0, 4),   # transbordo L1 <-> L3
    "Sur":         (0, 2),

    # --- Línea 2 (L2): troncal Occidente - Oriente (horizontal) ---
    "Occidente":   (-6, 6),
    "Universidad": (-3, 6),
    # "Centro" (0, 6) ya está definida  -> aquí L2 se cruza con L1
    "Hospital":    (3, 6),
    "Oriente":     (6, 6),

    # --- Línea 3 (L3): troncal Diagonal (Aeropuerto - Terminal) ---
    "Aeropuerto":  (-6, 4),
    "Parque":      (-3, 4),
    # "Mercado" (0, 4) ya está definida  -> aquí L3 se cruza con L1
    "Estadio":     (3, 4),
    "Terminal":    (6, 4),
}


# ---------------------------------------------------------------------------
# HECHOS 2: tramos directos entre estaciones consecutivas de una misma línea
# ---------------------------------------------------------------------------
# Cada tramo es un hecho:  tramo(origen, destino, linea, minutos)
#
#   - "linea"   permite detectar TRANSBORDOS (cambiar de línea cuesta tiempo).
#   - "minutos" es el costo real de recorrer ese tramo.
#
# OJO: solo declaramos el tramo en UN sentido. La REGLA R1 (más abajo) se
# encarga de deducir automáticamente el sentido contrario. Esto ilustra el
# capítulo 2: con pocos hechos + reglas se deduce conocimiento nuevo.

TRAMOS = [
    # Línea 1 (Norte - Sur)
    ("Norte",       "Prado",       "L1", 3),
    ("Prado",       "Centro",      "L1", 3),
    ("Centro",      "Mercado",     "L1", 3),
    ("Mercado",     "Sur",         "L1", 3),

    # Línea 2 (Occidente - Oriente)
    ("Occidente",   "Universidad", "L2", 4),
    ("Universidad", "Centro",      "L2", 4),
    ("Centro",      "Hospital",    "L2", 4),
    ("Hospital",    "Oriente",     "L2", 4),

    # Línea 3 (Diagonal)
    ("Aeropuerto",  "Parque",      "L3", 5),
    ("Parque",      "Mercado",     "L3", 5),
    ("Mercado",     "Estadio",     "L3", 5),
    ("Estadio",     "Terminal",    "L3", 5),
]


# ---------------------------------------------------------------------------
# HECHO 3: penalización por transbordo
# ---------------------------------------------------------------------------
# Cambiar de línea (bajarse de un bus/tren y esperar otro) tiene un costo.
# Lo representamos como un hecho numérico del dominio.
MINUTOS_POR_TRANSBORDO = 5


# ---------------------------------------------------------------------------
# REGLAS LÓGICAS (capítulo 3: sistemas basados en reglas)
# ---------------------------------------------------------------------------
# Las reglas se escriben en forma  SI <condiciones> ENTONCES <conclusión>.
# Aquí las definimos como texto legible (documentación viva de la KB) y como
# funciones que el motor de inferencia (motor_inferencia.py) aplica sobre los
# hechos. Separar "qué se sabe" (hechos) de "cómo se razona" (reglas) es
# justamente la arquitectura de un sistema basado en reglas.

REGLAS = [
    {
        "id": "R1",
        "nombre": "Bidireccionalidad de los tramos",
        "si":  "existe tramo(A, B, L, T)",
        "entonces": "también existe tramo(B, A, L, T)",
        "explicacion": (
            "Si se puede ir de A a B por la línea L en T minutos, entonces se "
            "puede volver de B a A por la misma línea en el mismo tiempo."
        ),
    },
    {
        "id": "R2",
        "nombre": "Estación de transbordo",
        "si":  "una estación aparece en tramos de dos o más líneas distintas",
        "entonces": "esa estación es un punto de transbordo entre esas líneas",
        "explicacion": (
            "Centro conecta L1 y L2; Mercado conecta L1 y L3. En esas "
            "estaciones el viajero puede cambiar de línea."
        ),
    },
    {
        "id": "R3",
        "nombre": "Costo de transbordo",
        "si":  "el viajero llega por la línea L1 y continúa por una línea L2 != L1",
        "entonces": f"se suman {MINUTOS_POR_TRANSBORDO} minutos al costo del viaje",
        "explicacion": (
            "Cambiar de línea implica esperar el siguiente servicio, por eso "
            "penaliza el tiempo total y el sistema preferirá rutas con menos "
            "transbordos cuando el tiempo es parecido."
        ),
    },
]


def reglas_como_texto():
    """Devuelve las reglas de la base de conocimiento en formato legible.

    Útil para el motor y para mostrarlas en pantalla (y explicarlas en el
    video): el sistema puede 'mostrar su conocimiento'.
    """
    lineas = []
    for r in REGLAS:
        lineas.append(f"[{r['id']}] {r['nombre']}")
        lineas.append(f"     SI  {r['si']}")
        lineas.append(f"     ENTONCES  {r['entonces']}")
        lineas.append(f"     ({r['explicacion']})")
        lineas.append("")
    return "\n".join(lineas)
