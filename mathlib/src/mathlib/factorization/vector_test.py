import pytest

from mathlib.factorization.vector import partial_vector_factorization, vector_factorization

def test_factor_exponents():
    
    assert vector_factorization(2**3 * 3**2 * 7, [2, 3, 5, 7]) == [3, 2, 0, 1]

def test_factor_exponents_no_base():
    
    assert vector_factorization(2**3 * 3**2 * 7) == [3, 2, 0, 1, 0, 0, 0, 0]


def test_factor_exponents_incomplete_base():
    assert vector_factorization(2**3 * 3**2 * 7 * 11, [2, 3, 7]) is None

def test_partial_factorization_cofactor():
    assert partial_vector_factorization(2**3 * 3**2 * 7 * 11, [2, 3, 7]) == ([3, 2, 1], 11)

def test_partial_factorization_complete():
    assert partial_vector_factorization(2**3 * 3**2, [2, 3, 7]) == ([3, 2, 0], 1)
