import math
import typing

from mathlib.quadratic_residue import legendre_symbol
from mathlib.eratoshenes import primes_less_than_n_generator
from mathlib.factorization.vector import partial_vector_factorization, vector_factorization
from mathlib.linalg.gf2_gaussian_elimination import find_dependencies
from mathlib.gcd import gcd
from mathlib.primality.miller_rabin import miller_rabin
from mathlib.tonelli_shanks import tonelli_shanks

# https://risencrypto.github.io/QuadraticSieve/#kraitchiks-factorization

MIN_SIEVE_B = 60
SIEVE_B_EXPONENT = 0.5
SIEVE_INTERVAL_PER_B = 2
SIEVE_SLACK = 4


def calculate_ceil_sqrt_n(n: int) -> int:
    root = math.isqrt(n)
    return root if root * root == n else root + 1

def calculate_b(n: int) -> int:

    ln_n = math.log(n)
    l = math.exp(math.sqrt(ln_n* math.log(ln_n)))
    return math.ceil(l**(1/math.sqrt(2)))

def polynomial_factory(n: int):
    ceil_sqrt_n = calculate_ceil_sqrt_n(n)

    def f(x):
        return (x + ceil_sqrt_n)**2 - n

    return f

def build_factor_base(n: int, b: int) -> list[int]:

    return [p for p in primes_less_than_n_generator(b) if legendre_symbol(n, p) == 1]

