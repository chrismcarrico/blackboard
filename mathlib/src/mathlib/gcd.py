def gcd(a: int, b: int) -> int:

    assert a > 0 and b > 0

    while b:
        a, b = b, a%b
    return a