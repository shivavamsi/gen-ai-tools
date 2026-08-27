# Makefile Reference

## Standard Makefile

```makefile
.PHONY: help install dev test lint format type-check clean build publish

help:
	@echo "Commands: dev test lint format type-check clean build publish"

dev:
	uv sync --extra dev --extra docs
	pre-commit install

test:
	uv run pytest

# lint must stay read-only and mirror CI exactly — no --fix here (that belongs in
# `format`). An auto-fixing lint target mutates files and exits 0, hiding real
# violations that CI's read-only check then fails on.
lint:
	uv run ruff check src tests
	uv run ruff format --check src tests   # formatting is NOT covered by ruff check

format:
	uv run ruff format src tests
	uv run ruff check --fix src tests

type-check:
	uv run mypy src

clean:
	rm -rf build dist *.egg-info .pytest_cache .mypy_cache .ruff_cache .coverage htmlcov
	find . -type d -name __pycache__ -exec rm -rf {} +

build: clean
	uv build

publish: build
	uvx twine upload dist/*
```

Every target runs through `uv run` so it uses the environment `uv sync` created —
a bare `pytest`/`ruff` only resolves when the venv happens to be activated, which
is exactly the local-vs-CI divergence the lint rules above are guarding against.
Tools that aren't project dependencies (`twine`) run via `uvx` in a throwaway env.

## Additional Targets

```makefile
# Documentation
docs:
	cd docs && make html

docs-serve:
	uv run python -m http.server --directory docs/_build/html

# Coverage report
coverage:
	uv run pytest --cov-report=html
	open htmlcov/index.html

# Security scanning
security:
	uv run python scripts/security_scan.py .
```
