from mathlib.palindrome import is_palindrome 

def test_even_palindrome():
    
    assert is_palindrome(8008)
    
def test_odd_palindrome():
    
    assert is_palindrome(8001008)
    
def test_not_palindrome():
    
    assert not is_palindrome(12345)  