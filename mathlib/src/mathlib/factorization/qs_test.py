import pytest

from mathlib.factorization.qs import calculate_b, build_relations, build_factor_base

@pytest.fixture
def psuedoprime():
    return 587*149

@pytest.fixture
def factor_base():
    return [2, 3, 13, 17, 19, 29, 41]

@pytest.fixture
def relations():
    return {
        3: [1, 1, 0, 1, 1, 0, 0], 
        11: [1, 2, 1, 0, 0, 1, 0], 
        20: [0, 6, 0, 1, 0, 0, 0], 
        51: [1, 1, 0, 2, 1, 0, 0], 
        89: [1, 1, 1, 0, 1, 0, 1], 
        98: [0, 1, 0, 0, 1, 1, 1], 
        117: [1, 7, 0, 0, 1, 0, 0], 
        180: [0, 2, 1, 0, 0, 1, 1], 
        765: [1, 4, 1, 1, 0, 1, 0], 
        918: [0, 2, 1, 2, 0, 0, 1]
    }

def test_calculate_b(psuedoprime):
    assert calculate_b(psuedoprime) == 42

def test_factor_base(psuedoprime, factor_base):
    fb = build_factor_base(psuedoprime)
    assert fb == factor_base

def test_build_relations(psuedoprime, factor_base, relations):

    r = build_relations(psuedoprime, factor_base, 10, 0)
    assert r == relations