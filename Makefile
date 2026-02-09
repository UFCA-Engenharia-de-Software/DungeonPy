commit:
	uv run cz commit

run:
	uv run python main.py

test:
	uv run pytest ./tests

lint:
	uv run ruff check . --fix
	uv run ruff format

setup:
	uv sync
	uv run pre-commit install
	uv run pre-commit install --hook-type commit-msg
	@echo "✅ Ambiente configurado! Pre-commit hooks instalados."
