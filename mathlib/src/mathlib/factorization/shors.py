import random

from mathlib.factorization.trial_division import distinct_prime_factors
from mathlib.gcd import gcd
from mathlib.perfect_power import perfect_power_root
from mathlib.phi import phi
from mathlib.primality.miller_rabin import miller_rabin

def find_order_of_a_modulo_n(a: int, n: int) -> int:
    """The step a quantum computer would do, the smallest r > 0 with a^r = 1 (mod n)"""

    phi_n = phi(n)
    prime_factors = distinct_prime_factors(phi_n)

    order_ = phi_n
    for p in prime_factors:
        while order_ % p == 0:
            # Check if a^(order/p) == 1 mod n
            if pow(a, order_ // p, n) == 1:
                order_ //= p
            else:
                break

    return order_

def find_factor(n: int, rng: random.Random | None = None) -> int:
    """Returns a non trivial factor of n, which must be odd with at least two distinct prime factors

    Order finding cannot split a power of a single prime
    """

    if rng is None:
        rng = random.Random()

    while True:
        a = rng.randint(2, n - 1)

        k = gcd(a, n)
        if k != 1:
            return k

        r = find_order_of_a_modulo_n(a, n)
        if r % 2 == 1:
            continue

        g = gcd(pow(a, r // 2, n) + 1, n)
        if g != 1 and g != n:
            return g

def _prime_factors(n: int, rng: random.Random) -> set[int]:

    if n == 1:
        return set()

    if n % 2 == 0:
        while n % 2 == 0:
            n //= 2
        return {2} | _prime_factors(n, rng)

    if miller_rabin(n, 20):
        return {n}

    root = perfect_power_root(n)
    if root is not None:
        return _prime_factors(root, rng)

    factor = find_factor(n, rng)
    return _prime_factors(factor, rng) | _prime_factors(n // factor, rng)

def shors(n: int, seed=None) -> list[int]:
    """The distinct prime factors of n, in increasing order"""

    if n < 2:
        raise ValueError("n must be greater than or equal to 2")

    return sorted(_prime_factors(n, random.Random(seed)))
