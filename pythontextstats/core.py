"""Core text metrics. Readability and syllable estimates target English."""

import re
import unicodedata
from collections import Counter
from dataclasses import asdict, dataclass
from typing import Dict

_WORD_RE = re.compile(r"\b\w+(?:['’]\w+)*\b", re.UNICODE)
_SENTENCE_RE = re.compile(r"[.!?]+")
_VOWEL_GROUP_RE = re.compile(r"[aeiouy]+")


def _require_text(text: str) -> str:
    if not isinstance(text, str):
        raise TypeError("text must be a string")
    return text


def _tokens(text: str):
    return _WORD_RE.findall(_require_text(text))


def _validate_wpm(wpm: float) -> float:
    if isinstance(wpm, bool) or not isinstance(wpm, (int, float)):
        raise TypeError("wpm must be a positive number")
    if not 0 < wpm < float("inf"):
        raise ValueError("wpm must be a positive, finite number")
    return float(wpm)


def word_count(text: str) -> int:
    """Count words, keeping contractions together."""
    return len(_tokens(text))


def sentence_count(text: str) -> int:
    """Count nonempty fragments separated by periods, exclamation or question marks."""
    return sum(bool(part.strip()) for part in _SENTENCE_RE.split(_require_text(text)))


def average_word_length(text: str) -> float:
    """Return mean characters per word, or 0 for empty text."""
    words = _tokens(text)
    return sum(map(len, words)) / len(words) if words else 0.0


def reading_time(text: str, wpm: float = 200) -> float:
    """Estimate reading time in minutes."""
    return word_count(text) / _validate_wpm(wpm)


def character_count(text: str) -> int:
    """Count non-whitespace Unicode characters."""
    return sum(not char.isspace() for char in _require_text(text))


def line_count(text: str) -> int:
    """Count logical lines, including a final blank line after a newline."""
    text = _require_text(text)
    return len(text.splitlines()) + int(text.endswith(("\r", "\n"))) if text else 0


def paragraph_count(text: str) -> int:
    """Count blocks of nonblank lines separated by blank lines."""
    paragraphs = 0
    in_paragraph = False
    for line in _require_text(text).splitlines():
        if line.strip():
            if not in_paragraph:
                paragraphs += 1
            in_paragraph = True
        else:
            in_paragraph = False
    return paragraphs


def _syllables_in_word(word: str) -> int:
    normalized = unicodedata.normalize("NFKD", word.casefold())
    latin = "".join(char for char in normalized if "a" <= char <= "z")
    if not latin:
        return 1
    groups = len(_VOWEL_GROUP_RE.findall(latin))
    if word.casefold().endswith("e") and not re.search(r"[^aeiouy]le$", latin):
        groups -= 1
    return max(1, groups)


def syllable_count(text: str) -> int:
    """Estimate English syllables."""
    return sum(_syllables_in_word(word) for word in _tokens(text))


def _reading_ease(words: int, sentences: int, syllables: int) -> float:
    if not words or not sentences:
        return 0.0
    return round(206.835 - 1.015 * words / sentences - 84.6 * syllables / words, 2)


def _grade_level(words: int, sentences: int, syllables: int) -> float:
    if not words or not sentences:
        return 0.0
    return round(0.39 * words / sentences + 11.8 * syllables / words - 15.59, 2)


def flesch_reading_ease(text: str) -> float:
    """Calculate the English Flesch Reading Ease estimate."""
    words = word_count(text)
    return _reading_ease(words, sentence_count(text), syllable_count(text))


def flesch_kincaid_grade(text: str) -> float:
    """Calculate the English Flesch-Kincaid grade estimate."""
    words = word_count(text)
    return _grade_level(words, sentence_count(text), syllable_count(text))


def word_frequency(text: str) -> Dict[str, int]:
    """Return case-insensitive counts, ordered by frequency then spelling."""
    counts = Counter(word.casefold() for word in _tokens(text))
    return dict(sorted(counts.items(), key=lambda item: (-item[1], item[0])))


def unique_word_count(text: str) -> int:
    """Count distinct words without regard to case."""
    return len(word_frequency(text))


def lexical_diversity(text: str) -> float:
    """Return distinct-word count divided by total-word count."""
    total = word_count(text)
    return unique_word_count(text) / total if total else 0.0


@dataclass(frozen=True)
class TextAnalysis:
    word_count: int
    unique_word_count: int
    sentence_count: int
    paragraph_count: int
    line_count: int
    character_count: int
    syllable_count: int
    average_word_length: float
    lexical_diversity: float
    reading_time: float
    flesch_reading_ease: float
    flesch_kincaid_grade: float
    word_frequencies: Dict[str, int]

    def as_dict(self) -> dict:
        """Return a JSON-ready copy of the result."""
        return asdict(self)


def analyze(text: str, wpm: float = 200) -> TextAnalysis:
    """Calculate all supported metrics in one call."""
    text = _require_text(text)
    rate = _validate_wpm(wpm)
    words = _tokens(text)
    total = len(words)
    sentences = sentence_count(text)
    syllables = sum(_syllables_in_word(word) for word in words)
    counts = Counter(word.casefold() for word in words)
    frequencies = dict(sorted(counts.items(), key=lambda item: (-item[1], item[0])))
    unique = len(frequencies)
    return TextAnalysis(
        word_count=total,
        unique_word_count=unique,
        sentence_count=sentences,
        paragraph_count=paragraph_count(text),
        line_count=line_count(text),
        character_count=character_count(text),
        syllable_count=syllables,
        average_word_length=sum(map(len, words)) / total if total else 0.0,
        lexical_diversity=unique / total if total else 0.0,
        reading_time=total / rate,
        flesch_reading_ease=_reading_ease(total, sentences, syllables),
        flesch_kincaid_grade=_grade_level(total, sentences, syllables),
        word_frequencies=frequencies,
    )
