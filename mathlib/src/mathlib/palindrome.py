def _str_is_palindrome(s: str) -> bool:
    
    lhs, rhs = s[:len(s)//2], s[len(s)//2+len(s)%2:]
    
    return lhs == rhs[::-1]

def is_palindrome(obj) -> bool:
    
    if isinstance(obj, int):
        return _str_is_palindrome(str(obj))
    
    elif isinstance(obj, str):
        return _str_is_palindrome(str(obj))
    
    raise ValueError