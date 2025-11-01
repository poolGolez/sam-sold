.PHONY: build-layer

build-layer:
	mkdir -p layers/sam_sold_dependencies/python
	pip install -r backend/src/requirements.txt -t backend/layers/sam_sold_dependencies/python
