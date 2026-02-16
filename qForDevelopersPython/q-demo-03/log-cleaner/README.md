# log-cleaner

A tiny multi-file Python project for practicing Amazon Q Developer workflows:

- navigating a project
- understanding structure quickly
- test-first debugging
- adding unit + integration-style tests
- making small, reviewable changes

## What it does

`logcleaner` reads one or more `.log` files, parses log lines, and produces a JSON summary report:

- total lines processed
- counts by level (INFO/WARN/ERROR)
- counts by component
- a few example error messages

## Quickstart

### 1) Install

From the repo root:

```bash
python -m venv .venv
source .venv/bin/activate  # (Windows: .venv\Scripts\activate)
pip install -e ".[dev]"
```
