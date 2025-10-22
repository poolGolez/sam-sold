.PHONY: build-layer

build-layer:
	mkdir -p layers/sam_sold_dependencies/python
	pip install -r layers/sam_sold_dependencies/requirements.txt -t layers/sam_sold_dependencies/python
