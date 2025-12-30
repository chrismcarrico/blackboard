import math

from mathlib.eratoshenes import primes_less_than_n_generator

def naive_factorization(n: int) -> list[int]:
    
    prime_factors = []
    
    if n < 2:
        return []
    
    sieve = primes_less_than_n_generator(n)
    
    p = 1
    while p < math.floor(math.sqrt(n)):
        try:
            p = next(sieve)
            if n % p == 0:
                prime_factors.append(p)
        except StopIteration:
            break
        
    if prime_factors:
        return prime_factors
        
    return [n]



    
        