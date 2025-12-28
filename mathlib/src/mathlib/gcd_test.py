from mathlib.gcd import gcd

def test_gcd_prime():

    assert gcd(7, 13) == 1

def test_gcd_coprime():
    
    assert gcd(8, 15) == 1

def test_gcd_greater_than_1():

    assert gcd(8, 16) == 8

def test_gcd_other_than_input():

    assert gcd(3*2*2*5, 5*7) == 5

def test_powers_of_two():
    
    assert gcd(64, 256) == 64