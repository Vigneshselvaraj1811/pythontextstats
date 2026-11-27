"""Dependency-free tools for English text statistics."""

from .core import (
    TextAnalysis,
    analyze,
    average_word_length,
    character_count,
    flesch_kincaid_grade,
    flesch_reading_ease,
    lexical_diversity,
    line_count,
    paragraph_count,
    reading_time,
    sentence_count,
    syllable_count,
    unique_word_count,
    word_count,
    word_frequency,
)

__version__ = "2.0.0a1"

__all__ = [
    "TextAnalysis", "analyze", "average_word_length", "character_count",
    "flesch_kincaid_grade", "flesch_reading_ease", "lexical_diversity",
    "line_count", "paragraph_count", "reading_time", "sentence_count",
    "syllable_count", "unique_word_count", "word_count", "word_frequency",
]
