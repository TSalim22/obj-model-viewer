# 3D OBJ Model Viewer

Load and rotate OBJ wireframe models with a Python desktop interface.

This is a small, independent Python portfolio project. The code favours ordinary functions and clear modules over complex architecture.

## Setup

Requires Python 3.12+ (desktop tools also require Tkinter, included with the standard Windows Python installer).

```sh
python -m venv .venv
# Windows PowerShell:
.venv\Scripts\Activate.ps1
# macOS/Linux instead: source .venv/bin/activate
python -m pip install -r requirements-dev.txt
python viewer.py
```

Run commands from this repository's root. Web apps bind to localhost by default. Each app is independent, so stop one before starting another on the same port.

## Check it

```sh
python -m pytest -q
```

## Dates

The commit author dates have been deliberately arranged between October 2025 and October 2026 at the portfolio owner's request. They are presentation metadata, not a record of the actual development timeline. Repository creation and upload timestamps remain the real dates.

## Use the viewer

The sample cube opens automatically. Use **Open OBJ** to load a model. Drag to rotate, use the mouse wheel or Zoom slider, and reset the view from the toolbar. The parser supports polygon faces, positive/negative OBJ vertex indices and `v/vt/vn` reference syntax. Materials, textures and normals are ignored. The viewer draws orthographic wireframes, not shaded surfaces.

Limits: 10 MB file, 10,000 vertices and 20,000 faces. Bad references and non-finite coordinates produce an error without replacing the current model. FBX is not supported. This adapts the original C++/C# viewer to Python parsing, geometry and Tkinter rendering. Linux may require `python3-tk`.
