from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from image_analyzer import analyze_image


class TestAnalyzeImage(unittest.TestCase):
    def test_analyze_simple_ppm_image(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            image_path = Path(tmp) / "simple.ppm"
            image_path.write_text(
                "\n".join(
                    [
                        "P3",
                        "2 2",
                        "255",
                        "255 0 0   255 0 0",
                        "255 0 0   0 0 255",
                    ]
                ),
                encoding="ascii",
            )

            result = analyze_image(image_path, top_colors=3)

            self.assertEqual(result["metadata"]["width"], 2)
            self.assertEqual(result["metadata"]["height"], 2)
            self.assertEqual(result["dominant_colors"][0]["rgb"], [255, 0, 0])
            self.assertAlmostEqual(result["dominant_colors"][0]["ratio"], 0.75, places=4)

    def test_missing_file(self) -> None:
        with self.assertRaises(FileNotFoundError):
            analyze_image("does_not_exist.ppm")


if __name__ == "__main__":
    unittest.main()
