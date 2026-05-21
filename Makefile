.PHONY: run test migrate shell

# make add pkg=requests: add requests package
add:
	poetry add $(pkg)

install:
	poetry install

run-server:
	poetry run python manage.py runserver

migrations:
	poetry run python manage.py makemigrations

migrate:
	poetry run python manage.py migrate

superuser:
	poetry run python manage.py createsuperuser

test:
	poetry run pytest

# example: make test-path path=cars/tests/test_models.py
test-path:
	poetry run pytest ${path}

shell:
	poetry run python manage.py shell

update: install migrate ;