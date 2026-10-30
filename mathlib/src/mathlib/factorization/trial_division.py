def trial_division(n: int) -> int | None:
    """Returns the smallest prime factor of n, or None if n is prime"""

    p = 2
    while p * p <= n:
        if n % p == 0:
            return p
        p += 1

    return None

def distinct_prime_factors(n: int) -> list[int]:
    """The distinct prime factors of n, in increasing order"""

    prime_factors = []

    p = 2
    while p * p <= n:
        if n % p == 0:
            prime_factors.append(p)
            while n % p == 0:
                n //= p
        p += 1

    if n > 1:
        prime_factors.append(n)

    return prime_factors
