# this should make it easier to run/use project
# ! does not play well with Windows (use wsl command before running)

SHELL := /bin/bash

include .env


.PHONY: help
help: ## show this help
	@egrep -h '\s##\s' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

.PHONY: install
install: ## install any requirements
	python -m pip install -r requirements.txt

migrate: ## make any migrations
	python manage.py migrate

.PHONY: run
run: ## run the server
	python manage.py runserver

.PHONY: start
start: install migrate run ## does "install", "migrate", and "run" commands

.PHONY: clean
clean: ## deletes any .pyc files
	find . -type f -name *.pyc -delete

.PHONY: add-admin
add-admin: ## adds a superuser
	python manage.py createsuperuser