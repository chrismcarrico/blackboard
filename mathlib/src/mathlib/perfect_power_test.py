from mathlib.perfect_power import integer_root, perfect_power, perfect_power_root

def test_integer_root():
    assert integer_root(26, 3) == 2
    assert integer_root(27, 3) == 3
    assert integer_root((10**20 + 1)**2, 2) == 10**20 + 1

def test_perfect_power():
    assert perfect_power(7**5) == (7, 5)
    assert perfect_power(3**6) == (27, 2)
    assert perfect_power(3 * 5 * 7) is None

def test_perfect_power_root():
    assert perfect_power_root(7**5) == 7
    assert perfect_power_root(3 * 5 * 7) is None
