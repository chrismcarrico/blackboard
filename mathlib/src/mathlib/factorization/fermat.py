import math

from mathlib.quadratic_residue import is_square

def fermat_factorization(n: int, max_steps: int | None = None) -> int | None:
    """Returns the largest factor of n that is no greater than its square root, n must be odd

    Returns None if n is prime, or if max_steps is given and nothing is found within that many steps
    """

    a = math.isqrt(n)
    if a**2 == n:
        return a

    a = a + 1
    b2 = a**2 - n
    steps = 0

    while not is_square(b2):

        if max_steps is not None and steps >= max_steps:
            return None

        a = a + 1
        b2 = a**2 - n
        steps += 1

    b = math.isqrt(b2)

    if a-b == 1:
        return None

    return a - b
