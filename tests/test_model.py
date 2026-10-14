import math
import pytest
from model import load_obj,normalize,project,parse_obj


def test_cube_geometry_and_projection():
    vertices,edges = load_obj('samples/cube.obj')
    assert len(vertices)==8 and len(edges)==12
    points = project(normalize(vertices),yaw=45,pitch=30)
    assert len(points)==8
    assert all(math.isfinite(value) for point in points for value in point)


def test_negative_indices_and_invalid_files():
    vertices,edges = parse_obj('v 0 0 0\nv 1 0 0\nv 0 1 0\nf -3 -2 -1')
    assert len(edges)==3
    with pytest.raises(ValueError): parse_obj('v nan 0 0\nf 1 1 1')
    with pytest.raises(ValueError): parse_obj('v 0 0 0\nf 1 2 3')
