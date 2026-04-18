# Python Setup

Este archivo explica como preparar Python en Windows para ejecutar los scripts dentro de `python_scripts`.

## Instalar Python

1. Descarga Python desde [python.org](https://www.python.org/downloads/windows/).
2. Ejecuta el instalador.
3. Marca la opcion `Add python.exe to PATH`.
4. Pulsa `Install Now`.
5. Cierra y vuelve a abrir la terminal cuando termine.

## Verificar instalacion

```bash
python --version
```

Si ese comando no funciona, prueba:

```bash
py --version
```

## Instalar librerias para scripts

Cada script puede requerir librerias distintas.

Ejemplo para `remove_bg_to_webp.py`:

```bash
pip install Pillow
```

## Ejecutar scripts de esta carpeta

Abre una terminal en la raiz del repositorio `scripts-vault` y luego ejecuta el script que necesites.

Ejemplo:

```bash
python python_scripts/remove_bg_to_webp.py --input "C:\ruta\entrada" --output "C:\ruta\salida"
```

Si usas el lanzador de Python en Windows, tambien puedes ejecutar:

```bash
py python_scripts/remove_bg_to_webp.py --input "C:\ruta\entrada" --output "C:\ruta\salida"
```
