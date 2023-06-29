.PHONY: all extract transform check publish

EXT = txt
INPUT_DIR = data/raw
OUTPUT_DIR = data
RESOURCE_NAMES := $(shell yq e '.resources[].name' datapackage.yaml)
OUTPUT_FILES := $(addsuffix .csv,$(addprefix $(OUTPUT_DIR)/,$(RESOURCE_NAMES)))

all: extract transform check publish

extract: 
	$(foreach resource_name, $(RESOURCE_NAMES), python scripts/extract.py $(resource_name);)

transform: $(OUTPUT_FILES)

$(OUTPUT_FILES): $(OUTPUT_DIR)/%.csv: $(INPUT_DIR)/%.$(EXT) schemas/%.yaml scripts/transform.py datapackage.yaml
	python scripts/transform.py $* $@

check: checks-python

checks-python:
	python -m pytest checks/python/

publish: 
	git add -Af data/*.csv
	git commit --author="Automated <actions@users.noreply.github.com>" -m "Update data package" || exit 0
	git push
