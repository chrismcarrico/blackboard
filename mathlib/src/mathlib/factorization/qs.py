import math

from functools import reduce
from mathlib.quadratic_residue import legendre_symbol
from mathlib.eratoshenes import primes_less_than_n_generator
from mathlib.factorization.vector import vector_factorization
from mathlib.linalg.gf2_gaussian_elimination import BinaryMatrix, gf2_gaussian_elimination
from mathlib.gcd import gcd

# https://risencrypto.github.io/QuadraticSieve/#kraitchiks-factorization


def calculate_ceil_sqrt_n(n: int) -> int:
    return math.ceil(math.sqrt(n))

def calculate_b(n: int) -> int:

    ln_n = math.log(n)
    l = math.exp(math.sqrt(ln_n* math.log(ln_n)))
    return math.ceil(l**(1/math.sqrt(2)))

def polynomial_factory(n: int):
    def f(x):
        return (x + calculate_ceil_sqrt_n(n))**2 - n

    return f

def build_factor_base(n: int, b: int) -> list[int]:

    return [p for p in primes_less_than_n_generator(b) if legendre_symbol(n, p) == 1]

def bitwise_xor(a, b):

    return [i^j for i,j in zip(a,b)]

def solve_for_solutions_v1(m: BinaryMatrix):

    solutions = []
    m, marked = gf2_gaussian_elimination(m)

    all_possible_solutions = [[(i >> j) & 1 for j in range(len(m) - 1, -1, -1)] for i in range(1, 2**len(m))]


    return solutions


def quadratic_sieve_v1(n: int, b: int | None = None, m: int = 5000, tolerance: int = 5) -> tuple[int, int] | None:
    
    f = polynomial_factory(n)

    if b is None:
        b = calculate_b(n)

    factor_base = build_factor_base(n, b)

    exponent_vectors = []
    fx_list = []
    x_list = []
    x = 1
    while len(exponent_vectors) < len(factor_base) + tolerance:
        fx = f(x)
        if exponent_vector := vector_factorization(fx, factor_base):
            x_list.append(x)
            fx_list.append(fx)
            exponent_vectors.append([i%2 for i in exponent_vector])

        x += 1
        if x > m:
            break

    assert len(exponent_vectors) >= len(factor_base)

    solutions = solve_for_solutions_v1(exponent_vectors)

    a = 1
    b_squared = 1

    for solution in solutions:

        a = (a * x_list[solution]) % n
        b_squared = (b_squared * fx_list[solution]) % n

        b = math.isqrt(b_squared)

        if a-b >= n or a-b < 0:
            continue

        factor = gcd(a-b, n)

        if 1 < factor < n:
            return factor, n // factor
    
    