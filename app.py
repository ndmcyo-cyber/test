from __future__ import annotations

import argparse
import json
from pathlib import Path

from image_analyzer import analyze_image


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Automatische Bildanalyse")
    parser.add_argument("--image", required=True, help="Pfad zum Bild")
    parser.add_argument(
        "--top-colors", type=int, default=5, help="Anzahl dominanter Farben"
    )
    parser.add_argument(
        "--output", type=str, default="", help="Optionaler Pfad für JSON-Output"
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    result = analyze_image(args.image, top_colors=args.top_colors)
    text = json.dumps(result, ensure_ascii=False, indent=2)

    if args.output:
        output_path = Path(args.output)
        output_path.write_text(text + "\n", encoding="utf-8")
        print(f"Analyse gespeichert: {output_path}")
    else:
        print(text)


if __name__ == "__main__":
    main()
