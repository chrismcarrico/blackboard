import math
import typing

from mathlib.gcd import gcd
from mathlib.linalg.gf2_gaussian_elimination import find_dependencies

# the step the quadratic and number field sieves share: find a set of relations whose product is a
# square, which gives x^2 = y^2 (mod n), and hope that gcd(x - y, n) is a non trivial factor of n

def log_sieve(size: int, progressions: typing.Iterable[tuple[int, int]]) -> list[float]:
    """For each (p, start), adds log2(p) at start, start + p, start + 2p, ... of a list of size zeros"""

    sieve = [0.0] * size
    for p, start in progressions:
        log_p = math.log2(p)
        for i in range(start, size, p):
            sieve[i] += log_p

    return sieve

def square_root_of_product(primes: list[int], exponents: typing.Iterable[int], n: int) -> int:
    """prod primes[j]^(exponents[j] / 2) (mod n), the exponents must all be even"""

    root = 1
    for p, exponent in zip(primes, exponents):
        root = (root * pow(p, exponent // 2, n)) % n

    return root

def factor_from_dependencies(
        n: int,
        rows: list[list[int]],
        square_roots: typing.Callable[[list[int]], tuple[int, int] | None],
    ) -> int | None:
    """Returns a non trivial factor of n, or None if no dependency gives one

    Each set of rows that sums to zero over GF(2) is passed to square_roots, which returns x and y with
    x^2 = y^2 (mod n), or None if the set turns out not to give a square after all
    """

    for dependency in find_dependencies(rows):

        roots = square_roots(dependency)
        if roots is None:
            continue

        # if gcd(x - y, n) is trivial so is gcd(x + y, n), since n divides their product
        x, y = roots
        difference = (x - y) % n
        if difference == 0:
            continue

        factor = gcd(difference, n)
        if 1 < factor < n:
            return factor

    return None
