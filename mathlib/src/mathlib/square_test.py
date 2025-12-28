from mathlib.square import is_square

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