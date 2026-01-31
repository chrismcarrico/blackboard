import pytest

from mathlib.linalg.gf2_gaussian_elimination import gf2_gaussian_elimination

@pytest.fixture
def a():
    return [[1,1,0,0], [1,1,0,1], [0,1,1,1], [0,0,1,0], [0,0,0,1]]

@pytest.fixture
def expected_triangular_form():
    return [[1,0,0,0], [0,0,0,1], [0,1,0,0], [0,0,1,0], [1,0,0,1]]

@pytest.fixture
def expected_marked():
    return [True, True, True, True, False]

def test_gf2_gaussian_elimination(a, expected_triangular_form, expected_marked):
    assert gf2_gaussian_elimination(a) == (expected_triangular_form, expected_marked)