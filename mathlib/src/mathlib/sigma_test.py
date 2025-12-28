from mathlib.sigma import sigma

def test_sigma_28_0():
    assert sigma(12, 0) == 6
    
def test_sigma_12_1():
    assert sigma(12, 1) == 28 