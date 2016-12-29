clean:
	rm -rf cache/

lint:
	flake8 code/*.py

docs:
	mkdir -p docs/
	cp notebooks/*html docs

data: boxoffice-data wikipedia-data csv

boxoffice-data:
	mkdir -p cache/
	python code/1-get-boxoffice-links.py
	python code/2-get-boxoffice-data.py

wikipedia-data:
	mkdir -p cache/
	python code/3-get-wikipedia-data.py

csv:
	python code/4-make-csv.py

help:
	@echo "    clean"   
	@echo "        Remove downloaded data, for fresh download." 
	@echo "    lint"
	@echo "        Check style with flake8."
	@echo "    docs"
	@echo "        Copy notebook output to docs/ for easy github pages html rendering."
	@echo "    data"
	@echo "        Download all data and make CSV files."
	@echo "    boxoffice-data"
	@echo "        Download movie boxoffice data (links to movies, and data from the links."
	@echo "    wikipedia-data"
	@echo "        Download movie article data using wikipedia API, log with *log file." 
	@echo "    csv"
	@echo "        Create CSV files for use in analyses."
