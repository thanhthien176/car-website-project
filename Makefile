.PHONY: run test migrate shell

# make add pkg=requests: add requests package
add:
	poetry add $(pkg)

config-venv:
	poetry config virtualenvs.in-project true	

install:
	poetry install

runserver:
	poetry run python manage.py runserver

migrations:
	poetry run python manage.py makemigrations

migrate:
	poetry run python manage.py migrate

superuser:
	poetry run python manage.py createsuperuser

shell:
	poetry run python manage.py shell

update: install migrate ;

check:
	poetry run python manage.py check


# ==========Test===============
pytest:
	poetry run pytest

# example: make test-path path=cars/tests/test_models.py
pytest-path:
	poetry run pytest ${path}

test_django:
	python manage.py test -v 2

# example: path=cars.tests.test_views
part_test_dj:
	python manage.py test ${path} -v 2

part_test_keepdb:
	python manage.py test ${path} -v 2 --keepdb

test_cover:
	pytest --cov --cov-report=term-missing