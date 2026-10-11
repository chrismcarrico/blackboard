import random

import pytest

from mathlib.linalg.gf2_gaussian_elimination import gf2_gaussian_elimination, find_dependencies

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

def test_gf2_gaussian_elimination_marks_pivot_rows():
    _, marked = gf2_gaussian_elimination([[0,0,0,1], [1,1,1,0], [1,1,1,1]])
    assert marked == [True, True, False]

def test_find_dependencies(a):
    dependencies = find_dependencies(a)
    assert dependencies == [[4, 0, 1]]

def test_find_dependencies_sum_to_zero():
    m = [[0,0,0,1], [1,1,1,0], [1,1,1,1], [1,1,1,0], [0,0,0,0]]
    dependencies = find_dependencies(m)
    assert len(dependencies) == 3
    for dependency in dependencies:
        assert len(set(dependency)) == len(dependency)
        for column in range(len(m[0])):
            assert sum(m[row][column] for row in dependency) % 2 == 0

def test_find_dependencies_independent_rows():
    assert find_dependencies([[1,0], [0,1]]) == []

def test_find_dependencies_random():
    rng = random.Random(0)
    n_rows, n_cols = 40, 30
    m = [[rng.randint(0, 1) for _ in range(n_cols)] for _ in range(n_rows)]
    dependencies = find_dependencies(m)
    assert len(dependencies) >= n_rows - n_cols
    for dependency in dependencies:
        for column in range(n_cols):
            assert sum(m[row][column] for row in dependency) % 2 == 0
