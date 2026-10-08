# Sistema Inteligente de Rutas en Transporte Masivo

Sistema inteligente que, a partir de una **base de conocimiento escrita en reglas
lógicas**, calcula la **mejor ruta** (menor tiempo) para desplazarse desde un
punto **A** hasta un punto **B** dentro de un sistema de transporte masivo.

Proyecto desarrollado para el curso de **Inteligencia Artificial**, aplicando los
capítulos 2, 3 y 9 del libro *Inteligencia artificial avanzada* de Raúl Benítez
(2014, Editorial UOC).

---

## 1. Marco teórico (capítulos del libro)

| Capítulo | Tema | Dónde se aplica en el proyecto |
|----------|------|--------------------------------|
| **Cap. 2** | Lógica y representación del conocimiento | La red de transporte se **declara** como hechos lógicos (`estacion`, `tramo`) en lugar de programarse. Ver `base_conocimiento.py`. |
| **Cap. 3** | Sistemas basados en reglas | Un **motor de inferencia** aplica reglas `SI... ENTONCES...` sobre los hechos para deducir el grafo de conexiones y las estaciones de transbordo. Ver `MotorInferencia` en `motor_inferencia.py`. |
| **Cap. 9** | Búsqueda heurística | El algoritmo **A\*** encuentra la ruta óptima usando `f(n) = g(n) + h(n)` con una heurística admisible (distancia en línea recta). Ver `a_estrella` en `motor_inferencia.py`. |

### La base de conocimiento

El conocimiento del dominio se representa con **hechos**:

```
estacion("Centro", 0, 6)            # existe una estación llamada Centro en (0,6)
tramo("Centro", "Prado", "L1", 3)   # hay un tramo directo de 3 minutos por la Línea 1
```

y con **reglas lógicas**:

- **R1 — Bidireccionalidad:** si existe `tramo(A, B, L, T)`, entonces también existe `tramo(B, A, L, T)`.
- **R2 — Transbordo:** si una estación aparece en dos o más líneas, es un punto de transbordo.
- **R3 — Costo de transbordo:** si el viajero cambia de línea, se suman 5 minutos al tiempo del viaje.

> Ventaja del enfoque: para cambiar la red **solo se edita `base_conocimiento.py`**;
> el motor y la búsqueda no se tocan. Esto es exactamente lo que persigue un
> sistema basado en conocimiento.

### El algoritmo A\*

A\* expande siempre el nodo con menor `f(n) = g(n) + h(n)`:

- `g(n)` = tiempo real acumulado desde el origen (incluye penalización por transbordos).
- `h(n)` = estimación del tiempo restante = distancia euclidiana al destino × (mínimo minutos/unidad de la red).

Como la distancia en línea recta **nunca sobreestima** el tiempo real que falta,
la heurística es **admisible** y A\* garantiza la **ruta óptima**. El estado de
búsqueda es `(estación, línea_actual)` para poder cobrar los transbordos.

---

## 2. La red modelada (ficticia)

Red genérica con tres troncales que se cruzan en dos estaciones de transbordo:

```
                 Norte (L1)
                   |
                 Prado
                   |
 Occidente-Universidad-CENTRO-Hospital-Oriente     (L2)
                   |   (transbordo L1<->L2)
 Aeropuerto-Parque-MERCADO-Estadio-Terminal        (L3)
                   |   (transbordo L1<->L3)
                  Sur (L1)
```

- **Línea 1 (Norte–Sur):** Norte, Prado, Centro, Mercado, Sur
- **Línea 2 (Occidente–Oriente):** Occidente, Universidad, Centro, Hospital, Oriente
- **Línea 3 (Diagonal):** Aeropuerto, Parque, Mercado, Estadio, Terminal
- **Transbordos:** Centro (L1↔L2) y Mercado (L1↔L3). Cada transbordo cuesta 5 min.

---

## 3. Estructura del proyecto

```
sistema-rutas-transporte/
├── base_conocimiento.py   # HECHOS y REGLAS (cap. 2 y 3)
├── motor_inferencia.py    # Motor de reglas + algoritmo A* (cap. 3 y 9)
├── main.py                # Programa principal (interfaz por consola)
├── pruebas.py             # Verificación: A* == óptimo (Dijkstra)
├── datos_trasnporte.csv   # Dataset 
├── modelo_supervisado.py # Arboles y Reglas de Decision
└── README.md
```

---

## 4. Requisitos e instalación

- **Python 3.8 o superior.** No requiere librerías externas (solo la librería estándar).

```bash
git clone <URL-del-repositorio>
cd sistema-rutas-transporte
python main.py --demo
```

---

## 5. Uso

**Modo interactivo** (pregunta origen y destino):

```bash
python main.py
```

**Ruta directa** por argumentos:

```bash
python main.py Norte Terminal
```

**Ejemplos de prueba** (útil para la demostración):

```bash
python main.py --demo
```

**Ver las reglas de la base de conocimiento:**

```bash
python main.py --reglas
```

---

## 6. Ejemplo de resultado

