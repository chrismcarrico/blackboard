def trial_division(n: int) -> int | None:
    """Returns the smallest prime factor of n, or None if n is prime"""

    p = 2
    while p * p <= n:
        if n % p == 0:
            return p
        p += 1

    return None
