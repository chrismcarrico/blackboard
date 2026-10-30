import pytest

from mathlib.eratoshenes import primes_less_than_n
from mathlib.factorization.nfs import (
    algebraic_square_root,
    build_algebraic_base,
    build_characters,
    derivative,
    evaluate,
    find_inert_prime,
    homogeneous_norm,
    is_irreducible_mod_p,
    make_relation,
    number_field_sieve,
    product_mod_f,
    roots_mod_p,
    select_polynomial,
    sieve_line,
)
from mathlib.factorization.vector import vector_factorization
from mathlib.primality.miller_rabin import miller_rabin, next_prime

@pytest.fixture
def n():
    return next_prime(10**9) * next_prime(3 * 10**9)

def test_evaluate():
    assert evaluate([5, 0, 3, 1], 2) == 5 + 3*4 + 8
    assert evaluate([5, 0, 3, 1], 2, 7) == 25 % 7

def test_derivative():
    assert derivative([5, 0, 3, 1]) == [0, 6, 3]

def test_homogeneous_norm():
    f = [5, 0, 3, 1]
    for a in range(-5, 6):
        for b in range(1, 4):
            assert homogeneous_norm(f, a, b) == 5*b**3 + 3*a*a*b + a**3

@pytest.mark.parametrize("degree", [3, 5])
def test_select_polynomial(n, degree):
    f, m = select_polynomial(n, degree)
    assert len(f) == degree + 1
    assert f[-1] == 1
    assert evaluate(f, m) == n
    assert all(0 <= c < m for c in f)

@pytest.mark.parametrize("p", [2, 3, 5, 101, 103, 1009, 10007])
def test_roots_mod_p(p):
    for f in ([5, 0, 3, 1], [-2, 0, 0, 1], [6, 11, 6, 1], [1, 2, 3, 4, 5, 1]):
        assert roots_mod_p(f, p) == [r for r in range(p) if evaluate(f, r, p) == 0]

def test_is_irreducible_mod_p():
    # x^3 - 2 has a root modulo 5, x^2 + 1 is irreducible modulo 3 but not modulo 5
    assert not is_irreducible_mod_p([-2, 0, 0, 1], 5)
    assert is_irreducible_mod_p([1, 0, 1], 3)
    assert not is_irreducible_mod_p([1, 0, 1], 5)
    # a product of two irreducible quadratics has no roots but is not irreducible
    assert not is_irreducible_mod_p([1, 0, 2, 0, 1], 3)
    # x^5 - x - 1 is irreducible modulo 5
    assert is_irreducible_mod_p([-1, -1, 0, 0, 0, 1], 5)

def test_find_inert_prime():
    f = [5, 0, 3, 1]
    p = find_inert_prime(f)
    assert p is not None and p % 4 == 3
    assert is_irreducible_mod_p(f, p)

def test_find_inert_prime_reducible():
    # (x - 1)(x^2 + x + 3) has a root modulo every prime
    assert find_inert_prime([-3, 2, 0, 1], limit=1000) is None

def test_build_algebraic_base():
    f = [5, 0, 3, 1]
    base = build_algebraic_base(f, [2, 3, 5, 7, 11, 13])
    assert base and all(evaluate(f, r, p) == 0 for p, r in base)

def test_build_characters():
    f = [5, 0, 3, 1]
    characters = build_characters(f, 1000, 10)
    assert len(characters) == 10
    for q, s in characters:
        assert q >= 1000 and miller_rabin(q, 20)
        assert evaluate(f, s, q) == 0
        assert evaluate(derivative(f), s, q) != 0

@pytest.mark.parametrize("beta", [[12345, -678, 91], [1, 0, 0], [-3, 7, -2], [10**30, -10**25, 7]])
def test_algebraic_square_root(beta):
    f = [5, 0, 3, 1]
    gamma = product_mod_f([beta, beta], f)
    root = algebraic_square_root(gamma, f, find_inert_prime(f))  # pyright: ignore[reportArgumentType]
    assert root in (beta, [-c for c in beta])

def test_algebraic_square_root_not_a_square():
    f = [5, 0, 3, 1]
    assert algebraic_square_root([2, 0, 0], f, find_inert_prime(f)) is None  # pyright: ignore[reportArgumentType]

def test_sieve_line_relations_are_smooth(n):
    f, m = select_polynomial(n, 3)
    rational_base = primes_less_than_n(1000)
    algebraic_base = build_algebraic_base(f, rational_base)
    algebraic_primes = sorted({p for p, _ in algebraic_base})
    algebraic_columns = {pair: i for i, pair in enumerate(algebraic_base)}

    relations = 0
    for b in range(1, 6):
        for a, rational_norm, algebraic_norm in sieve_line(f, m, b, 5000, rational_base, algebraic_base, 10):
            assert rational_norm == a - b*m
            assert algebraic_norm == homogeneous_norm(f, a, b)

            relation = make_relation(a, b, rational_norm, algebraic_norm, rational_base, algebraic_primes, algebraic_columns, [])
            if relation is None:
                continue

            relations += 1
            assert vector_factorization(abs(rational_norm), rational_base) is not None
            assert vector_factorization(abs(algebraic_norm), algebraic_primes) is not None
            assert len(relation.row) == 1 + len(rational_base) + 1 + len(algebraic_base)

    assert relations > 0

@pytest.mark.parametrize("p, q", [
    (1000003, 3000017),
    (next_prime(10**7), next_prime(3 * 10**7)),
    (next_prime(10**9), next_prime(3 * 10**9)),
])
def test_number_field_sieve(p, q):
    assert number_field_sieve(p * q) in (p, q)

def test_number_field_sieve_three_factors():
    n = 1000000007 * 998244353 * 1000003
    factor = number_field_sieve(n)
    assert factor is not None and 1 < factor < n and n % factor == 0

def test_number_field_sieve_special_polynomial():
    # 2^71 - 1 = 228479 * 48544121 * 212885833, and x^3 - 2 has the root 2^24 modulo it
    n = 2**71 - 1
    factor = number_field_sieve(n, polynomial=([-2, 0, 0, 1], 2**24))
    assert factor is not None and 1 < factor < n and n % factor == 0

def test_number_field_sieve_bad_polynomial():
    with pytest.raises(ValueError):
        number_field_sieve(1000003 * 3000017, polynomial=([-2, 0, 0, 1], 2**24))

    # x^2 - 2 does have the root 2^36 modulo 2^71 - 1, but its degree is even
    n = 2**71 - 1
    with pytest.raises(ValueError):
        number_field_sieve(n, polynomial=([-2, 0, 1], 2**36))

def test_number_field_sieve_small_factor():
    assert number_field_sieve(101 * 1000003) == 101