```
------------------------------------------------------------
 MEJOR RUTA: Occidente  ->  Terminal
------------------------------------------------------------
  ▶ Inicio en Occidente  (tomar Línea 2)
  → Universidad  [Línea 2]
  → Centro  [Línea 2]
  ⇄ TRANSBORDO en Centro (cambiar a Línea 1)
  → Mercado  [Línea 1]
  ⇄ TRANSBORDO en Mercado (cambiar a Línea 3)
  → Estadio  [Línea 3]
  → Terminal  [Línea 3]
------------------------------------------------------------
  Tiempo total estimado : 31 minutos
  Tramos recorridos     : 5
  Transbordos           : 2
------------------------------------------------------------
```

---

## 7. Verificación

`pruebas.py` compara A\* con una búsqueda de costo uniforme (Dijkstra), que se
sabe óptima, en **todos** los pares origen–destino posibles:

```bash
python pruebas.py
```

Salida esperada:

```
Pares evaluados: 156
RESULTADO: OK  -> A* coincide con el óptimo en todos los casos.
```

Esto demuestra que la heurística es admisible y que el sistema entrega siempre
la mejor ruta.

---

## 8. Autores

Actividad grupal (equipo de máximo 4 estudiantes).

- Sergio Armando Ladino Ocampo
- Juan David Fernandez Farfan
- Luisa Veronica Cruz Velandia 

---

## 9. Referencia

Benítez, R. (2014). *Inteligencia artificial avanzada*. Barcelona: Editorial UOC.

Referencia Bibliográfica Adicional
* Palma Méndez, J. T. (2008). *Inteligencia artificial: métodos, técnicas y aplicaciones*. Madrid: McGraw-Hill España.

---
##  10. Componente de Aprendizaje Supervisado (Machine Learning)
*Basado en los lineamientos teóricos del Capítulo 17 (Aprendizaje de árboles y reglas de decisión) de Palma Méndez, J. T. (2008).*

Para complementar el sistema basado en conocimiento, implementamos un modelo predictivo capaz de anticipar contingencias operativas (retrasos severos) en la red de transporte masivo mediante un clasificador de Árbol de Decisión.

###  Ficha Técnica del Dataset (`datos_transporte.csv`)
* **Volumen de la muestra:** 1,000 registros históricos simulados de estrés operativo.
* **Tipo de Aprendizaje:** Clasificación Binaria Supervisada.
* **Criterio de División de Nodos:** Entropía (Ganancia de Información).

###  Diccionario de Variables Predictivas (Características)
1. **Hora_Pico (Binaria):** Indica si el trayecto coincide con ventanas de alta congestión (1 = Sí, 0 = No).
2. **Dia_Semana (Entera):** Representa el día del viaje indexado numéricamente (0 = Lunes, 6 = Domingo).
3. **Clima_Lluvia (Binaria):** Factores ambientales que reducen la velocidad comercial de los articulados (1 = Lluvia, 0 = Despejado).
4. **Bloqueo_Via (Binaria):** Eventos imprevistos de fuerza mayor como accidentes o manifestaciones (1 = Bloqueo, 0 = Flujo normal).
5. **Ocupacion_Estacion (Categórica):** Densidad de pasajeros en plataformas de abordaje (0 = Baja, 1 = Media, 2 = Alta).

###  Variable Objetivo (Target a predecir)
* **Retraso_Alto (Binaria):** Clasificación del estado del itinerario (1 = Retraso severo reportado en ruta, 0 = Operación a tiempo).

###  Instrucciones para Ejecutar las Pruebas del Modelo
1. Instale las dependencias necesarias en su entorno de Python:
   ```bash
   pip install pandas numpy scikit-learn
   ```
2. Ejecute el script del clasificador supervisado desde la terminal de comandos:
   ```bash
   python modelo_supervisado.py
   ```
3. El sistema entrenará el árbol, mostrará las métricas de exactitud y desplegará un menú interactivo en la consola para ingresar datos de prueba en vivo


##  11. Componente de Aprendizaje No Supervisado (Clustering)
*Basado en los lineamientos del Capítulo 16 (Técnicas de agrupamiento) de Palma Méndez, J. T. (2008).*

Como complemento avanzado, se desarrolló un módulo de aprendizaje no supervisado utilizando el algoritmo K-Means. A diferencia del modelo supervisado, este componente procesa flujos de datos sin etiquetas previas, descubriendo agrupaciones naturales para segmentar el nivel de congestión de la red en tiempo real.

###  Ficha Técnica del Dataset (`datos_agrupamiento.csv`)
* **Volumen de la muestra:** 500 muestras operacionales continuas.
* **Métrica de proximidad:** Distancia Euclidiana sobre características normalizadas (`StandardScaler`).
* **Número de grupos (k):** 3 clústeres autonómicos (Tráfico Fluido, Moderado y Crítico).

### 🔍 Atributos del Dominio Procesados
1. **Tiempo_Viaje_Min:** Duración en minutos registrada por los vehículos en un tramo.
2. **Flujo_Pasajeros_Min:** Tasa de entrada de usuarios en las zonas de abordaje.

###  Instrucciones de Ejecución
Ejecute el script del clasificador no supervisado desde la terminal:
```bash
python modelo_no_supervisado.py
```

```

