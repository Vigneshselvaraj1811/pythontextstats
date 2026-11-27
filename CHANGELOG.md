# Changelog

All notable changes to this project are documented here. Versions before 2.0
are summarized from the published release history.

## 2.0.0a1 — unreleased

### Added

- Combined `analyze()` API and `TextAnalysis` result.
- Word frequency, unique word count, lexical diversity, line count, and
  paragraph count.
- Command-line interface for files, piped input, and JSON output.
- Automated tests and GitHub Actions checks.
- API reference, migration guide, and contributor documentation.

### Changed

- Contractions count as one token.
- Character counts exclude all Unicode whitespace.
- Syllable estimation normalizes accented Latin letters and handles final
  `-le` words.
- Invalid reading speed values raise descriptive exceptions.
- Packaging uses `pyproject.toml` and requires Python 3.9 or newer.

### Fixed

- Example imports the correct package.
- Repository URL and missing MIT license text.

## 0.1.3 — 2025-06-02

Latest published 0.1.x release.
