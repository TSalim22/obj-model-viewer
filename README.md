# 3D OBJ Model Viewer

Open OBJ files and view them as rotating wireframes.

## Run it

Python 3.12 or later. Run these commands from the project folder:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements-dev.txt
python viewer.py
```

On macOS or Linux, activate with `source .venv/bin/activate` instead.

## How to use it

The sample cube opens when the app starts. Use **Open OBJ** to choose a model.

Drag to rotate, scroll to zoom, or use the sliders. **Reset view** restores the starting angle.

Supports OBJ polygon models up to 10 MB, 10,000 vertices and 20,000 faces. FBX, textures and shading aren't supported. Linux may need `python3-tk`.

## Tests

```sh
python -m pytest -q
```
