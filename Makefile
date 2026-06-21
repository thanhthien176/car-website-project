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

# =======migrate===========
migrations:
	poetry run python manage.py makemigrations

migrate:
	poetry run python manage.py migrate

migrate-plan:
	poetry run python manage.py migrate --plan

backup_db:
	pg_dump -U <db_user> -h <db_host> carcompare_db > backup_$(date +%Y%m%d_%H%M%S).sqlXac


superuser:
	poetry run python manage.py createsuperuser

collectstatic:
	python manage.py collectstatic --noinput --clear --settings=config.settings.production

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