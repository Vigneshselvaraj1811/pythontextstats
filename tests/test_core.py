import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

import pythontextstats as pts


class TextStatsTests(unittest.TestCase):
    def test_existing_api_on_basic_text(self):
        text = "Hello world. Read this!"
        self.assertEqual(pts.word_count(text), 4)
        self.assertEqual(pts.sentence_count(text), 2)
        self.assertEqual(pts.reading_time(text), 0.02)
        self.assertIsInstance(pts.flesch_reading_ease(text), float)
        self.assertIsInstance(pts.flesch_kincaid_grade(text), float)

    def test_contractions_and_casefolded_frequency(self):
        text = "Don't stop. don't stop!"
        self.assertEqual(pts.word_count(text), 4)
        self.assertEqual(pts.word_frequency(text), {"don't": 2, "stop": 2})
        self.assertEqual(pts.unique_word_count(text), 2)
        self.assertEqual(pts.lexical_diversity(text), 0.5)

    def test_unicode_whitespace_and_paragraphs(self):
        text = "First\r\n\r\nSecond\u00a0line\n"
        self.assertEqual(pts.character_count(text), 15)
        self.assertEqual(pts.paragraph_count(text), 2)
        self.assertEqual(pts.line_count(text), 4)

    def test_syllables_keep_accented_vowel(self):
        self.assertEqual(pts.syllable_count("café"), 2)
        self.assertEqual(pts.syllable_count("table"), 2)
        self.assertEqual(pts.syllable_count("make"), 1)

    def test_empty_and_invalid_inputs(self):
        result = pts.analyze("")
        self.assertEqual(result.word_count, 0)
        self.assertEqual(result.lexical_diversity, 0)
        self.assertEqual(result.word_frequencies, {})
        with self.assertRaises(TypeError):
            pts.word_count(None)
        with self.assertRaises(ValueError):
            pts.reading_time("word", 0)
        with self.assertRaises(ValueError):
            pts.reading_time("word", float("nan"))

    def test_analyze_agrees_with_individual_functions(self):
        text = "One line.\n\nAnother line!"
        result = pts.analyze(text, wpm=100)
        self.assertEqual(result.word_count, pts.word_count(text))
        self.assertEqual(result.sentence_count, pts.sentence_count(text))
        self.assertEqual(result.syllable_count, pts.syllable_count(text))
        self.assertEqual(result.reading_time, pts.reading_time(text, 100))
        self.assertEqual(result.flesch_reading_ease, pts.flesch_reading_ease(text))
        self.assertEqual(result.flesch_kincaid_grade, pts.flesch_kincaid_grade(text))

    def test_cli_reads_file_and_returns_json(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "sample.txt"
            path.write_text("Hello hello world.", encoding="utf-8")
            completed = subprocess.run(
                [sys.executable, "-m", "pythontextstats", str(path), "--json", "--top", "1"],
                check=True, capture_output=True, text=True,
            )
        result = json.loads(completed.stdout)
        self.assertEqual(result["word_count"], 3)
        self.assertEqual(result["word_frequencies"], {"hello": 2})


if __name__ == "__main__":
    unittest.main()
