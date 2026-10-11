import random

import pytest

from mathlib.factorization.qs import (
    calculate_b,
    build_factor_base,
    quadratic_sieve,
    quadratic_sieve_v1,
    calculate_ceil_sqrt_n,
    lift_square_root,
    polynomial_generator,
    polynomial_roots,
    sieve_polynomial,
    square_roots,
)
from mathlib.factorization.vector import vector_factorization
from mathlib.primality.miller_rabin import miller_rabin

def _sorted_factors(n: int, factor: int | None) -> list[int]:
    assert factor is not None
    return sorted([factor, n // factor])

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
    assert _sorted_factors(psuedoprime, quadratic_sieve_v1(psuedoprime)) == [149, 587]

@pytest.mark.parametrize("p, q", [(1009, 1013), (10007, 10009), (100003, 100019), (1000003, 1000033)])
def test_quadratic_sieve_larger(p, q):
    assert _sorted_factors(p*q, quadratic_sieve_v1(p*q)) == [p, q]

def test_quadratic_sieve_perfect_square():
    assert quadratic_sieve_v1(587**2) == 587

def test_quadratic_sieve_too_few_relations():
    assert quadratic_sieve_v1(109*443) is None

def test_calculate_ceil_sqrt_n():
    assert calculate_ceil_sqrt_n(16) == 4
    assert calculate_ceil_sqrt_n(17) == 5
    assert calculate_ceil_sqrt_n((10**20 + 1)**2 + 1) == 10**20 + 2

def test_square_roots(psuedoprime, expected_factor_base, expected_roots):
    roots = square_roots(psuedoprime, expected_factor_base)
    assert [(t, p - t) for t, p in zip(roots, expected_factor_base)] == expected_roots

def test_polynomial_roots(psuedoprime, expected_factor_base, expected_adjusted_roots):
    b = calculate_ceil_sqrt_n(psuedoprime)
    roots = square_roots(psuedoprime, expected_factor_base)
    assert [polynomial_roots(1, b, p, t) for p, t in zip(expected_factor_base, roots)] == expected_adjusted_roots

def test_sieve_polynomial(psuedoprime, expected_factor_base, expected_x_list, expected_fx_list):
    b = calculate_ceil_sqrt_n(psuedoprime)
    roots = square_roots(psuedoprime, expected_factor_base)
    # prime powers are not sieved, so 2171546 = 2 * 13 * 17**4 needs plenty of slack to be a candidate
    candidates = sieve_polynomial(psuedoprime, 1, b, 1600, expected_factor_base, roots, slack=16)
    smooth = [(x, fx) for x, fx in candidates if x > 0 and vector_factorization(fx, expected_factor_base) is not None]
    assert [x for x, _ in smooth] == expected_x_list
    assert [fx for _, fx in smooth] == expected_fx_list

def test_sieve_polynomial_candidates_are_divisible(psuedoprime, expected_factor_base):
    b = calculate_ceil_sqrt_n(psuedoprime)
    roots = square_roots(psuedoprime, expected_factor_base)
    for x, fx in sieve_polynomial(psuedoprime, 1, b, 200, expected_factor_base, roots, slack=0):
        assert fx == (x + b)**2 - psuedoprime
        assert vector_factorization(abs(fx), expected_factor_base) is not None

def test_lift_square_root():
    n, q = 87463, 13
    b = lift_square_root(n, q)
    assert 0 <= b < q*q
    assert (b*b - n) % (q*q) == 0

def test_polynomial_generator(psuedoprime):
    polynomials = polynomial_generator(psuedoprime, 100)
    assert next(polynomials) == (1, calculate_ceil_sqrt_n(psuedoprime))
    for _ in range(5):
        q, b = next(polynomials)
        assert miller_rabin(q, 20)
        assert (b*b - psuedoprime) % (q*q) == 0

def test_quadratic_sieve_sieving(psuedoprime):
    assert _sorted_factors(psuedoprime, quadratic_sieve(psuedoprime)) == [149, 587]

def test_quadratic_sieve_sieving_finds_what_v1_misses():
    assert _sorted_factors(109*443, quadratic_sieve(109*443)) == [109, 443]

def test_quadratic_sieve_sieving_perfect_square():
    assert quadratic_sieve(587**2) == 587

def test_quadratic_sieve_sieving_prime():
    assert quadratic_sieve(1000003) is None

def test_quadratic_sieve_sieving_small_composites():
    for n in range(9, 500, 2):
        if miller_rabin(n, 20):
            continue
        p, q = _sorted_factors(n, quadratic_sieve(n))
        assert p * q == n and 1 < p < n

def _random_prime(bits: int, rng: random.Random) -> int:
    while True:
        candidate = rng.getrandbits(bits) | 1 | (1 << (bits - 1))
        if miller_rabin(candidate, 20):
            return candidate

@pytest.mark.parametrize("bits", [8, 12, 16, 20, 24, 32, 40, 48])
def test_quadratic_sieve_sieving_random_semiprimes(bits):
    rng = random.Random(bits)
    for _ in range(5):
        p, q = _random_prime(bits, rng), _random_prime(bits, rng)
        assert _sorted_factors(p*q, quadratic_sieve(p*q)) == sorted([p, q])

def test_quadratic_sieve_sieving_multiple_polynomials():
    # an interval this short forces many polynomials to be used
    p, q = 1000000007, 1000000009
    assert _sorted_factors(p*q, quadratic_sieve(p*q, m=50)) == [p, q]

def test_quadratic_sieve_sieving_without_large_primes():
    p, q = 1000003, 1000033
    assert _sorted_factors(p*q, quadratic_sieve(p*q, large_prime_multiplier=1)) == [p, q]