def factor_from_dependencies(n: int, a_list: list[int], exponent_vectors: list[list[int]], primes: list[int]) -> int | None:
    """Returns a non trivial factor of n

    Each relation is a_list[i]^2 = prod primes[j]^exponent_vectors[i][j] (mod n)
    """

    # each dependency is a set of relations whose right hand sides multiply to a perfect square
    dependencies = find_dependencies([[i%2 for i in exponent_vector] for exponent_vector in exponent_vectors])

    for dependency in dependencies:

        # a^2 = c^2 (mod n)
        a = 1
        for i in dependency:
            a = (a * a_list[i]) % n

        c = 1
        for j, p in enumerate(primes):
            exponent = sum(exponent_vectors[i][j] for i in dependency)
            c = (c * pow(p, exponent // 2, n)) % n

        difference = (a - c) % n
        if difference == 0:
            continue

        factor = gcd(difference, n)

        if 1 < factor < n:
            return factor

    return None

def quadratic_sieve_v1(n: int, b: int | None = None, m: int = 5000, tolerance: int = 5) -> int | None:
    """Returns a non trivial factor of n, or None if it fails to find one

    Finds smooth values of f(x) by trial division rather than by sieving
    """

    ceil_sqrt_n = calculate_ceil_sqrt_n(n)
    if ceil_sqrt_n**2 == n:
        return ceil_sqrt_n

    f = polynomial_factory(n)

    if b is None:
        b = calculate_b(n)

    factor_base = build_factor_base(n, b)

    exponent_vectors = []
    a_list = []
    x = 1
    while len(exponent_vectors) < len(factor_base) + tolerance:
        exponent_vector = vector_factorization(f(x), factor_base)
        if exponent_vector is not None:
            a_list.append(x + ceil_sqrt_n)
            exponent_vectors.append(exponent_vector)

        x += 1
        if x > m:
            break

    if not exponent_vectors:
        return None

    return factor_from_dependencies(n, a_list, exponent_vectors, factor_base)

def calculate_sieve_b(n: int) -> int:

    ln_n = math.log(n)
    l = math.exp(math.sqrt(ln_n * math.log(ln_n)))
    return max(MIN_SIEVE_B, math.ceil(l**SIEVE_B_EXPONENT))

def square_root(n: int, p: int) -> int:
    """A square root of n modulo the prime p, of which n must be a quadratic residue"""

    roots = tonelli_shanks(n % p, p)
    assert roots is not None
    return roots[0]

def square_roots(n: int, factor_base: list[int]) -> list[int]:
    """A square root of n modulo each prime of the factor base"""

    return [square_root(n, p) for p in factor_base]

def polynomial_roots(q: int, b: int, p: int, t: int) -> tuple[int, int]:
    """Both x (mod p) with (q^2*x + b)^2 = n (mod p), where t^2 = n (mod p)"""

    a_inverse = pow(q*q, -1, p)
    return ((t - b) * a_inverse) % p, ((-t - b) * a_inverse) % p

def lift_square_root(n: int, q: int) -> int:
    """Hensel lifts a square root of n modulo q to one modulo q^2"""

    t = square_root(n, q)
    return (t + q * ((((n - t*t) // q) * pow(2*t, -1, q)) % q)) % (q*q)

def polynomial_generator(n: int, m: int) -> typing.Generator[tuple[int, int]]:
    """Yields (q, b) with b^2 = n (mod q^2), so that (q^2*x + b)^2 - n = q^2 * g(x)

    The first is the single polynomial of the basic sieve (q = 1), the rest are those of the
    multiple polynomial sieve, with q chosen to keep g(x) small over -m <= x <= m
    """

    yield 1, calculate_ceil_sqrt_n(n)

    q = max(3, math.isqrt(math.isqrt(2*n) // m) | 1)
    while True:
        if miller_rabin(q, 20) and legendre_symbol(n, q) == 1:
            yield q, lift_square_root(n, q)
        q += 2

def sieve_polynomial(n: int, q: int, b: int, m: int, factor_base: list[int], roots: list[int], slack: float) -> typing.Generator[tuple[int, int]]:
    """Yields (x, g(x)) for -m <= x <= m where g(x) is likely to be smooth over the factor base"""

    a = q*q
    c = (b*b - n) // a

    size = 2*m + 1
    sieve = [0.0]*size

    for p, t in zip(factor_base, roots):

        # g(x) is linear rather than quadratic modulo these, trial division will still find them
        if p == 2 or a % p == 0:
            continue

        log_p = math.log2(p)
        for root in set(polynomial_roots(q, b, p, t)):
            for i in range((root + m) % p, size, p):
                sieve[i] += log_p

    for i, log_smooth_part in enumerate(sieve):
        x = i - m
        gx = (a*x + 2*b)*x + c
        if gx != 0 and log_smooth_part + slack >= abs(gx).bit_length():
            yield x, gx

def quadratic_sieve(
        n: int,
        b: int | None = None,
        m: int | None = None,
        tolerance: int = 5,
        large_prime_multiplier: int = 100,
        max_polynomials: int = 10000,
        max_attempts: int = 5,
    ) -> int | None:
    """Returns a non trivial factor of n, or None if it fails to find one"""

    ceil_sqrt_n = calculate_ceil_sqrt_n(n)
    if ceil_sqrt_n**2 == n:
        return ceil_sqrt_n

    if b is None:
        b = calculate_sieve_b(n)

    if m is None:
        m = SIEVE_INTERVAL_PER_B * b

    factor_base = build_factor_base(n, b)
    roots = square_roots(n, factor_base)

    # g(x) may be negative, so -1 is treated as one more prime
    primes = [-1] + factor_base

    large_prime_bound = large_prime_multiplier * factor_base[-1]
    slack = math.log2(large_prime_bound) + SIEVE_SLACK

    a_list = []
    exponent_vectors = []
    seen = set()
    partials = {}

    polynomials = polynomial_generator(n, m)
    polynomials_used = 0
    relations_needed = len(primes) + tolerance

    for _ in range(max_attempts):

        while len(a_list) < relations_needed and polynomials_used < max_polynomials:

            q, poly_b = next(polynomials)
            polynomials_used += 1
            q_inverse = pow(q, -1, n)

            for x, gx in sieve_polynomial(n, q, poly_b, m, factor_base, roots, slack):

                # a^2 = g(x) (mod n)
                a = ((q*q*x + poly_b) * q_inverse) % n

                # small n produce the same relation again and again
                relation = (min(a, n - a), gx)
                if relation in seen:
                    continue
                seen.add(relation)

                exponent_vector, cofactor = partial_vector_factorization(abs(gx), factor_base)
                exponent_vector = [int(gx < 0)] + exponent_vector

                if cofactor == 1:
                    a_list.append(a)
                    exponent_vectors.append(exponent_vector)

                elif cofactor < large_prime_bound:

                    # two relations sharing a large prime multiply to one without it
                    if cofactor not in partials:
                        partials[cofactor] = (a, exponent_vector)
                        continue

                    factor = gcd(cofactor, n)
                    if 1 < factor < n:
                        return factor
                    elif factor == n:
                        continue

                    other_a, other_exponent_vector = partials[cofactor]
                    a_list.append((a * other_a * pow(cofactor, -1, n)) % n)
                    exponent_vectors.append([i + j for i, j in zip(exponent_vector, other_exponent_vector)])

        if not a_list:
            return None

        if factor := factor_from_dependencies(n, a_list, exponent_vectors, primes):
            return factor

        if polynomials_used >= max_polynomials:
            return None

        relations_needed = len(a_list) + tolerance

    return None
