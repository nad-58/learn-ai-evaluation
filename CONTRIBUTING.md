# Contributing

Contributions that improve tutorials, examples, tests, diagrams, and documentation are welcome.

## Development setup

```bash
python -m venv .venv
pip install -r requirements.txt
pip install -r requirements-dev.txt
python -m pytest tests/ -q
```

## Guidelines

- Keep changes focused and clearly explained.
- Add tests for new Python behaviour.
- Use type hints and docstrings in reusable modules.
- Make examples runnable from the repository root.
- Use original, synthetic, or publicly shareable content.

## Commit prefixes

Use `feat:`, `fix:`, `docs:`, `test:`, `refactor:`, or `chore:`.

## Pull requests

Describe the purpose, files changed, tests run, and known limitations.
