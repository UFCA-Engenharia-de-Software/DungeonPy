commit:
	uv run cz commit

test:
	uv run pytest ./tests

lint:
	uv run ruff check . --fix
	uv run ruff format
