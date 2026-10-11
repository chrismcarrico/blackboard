from mathlib.gcd import gcd

DEFAULT_STARTING_VALUES = range(2, 12)

def _walk(n: int, starting_value: int, max_steps: int | None) -> int | None:

    def g(x):
        return pow(x+1, 2, n)

    x = starting_value
    y = x
    d = 1
    steps = 0

    while d == 1:

        if max_steps is not None and steps >= max_steps:
            return None

        x = g(x)
        y = g(g(y))
        steps += 1

        if x == y:
            return None

        d = gcd(abs(x-y), n)

    if d == n:
        return None

    return d

def pollard_rho(n: int, starting_value: int | None = None, max_steps: int | None = None) -> int | None:
    """Returns a non trivial factor of n, or None if it fails to find one

    A walk can cycle without finding a factor, so unless a starting value is given several are tried.
    max_steps limits the length of each walk.
    """

    starting_values = DEFAULT_STARTING_VALUES if starting_value is None else [starting_value]

    for value in starting_values:
        if factor := _walk(n, value, max_steps):
            return factor

    return None
