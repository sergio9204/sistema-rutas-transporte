# -*- coding: utf-8 -*-
"""
motor_inferencia.py
===================

MOTOR DE INFERENCIA + BÚSQUEDA HEURÍSTICA.

Este módulo combina dos capítulos del libro de Benítez (2014):

  * CAPÍTULO 3 (Sistemas basados en reglas):
        La clase MotorInferencia toma los HECHOS de la base de conocimiento y
        aplica las REGLAS para deducir hechos nuevos (encadenamiento hacia
        adelante / forward chaining). En concreto construye el grafo completo
        de conexiones aplicando la regla R1 (bidireccionalidad) y detecta las
        estaciones de transbordo con la regla R2.

  * CAPÍTULO 9 (Técnicas basadas en búsquedas heurísticas):
        La función a_estrella implementa el algoritmo A* para encontrar la
        MEJOR ruta (menor tiempo) entre dos estaciones. A* usa:
            f(n) = g(n) + h(n)
        donde g(n) es el costo real acumulado y h(n) es una heurística
        ADMISIBLE (distancia en línea recta convertida a minutos), que nunca
        sobreestima el costo restante, garantizando la ruta óptima.
"""

import heapq
import math

import base_conocimiento as kb


class MotorInferencia:
    """Aplica las reglas de la base de conocimiento sobre los hechos.

    Resultado del razonamiento:
      - self.conexiones: dict {estacion: [(vecina, linea, minutos), ...]}
        (grafo de conexiones ya bidireccional, según la regla R1)
      - self.lineas_de: dict {estacion: set(líneas que la sirven)}
      - self.transbordos: set de estaciones donde se puede cambiar de línea
        (según la regla R2)
    """

    def __init__(self):
        self.conexiones = {}
        self.lineas_de = {}
        self.transbordos = set()
        self._inferir()

    def _agregar_conexion(self, origen, destino, linea, minutos):
        self.conexiones.setdefault(origen, []).append((destino, linea, minutos))
        self.lineas_de.setdefault(origen, set()).add(linea)

    def _inferir(self):
        """Encadenamiento hacia adelante: de los hechos deducimos el grafo."""
        # Regla R1: cada tramo declarado genera el sentido de ida Y el de vuelta.
        for origen, destino, linea, minutos in kb.TRAMOS:
            self._agregar_conexion(origen, destino, linea, minutos)   # ida
            self._agregar_conexion(destino, origen, linea, minutos)   # vuelta (R1)

        # Regla R2: una estación servida por 2+ líneas es punto de transbordo.
        for estacion, lineas in self.lineas_de.items():
            if len(lineas) >= 2:
                self.transbordos.add(estacion)

    # -- utilidades de consulta sobre el conocimiento inferido ---------------
    def vecinos(self, estacion):
        """Devuelve las conexiones directas de una estación."""
        return self.conexiones.get(estacion, [])

    def existe(self, estacion):
        return estacion in kb.ESTACIONES


def heuristica(estacion_a, estacion_b, min_por_unidad):
    """Heurística ADMISIBLE para A* (capítulo 9).

    Estima el tiempo mínimo que faltaría para llegar al destino usando la
    distancia euclidiana (en línea recta) entre las dos estaciones,
    multiplicada por el menor tiempo posible por unidad de distancia de toda
    la red.

    Como en la realidad hay que seguir las vías (nunca es más corto que la
    línea recta) y además puede haber transbordos, este valor NUNCA
    sobreestima el costo real -> la heurística es admisible -> A* encuentra la
    ruta óptima.
    """
    (x1, y1) = kb.ESTACIONES[estacion_a]
    (x2, y2) = kb.ESTACIONES[estacion_b]
    distancia = math.hypot(x2 - x1, y2 - y1)
    return distancia * min_por_unidad


def _min_por_unidad(motor):
    """Calcula el menor 'minutos por unidad de distancia' de toda la red.

    Se usa como factor de la heurística para garantizar su admisibilidad.
    """
    factores = []
    for origen, destino, linea, minutos in kb.TRAMOS:
        (x1, y1) = kb.ESTACIONES[origen]
        (x2, y2) = kb.ESTACIONES[destino]
        dist = math.hypot(x2 - x1, y2 - y1)
        if dist > 0:
            factores.append(minutos / dist)
    return min(factores) if factores else 1.0


