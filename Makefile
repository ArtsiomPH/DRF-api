SHELL=/bin/bash

lint:
	poetry run mypy --sqlite-cache .

test:
	poetry run pytest

check: lint test

format_code:
	poetry run isort .
	poetry run black .

create_admin:
	poetry run python manage.py init_admin