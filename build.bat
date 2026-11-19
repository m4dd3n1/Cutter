@echo off
setlocal
py -m pip install -r requirements.txt
py -m pip install -r build-requirements.txt
pyinstaller --noconsole --onefile --name Cutter app.py
start dist
