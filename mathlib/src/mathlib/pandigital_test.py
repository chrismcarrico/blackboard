from mathlib.pandigital import is_pandigital

def test_basic_true():
    assert is_pandigital(123)
    
def test_basic_false():
    assert not is_pandigital(13)
    
def test_true():
    assert is_pandigital(15234)
    
def test_false():
    assert not is_pandigital(3125)
    
def test_is_9_pandigital():
    assert is_pandigital(391867254)
    
def test_is_not_9_pandigital():
    assert not is_pandigital(31867254, p=9)