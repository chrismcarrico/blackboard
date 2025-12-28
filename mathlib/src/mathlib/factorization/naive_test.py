from mathlib.factorization.naive import naive_factorization

def test_factor_13195():
    
    assert naive_factorization(13195) == [5,7,13,29]
    
def test_factor_2179():

    assert naive_factorization(2179) == [2179]
    
def test_factor_2():
    assert naive_factorization(2) == [2]    
    
def test_factor_1():
    assert naive_factorization(1) == []
    
def test_factor_8():
    assert naive_factorization(8) == [2]