.DEFAULT_GOAL := help
SHELL := /bin/sh
ENV ?= dev
SERVICE ?= app

DC ?= docker compose -f stack/docker/docker-compose.y*ml -f stack/docker/docker-compose.${ENV}.y*ml

help: ## Show this help
	@echo -e "$$(grep -hE '^\S+:.*##' $(MAKEFILE_LIST) | sed -e 's/:.*##\s*/:/' -e 's/^\(.\+\):\(.*\)/\\x1b[36m\1\\x1b[m:\2/' | column -c2 -t -s :)"

whereami: ## Show current environment
	@echo ${ENV}

push: ## Push docker containers
	${DC} push ${SERVICE}

build: ## Build docker containers
	${DC} build

up: ## Start docker containers
	${DC} up -d

run: ## Start docker containers attached
	${DC} up

down: ## Shutdown docker containers
	${DC} down

ps: ## List docker containers
	${DC} ps

logs: ## Show docker containers logs
	${DC} logs ${SERVICE}

tail: ## Tail on docker containers logs
	${DC} logs --follow ${SERVICE}

exec: ## Open shell in docker container
	${DC} exec ${SERVICE} sh

shell: ## Open shell in docker container
	${DC} run --rm ${SERVICE} sh

context: ## Show docker contexts
	docker context ls

generate-dist: ## Generate Dist from .env file
	cat ${FILE} | grep -o '.*=' > ${FILE}.dist

repl: build run ## Start a read-eval-print-loop

test: ## Run tests

cs: ## Run code style checks
	${DC} run --rm ${SERVICE} poetry run black --check .

format: ## Format code
	${DC} run --rm ${SERVICE} poetry run black .

type-check: ## Run type checks
	${DC} run --rm ${SERVICE} poetry run pyright .

lint: ## Run linting
	${DC} run --rm ${SERVICE} poetry run pylint .

unit: ## Run code coverage
	${DC} run --rm ${SERVICE} poetry run coverage run -a -m pytest -vvv

functional: ## Run code coverage
	${DC} run --rm ${SERVICE} poetry run coverage run -a -m behave

coverage: ## Run code coverage
	${DC} run --rm ${SERVICE} poetry run coverage report

coverage-html: ## Run code coverage
	${DC} run --rm ${SERVICE} poetry run coverage html

check: cs lint type-check unit functional coverage ## Run all checks

cicd: ## Run cicd pipeline
	${DC} run --rm ${SERVICE} poetry run invoke cicd
