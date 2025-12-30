def legendre_symbol(a: int, p: int):
    
    residue = pow(a, (p-1)//2, p)
    
    return residue - p if residue > 1 else residue

def jacobi_symbol(a: int, n: int):

    assert a > 0 and n > 0

    a %= n
    result = 1
    while a != 0:
        while a % 2 == 0:
            a //= 2
            n_mod_8 = n % 8
            if n_mod_8 in (3, 5):
                result = -result
        a, n = n, a
        if a % 4 == 3 and n % 4 == 3:
            result = -result
        a %= n
    if n == 1:
        return result
    else:
        return 0

def is_square(n: int, z: int | None = None) -> bool:
    """Returns true if n can be represented as n=m**2, for some integer m"""

    if n == 1:
        return True

    if z is not None:
        return legendre_symbol(n, z) == 1

    x = n // 2
    seen = set([x])
    while x * x != n:
        x = (x + (n // x)) // 2
        if x in seen: 
            return False
        seen.add(x)
    return True
