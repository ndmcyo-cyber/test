# App zur automatischen Bildanalyse

Diese Python-App analysiert Bilder automatisch und gibt strukturierte Ergebnisse als JSON aus.

## Hinweis zum Format

In dieser Offline-Umgebung arbeitet die App **ohne externe Bibliotheken** und unterstützt daher aktuell **ASCII-PPM/PGM** (`P3`/`P2`).

## Funktionen

- Bildmetadaten (Format, Modus, Breite, Höhe)
- Helligkeit (durchschnittlich)
- Kontrast (Standardabweichung der Luminanz)
- Dominante Farben (Top-N RGB-Werte)
- Vorschlag einer einfachen Bildkategorie auf Basis von Helligkeit/Kontrast

## Nutzung

```bash
python app.py --image ./beispiel.ppm --top-colors 5
```

Optional als Datei speichern:

```bash
python app.py --image ./beispiel.ppm --output result.json
```

## Beispielausgabe

```json
{
  "path": "beispiel.ppm",
  "metadata": {
    "format": "PPM",
    "mode": "RGB",
    "width": 2,
    "height": 2
  },
  "brightness": 61.41,
  "contrast": 38.66,
  "dominant_colors": [
    {"rgb": [255, 0, 0], "ratio": 0.75},
    {"rgb": [0, 0, 255], "ratio": 0.25}
  ],
  "category_hint": "balanced_scene"
}
```

## Tests

```bash
python -m unittest discover -s tests -v
```
