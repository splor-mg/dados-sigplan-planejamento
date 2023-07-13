.PHONY: all init extract validate transform build check publish clean

EXT = txt
RESOURCE_NAMES := $(shell python main.py resources)
OUTPUT_FILES := $(addsuffix .csv,$(addprefix data/,$(RESOURCE_NAMES)))

all: init extract validate transform build check

init:
	python main.py init

extract: 
	$(foreach resource_name, $(RESOURCE_NAMES),python main.py extract $(resource_name) &&) true

validate: 
	frictionless validate datapackage.yaml

transform:
	$(foreach resource_name, $(RESOURCE_NAMES),python main.py transform $(resource_name) &&) true

build:
	python main.py build

check:
	@echo 'No checks implemented...'

publish: 
	git add -Af datapackage.json data/*.csv data-raw/*.$(EXT)
	git commit --author="Automated <actions@users.noreply.github.com>" -m "Update data package at: $$(date +%Y-%m-%dT%H:%M:%SZ)" || exit 0
	git push

clean:
	rm -f datapackage.json data/*.csv
