ENV_DIR := $(shell pwd)/_env
PYTHON_BIN := $(shell which python)

# The build has been seen to fail on Mac OSX when trying to build on i386. Enable this to build for x86_64 only
X86_64_ONLY=0

.DEFAULT_GOAL = all

.PHONY: all
all: help

.PHONY: help
help:
	@cat README.md

.PHONY: test
test: bin/python setup.py
	bin/python setup.py test

.PHONY: coverage
coverage: bin/coverage setup.py
	rm -rf htmlcov/
	bin/coverage erase
	bin/coverage run --source metaswitch --omit "**/test/**"  setup.py test
	bin/coverage report -m
	bin/coverage html

.PHONY: env
env: bin/python 

bin/python bin/coverage: bin/buildout buildout.cfg
ifeq ($(X86_64_ONLY),1)
	ARCHFLAGS="-arch x86_64" ./bin/buildout -N
else
	ARCHFLAGS="-arch i386 -arch x86_64" ./bin/buildout -N
endif

bin/buildout: $(ENV_DIR)/bin/python
	mkdir -p .buildout_downloads/dist
	$(ENV_DIR)/bin/easy_install "setuptools>0.7"
	$(ENV_DIR)/bin/easy_install distribute
	$(ENV_DIR)/bin/easy_install zc.buildout
	mkdir -p bin/
	ln -s $(ENV_DIR)/bin/buildout bin/

$(ENV_DIR)/bin/python:
	virtualenv --no-site-packages --setuptools --python=$(PYTHON_BIN) $(ENV_DIR)

.PHONY: clean
clean: envclean pyclean

.PHONY: pyclean
pyclean:
	find . -name \*.pyc -exec rm -f {} \;
	rm -rf *.egg-info dist
	rm -f .coverage
	rm -rf htmlcov/

.PHONY: envclean
envclean:
	rm -rf bin eggs develop-eggs parts .installed.cfg bootstrap.py .downloads .buildout_downloads
	rm -rf distribute-*.tar.gz
	rm -rf $(ENV_DIR)

