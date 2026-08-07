import random

from mathlib.gcd import gcd
from mathlib.phi import phi
from mathlib.factorization.naive import naive_factorization

def find_order_of_a_modulo_n(a: int, n: int) -> int:
    
    phi_n = phi(n)
    prime_factors = naive_factorization(phi_n)
    
    order_ = phi_n
    for p in prime_factors:
        while order_ % p == 0:
            # Check if a^(order/p) == 1 mod n
            if pow(a, order_ // p, n) == 1:
                order_ //= p
            else:
                break
                
    return order_

def shors(n: int, seed=None) -> list[int]:

    random.seed(seed)

    if n < 2:
        raise ValueError("n must be greater than or equal to 2")
    elif n == 2:
        return [2]
    elif n % 2 == 0:
        return [2, n // 2]
    
    while True:
        a = random.randint(2, n - 1)
        
        k = gcd(a, n)
        if k != 1:
            return [k, n//k]

        r = find_order_of_a_modulo_n(a, n)
        if r % 2 == 1:
            continue
        else:
            g = gcd(pow(a, r // 2, n
                        ) + 1, n)
            if g != 1 and g != n:
                return [g, n//g]