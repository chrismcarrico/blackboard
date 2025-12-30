import math
import typing

def primes_less_than_n(n: int) -> list[int]:
    is_prime = [1]*n

    is_prime[0] = 0
    is_prime[1] = 0

    for i in range(2, math.isqrt(n)+1): 
        if is_prime[i]:
            for j in range(i*i, n, i):
                is_prime[j] = 0

    return [i for i, prime in enumerate(is_prime) if prime]

def primes_less_than_n_generator(n: int) -> typing.Generator[int]:
    
    assert n > 1

    integers = [1]*(n)
    integers[0] = 0
    integers[1] = 0
    
    for i, is_prime in enumerate(integers):
        if is_prime:
            yield i
            for k in range(i*i, n, i):
                integers[k] = 0
                
