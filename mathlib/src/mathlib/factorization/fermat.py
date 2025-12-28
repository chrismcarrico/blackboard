import math

from mathlib.square import is_square

def fermat_factorization(n: int) -> list[int]:

    a = math.ceil(math.sqrt(n))
    b2 = a**2 - n

    if a**2 == n:
        return [a]

    while not is_square(b2):
        a = a + 1
        b2 = a**2 - n

    b = math.isqrt(b2)

    if a-b == 1:
        return [a+b]

    return sorted([a + b, a - b], reverse=True)
    
