GIT_VERSION = 2.9
NODE_VERSION = 14.16
POETRY_VERSION = 1.1.5
PYTHON_VERSION = 3.7

# Managing
# ========
.PHONY: poetry
poetry:
	curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python - --version $(POETRY_VERSION)

.PHONY: venv-with-dependencies
venv-with-dependencies:
	python$(PYTHON_VERSION) -m venv .venv
	poetry run pip install --upgrade pip
	poetry install

.PHONY: ispezione
ispezione:
	poetry run python scripts/ispettore.py git@$(GIT_VERSION) node@$(NODE_VERSION) poetry@$(POETRY_VERSION) python@$(PYTHON_VERSION)

# Building
# ========
.PHONY: build
build:
	COMPOSE_DOCKER_CLI_BUILD=1 DOCKER_BUILDKIT=1 docker-compose build --parallel $(service)

.PHONY: build-ci
build-ci:
	COMPOSE_DOCKER_CLI_BUILD=1 DOCKER_BUILDKIT=1 docker-compose --file docker-compose.ci.yaml build --parallel $(service)

.PHONY: build-production
build-production:
	COMPOSE_DOCKER_CLI_BUILD=1 DOCKER_BUILDKIT=1 docker-compose --file docker-compose.production.yaml build --parallel $(service)

# Testing
# =======
.PHONY: pytests
pytests:
	docker-compose --file docker-compose.ci.yaml run web python manage.py test --noinput --debug-mode

.PHONY: cypress
cypress:
	docker-compose --file docker-compose.ci.yaml run cypress npm run tests

# Linting
# =======
.PHONY: black
black:
	poetry run black estudio scripts --check

.PHONY: black!
black!:
	poetry run black estudio scripts

.PHONY: flake8
flake8:
	poetry run flake8 estudio scripts

.PHONY: isort
isort:
	poetry run isort estudio scripts --check

.PHONY: isort!
isort!:
	poetry run isort estudio scripts

.PHONY: pylint
pylint:
	cd estudio && poetry run pylint --rcfile=../.pylintrc *

.PHONY: pylinters
pylinters: black flake8 isort pylint

.PHONY: markdownlint
markdownlint:
	npx markdownlint **/*.md --ignore node_modules

.PHONY: markdownlint!
markdownlint!:
	npx markdownlint **/*.md --ignore node_modules --fix


.PHONY: allint
allint: pylinters markdownlint

