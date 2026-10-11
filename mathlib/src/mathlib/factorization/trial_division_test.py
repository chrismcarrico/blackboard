from mathlib.factorization.trial_division import trial_division

def test_composite():
    assert trial_division(7 * 11) == 7

def test_prime():
    assert trial_division(101) is None

def test_2():
    assert trial_division(2) is None

def test_even():
    assert trial_division(2 * 101) == 2

def test_square():
    assert trial_division(101**2) == 101

def test_smallest_factor():
    assert trial_division(3 * 5 * 7) == 3
