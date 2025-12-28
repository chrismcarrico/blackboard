import mathlib.legendre as legendre

def test_1_and_3():
    assert legendre.legendre_symbol(1,3) == 1
    
def test_2_and_3():
    assert legendre.legendre_symbol(2,3) == -1
    
def test_3_and_11():
    assert legendre.legendre_symbol(3, 11) == 1
    
def test_6_and_11():
    assert legendre.legendre_symbol(6, 11) == -1
    
def test_0_and_11():
    assert legendre.legendre_symbol(0, 11) == 0
