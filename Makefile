.PHONY: all extract transform build validate publish

EXT = txt
INPUT_DIR = data-raw
OUTPUT_DIR = data
RESOURCE_NAMES := $(shell python main.py resources)
OUTPUT_FILES := $(addsuffix .csv,$(addprefix $(OUTPUT_DIR)/,$(RESOURCE_NAMES)))

all: init extract transform build validate

init: 
	python main.py init

extract: 
	$(foreach resource_name, $(RESOURCE_NAMES),python main.py extract $(resource_name) &&) true

transform: $(OUTPUT_FILES)

$(OUTPUT_FILES): $(OUTPUT_DIR)/%.csv: $(INPUT_DIR)/%.$(EXT) schemas/%.yaml scripts/transform.py datapackage.yaml
	python main.py transform $*

build: transform
	python main.py build

validate: 
	frictionless validate datapackage.yaml

publish: 
	git add -Af $(OUTPUT_DIR)/*.csv $(INPUT_DIR)/*.$(EXT) datapackage.json
	git commit --author="Automated <actions@users.noreply.github.com>" -m "Update data package at: $$(date +%Y-%m-%dT%H:%M:%SZ)" || exit 0
	git push
