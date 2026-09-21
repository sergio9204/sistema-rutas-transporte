# Como crear el repositorio Git y obtener el enlace para la entrega

La entrega pide el **link del repositorio Git**. Estos son los pasos (opcion GitHub,
que es la mas comun y gratuita).

## 1. Instalar Git (si no lo tienen)
Descarguenlo de https://git-scm.com/downloads y acepten las opciones por defecto.

## 2. Crear una cuenta y un repositorio vacio en GitHub
1. Entren a https://github.com y creen una cuenta (o inicien sesion).
2. Clic en **New repository** (botonn verde).
3. Nombre sugerido: `sistema-rutas-transporte`.
4. Dejenlo **Publico** (para que el docente pueda abrirlo) y **NO** marquen
   "Add a README" (ya tenemos uno).
5. Clic en **Create repository**. Copien la URL que aparece, del tipo
   `https://github.com/usuario/sistema-rutas-transporte.git`.

## 3. Subir el proyecto desde la terminal
Abran una terminal **dentro de la carpeta del proyecto** (donde estan `main.py`,
`README.md`, etc.) y ejecuten:

```bash
git init
git add .
git commit -m "Sistema inteligente de rutas en transporte masivo (A* + reglas lógicas)"
git branch -M main
git remote add origin https://github.com/usuario/sistema-rutas-transporte.git
git push -u origin main
```

> Reemplacen la URL de `git remote add origin ...` por la del repositorio que crearon.
> GitHub puede pedir usuario y un **token** (Personal Access Token) en vez de contraseña:
> se genera en GitHub → Settings → Developer settings → Personal access tokens.

## 4. Verificar
Recarguen la página del repositorio en GitHub: deben verse todos los archivos.
**Esa URL** (`https://github.com/usuario/sistema-rutas-transporte`) es el link que
se pega en la entrega.

## 5. Recordatorio final de la entrega
En el enlace de la tarea deben indicar:
- **Link del repositorio Git:** la URL de GitHub.
- **Link del video:** YouTube ("no listado") o Google Drive con permiso de lectura.
