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

test:
	poetry run pytest

# example: make test-path path=cars/tests/test_models.py
test-path:
	poetry run pytest ${path}

shell:
	poetry run python manage.py shell

all_test:
	python manage.py test -v 2

# example: path=cars.tests.test_views
part_test:
	python manage.py test ${path} -v 2

part_test_keepdb:
	python manage.py test ${path} -v 2 --keepdb

update: install migrate ;

check:
	poetry run python manage.py check