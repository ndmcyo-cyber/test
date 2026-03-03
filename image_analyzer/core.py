from __future__ import annotations

from collections import Counter
from pathlib import Path
from typing import Any


def _category_hint(brightness: float, contrast: float) -> str:
    if brightness < 60:
        return "dark_scene"
    if brightness > 190:
        return "bright_scene"
    if contrast < 25:
        return "low_detail"
    if contrast > 70:
        return "high_detail"
    return "balanced_scene"


def _tokenize_ppm_pgm(data: bytes) -> list[str]:
    text = data.decode("ascii", errors="strict")
    cleaned = []
    for line in text.splitlines():
        line = line.split("#", 1)[0].strip()
        if line:
            cleaned.append(line)
    return " ".join(cleaned).split()


def _parse_ascii_ppm_pgm(path: Path) -> tuple[str, int, int, list[tuple[int, int, int]]]:
    tokens = _tokenize_ppm_pgm(path.read_bytes())
    if len(tokens) < 4:
        raise ValueError("Invalid PPM/PGM file")

    magic = tokens[0]
    if magic not in {"P2", "P3"}:
        raise ValueError("Only ASCII PPM/PGM (P2/P3) are supported")

    width = int(tokens[1])
    height = int(tokens[2])
    maxval = int(tokens[3])
    values = [int(v) for v in tokens[4:]]

    if maxval <= 0:
        raise ValueError("Invalid max value")

    if magic == "P2":
        if len(values) != width * height:
            raise ValueError("Invalid pixel count for P2")
        pixels = [(v, v, v) for v in values]
        mode = "L"
        fmt = "PGM"
    else:
        if len(values) != width * height * 3:
            raise ValueError("Invalid pixel count for P3")
        pixels = list(zip(values[0::3], values[1::3], values[2::3]))
        mode = "RGB"
        fmt = "PPM"

    if maxval != 255:
        scale = 255 / maxval
        pixels = [
            (
                max(0, min(255, round(r * scale))),
                max(0, min(255, round(g * scale))),
                max(0, min(255, round(b * scale))),
            )
            for r, g, b in pixels
        ]

    return fmt, width, height, pixels if mode == "RGB" else pixels


def analyze_image(path: str | Path, top_colors: int = 5) -> dict[str, Any]:
    image_path = Path(path)
    if not image_path.exists():
        raise FileNotFoundError(f"Image not found: {image_path}")

    fmt, width, height, pixels = _parse_ascii_ppm_pgm(image_path)

    luminance = [0.299 * r + 0.587 * g + 0.114 * b for r, g, b in pixels]
    brightness = sum(luminance) / len(luminance)
    mean = brightness
    contrast = (sum((v - mean) ** 2 for v in luminance) / len(luminance)) ** 0.5

    color_counts = Counter(pixels)
    total_pixels = len(pixels)
    dominant = [
        {
            "rgb": [int(c[0]), int(c[1]), int(c[2])],
            "ratio": round(count / total_pixels, 4),
        }
        for c, count in color_counts.most_common(max(1, top_colors))
    ]

    return {
        "path": str(image_path),
        "metadata": {
            "format": fmt,
            "mode": "RGB",
            "width": width,
            "height": height,
        },
        "brightness": round(brightness, 2),
        "contrast": round(contrast, 2),
        "dominant_colors": dominant,
        "category_hint": _category_hint(brightness, contrast),
    }
