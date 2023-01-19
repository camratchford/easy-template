#!/bin/bash
EXE_NAME="ezt"
INCLUDE_PATHS="../"
SCRIPT_FILE="../cli.py"

../venv/bin/pyinstaller -y --clean --console --onefile --name="${EXE_NAME}" --paths="${INCLUDE_PATHS}" --collect-submodules="ez_temp" "${SCRIPT_FILE}"