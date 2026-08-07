from mathlib.factorization.shors import shors

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