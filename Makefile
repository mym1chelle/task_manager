install:
	poetry install

dev:
	poetry run python manage.py runserver

makemigrations:
	poetry run python manage.py makemigrations

migrate:
	poetry run python manage.py migrate

lint:
	poetry run flake8 test_api

test:
	poetry run python manage.py test

test-coverage:
	poetry run coverage run --source=. manage.py test && poetry run coverage xml