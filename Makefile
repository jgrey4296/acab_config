SHELL   := /usr/local/bin/bash
TOP     := ./acab_config
LOGLEVEL := WARNING

TEST_TARGET		?= ${TOP}
TEST_PAT		:=
TEST_FILE_PAT	:= "test_*.py"

# Clean Variables
PYS		!= find ${TOP} -name '*.py' -not -name '*context.py' -not -name '__init__.py'
LOGS	!= find ${TOP} -name '*log.*'
CACHES	!= find ${TOP} -regextype posix-egrep -regex .*\(.mypy_cache\|__pycache__\)$

# You can set these variables from the command line, and also
# from the environment for the first two.
doc_target    ?= "html"
SPHINXOPTS    ?=
SPHINXBUILD   ?= sphinx-build
DOCSOURCEDIR   = docs
DOCBUILDDIR    = dist/build

# If defined, use these overrides
ifneq (${pat}, )
	TEST_PAT = -k ${pat}
endif

ifneq (${fpat}, )
	TEST_FILE_PAT := ${fpat}
endif

.PHONY: help Makefile all pylint clean


# Put it first so that "make" without argument is like "make help".
help:
	@$(SPHINXBUILD) -M help "$(DOCSOURCEDIR)" "$(DOCBUILDDIR)" $(SPHINXOPTS) $(O)

# "make mode" option.  $(O) is meant as a shortcut for $(SPHINXOPTS).
# run with Symbol’s value as variable is void: make =clean etc
sphinx: Makefile
	@$(SPHINXBUILD) -M target "$(DOCSOURCEDIR)" "$(DOCBUILDDIR)" $(SPHINXOPTS) $(O)


all: verbose long

# Building ####################################################################
build:
	python -m build
	pip install -U -e .

dist:
# use --collect-all {package} for binaries like tkinterdnd2
	pyinstaller -w acab_config/default.py

# Linting #####################################################################
pylint:
	@echo "Linting"
	pylint --rcfile=./.pylintrc ${TOP} --ignore=${ig} --ignore-patterns=${igpat}

elint:
	@echo "Linting -E"
	pylint --rcfile=./.pylintrc ${TOP} --ignore=${ig} --ignore-patterns=${igpat} -E

# Testing #####################################################################
long:
	python -m unittest discover -s ${TEST_TARGET} -p "*_tests.py"

test:
	python -m unittest discover -v -s ${TEST_TARGET} -p ${TEST_FILE_PAT} -t ${TOP} ${TEST_PAT}

faily:
	@echo "Testing with early fail"
	python -m unittest discover -v -f -s ${TEST_TARGET} ${TEST_PAT} -t ${TOP} -p ${TEST_FILE_PAT}


# Reports #####################################################################
check:
	@echo "Shell	= " ${SHELL}
	@echo "Top		= " ${TOP}
	@echo "Search	= " ${TEST_TARGET}
	@echo "Pattern	= " ${TEST_PAT}


line_report:
	@echo "Counting Lines into linecounts.stats"
	find . -name "*.py" -not -path "./.git/*" -not -name "test_*.py" -not -name "*__init__.py" -print0 | xargs -0 wc -l | sort > linecounts.report

class_report:
	@echo "Getting Class Relations"
	find ./acab_config -name "*.py" -not -name "flycheck*" | xargs awk '/^class/ {print $0}' > class.report

export_env:
	conda env export --from-history > default.yaml

# Cleaning ####################################################################
init:
	@echo "Auto-creating empty __init__.py's"
	find ${TOP} -type d -print0 | xargs -0 -I {} touch "{}/__init__.py"

clean:
	@echo "Cleaning"
ifeq (${LOGS}, )
	@echo "No Logs to delete"
else
	-rm ${LOGS}
endif
ifeq (${CACHES}, )
	@echo "No Caches to delete"
else
	-rm -r ${CACHES}
endif
	-rm -rf ./dist
	-rm -rf ./build
