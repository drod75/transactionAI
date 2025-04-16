# Makefile for running the Flask app

# Variables
APP_NAME=app.py
VENV_DIR=venv
PYTHON=$(VENV_DIR)/bin/python
PIP=$(VENV_DIR)/bin/pip

# For Windows
PYTHON=$(VENV_DIR)\Scripts\python.exe
PIP=$(VENV_DIR)\Scripts\pip.exe

.PHONY: run setup install clean

setup:
	python -m venv $(VENV_DIR)
	$(PIP) install -r requirements.txt

install:
	$(PIP) install -r requirements.txt

run:
	FLASK_APP=$(APP_NAME) FLASK_ENV=development $(PYTHON) -m flask run

clean:
	rm -rf __pycache__ $(VENV_DIR)