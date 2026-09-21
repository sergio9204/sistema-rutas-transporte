# Guion del video — Sistema Inteligente de Rutas en Transporte Masivo

**Duración sugerida:** 5 a 7 minutos
**Herramientas:** grabador de pantalla (OBS, Loom, o la grabación de Zoom/Teams) + micrófono.
**Recomendación:** tener abierto el editor de código y una terminal en la carpeta del proyecto.

> Reparto sugerido para 4 integrantes: cada bloque lo puede narrar una persona
> distinta. Los nombres [Integrante 1..4] son solo una guía.

---

## Bloque 0 — Portada (0:00 – 0:20)  · [Integrante 1]

**En pantalla:** diapositiva o pantalla con el título del proyecto y los nombres.

**Texto a decir:**
> "Buenas, somos [nombres]. En este video presentamos nuestro proyecto de
> Inteligencia Artificial: un sistema inteligente que, a partir de una base de
> conocimiento escrita en reglas lógicas, calcula la mejor ruta para moverse de
> un punto A a un punto B en un sistema de transporte masivo. El proyecto aplica
> los capítulos 2, 3 y 9 del libro de Benítez."

---

## Bloque 1 — El problema y el enfoque (0:20 – 1:20)  · [Integrante 1]

**En pantalla:** el diagrama de la red del README (sección 2).

**Texto a decir:**
> "El problema es clásico: encontrar la ruta de menor tiempo en una red de
> transporte. Lo interesante es CÓMO lo resolvemos. En vez de programar el mapa
> a mano, representamos el conocimiento con lógica (capítulo 2), usamos un
> sistema basado en reglas para razonar sobre él (capítulo 3) y una búsqueda
> heurística, el algoritmo A\*, para hallar la ruta óptima (capítulo 9).
>
> Modelamos una red ficticia con tres líneas —Norte-Sur, Occidente-Oriente y una
> Diagonal— que se cruzan en dos estaciones de transbordo: Centro y Mercado."

---

## Bloque 2 — La base de conocimiento (1:20 – 2:40)  · [Integrante 2]

**En pantalla:** abrir `base_conocimiento.py` y hacer scroll por HECHOS y REGLAS.

**Texto a decir:**
> "Aquí está el corazón del sistema: la base de conocimiento. Primero los
> HECHOS. Cada estación es un hecho con sus coordenadas, por ejemplo
> `estacion(Centro, 0, 6)`. Y cada tramo directo entre estaciones es otro hecho:
> `tramo(Centro, Prado, L1, 3)`, que significa que hay un tramo de 3 minutos por
> la Línea 1.
>
> Fíjense que solo declaramos cada tramo en un sentido. El sentido contrario lo
> deduce una regla. Esas son las REGLAS LÓGICAS:
> - R1, bidireccionalidad: si puedo ir de A a B, puedo volver de B a A.
> - R2, transbordo: si una estación está en dos líneas, es punto de transbordo.
> - R3, costo de transbordo: cambiar de línea suma 5 minutos.
>
> La gran ventaja: si mañana cambia la red, solo edito este archivo; el resto
> del sistema no se toca."

**Acción en terminal (opcional):**
```bash
python main.py --reglas
```
> "Incluso el sistema puede mostrar sus propias reglas."

---

## Bloque 3 — El motor de inferencia (2:40 – 3:40)  · [Integrante 3]

**En pantalla:** abrir `motor_inferencia.py`, mostrar la clase `MotorInferencia`.

**Texto a decir:**
> "El motor de inferencia toma esos hechos y aplica las reglas mediante
> encadenamiento hacia adelante. Con la regla R1 construye el grafo completo de
> conexiones, agregando cada tramo en los dos sentidos. Con la regla R2 detecta
> automáticamente que Centro y Mercado son estaciones de transbordo, porque
> aparecen en más de una línea.
>
> Es decir: partimos de pocos hechos y el motor DEDUCE el conocimiento que
> necesitamos para buscar rutas."

---

## Bloque 4 — La búsqueda A\* (3:40 – 5:00)  · [Integrante 3]

**En pantalla:** mostrar la función `a_estrella` y la función `heuristica`.

**Texto a decir:**
> "Para encontrar la mejor ruta usamos A\*. A\* siempre expande el nodo con
> menor `f = g + h`. La `g` es el tiempo real que llevamos acumulado, incluyendo
> los 5 minutos de cada transbordo. La `h` es la heurística: estimamos el tiempo
> que falta con la distancia en línea recta al destino.
>
> Como la línea recta nunca es más larga que el recorrido real, la heurística
> nunca sobreestima; decimos que es ADMISIBLE, y eso garantiza que A\* encuentra
> la ruta óptima. Un detalle importante: el estado de búsqueda no es solo la
> estación, sino la pareja (estación, línea en la que vengo), para poder cobrar
> correctamente los transbordos."

---

## Bloque 5 — Demostración en vivo (5:00 – 6:20)  · [Integrante 4]

**En pantalla:** terminal en la carpeta del proyecto.

**Comando 1 — ruta simple, sin transbordos:**
```bash
python main.py Norte Sur
```
> "De Norte a Sur, todo por la Línea 1: 12 minutos, cero transbordos."

**Comando 2 — ruta con un transbordo:**
```bash
python main.py Norte Oriente
```
> "De Norte a Oriente el sistema decide bajar por la Línea 1 hasta Centro,
> hacer transbordo a la Línea 2 y llegar a Oriente: 19 minutos, un transbordo."

**Comando 3 — ruta con dos transbordos:**
```bash
python main.py Occidente Terminal
```
> "El caso más complejo: de Occidente a Terminal hay que cambiar dos veces, en
> Centro y en Mercado. El sistema lo resuelve: 31 minutos, dos transbordos.
> Observen que el transbordo se anuncia en la estación exacta donde ocurre."

**Comando 4 — modo interactivo (opcional):**
```bash
python main.py
```
> "También tiene un modo interactivo donde uno escribe el origen y el destino."

---

## Bloque 6 — Verificación y cierre (6:20 – 7:00)  · [Integrante 4]

**En pantalla:** ejecutar las pruebas.

```bash
python pruebas.py
```
> "Para demostrar que las rutas son realmente óptimas, comparamos A\* con el
> algoritmo de Dijkstra en los 156 pares posibles de la red. Coinciden en todos:
> la heurística es admisible y el sistema siempre entrega la mejor ruta.
>
> En resumen: representamos el conocimiento con lógica y reglas, un motor de
> inferencia razonó sobre él, y A\* encontró la ruta óptima entre A y B. El
> código está en el repositorio cuyo enlace dejamos en la entrega. Gracias."

---

## Lista de verificación antes de grabar

- [ ] El proyecto corre sin errores (`python main.py --demo`).
- [ ] La terminal tiene una fuente grande y legible.
- [ ] El código se ve con buen tamaño en el editor.
- [ ] Audio claro, sin ruido de fondo.
- [ ] Cada integrante sabe qué bloque narra.
- [ ] Al final, mencionar el enlace del repositorio Git.
- [ ] Subir el video (YouTube "no listado", Drive con permiso de lectura, etc.) y copiar el enlace en la entrega.
