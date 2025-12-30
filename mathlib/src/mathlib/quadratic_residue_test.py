from mathlib.quadratic_residue import legendre_symbol, is_square

def test_1_and_3():
    assert legendre_symbol(1,3) == 1
    
def test_2_and_3():
    assert legendre_symbol(2,3) == -1
    
def test_3_and_11():
    assert legendre_symbol(3, 11) == 1
    
def test_6_and_11():
    assert legendre_symbol(6, 11) == -1
    
def test_0_and_11():
    assert legendre_symbol(0, 11) == 0


def test_is_square_0():

    assert is_square(0)

def test_is_square_1():

    assert is_square(1)

def test_is_square_4():

    assert is_square(4)

def test_is_square_large():
    assert is_square(1234567890**2)

def test_is_not_square_5():
    assert not is_square(5)

def test_is_not_square_large():
    assert not is_square(1234567890)

def test_is_square_modulo():
    assert is_square(4, 7)

def test_is_square_modulo_large():
    assert is_square(1234567890**2, 53)

def test_is_not_square_modulo():
    assert not is_square(5, 13)