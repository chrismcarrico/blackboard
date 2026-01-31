import pytest

from mathlib.factorization.qs import calculate_b, build_factor_base, quadratic_sieve_v1, calculate_ceil_sqrt_n

@pytest.fixture
def psuedoprime():
    return 587*149

@pytest.fixture
def expected_factor_base():
    return [2, 3, 13, 17, 19, 29, 41]

@pytest.fixture
def expected_roots():
    return [(1, 1), (1, 2), (8, 5), (7, 10), (5, 14), (12, 17), (16, 25)]

@pytest.fixture
def expected_adjusted_roots():
    return [(1, 1), (2, 0), (11, 8), (0, 3), (13, 3), (6, 11), (7, 16)]

@pytest.fixture
def expected_b():
    return 42

@pytest.fixture
def expected_x_list():
    return [3, 11, 20, 51, 89, 98, 117, 180, 765, 918, 1207, 1533]

@pytest.fixture
def expected_fx_list():
    return [1938, 6786, 12393, 32946, 60762, 67773, 83106, 139113, 1038258, 1386333, 2171546, 3257778]

def test_calculate_b(psuedoprime, expected_b):
    assert calculate_b(psuedoprime) == expected_b

def test_factor_base(psuedoprime, expected_factor_base, expected_b):
    fb = build_factor_base(psuedoprime, expected_b)
    assert fb == expected_factor_base

def test_quadratic_sieve(psuedoprime):

    assert quadratic_sieve_v1(psuedoprime)