#!/bin/bash
pip install pyinstaller
pyinstaller --onefile --windowed app/main.py \
    --name FileOrganizer \
    --icon assets/icon.png
