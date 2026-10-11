import random

import pytest

from mathlib.factorization.shors import shors, find_factor, find_order_of_a_modulo_n

def test_shors_2():
    assert shors(2) == [2]
    
def test_shors_15():
    factors = shors(15)
    assert sorted(factors) == [3, 5]
    
def test_shors_large():
    factors = shors(221)
    assert sorted(factors) == [13, 17]

def test_shors_prime_powers():
    factors = shors(7**3 * 11**2)
    assert sorted(factors) == [7, 11]

def test_shors_prime():
    assert shors(104729) == [104729]

def test_shors_power_of_two():
    assert shors(2**10) == [2]

def test_shors_single_prime_power():
    assert shors(7**5) == [7]

def test_shors_even():
    assert shors(2**4 * 3**2 * 13) == [2, 3, 13]

def test_shors_many_factors():
    assert shors(3 * 5 * 7 * 11 * 13 * 17) == [3, 5, 7, 11, 13, 17]

def test_shors_perfect_power_of_composite():
    assert shors((3 * 5)**4) == [3, 5]

def test_shors_less_than_2():
    with pytest.raises(ValueError):
        shors(1)

def test_shors_any_seed():
    for seed in range(20):
        assert shors(3**2 * 29 * 101, seed) == [3, 29, 101]

def test_shors_matches_trial_division():
    for n in range(2, 2000):
        expected = [p for p in range(2, n + 1) if n % p == 0 and all(p % d for d in range(2, p))]
        assert shors(n, seed=n) == expected

def test_shors_does_not_reseed_global_random():
    random.seed(0)
    expected = random.random()
    random.seed(0)
    shors(221, seed=5)
    assert random.random() == expected

def test_find_factor():
    rng = random.Random(0)
    for n in [15, 221, 7**3 * 11**2, 101 * 103 * 107]:
        factor = find_factor(n, rng)
        assert 1 < factor < n and n % factor == 0

def test_find_order():
    assert find_order_of_a_modulo_n(2, 7) == 3
    assert find_order_of_a_modulo_n(3, 7) == 6
    assert find_order_of_a_modulo_n(2, 15) == 4
    assert find_order_of_a_modulo_n(10, 11) == 2
