# Cutter

Desktop video cutter for Windows.

## Install

```powershell
py -m pip install -r requirements.txt
py -m pip install -r build-requirements.txt
```

FFmpeg and FFprobe must be installed and available in `PATH`.

## Run

```powershell
py app.py
```

## Build

```powershell
pyinstaller --noconsole --onefile --name Cutter app.py
```

The EXE is written to `dist\Cutter.exe`.
