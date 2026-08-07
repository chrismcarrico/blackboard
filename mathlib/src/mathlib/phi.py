def phi(n: int) -> int:
    """Compute the Euler's totient function of n."""
    if n < 1:
        raise ValueError("n must be greater than or equal to 1")
    elif n == 1:
        return 1

    result = n
    p = 2
    while p * p <= n:
        if n % p == 0:
            while n % p == 0:
                n //= p
            result -= result // p
        p += 1

    if n > 1:
        result -= result // n

    return result