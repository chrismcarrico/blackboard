import math

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

def solve_for_solutions(m: BinaryMatrix):

    m, marked = gf2_gaussian_elimination(m)

    dependent_columns = []
    for r, is_marked in enumerate(marked):
        if not is_marked:
            for c, value in enumerate(m[r]):
                if value == 1:
                    dependent_columns.append(c)


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

    solutions = gf2_gaussian_elimination(exponent_vectors)

    a = 1
    b_squared = 1

    for solution in solutions:
        for i, is_solution in enumerate(solution):

            if is_solution:
                a = (a * x_list[i]) % n
                b_squared = (b_squared * fx_list[i]) % n

        b = math.isqrt(b_squared)
        factor = gcd(a-b, n)

        if 1 < factor < n:
            return factor, n // factor
    
    return None
