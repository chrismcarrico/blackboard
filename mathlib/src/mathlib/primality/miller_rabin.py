import random
from mathlib.data import get_known_primes

def is_known_prime(n: int) -> bool:
    known_primes = get_known_primes()
    return n in known_primes

def seperate_powers_of_two(n: int) -> tuple[int, int]:
    d, s = n, 0
    while not d % 2:
        d, s = d >> 1, s + 1

    return s, d

def _try_composite(a, d, n, s):
    x = pow(a,d,n)
    if x == 1:
        return False
    for _ in range(s):
        x = pow(x, 2, n)
        if x == n -1:
            return False
    return True # n  is definitely composite

def miller_rabin(n: int, max_trials: int):
    # https://rosettacode.org/wiki/Miller-Rabin_primality_test#Python:_Proved_correct_up_to_large_N

    assert n > 0

    known_primes = get_known_primes()

    if is_known_prime(n):
        return True
    
    if any((n % p) == 0 for p in known_primes) or n in (0, 1):
        return False

    s,d = seperate_powers_of_two(n-1)

    if n < 1373653: 
        return not any(_try_composite(a, d, n, s) for a in (2, 3))
    if n < 25326001: 
        return not any(_try_composite(a, d, n, s) for a in (2, 3, 5))
    if n < 118670087467: 
        if n == 3215031751: 
            return False
        return not any(_try_composite(a, d, n, s) for a in (2, 3, 5, 7))
    if n < 2152302898747: 
        return not any(_try_composite(a, d, n, s) for a in (2, 3, 5, 7, 11))
    if n < 3474749660383: 
        return not any(_try_composite(a, d, n, s) for a in (2, 3, 5, 7, 11, 13))
    if n < 341550071728321: 
        return not any(_try_composite(a, d, n, s) for a in (2, 3, 5, 7, 11, 13, 17))

    return not any(_try_composite(a, d, n, s) 
                   for a in known_primes[:max_trials])
    