.PHONY: lint ruff mypy pylint format

lint: ruff mypy pylint
	
format:
	uv run ruff format

ruff:
	uv run ruff check
mypy:
	uv run mypy ./autoexpense3/
	uv run mypy ./tests/
	uv run mypy ./app.py
pylint:
	uv run pylint ./autoexpense3/
	uv run pylint ./tests/