def a_estrella(motor, origen, destino):
    """Algoritmo A* (capítulo 9).

    Busca la ruta de MENOR TIEMPO entre 'origen' y 'destino' sobre el grafo
    de conexiones inferido por el motor de reglas.

    El ESTADO de la búsqueda es (estacion, linea_actual) porque el costo
    depende de la línea en la que se viene: continuar en la misma línea es
    gratis, pero cambiar de línea aplica la penalización de transbordo (R3).

    Devuelve un diccionario con la ruta y sus métricas, o None si no hay ruta.
    """
    if not motor.existe(origen) or not motor.existe(destino):
        return None

    factor = _min_por_unidad(motor)

    # Estado inicial: estamos en 'origen' sin línea previa (None).
    estado_inicial = (origen, None)

    # g(n): costo real mínimo conocido para llegar a cada estado.
    g = {estado_inicial: 0}
    # Para reconstruir la ruta: de dónde vino cada estado.
    padre = {estado_inicial: None}

    # Cola de prioridad ordenada por f(n) = g(n) + h(n).
    # Cada elemento: (f, g, estado)
    h0 = heuristica(origen, destino, factor)
    frontera = [(h0, 0, estado_inicial)]
    visitados = set()

    while frontera:
        f_actual, g_actual, estado = heapq.heappop(frontera)
        estacion, linea_actual = estado

        if estacion == destino:
            return _reconstruir(padre, estado, g_actual, motor)

        if estado in visitados:
            continue
        visitados.add(estado)

        # Expandir vecinos aplicando el conocimiento del motor de reglas.
        for (vecina, linea, minutos) in motor.vecinos(estacion):
            # Regla R3: si cambiamos de línea, sumamos la penalización.
            costo_transbordo = 0
            if linea_actual is not None and linea != linea_actual:
                costo_transbordo = kb.MINUTOS_POR_TRANSBORDO

            nuevo_g = g_actual + minutos + costo_transbordo
            nuevo_estado = (vecina, linea)

            if nuevo_estado not in g or nuevo_g < g[nuevo_estado]:
                g[nuevo_estado] = nuevo_g
                padre[nuevo_estado] = estado
                f = nuevo_g + heuristica(vecina, destino, factor)
                heapq.heappush(frontera, (f, nuevo_g, nuevo_estado))

    return None  # no se encontró ruta


def _reconstruir(padre, estado_final, costo_total, motor):
    """Reconstruye la ruta desde el estado final hasta el inicial.

    Devuelve dos listas alineadas por índice:
      - estaciones: [origen, ..., destino]
      - lineas:     línea con la que se LLEGA a cada estación
                    (lineas[0] es None porque en el origen aún no se viaja)

    El viaje entre estaciones[i-1] y estaciones[i] se hace por lineas[i]; por
    eso, cuando lineas[i] != lineas[i-1] hay un transbordo y este ocurre en la
    estación COMPARTIDA por ambas líneas, que es estaciones[i-1].
    """
    camino = []  # lista de (estacion, linea_con_la_que_se_llega)
    estado = estado_final
    while estado is not None:
        camino.append(estado)
        estado = padre[estado]
    camino.reverse()

    estaciones = [e for (e, _l) in camino]
    lineas = [l for (_e, l) in camino]  # lineas[0] == None

    # Un transbordo ocurre cuando dos tramos consecutivos usan líneas distintas.
    transbordos = 0
    for i in range(2, len(lineas)):
        if lineas[i] != lineas[i - 1]:
            transbordos += 1

    return {
        "origen": estaciones[0],
        "destino": estaciones[-1],
        "estaciones": estaciones,
        "lineas": lineas,
        "tiempo_total": costo_total,
        "num_transbordos": transbordos,
        "num_estaciones": len(estaciones) - 1,  # tramos recorridos
    }
