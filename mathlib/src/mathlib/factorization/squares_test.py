import math

from mathlib.factorization.squares import factor_from_dependencies, log_sieve, square_root_of_product

def test_log_sieve():
    sieve = log_sieve(10, [(2, 0), (3, 1)])
    assert sieve[0] == 1 and sieve[1] == math.log2(3) and sieve[4] == 1 + math.log2(3) and sieve[9] == 0

def test_log_sieve_empty():
    assert log_sieve(4, []) == [0.0] * 4

def test_square_root_of_product():
    assert square_root_of_product([-1, 2, 3, 5], [2, 4, 2, 0], 1000) == (-1 * 4 * 3) % 1000

def test_factor_from_dependencies():
    # 10^2 = 3^2 (mod 91) and 91 = 7 * 13
    n = 91
    assert factor_from_dependencies(n, [[1, 0], [1, 0]], lambda dependency: (10, 3)) in (7, 13)

def test_factor_from_dependencies_trivial():
    n = 91
    assert factor_from_dependencies(n, [[1, 0], [1, 0]], lambda dependency: (10, 10)) is None
    assert factor_from_dependencies(n, [[1, 0], [1, 0]], lambda dependency: None) is None
    # no dependencies at all
    assert factor_from_dependencies(n, [[1, 0], [0, 1]], lambda dependency: (10, 3)) is None
