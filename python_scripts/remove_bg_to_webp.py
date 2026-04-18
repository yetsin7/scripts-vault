from __future__ import annotations

"""Convierte imagenes con fondo uniforme a WEBP con transparencia.

Instalacion:
- Abre una terminal dentro de la raiz del proyecto `scripts-vault`.
- Si no tienes Pillow instalado, ejecuta: `pip install Pillow`

Ejecucion:
- Desde la misma raiz del proyecto ejecuta:
  `python python_scripts/remove_bg_to_webp.py --input "C:\ruta\entrada" --output "C:\ruta\salida"`
"""
import argparse
import io
import math
from pathlib import Path

from PIL import Image, ImageEnhance, ImageFilter

VALID_EXTENSIONS = {".png", ".jpg", ".jpeg", ".bmp", ".tiff", ".webp"}
MAX_SIZE_KB = 90
BACKGROUND_TOLERANCE = 95
PROTECT_RED = True
RED_THRESHOLD = 80
CONTRAST_BOOST = 1.08
COLOR_BOOST = 1.08
SHARPNESS_BOOST = 1.10
ALPHA_BLUR = 0.7
CROP_TRANSPARENCY = True
CROP_MARGIN = 2
INITIAL_MAX_DIMENSION = 1600
MIN_MAX_DIMENSION = 700
REDUCTION_STEP = 0.9


def parse_args() -> argparse.Namespace:
    """Recibe y valida las carpetas de entrada y salida desde consola."""
    parser = argparse.ArgumentParser(
        description="Quita fondos uniformes y exporta logos a WEBP con transparencia."
    )
    parser.add_argument(
        "--input",
        required=True,
        type=Path,
        help="Carpeta que contiene las imagenes originales.",
    )
    parser.add_argument(
        "--output",
        required=True,
        type=Path,
        help="Carpeta donde se guardaran los archivos WEBP.",
    )
    parser.add_argument(
        "--max-size-kb",
        default=MAX_SIZE_KB,
        type=int,
        help="Peso maximo permitido por archivo en KB.",
    )
    return parser.parse_args()


def is_image(path: Path) -> bool:
    """Indica si una ruta apunta a un archivo de imagen soportado."""
    return path.is_file() and path.suffix.lower() in VALID_EXTENSIONS


def rgb_distance(color_a: tuple[int, int, int], color_b: tuple[int, int, int]) -> float:
    """Calcula la distancia euclidiana entre dos colores RGB."""
    return math.sqrt(
        (color_a[0] - color_b[0]) ** 2
        + (color_a[1] - color_b[1]) ** 2
        + (color_a[2] - color_b[2]) ** 2
    )


def average_colors(colors: list[tuple[int, int, int]]) -> tuple[int, int, int]:
    """Promedia una lista de colores para estimar un tono dominante."""
    if not colors:
        return (255, 255, 255)

    red = sum(color[0] for color in colors) / len(colors)
    green = sum(color[1] for color in colors) / len(colors)
    blue = sum(color[2] for color in colors) / len(colors)
    return (int(red), int(green), int(blue))


def get_corner_background_color(
    image: Image.Image, sample_size: int = 12
) -> tuple[int, int, int]:
    """Estima el color del fondo usando muestras tomadas de las esquinas."""
    rgb_image = image.convert("RGB")
    width, height = rgb_image.size
    pixels = rgb_image.load()
    colors: list[tuple[int, int, int]] = []
    zones = [
        (0, 0, sample_size, sample_size),
        (width - sample_size, 0, width, sample_size),
        (0, height - sample_size, sample_size, height),
        (width - sample_size, height - sample_size, width, height),
    ]

    for left, top, right, bottom in zones:
        for y in range(max(0, top), min(height, bottom)):
            for x in range(max(0, left), min(width, right)):
                colors.append(pixels[x, y])

    return average_colors(colors)


def is_protected_red(red: int, green: int, blue: int, threshold: int = 80) -> bool:
    """Evita eliminar pixeles rojizos cuando el logo usa rojo dominante."""
    return (red > green + threshold) and (red > blue + threshold)


def create_alpha_from_background(
    image: Image.Image, background_color: tuple[int, int, int], tolerance: int
) -> Image.Image:
    """Genera un canal alpha segun la cercania de cada pixel al fondo."""
    rgb_image = image.convert("RGB")
    width, height = rgb_image.size
    source = rgb_image.load()
    alpha = Image.new("L", (width, height), 255)
    alpha_pixels = alpha.load()

    for y in range(height):
        for x in range(width):
            red, green, blue = source[x, y]
            distance = rgb_distance((red, green, blue), background_color)

            if PROTECT_RED and is_protected_red(red, green, blue, RED_THRESHOLD):
                alpha_pixels[x, y] = 255
                continue

            if distance <= tolerance:
                alpha_pixels[x, y] = 0
            elif distance <= tolerance * 1.8:
                fade = int(255 * ((distance - tolerance) / (tolerance * 0.8)))
                alpha_pixels[x, y] = max(0, min(255, fade))
            else:
                alpha_pixels[x, y] = 255

    if ALPHA_BLUR > 0:
        alpha = alpha.filter(ImageFilter.GaussianBlur(radius=ALPHA_BLUR))

    return alpha


def clean_alpha_edges(alpha: Image.Image) -> Image.Image:
    """Refuerza los extremos del alpha para reducir halos visuales."""

    def adjust(value: int) -> int:
        if value <= 12:
            return 0
        if value >= 245:
            return 255
        return value

    return alpha.point(adjust)


