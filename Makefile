.PHONY: build-layer

build-layer:
	mkdir -p layers/sam_sold_dependencies/python
	pip install -r src/requirements.txt -t layers/sam_sold_dependencies/python
