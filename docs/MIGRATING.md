# Migrating from 0.1.x to 2.0

Version `2.0.0a1` is a preview. Update tests that assert exact counts before
switching from the published `0.1.3` release.

## Existing API

The following callables retain their names and basic signatures:
`word_count`, `sentence_count`, `average_word_length`, `reading_time`,
`character_count`, `syllable_count`, `flesch_reading_ease`, and
`flesch_kincaid_grade`.

## Behavior changes

| Area | 0.1.x | 2.0 preview |
| --- | --- | --- |
| Contractions | `don't` counted as two words | Counts as one word |
| Characters | Excluded spaces, tabs, and newlines | Excludes all Unicode whitespace, including carriage returns |
| Syllables | Basic vowel grouping | Normalizes accented Latin letters and handles final `-le` |
| Reading speed | Zero raised `ZeroDivisionError` | Invalid values raise `ValueError` or `TypeError` |
| Package metadata | `setup.py`, Python ≥3.6 | `pyproject.toml`, Python ≥3.9 |

Readability scores can change because they depend on word and syllable counts.
If your application requires the old values, pin `pythontextstats<2` until
you have updated your expectations.

## New capabilities

- `analyze(text, wpm=200)` returns a `TextAnalysis` result containing all
  metrics.
- `word_frequency`, `unique_word_count`, and `lexical_diversity` describe
  vocabulary.
- `paragraph_count` and `line_count` describe document structure.
- `pythontextstats` and `python -m pythontextstats` provide a CLI with file,
  piped-input, plain-text, and JSON output.

## Installation

Until a v2 release is published, install the branch from GitHub or from a
local checkout. The PyPI command `pip install pythontextstats` still installs
0.1.3.
