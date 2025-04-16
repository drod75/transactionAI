# Makefile for Flask App (Windows)

VENV_DIR=venv

run: $(VENV_DIR)\Scripts\activate
	$(VENV_DIR)\Scripts\python.exe -m flask run

$(VENV_DIR)\Scripts\activate:
	python -m venv $(VENV_DIR)
	$(VENV_DIR)\Scripts\pip.exe install -r requirements.txt
