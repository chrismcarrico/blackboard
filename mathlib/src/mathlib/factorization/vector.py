import math

from mathlib.eratoshenes import eratosthenes_generator

def vector_factorization(n: int, primes: list[int] | None = None) ->list[int] | None:
    
    if primes is None:
        primes = [i for i in eratosthenes_generator(math.isqrt(n))]

    factors = [0]*len(primes)

    for i, prime in enumerate(primes):

        while n % prime == 0:
            factors[i] += 1
            n //= prime

    if n == 1:
        return factors
    
    return None
        