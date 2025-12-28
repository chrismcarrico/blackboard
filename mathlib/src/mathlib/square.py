from mathlib.legendre import legendre_symbol

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
