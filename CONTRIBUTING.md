# Contributing

Thanks for helping improve Python Text Stats. Bug reports and focused pull
requests are welcome.

## Development setup

Use Python 3.9 or newer. From the repository root:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -e .
python -m unittest discover -s tests -v
```

On Windows, activate with `.venv\Scripts\activate`.

## Before opening a pull request

1. Add or update tests for behavior changes, especially tokenization and
   readability edge cases.
2. Update the API reference and migration guide when public behavior changes.
3. Run `python -m unittest discover -s tests -v`.
4. If packaging changed, install `build` and run `python -m build`.

Keep the core free of runtime dependencies. The readability functions are
English estimates; describe their limits when proposing new metrics.

## Reporting bugs

Open a GitHub issue with the Python version, package version, input text,
expected result, and actual result. Remove private text from examples before
posting.
