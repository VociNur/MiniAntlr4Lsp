VENV = .venv
PYTHON = $(VENV)/bin/python
PIP = $(VENV)/bin/pip

env:
	rm -r $(VENV)
	python3 -m venv $(VENV)
	$(PIP) install -r requirements.txt

install: env
	mkdir -p $(HOME)/.local/bin
	ln -sf $(CURDIR)/myantlr-lsp-launcher.sh $(HOME)/.local/bin/myantlr-lsp

