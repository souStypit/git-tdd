VENV = .venv
PYTHON = $(VENV)/bin/python3
PIP = $(VENV)/bin/pip

all: $(VENV)/bin/activate
	$(PYTHON) app/routes.py

tests: $(VENV)/bin/activate
	pytest -s app/tests.py --name TEST --html=report.html
	
setup: requirements.txt
	pip install -r requirements.txt

clean:
	rm -rf __pycache__ .pytest_cache assets app/instance app/__pycache__ report.html

clean_with_venv: clean
	rm -rf $(VENV)
