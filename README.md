# scripts-vault

Repositorio personal para guardar scripts utiles y bien organizados por lenguaje.

## Estructura

- `python_scripts/`: scripts escritos en Python

Con el tiempo se pueden agregar carpetas como `javascript_scripts/`, `java_scripts/` u otras segun el lenguaje.

## Script actual

### `python_scripts/remove_bg_to_webp.py`

Convierte imagenes con fondo uniforme a archivos `.webp` con transparencia, intentando mantener un peso maximo configurable.

## Requisitos

Instala Pillow:

```bash
pip install -r python_scripts/requirements.txt
```

## Uso

```bash
python python_scripts/remove_bg_to_webp.py --input "C:\Users\Yetsin\Downloads\entrada" --output "C:\Users\Yetsin\Downloads\salida"
```

Opcionalmente puedes cambiar el peso maximo:

```bash
python python_scripts/remove_bg_to_webp.py --input "C:\ruta\entrada" --output "C:\ruta\salida" --max-size-kb 90
```
