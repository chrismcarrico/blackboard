import math

import pytest

from mathlib.factorization.factor import METHODS, factor, plan, split
from mathlib.primality.miller_rabin import next_prime

def _product(factors: dict[int, int]) -> int:
    return math.prod(p**e for p, e in factors.items())

def _slow_factor(n: int) -> dict[int, int]:
    factors = {}
    p = 2
    while n > 1:
        while n % p == 0:
            factors[p] = factors.get(p, 0) + 1
            n //= p
        p += 1
    return factors

def test_factor_1():
    assert factor(1) == {}

def test_factor_prime():
    assert factor(104729) == {104729: 1}

def test_factor_large_prime():
    assert factor(2**89 - 1) == {2**89 - 1: 1}

def test_factor_multiplicity():
    assert factor(2**10 * 3**4 * 7 * 11**2) == {2: 10, 3: 4, 7: 1, 11: 2}

def test_factor_is_sorted():
    assert list(factor(13 * 2 * 1000003 * 7)) == [2, 7, 13, 1000003]

def test_factor_less_than_1():
    with pytest.raises(ValueError):
        factor(0)

def test_factor_unknown_method():
    with pytest.raises(ValueError):
        factor(15, "magic")  # pyright: ignore[reportArgumentType]

def test_factor_small():
    for n in range(1, 3000):
        assert factor(n) == _slow_factor(n)

def test_factor_medium_semiprime():
    p, q = 1000003, 1000033
    assert factor(p * q) == {p: 1, q: 1}

def test_factor_large_semiprime():
    p, q = next_prime(10**14), next_prime(3 * 10**14)
    assert factor(p * q) == {p: 1, q: 1}

def test_factor_large_prime_power():
    p = 10**9 + 7
    assert factor(p**3) == {p: 3}

def test_factor_power_of_composite():
    p, q = 1000003, 1000033
    assert factor((p * q)**2 * 3) == {3: 1, p: 2, q: 2}

def test_factor_small_factor_of_huge_number():
    # far too big to sieve, but pollard rho finds the small factor and what is left is prime
    p, q = 1000003, 2**127 - 1
    assert factor(p * q) == {p: 1, q: 1}

def test_factor_close_factors_of_huge_number():
    # far too big to sieve, but fermat finds factors this close together straight away
    p = next_prime(10**40)
    q = next_prime(p)
    assert factor(p * q) == {p: 1, q: 1}

def test_factor_many_factors():
    primes = [3, 10007, 1000003, 1000033, next_prime(10**10), next_prime(10**12)]
    assert factor(math.prod(primes) * 10007) == {p: 2 if p == 10007 else 1 for p in primes}

@pytest.mark.parametrize("method", METHODS)
def test_factor_with_method(method):
    n = 2**3 * 3**2 * 101 * 103**2 * 1009
    assert factor(n, method) == {2: 3, 3: 2, 101: 1, 103: 2, 1009: 1}

@pytest.mark.parametrize("method", METHODS)
def test_factor_with_method_small(method):
    for n in range(1, 300):
        assert factor(n, method) == _slow_factor(n)

def test_split():
    n = 1000003 * 1000033
    assert split(n) in (1000003, 1000033)

def test_plan_small():
    assert plan(10007 * 10009)[0][0] == "pollard_rho"

def test_plan_large():
    assert [name for name, _ in plan(next_prime(10**14) * next_prime(3 * 10**14))] == ["fermat", "pollard_rho", "quadratic_sieve", "pollard_rho"]

def test_plan_number_field_sieve_min_bits():
    n = next_prime(10**14) * next_prime(3 * 10**14)
    assert "number_field_sieve" not in [name for name, _ in plan(n)]
    assert [name for name, _ in plan(n, number_field_sieve_min_bits=60)] == ["fermat", "pollard_rho", "number_field_sieve", "quadratic_sieve", "pollard_rho"]

def test_factor_number_field_sieve():
    p, q = next_prime(10**9), next_prime(3 * 10**9)
    assert factor(p * q, "number_field_sieve") == {p: 1, q: 1}
    # pollard rho and fermat get no chance to split it before the number field sieve
    assert factor(p * q, pollard_rho_steps_large=0, fermat_steps=0, number_field_sieve_min_bits=60) == {p: 1, q: 1}

def test_plan_pollard_rho_max_bits():
    n = 10007 * 10009
    assert plan(n, pollard_rho_max_bits=10)[0][0] == "fermat"

def test_plan_steps():
    n = next_prime(10**14) * next_prime(3 * 10**14)
    steps = {"fermat_steps": 7, "pollard_rho_steps": 11, "pollard_rho_steps_large": 13}

    splitters = plan(n, **steps)
    assert splitters[0][1].keywords == {"max_steps": 7}  # pyright: ignore[reportFunctionMemberAccess]
    assert splitters[1][1].keywords == {"starting_value": 2, "max_steps": 13}  # pyright: ignore[reportFunctionMemberAccess]

    splitters = plan(n, large_bits=200, **steps)
    assert splitters[1][1].keywords == {"starting_value": 2, "max_steps": 11}  # pyright: ignore[reportFunctionMemberAccess]

def test_split_options():
    n = 1000003 * 1000033
    assert split(n, pollard_rho_max_bits=0) in (1000003, 1000033)

def test_split_unknown_option():
    with pytest.raises(TypeError):
        split(1000003 * 1000033, magic=1)

@pytest.mark.parametrize("options", [
    {"small_prime_bound": 0},
    {"small_prime_bound": 100_000},
    {"pollard_rho_max_bits": 0},
    {"pollard_rho_max_bits": 200},
    {"fermat_steps": 0, "pollard_rho_steps": 0, "pollard_rho_steps_large": 0},
    {"large_bits": 0},
    {"miller_rabin_trials": 5},
])
def test_factor_options(options):
    n = 2**3 * 3**2 * 101 * 103**2 * 1009 * 1000003 * 1000033
    assert factor(n, **options) == {2: 3, 3: 2, 101: 1, 103: 2, 1009: 1, 1000003: 1, 1000033: 1}
    for n in range(1, 300):
        assert factor(n, **options) == _slow_factor(n)

def test_factor_options_are_keyword_only():
    with pytest.raises(TypeError):
        factor(15, "auto", 100)  # pyright: ignore[reportCallIssue]
