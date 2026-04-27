<p align="center">
  <img src="assets/readme-banner.svg" alt="Scripts Vault banner" width="100%" />
</p>

<h1 align="center">Scripts Vault</h1>

<p align="center">
  Un vault curado de scripts útiles, organizados por lenguaje y documentados para que cualquier persona pueda instalarlos, entenderlos y ejecutarlos con confianza.
</p>

<p align="center">
  <img src="https://img.shields.io/badge/estado-activo-2ea44f" alt="Estado activo" />
  <img src="https://img.shields.io/badge/organizado-por_lenguaje-1f6feb" alt="Organizado por lenguaje" />
  <img src="https://img.shields.io/badge/setup-por_carpeta-6f42c1" alt="Setup por carpeta" />
  <img src="https://img.shields.io/badge/enfoque-scripts_limpios-ffb000" alt="Scripts limpios" />
</p>

<p align="center">
  <a href="#qué-es">¿Qué es?</a> •
  <a href="#por-qué-transmite-confianza">¿Por qué transmite confianza?</a> •
  <a href="#estructura">Estructura</a> •
  <a href="#empezar-rápido">Empezar rápido</a>
</p>

## ¿Qué es?

`Scripts Vault` es un repositorio pensado para guardar solo scripts que realmente valen la pena.

La idea base del proyecto es:

- guardar scripts útiles
- organizarlos por lenguaje
- documentar cada entorno por carpeta
- dejar que cada script explique sus dependencias puntuales

## ¿Por qué transmite confianza?

<table>
  <tr>
    <td width="50%" valign="top">
      <h3>🗂️ Orden claro</h3>
      <p>Cada lenguaje vive en su propia carpeta. Nada queda mezclado ni confuso.</p>
    </td>
    <td width="50%" valign="top">
      <h3>📘 Setup por carpeta</h3>
      <p>Cada carpeta incluye su propia guía para instalar o preparar ese lenguaje.</p>
    </td>
  </tr>
  <tr>
    <td width="50%" valign="top">
      <h3>🧩 Scripts documentados</h3>
      <p>Cada script indica qué librerías usa, cómo se ejecuta y qué necesita.</p>
    </td>
    <td width="50%" valign="top">
      <h3>✨ Escalable</h3>
      <p>La estructura ya está pensada para crecer con Python, JavaScript, Java, TypeScript y más.</p>
    </td>
  </tr>
</table>

> La regla del repositorio es simple: el `README.md` presenta el proyecto y cada carpeta de lenguaje explica su propio entorno.

## Estructura

```text
scripts-vault/
|
|-- assets/
|   `-- readme-banner.svg
|
|-- python_scripts/
|   |-- PYTHON_SETUP.md
|   `-- remove_bg_to_webp.py
|
`-- README.md
```

## Carpetas disponibles

| Icono | Carpeta | Uso | Guía |
| --- | --- | --- | --- |
| 🐍 | [`python_scripts/`](python_scripts/) | Scripts y utilidades en Python | [`PYTHON_SETUP.md`](python_scripts/PYTHON_SETUP.md) |

Carpetas futuras que encajan perfecto en este vault:

- `javascript_scripts/`
- `typescript_scripts/`
- `java_scripts/`

## Script actual

El primer script incluido es:

- [`python_scripts/remove_bg_to_webp.py`](python_scripts/remove_bg_to_webp.py)

Este script convierte imágenes con fondo uniforme a `.webp` con transparencia y deja dentro del propio archivo sus notas de uso y dependencias concretas.

## Empezar rápido

<table>
  <tr>
    <td align="center"><strong>1</strong></td>
    <td>Entra a la carpeta del lenguaje que quieras usar.</td>
  </tr>
  <tr>
    <td align="center"><strong>2</strong></td>
    <td>Abre la guía de instalación de esa carpeta.</td>
  </tr>
  <tr>
    <td align="center"><strong>3</strong></td>
    <td>Instala el lenguaje o runtime si hace falta.</td>
  </tr>
  <tr>
    <td align="center"><strong>4</strong></td>
    <td>Lee los comentarios del script para ver librerías y comandos propios.</td>
  </tr>
  <tr>
    <td align="center"><strong>5</strong></td>
    <td>Ejecuta el script.</td>
  </tr>
</table>

## Empieza por aquí

Si quieres comenzar con Python:

- [Abrir guía de Python](python_scripts/PYTHON_SETUP.md)
- [Abrir script actual](python_scripts/remove_bg_to_webp.py)

<details>
  <summary><strong>Visión del proyecto</strong></summary>
  <br />
  Este repositorio puede crecer como una colección limpia y confiable de:
  <ul>
    <li>scripts de procesamiento de imágenes</li>
    <li>herramientas de conversión de archivos</li>
    <li>automatizaciones útiles</li>
    <li>utilidades para desarrollo</li>
    <li>colecciones por lenguaje con su propia guía de instalación</li>
  </ul>
</details>
