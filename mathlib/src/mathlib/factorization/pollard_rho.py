from mathlib.gcd import gcd

def pollard_rho(n, starting_value=2):

    def g(x):
        return pow(x+1, 2, n)

    x = starting_value
    y = x
    d = 1

    while d == 1:
        x = g(x)
        y = g(g(y))
        d = gcd(abs(x-y), n)

    assert not d == n

    return d
        