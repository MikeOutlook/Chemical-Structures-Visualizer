# Contributing

## Development setup

```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS / Linux
source .venv/bin/activate
pip install -e .[dev]
```

## Local checks

Run the automated test suite:

```bash
pytest
```

Run a CLI smoke test against the bundled sample dataset:

```bash
python -m chemical_visualizer.cli chemical_structures_data.csv
```

## Pull requests

- Keep changes focused and easy to review.
- Add or update tests when behavior changes.
- Update README or other user-facing docs when workflows change.
- Make sure `pytest` passes before opening a pull request.
