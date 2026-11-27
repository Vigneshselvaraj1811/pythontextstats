# API reference

All public functions accept a `str` and raise `TypeError` for other input
types. They do not modify the input. The package has no runtime dependencies.

```python
import pythontextstats as pts
```

## Counting

### `word_count(text: str) -> int`

Counts tokens matched by Unicode word characters. Internal straight or curly
apostrophes remain part of a word: `don't` and `don’t` each count as one.
Hyphens separate words. Digits and underscores are word characters.

### `sentence_count(text: str) -> int`

Counts nonempty segments separated by one or more `.`, `!`, or `?`
characters. Text without terminal punctuation counts as one sentence if it
contains non-whitespace characters. Punctuation-only input counts as zero.
Abbreviations and decimal points are not recognized specially.

### `paragraph_count(text: str) -> int`

Counts blocks of nonblank lines. Blank lines, including lines containing only
spaces or tabs, separate blocks. Empty or whitespace-only input returns zero.

### `line_count(text: str) -> int`

Counts logical lines. An empty string has zero lines. A trailing newline adds
a final empty line, so `line_count("a\n") == 2`. Python's `splitlines`
rules recognize common newline formats.

### `character_count(text: str) -> int`

Counts Unicode characters whose `isspace()` value is false. This excludes
spaces, tabs, newlines, carriage returns, and other Unicode whitespace.

### `syllable_count(text: str) -> int`

Estimates English syllables by counting vowel groups in each token, with a
simple final-`e` adjustment. Accented Latin letters are normalized before
counting. This is an approximation, especially for proper names, acronyms,
numbers, and non-English text.

## Vocabulary

### `word_frequency(text: str) -> dict[str, int]`

Returns token counts after Unicode case folding. Keys are ordered by
descending count and then alphabetical spelling for ties.

```python
pts.word_frequency("Hello hello, world")
# {"hello": 2, "world": 1}
```

### `unique_word_count(text: str) -> int`

Returns the number of keys in `word_frequency(text)`.

### `lexical_diversity(text: str) -> float`

Returns `unique_word_count(text) / word_count(text)`. Empty text returns
`0.0`. This simple type-token ratio depends on text length; compare texts
of similar lengths.

### `average_word_length(text: str) -> float`

Returns the mean number of Unicode characters in matched tokens. Internal
apostrophes are included in token length. Empty text returns `0.0`.

## Reading estimates

### `reading_time(text: str, wpm: float = 200) -> float`

Returns estimated minutes as `word_count(text) / wpm`. `wpm` must be a
positive, finite `int` or `float`; zero, negative values, infinity, and
NaN raise `ValueError`. Non-numeric values and booleans raise `TypeError`.

### `flesch_reading_ease(text: str) -> float`

Returns the Flesch Reading Ease estimate, rounded to two decimal places:

```text
206.835 - 1.015 × (words / sentences) - 84.6 × (syllables / words)
```

### `flesch_kincaid_grade(text: str) -> float`

Returns the Flesch-Kincaid grade estimate, rounded to two decimal places:

```text
0.39 × (words / sentences) + 11.8 × (syllables / words) - 15.59
```

Both functions return `0.0` when no words or sentences are found. Scores can
be outside familiar ranges for very short or unusual text.

## Combined analysis

### `analyze(text: str, wpm: float = 200) -> TextAnalysis`

Calculates every metric in one pass over the tokens. `TextAnalysis` is a
frozen dataclass with fields named after the metrics above and a
`word_frequencies` dictionary. Its `as_dict()` method returns a separate
dictionary suitable for JSON serialization.

```python
import json
from pythontextstats import analyze

report = analyze("Hello hello. Welcome!", wpm=180)
print(report.word_count)
print(json.dumps(report.as_dict(), ensure_ascii=False))
```

The dataclass prevents reassigning fields. Its nested frequency dictionary
remains a normal mutable dictionary, so treat the result as a value object
and avoid modifying that field.
