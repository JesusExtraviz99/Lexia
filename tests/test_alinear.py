import json
from pathlib import Path
import unittest
from scripts.alinear import align, tokens, observed_words

ROOT = Path(__file__).resolve().parents[1]


def words(text):
    return [{"word": w} for w in tokens(text)]


class AlignmentTests(unittest.TestCase):
    def test_case_punctuation_accents(self):
        rows, distance = align(tokens("¡Ana salió!"), words("ana salió"))
        self.assertEqual(distance, 0)
        self.assertEqual([r["story_index"] for r in rows], [1, 2])
        _, distance = align(tokens("sí"), words("si"))
        self.assertEqual(distance, 1)

    def test_repeated_phrase(self):
        rows, distance = align(tokens("el gato duerme"), words("el gato el gato duerme"))
        self.assertEqual(distance, 2)
        repeated = [r for r in rows if r["type"] == "repeticion_candidata"]
        self.assertEqual([r["repeated_story_index"] for r in repeated], [1, 2])

    def test_insertion_is_not_always_repetition(self):
        rows, _ = align(tokens("el gato duerme"), words("el pequeño gato duerme"))
        self.assertEqual(sum(r["type"] == "insercion_candidata" for r in rows), 1)

    def test_omission_without_fabricated_times(self):
        rows, _ = align(tokens("Ana salió"), [])
        self.assertTrue(all(r["type"] == "omision_candidata" and r["start"] is None for r in rows))

    def test_real_recordings(self):
        expected = tokens((ROOT / "datos/textos/lectura_01.txt").read_text(encoding="utf-8"))
        cases = [("lectura_20261014_081816_009646_20261014_082118_900314.json", 0),
                 ("lectura_20261014_082953_219058_20261014_083013_046227.json", 3)]
        for name, target in cases:
            raw = json.loads((ROOT / "resultados" / name).read_text(encoding="utf-8"))
            rows, distance = align(expected, observed_words(raw))
            self.assertEqual(distance, target)
            if target:
                differences = [r for r in rows if r["type"] != "coincidencia"]
                self.assertEqual([r["type"] for r in differences],
                                 ["repeticion_candidata", "omision_candidata", "sustitucion_candidata"])
                self.assertEqual(differences[1]["story_word"], "despacio")
                self.assertIsNone(differences[1]["start"])
                self.assertEqual(differences[2]["story_word"], "silencio")
                self.assertEqual(differences[2]["asr_word"], "cinesio")


if __name__ == "__main__":
    unittest.main()
