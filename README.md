# Python Text Stats

Text statistics and English readability estimates for Python, with no runtime
dependencies. Analyze a string with individual functions, collect every metric
in one result, or use the command line.

> **Preview release:** Version `2.0.0a1` is an alpha release. Install it
> explicitly; the default install selects the latest stable release.

## Requirements and installation

Python 3.9 or newer is required for v2. To install this preview from PyPI:

```bash
python -m pip install "pythontextstats==2.0.0a1"
```

To work from source:

```bash
git clone https://github.com/Vigneshselvaraj1811/pythontextstats.git
cd pythontextstats
python -m pip install -e .
```

`python -m pip install pythontextstats` selects the latest stable release.
Until a stable v2 release exists, that is `0.1.3`.

## Quick start

```python
import pythontextstats as pts

text = "Hello world! Don't stop reading."

print(pts.word_count(text))          # 5
print(pts.word_frequency(text))      # {"don't": 1, ...}

report = pts.analyze(text, wpm=200)
print(report.reading_time)           # Minutes
print(report.flesch_reading_ease)    # English readability estimate
print(report.as_dict())              # JSON-ready dictionary
```

## Available metrics

| Metric | Python function | Meaning |
| --- | --- | --- |
| Words | `word_count` | Tokens, with contractions kept together |
| Unique words | `unique_word_count` | Distinct tokens after case folding |
| Frequencies | `word_frequency` | Counts ordered by frequency, then spelling |
| Sentences | `sentence_count` | Nonempty text segments separated by `.`, `!`, or `?` |
| Paragraphs | `paragraph_count` | Nonblank blocks separated by blank lines |
| Lines | `line_count` | Logical lines, including a final empty line |
| Characters | `character_count` | Unicode characters excluding whitespace |
| Syllables | `syllable_count` | Approximate English syllables |
| Average word length | `average_word_length` | Mean token length in characters |
| Lexical diversity | `lexical_diversity` | Unique words divided by all words |
| Reading time | `reading_time` | Minutes at a configurable words-per-minute rate |
| Readability | `flesch_reading_ease`, `flesch_kincaid_grade` | English readability estimates |

`analyze(text, wpm=200)` returns all of these metrics as a frozen
`TextAnalysis` object. See the
[API reference](https://github.com/Vigneshselvaraj1811/pythontextstats/blob/main/docs/API.md)
for return types,
empty-input behavior, and validation rules.

## Command line

```bash
python -m pythontextstats --text "Hello world!" --json
python -m pythontextstats article.txt --top 5
cat article.txt | python -m pythontextstats
```

Installing the package also provides the `pythontextstats` command. It reads
UTF-8 files or piped text and prints a readable summary by default. Use
`--json` for machine-readable output, `--wpm` for reading speed, and
`--top` to limit the frequency list. Run `python -m pythontextstats --help`
for all options.

## Accuracy and scope

The library uses deterministic rules, not language detection or a dictionary.
Word matching includes Unicode word characters and treats apostrophes inside
words as part of a token. Sentence counting does not recognize abbreviations,
decimals, or dialogue. Syllable counts are heuristics for English and may be
inaccurate for names, borrowed words, and non-English text. Readability scores
inherit those limits. Use them as estimates, not a measure of comprehension.

## Moving from 0.1.x

The eight original function names remain available. Several edge cases changed
in v2, including contractions, whitespace handling, and invalid `wpm` values.
Read the
[migration guide](https://github.com/Vigneshselvaraj1811/pythontextstats/blob/main/docs/MIGRATING.md)
before upgrading an application
that depends on exact counts.

## Development

```bash
python -m unittest discover -s tests -v
python -m build
```

Build artifacts go in `dist/` and are ignored by Git. See
[CONTRIBUTING.md](https://github.com/Vigneshselvaraj1811/pythontextstats/blob/main/CONTRIBUTING.md)
for the development workflow and
[CHANGELOG.md](https://github.com/Vigneshselvaraj1811/pythontextstats/blob/main/CHANGELOG.md)
for release history. Maintainers can use the
[release guide](https://github.com/Vigneshselvaraj1811/pythontextstats/blob/main/docs/RELEASING.md)
for PyPI publishing.

## License

MIT. See [LICENSE](https://github.com/Vigneshselvaraj1811/pythontextstats/blob/main/LICENSE).
