# Contributing

Thanks for your interest in `agent-observer`!

## Setup

```bash
git clone https://github.com/darshjme-codes/agent-observer
cd agent-observer
pip install -e ".[dev]"
pip install pytest
```

## Running Tests

```bash
PYTHONPATH=src python -m pytest tests/ -v
```

All 36 tests must pass before opening a PR.

## Guidelines

- **Zero deps** — no new runtime dependencies; stdlib only
- **Tests required** — every new feature or bugfix must include tests
- **Type hints** — use `from __future__ import annotations` + PEP 604 union syntax
- **Docstrings** — public API must be documented
- **Style** — follow existing code conventions; no linter config wars

## Pull Requests

1. Fork → branch → implement → test → PR
2. Describe *what* and *why* in the PR description
3. Reference any related issues

## Reporting Issues

Open a GitHub issue with a minimal reproducer.
