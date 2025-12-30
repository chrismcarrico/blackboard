from mathlib.eratoshenes import primes_less_than_n

def vector_factorization(n: int, primes: list[int] | None = None) -> list[int] | None:        
    
    primes = primes_less_than_n(n+1)

    factors = [0]*len(primes)

    for i, prime in enumerate(primes):

        while n % prime == 0:
            factors[i] += 1
            n //= prime

    if n == 1:
        return factors
    
    return None
        