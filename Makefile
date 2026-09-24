VENV := .venv
PYTHON := $(VENV)/bin/python
PIP := $(VENV)/bin/pip

.PHONY: run freeze install dev

run:
	python -m grout.main

dev:
	watchexec -e py,qml,json -r -- $(PYTHON) -m grout.main

freeze:
	pip freeze > requirements.txt

install: $(VENV)/bin/activate
	$(PIP) install -r requirements.txt
	mkdir -p ~/.local/bin
	chmod +x grout/toggle.py
	ln -sf $(CURDIR)/grout/toggle.py ~/.local/bin/grout-toggle
	@echo ""
	@echo "Installed. Two manual steps left:"
	@echo ""
	@echo "1) Add a keybind in ~/.config/openbox/rc.xml:"
	@echo '   <keybind key="W-space">'
	@echo '     <action name="Execute"><command>grout-toggle</command></action>'
	@echo '   </keybind>'
	@echo ""
	@echo "2) Start the daemon on login, in ~/.config/openbox/autostart:"
	@echo "   $(CURDIR)/$(VENV)/bin/python -m grout.main &"
	@echo ""
	@echo "Then: openbox --reconfigure"

$(VENV)/bin/activate:
	python -m virtualenv $(VENV)
