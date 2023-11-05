# ==============================================================================
# Makefile for movie index docker image.
#
#	This makefile is meant to be used in a directory structure shown below:
#		project_dir/
#    	├── LICENSE
#    	├── Makefile
#    	├── README.md
#    	├── Dockerfile
#    	└── movie-index/
#
# ==============================================================================
TARGET=docker_image
PYTHON_SRC=$(shell find movie_index/ -type f -name '*.py')

# ------------------------------------------------------------------------------
# Rules!
# ------------------------------------------------------------------------------
all: ${TARGET}

${TARGET}: .dist/movie_index-1.0.0-py3-none-any.whl
	@docker build -t ${TARGET} .

.venv/lib/python3.10/site-packages/pdm:
	@python3 -m venv .venv
	@. .venv/bin/activate
	@python -m pip install pdm

.venv/lib/python3.10/site-packages/black:
	@python3 -m venv .venv
	@. .venv/bin/activate
	@python -m pip install black

.venv/lib/python3.10/site-packages/isort:
	@python3 -m venv .venv
	@. .venv/bin/activate
	@python -m pip install isort

.venv/lib/python3.10/site-packages/ruff:
	@python3 -m venv .venv
	@. .venv/bin/activate
	@python -m pip install ruff

.dist/movie_index-1.0.0-py3-none-any.whl: .venv/lib/python3.10/site-packages/pdm ${PYTHON_SRC} movie_index/pyproject.toml
	@. .venv/bin/activate
	@python -m pdm build --no-sdist -d ../.dist/ -p movie_index/

cache:
	@mkdir cache
	@chmod 777 cache

# ------------------------------------------------------------------------------
# Phonies! (Utility Commands)
# ------------------------------------------------------------------------------
.PHONY: doc
doc:
	@doxygen doxygen.conf

.PHONY: clean
clean:
	@rm -rf .dist
	@rm -rf .venv
	@docker image rm ${TARGET}

.PHONY: lint
lint: .venv/lib/python3.10/site-packages/ruff
	@. .venv/bin/activate
	@python -m ruff check movie_index/ --select F401 --select F403 --quiet

.PHONY: format
format: .venv/lib/python3.10/site-packages/black .venv/lib/python3.10/site-packages/isort
	@. .venv/bin/activate
	@python -m black movie_index
	@python -m isort movie_index

.PHONY: run
run: ${TARGET} cache
	@docker run -ti -v $(CURDIR)/cache:/home/u_movie_index/cache ${TARGET}

.PHONY: help
help:
	@echo "Targets of this Makefile:"
	@echo "  all		Build main target: ${TARGET}"
	@echo "  clean		Cleans project by removing .venv and .dist"
	@echo "  doc		Builds the documentation for this project (WIP)"
	@echo "  format		Formats the project with black and isort"
	@echo "  help		Prints out this help information"
	@echo "  lint		Lints the project with ruff"
	@echo "  run		Runs: ${TARGET}"
