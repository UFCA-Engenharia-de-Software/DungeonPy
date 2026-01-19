commit:
	uv run cz commit

tests:
	pytest tests/

lint-check:
	uv run ruff check

lint-fix:
	uv run ruff check --fix
