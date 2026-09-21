# -*- coding: utf-8 -*-
"""
main.py
=======

PROGRAMA PRINCIPAL del sistema inteligente de rutas de transporte masivo.

Une todo:
  1. Carga la BASE DE CONOCIMIENTO (hechos + reglas)   -> base_conocimiento.py
  2. Ejecuta el MOTOR DE INFERENCIA (aplica las reglas) -> motor_inferencia.py
  3. Pide un punto A (origen) y un punto B (destino)
  4. Usa BÚSQUEDA HEURÍSTICA A* para calcular la mejor ruta
  5. Muestra la ruta paso a paso, con tiempo total y número de transbordos

Uso
---
    python main.py                 -> modo interactivo (pregunta origen y destino)
    python main.py Norte Terminal  -> calcula directamente esa ruta
    python main.py --demo          -> ejecuta varios ejemplos de prueba
"""

import sys

import base_conocimiento as kb
from motor_inferencia import MotorInferencia, a_estrella


def mostrar_red():
    """Imprime las estaciones disponibles agrupadas por línea."""
    print("=" * 60)
    print(" RED DE TRANSPORTE MASIVO (base de conocimiento)")
    print("=" * 60)
    lineas = {}
    for origen, destino, linea, _min in kb.TRAMOS:
        lineas.setdefault(linea, [])
        for est in (origen, destino):
            if est not in lineas[linea]:
                lineas[linea].append(est)
    nombres = {"L1": "L1 Norte-Sur", "L2": "L2 Occidente-Oriente", "L3": "L3 Diagonal"}
    for linea, estaciones in lineas.items():
        print(f"  {nombres.get(linea, linea):22}: {' - '.join(estaciones)}")
    print(f"\n  Transbordos: Centro (L1<->L2), Mercado (L1<->L3)")
    print(f"  Penalización por transbordo: {kb.MINUTOS_POR_TRANSBORDO} min")
    print("=" * 60)


def mostrar_reglas():
    print("\n" + "=" * 60)
    print(" REGLAS LÓGICAS DE LA BASE DE CONOCIMIENTO")
    print("=" * 60)
    print(kb.reglas_como_texto())


def imprimir_ruta(resultado):
    """Muestra el resultado de A* de forma legible."""
    if resultado is None:
        print("\n[!] No fue posible calcular la ruta. Revise los nombres de las estaciones.")
        return

    nombres_linea = {"L1": "Línea 1", "L2": "Línea 2", "L3": "Línea 3"}

    def nombre(l):
        return nombres_linea.get(l, l)

    estaciones = resultado["estaciones"]
    lineas = resultado["lineas"]

    print("\n" + "-" * 60)
    print(f" MEJOR RUTA: {resultado['origen']}  ->  {resultado['destino']}")
    print("-" * 60)

    # Origen: se anuncia con qué línea se empieza el viaje.
    if len(estaciones) > 1:
        print(f"  ▶ Inicio en {estaciones[0]}  (tomar {nombre(lineas[1])})")
    else:
        print(f"  ▶ Inicio en {estaciones[0]}")

    for i in range(1, len(estaciones)):
        # El transbordo se produce en la estación anterior (la compartida).
        if i >= 2 and lineas[i] != lineas[i - 1]:
            print(f"  ⇄ TRANSBORDO en {estaciones[i - 1]} "
                  f"(cambiar a {nombre(lineas[i])})")
        print(f"  → {estaciones[i]}  [{nombre(lineas[i])}]")

    print("-" * 60)
    print(f"  Tiempo total estimado : {resultado['tiempo_total']} minutos")
    print(f"  Tramos recorridos     : {resultado['num_estaciones']}")
    print(f"  Transbordos           : {resultado['num_transbordos']}")
    print("-" * 60)


def calcular(motor, origen, destino):
    origen = origen.strip().title()
    destino = destino.strip().title()
    if not motor.existe(origen):
        print(f"\n[!] La estación '{origen}' no existe en la red.")
        return
    if not motor.existe(destino):
        print(f"\n[!] La estación '{destino}' no existe en la red.")
        return
    resultado = a_estrella(motor, origen, destino)
    imprimir_ruta(resultado)


def modo_demo(motor):
    """Ejecuta varias rutas de ejemplo (útil para grabar el video)."""
    ejemplos = [
        ("Norte", "Sur"),          # misma línea, sin transbordos
        ("Norte", "Oriente"),      # 1 transbordo en Centro
        ("Aeropuerto", "Norte"),   # 1 transbordo en Mercado
        ("Occidente", "Terminal"), # 2 transbordos
    ]
    mostrar_red()
    for origen, destino in ejemplos:
        resultado = a_estrella(motor, origen, destino)
        imprimir_ruta(resultado)


def modo_interactivo(motor):
    mostrar_red()
    print("\nEscriba el nombre de la estación de ORIGEN y de DESTINO.")
    print("(escriba 'reglas' para ver las reglas, o 'salir' para terminar)\n")
    while True:
        origen = input("Origen  (A): ").strip()
        if origen.lower() in ("salir", "exit", "q"):
            break
        if origen.lower() == "reglas":
            mostrar_reglas()
            continue
        destino = input("Destino (B): ").strip()
        if destino.lower() in ("salir", "exit", "q"):
            break
        calcular(motor, origen, destino)
        print()


def main():
    # 1) y 2): construir el motor aplica automáticamente las reglas sobre los hechos.
    motor = MotorInferencia()

    args = sys.argv[1:]

    if not args:
        modo_interactivo(motor)
    elif args[0] == "--demo":
        modo_demo(motor)
    elif args[0] == "--reglas":
        mostrar_reglas()
    elif len(args) >= 2:
        mostrar_red()
        calcular(motor, args[0], args[1])
    else:
        print("Uso:")
        print("  python main.py                 (modo interactivo)")
        print("  python main.py Norte Terminal  (ruta directa)")
        print("  python main.py --demo          (ejemplos de prueba)")
        print("  python main.py --reglas        (ver reglas de la KB)")


if __name__ == "__main__":
    main()
