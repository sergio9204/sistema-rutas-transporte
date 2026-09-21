# -*- coding: utf-8 -*-
"""
pruebas.py
==========

Pruebas de verificación del sistema.

Objetivo principal: demostrar que la búsqueda heurística A* (capítulo 9)
encuentra la ruta ÓPTIMA. Para ello comparamos su resultado con el de una
búsqueda de costo uniforme (Dijkstra), que es A* con heurística h(n)=0 y que
se sabe óptima. Si ambas dan el mismo tiempo total, A* es correcta y su
heurística es admisible.

Ejecutar con:   python pruebas.py
"""

import heapq

import base_conocimiento as kb
from motor_inferencia import MotorInferencia, a_estrella


def dijkstra(motor, origen, destino):
    """Búsqueda de costo uniforme (referencia óptima, sin heurística)."""
    inicio = (origen, None)
    g = {inicio: 0}
    frontera = [(0, inicio)]
    visitados = set()
    while frontera:
        costo, estado = heapq.heappop(frontera)
        estacion, linea_actual = estado
        if estacion == destino:
            return costo
        if estado in visitados:
            continue
        visitados.add(estado)
        for (vecina, linea, minutos) in motor.vecinos(estacion):
            extra = 0
            if linea_actual is not None and linea != linea_actual:
                extra = kb.MINUTOS_POR_TRANSBORDO
            nuevo = costo + minutos + extra
            nuevo_estado = (vecina, linea)
            if nuevo_estado not in g or nuevo < g[nuevo_estado]:
                g[nuevo_estado] = nuevo
                heapq.heappush(frontera, (nuevo, nuevo_estado))
    return None


def main():
    motor = MotorInferencia()
    estaciones = list(kb.ESTACIONES.keys())

    print("Verificando que A* == Dijkstra (óptimo) en TODOS los pares...")
    fallos = 0
    total = 0
    for origen in estaciones:
        for destino in estaciones:
            if origen == destino:
                continue
            total += 1
            r = a_estrella(motor, origen, destino)
            optimo = dijkstra(motor, origen, destino)
            t_astar = r["tiempo_total"] if r else None
            if t_astar != optimo:
                fallos += 1
                print(f"  [FALLO] {origen}->{destino}: A*={t_astar} Dijkstra={optimo}")

    print(f"\nPares evaluados: {total}")
    if fallos == 0:
        print("RESULTADO: OK  -> A* coincide con el óptimo en todos los casos.")
    else:
        print(f"RESULTADO: {fallos} discrepancias (revisar la heurística).")

    # Algunos valores esperados concretos (regresión).
    print("\nValores esperados en rutas de ejemplo:")
    casos = {
        ("Norte", "Sur"): (12, 0),
        ("Norte", "Oriente"): (19, 1),
        ("Occidente", "Terminal"): (31, 2),
    }
    for (o, d), (t_esp, tr_esp) in casos.items():
        r = a_estrella(motor, o, d)
        ok = (r["tiempo_total"] == t_esp and r["num_transbordos"] == tr_esp)
        marca = "OK " if ok else "XX "
        print(f"  {marca}{o}->{d}: {r['tiempo_total']} min, "
              f"{r['num_transbordos']} transbordos "
              f"(esperado {t_esp} min, {tr_esp} transbordos)")


if __name__ == "__main__":
    main()
