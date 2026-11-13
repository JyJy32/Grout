#!/usr/bin/env bash
cd /home/joren/projects/grout/ || exit 1
source .venv/bin/activate
exec python -m grout.main