def apply_alpha(image: Image.Image, alpha: Image.Image) -> Image.Image:
    """Combina la imagen base con el canal alpha generado."""
    rgba_image = image.convert("RGBA")
    rgba_image.putalpha(alpha)
    return rgba_image


def crop_transparency(image: Image.Image, margin: int = 0) -> Image.Image:
    """Recorta el espacio transparente sobrante alrededor del contenido."""
    rgba_image = image if image.mode == "RGBA" else image.convert("RGBA")
    box = rgba_image.getchannel("A").getbbox()

    if not box:
        return rgba_image

    left, top, right, bottom = box
    return rgba_image.crop(
        (
            max(0, left - margin),
            max(0, top - margin),
            min(rgba_image.width, right + margin),
            min(rgba_image.height, bottom + margin),
        )
    )


def enhance_logo(image: Image.Image) -> Image.Image:
    """Aplica mejoras suaves de contraste, color y nitidez."""
    base = image.convert("RGBA")
    composed = Image.alpha_composite(Image.new("RGBA", base.size, (0, 0, 0, 0)), base)
    rgb_image = composed.convert("RGB")
    rgb_image = ImageEnhance.Contrast(rgb_image).enhance(CONTRAST_BOOST)
    rgb_image = ImageEnhance.Color(rgb_image).enhance(COLOR_BOOST)
    rgb_image = ImageEnhance.Sharpness(rgb_image).enhance(SHARPNESS_BOOST)
    result = rgb_image.convert("RGBA")
    result.putalpha(base.getchannel("A"))
    return result


def resize_image(image: Image.Image, max_dimension: int) -> Image.Image:
    """Reduce proporcionalmente la imagen si supera la dimension maxima."""
    width, height = image.size
    largest_side = max(width, height)

    if largest_side <= max_dimension:
        return image

    scale = max_dimension / largest_side
    return image.resize(
        (max(1, int(width * scale)), max(1, int(height * scale))),
        Image.LANCZOS,
    )


def export_webp_bytes(image: Image.Image, quality: int | None, lossless: bool) -> bytes:
    """Serializa la imagen en WEBP usando modo lossless o con calidad."""
    buffer = io.BytesIO()

    if lossless:
        image.save(buffer, format="WEBP", lossless=True, method=6)
    else:
        image.save(buffer, format="WEBP", lossless=False, quality=quality or 80, method=6)

    return buffer.getvalue()


def export_webp_with_limit(
    image: Image.Image, output_path: Path, max_size_kb: int
) -> tuple[bool, float, str]:
    """Exporta WEBP intentando respetar el limite de peso definido."""
    max_bytes = max_size_kb * 1024
    data = export_webp_bytes(image, quality=None, lossless=True)

    if len(data) <= max_bytes:
        output_path.write_bytes(data)
        return True, len(data) / 1024, "lossless"

    low, high = 15, 100
    best_data: bytes | None = None
    best_quality: int | None = None

    while low <= high:
        mid = (low + high) // 2
        data = export_webp_bytes(image, quality=mid, lossless=False)
        if len(data) <= max_bytes:
            best_data = data
            best_quality = mid
            low = mid + 1
        else:
            high = mid - 1

    final_data = best_data or export_webp_bytes(image, quality=15, lossless=False)
    output_path.write_bytes(final_data)
    mode = f"quality={best_quality}" if best_quality is not None else "quality=15"
    return best_data is not None, len(final_data) / 1024, mode


def process_logo(input_path: Path, output_dir: Path, max_size_kb: int) -> None:
    """Procesa una imagen individual y la exporta como WEBP transparente."""
    image = Image.open(input_path).convert("RGB")
    background_color = get_corner_background_color(image)
    alpha = clean_alpha_edges(
        create_alpha_from_background(image, background_color, BACKGROUND_TOLERANCE)
    )
    rgba_image = enhance_logo(apply_alpha(image, alpha))

    if CROP_TRANSPARENCY:
        rgba_image = crop_transparency(rgba_image, CROP_MARGIN)

    output_path = output_dir / f"{input_path.stem}.webp"
    current_dimension = INITIAL_MAX_DIMENSION
    best_result = (False, 0.0, "quality=15", current_dimension)

    while current_dimension >= MIN_MAX_DIMENSION:
        candidate = resize_image(rgba_image, current_dimension)
        ok, size_kb, mode = export_webp_with_limit(candidate, output_path, max_size_kb)
        best_result = (ok, size_kb, mode, current_dimension)
        if ok:
            break
        current_dimension = int(current_dimension * REDUCTION_STEP)

    ok, size_kb, mode, dimension = best_result
    status = "OK" if ok else "AVISO"
    print(
        f"[{status}] {input_path.name} -> {output_path.name} | "
        f"{size_kb:.2f} KB | {mode} | max_dim={dimension}"
    )


def main() -> None:
    """Ejecuta el flujo completo sobre todas las imagenes de entrada."""
    args = parse_args()
    input_dir = args.input
    output_dir = args.output

    if not input_dir.exists():
        print("La carpeta de entrada no existe:")
        print(input_dir)
        return

    output_dir.mkdir(parents=True, exist_ok=True)
    files = [path for path in input_dir.iterdir() if is_image(path)]

    if not files:
        print("No se encontraron imagenes.")
        return

    print(f"Procesando {len(files)} imagen(es)...\n")

    for file_path in files:
        try:
            process_logo(file_path, output_dir, args.max_size_kb)
        except Exception as error:
            print(f"[ERROR] {file_path.name}: {error}")

    print("\nProceso finalizado.")


if __name__ == "__main__":
    main()
