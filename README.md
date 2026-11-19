# Cutter

Desktop video cutter for Windows. It splits videos into fixed-length clips and shuffles clips from different sources.

## Run

```powershell
py -m pip install -r requirements.txt
py app.py
```

## Build EXE

```powershell
py -m pip install -r build-requirements.txt
pyinstaller --noconsole --onefile --name Cutter app.py
```
