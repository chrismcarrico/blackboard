import math

from mathlib.eratoshenes import primes_less_than_n

def partial_vector_factorization(n: int, primes: list[int]) -> tuple[list[int], int]:
    """Returns the exponents of primes in n, and whatever is left of n after dividing them out"""

    factors = [0]*len(primes)

    for i, prime in enumerate(primes):

        if n == 1:
            break

        while n % prime == 0:
            factors[i] += 1
            n //= prime

    return factors, n

def vector_factorization(n: int, primes: list[int] | None = None) -> list[int] | None:

    if primes is None:
        primes = primes_less_than_n(math.isqrt(n))

    factors, cofactor = partial_vector_factorization(n, primes)

    if cofactor == 1:
        return factors

    return None
