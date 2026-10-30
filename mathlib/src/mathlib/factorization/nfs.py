import math
import random
import typing

from mathlib.eratoshenes import primes_less_than_n
from mathlib.factorization.squares import factor_from_dependencies as factor_from_squares
from mathlib.factorization.squares import log_sieve, square_root_of_product
from mathlib.factorization.trial_division import distinct_prime_factors
from mathlib.factorization.vector import partial_vector_factorization
from mathlib.perfect_power import integer_root
from mathlib.primality.miller_rabin import next_prime
from mathlib.quadratic_residue import legendre_symbol

# Matthew Briggs, An Introduction to the General Number Field Sieve (1998)
#
# f is a monic polynomial of odd degree d with f(m) = 0 (mod n), alpha is a root of f.
# a relation is a coprime pair (a, b) for which both a - b*m and the norm of a - b*alpha are smooth.
# a set of relations whose product is a square on both sides gives x^2 = y^2 (mod n) through the
# homomorphism Z[alpha] -> Z/nZ that sends alpha to m.

# a polynomial is the list of its coefficients, lowest degree first
Polynomial = list[int]

MIN_B = 500
B_MULTIPLIER = 0.5
A_PER_B = 10
SIEVE_SLACK = 10
CHARACTERS = 30
LARGE_DEGREE_DIGITS = 100
BRUTE_FORCE_ROOTS_BELOW = 100
INERT_PRIME_LIMIT = 100_000


def evaluate(f: Polynomial, x: int, modulus: int | None = None) -> int:

    result = 0
    for c in reversed(f):
        result = result * x + c
        if modulus is not None:
            result %= modulus

    return result

def derivative(f: Polynomial) -> Polynomial:

    return [i * c for i, c in enumerate(f)][1:]

def homogeneous_norm(f: Polynomial, a: int, b: int) -> int:
    """F(a, b) = b^d * f(a/b), which for monic f is the norm of a - b*alpha"""

    # horner's rule in a, with c_i picking up b^(d-i) on the way in
    result = 0
    b_power = 1
    for c in reversed(f):
        result = result * a + c * b_power
        b_power *= b

    return result

def _trim(f: Polynomial) -> Polynomial:

    while f and f[-1] == 0:
        f.pop()
    return f

def _reduce(f: Polynomial, p: int) -> Polynomial:

    return _trim([c % p for c in f])

def _subtract(f: Polynomial, g: Polynomial, p: int) -> Polynomial:

    length = max(len(f), len(g))
    f = f + [0] * (length - len(f))
    g = g + [0] * (length - len(g))
    return _reduce([i - j for i, j in zip(f, g)], p)

def _multiply(f: Polynomial, g: Polynomial) -> Polynomial:

    if not f or not g:
        return []

    product = [0] * (len(f) + len(g) - 1)
    for i, x in enumerate(f):
        if x:
            for j, y in enumerate(g):
                product[i + j] += x * y

    return product

def _mod_f(g: Polynomial, f: Polynomial, modulus: int | None = None) -> Polynomial:
    """g reduced modulo the monic polynomial f, as exactly d coefficients, and modulo modulus if given"""

    d = len(f) - 1
    g = g + [0] * max(0, d - len(g))

    for k in range(len(g) - 1, d - 1, -1):
        c = g[k]
        if c:
            for i in range(d):
                g[k - d + i] -= c * f[i]

    g = g[:d]
    if modulus is not None:
        g = [c % modulus for c in g]

    return g

def _mulmod(g: Polynomial, h: Polynomial, f: Polynomial, modulus: int | None = None) -> Polynomial:

    return _mod_f(_multiply(g, h), f, modulus)

def _powmod(g: Polynomial, e: int, f: Polynomial, modulus: int) -> Polynomial:
    """g^e modulo the monic polynomial f and modulus"""

    result = _mod_f([1], f, modulus)
    g = _mod_f(g, f, modulus)
    while e:
        if e & 1:
            result = _mulmod(result, g, f, modulus)
        g = _mulmod(g, g, f, modulus)
        e >>= 1

    return result

def _divmod_mod_p(f: Polynomial, g: Polynomial, p: int) -> tuple[Polynomial, Polynomial]:

    f = _reduce(f, p)
    g = _reduce(g, p)
    inverse = pow(g[-1], -1, p)

    quotient = [0] * max(0, len(f) - len(g) + 1)
    while len(f) >= len(g):
        c = (f[-1] * inverse) % p
        shift = len(f) - len(g)
        quotient[shift] = c
        for i, x in enumerate(g):
            f[shift + i] = (f[shift + i] - c * x) % p
        _trim(f)

    return quotient, f

def _gcd_mod_p(f: Polynomial, g: Polynomial, p: int) -> Polynomial:
    """The monic greatest common divisor of f and g over F_p"""

    f = _reduce(f, p)
    g = _reduce(g, p)
    while g:
        f, g = g, _divmod_mod_p(f, g, p)[1]

    inverse = pow(f[-1], -1, p)
    return [(c * inverse) % p for c in f]

def _split_roots(g: Polynomial, p: int) -> list[int]:
    """The roots of g over F_p, where g is monic and a product of distinct linear factors (Cantor-Zassenhaus)"""

    d = len(g) - 1
    if d == 0:
        return []
    if d == 1:
        return [(-g[0]) % p]

    while True:
        # (x + delta)^((p-1)/2) is 1 at about half of the roots, so the gcd splits g
        delta = random.randrange(p)
        h = _subtract(_powmod([delta, 1], (p - 1) // 2, g, p), [1], p)
        k = _gcd_mod_p(g, h, p)
        if 0 < len(k) - 1 < d:
            return _split_roots(k, p) + _split_roots(_divmod_mod_p(g, k, p)[0], p)

def roots_mod_p(f: Polynomial, p: int) -> list[int]:
    """The distinct roots of the monic polynomial f modulo the prime p, in increasing order"""

    if p < BRUTE_FORCE_ROOTS_BELOW:
        return [r for r in range(p) if evaluate(f, r, p) == 0]

    f = _reduce(f, p)

    # the roots of x^p - x are exactly the elements of F_p
    x_to_the_p = _powmod([0, 1], p, f, p)
    g = _gcd_mod_p(f, _subtract(x_to_the_p, [0, 1], p), p)

    return sorted(_split_roots(g, p))

def is_irreducible_mod_p(f: Polynomial, p: int) -> bool:
    """Whether the monic polynomial f is irreducible over F_p (Rabin's test)"""

    d = len(f) - 1
    f = _reduce(f, p)
    x = [0, 1]

    # x^(p^k) for k = 0..d
    powers = [_mod_f(x, f, p)]
    for _ in range(d):
        powers.append(_powmod(powers[-1], p, f, p))

    if _subtract(powers[d], x, p) != []:
        return False

    for q in distinct_prime_factors(d):
        if len(_gcd_mod_p(f, _subtract(powers[d // q], x, p), p)) > 1:
            return False

    return True

def calculate_degree(n: int) -> int:

    return 5 if len(str(n)) > LARGE_DEGREE_DIGITS else 3

def calculate_b(n: int) -> int:

    # L_n[1/3, (8/9)^(1/3)], the smoothness bound that is optimal in theory
    ln_n = math.log(n)
    l = math.exp((8 / 9) ** (1 / 3) * ln_n ** (1 / 3) * math.log(ln_n) ** (2 / 3))
    return max(MIN_B, math.ceil(B_MULTIPLIER * l))

def select_polynomial(n: int, degree: int) -> tuple[Polynomial, int]:
    """(f, m) with f(m) = n, the coefficients of f being the base m digits of n

    f is monic as long as n < 2*m^degree, which holds for any n that is not tiny
    """

    m = integer_root(n, degree)

    f = []
    remainder = n
    for _ in range(degree):
        f.append(remainder % m)
        remainder //= m
    f.append(remainder)

    return f, m

def find_inert_prime(f: Polynomial, limit: int = INERT_PRIME_LIMIT) -> int | None:
    """A prime p = 3 (mod 4) modulo which f is irreducible

    Such a prime also proves that f is irreducible over the integers
    """

    return next((p for p in primes_less_than_n(limit) if p % 4 == 3 and is_irreducible_mod_p(f, p)), None)

def build_algebraic_base(f: Polynomial, primes: list[int]) -> list[tuple[int, int]]:
    """The pairs (p, r) with f(r) = 0 (mod p), each of which stands for a first degree prime ideal of Z[alpha]"""

    return [(p, r) for p in primes for r in roots_mod_p(f, p)]

def build_characters(f: Polynomial, start: int, count: int) -> list[tuple[int, int]]:
    """count pairs (q, s) with q >= start, f(s) = 0 and f'(s) != 0 (mod q)

    The legendre symbol of a - b*s modulo q is a quadratic character, a product of relations that is a
    square in Z[alpha] has all of them equal to 1
    """

    f_prime = derivative(f)
    characters = []
    q = start - 1
    while len(characters) < count:
        q = next_prime(q)
        characters.extend((q, s) for s in roots_mod_p(f, q) if evaluate(f_prime, s, q) != 0)

    return characters[:count]

def sieve_line(
        f: Polynomial,
        m: int,
        b: int,
        a_range: int,
        rational_base: list[int],
        algebraic_base: list[tuple[int, int]],
        slack: float,
    ) -> typing.Generator[tuple[int, int, int]]:
    """Yields (a, a - b*m, F(a, b)) for coprime a, b with -a_range <= a <= a_range where both are likely to be smooth"""

    size = 2 * a_range + 1

    # p divides a - b*m when a = b*m (mod p), and F(a, b) when a = b*r (mod p) for a root r of f
    rational = log_sieve(size, ((p, (b * m + a_range) % p) for p in rational_base))
    algebraic = log_sieve(size, ((p, (b * r + a_range) % p) for p, r in algebraic_base))

    # every |a - b*m| is at least this, so most of the line can be passed over without computing anything
    smallest = max(1, b * m - a_range).bit_length() - slack

    for i, log_smooth_part in enumerate(rational):

        if log_smooth_part < smallest:
            continue

        a = i - a_range
        if math.gcd(a, b) != 1:
            continue

        rational_norm = a - b * m
        if rational_norm == 0 or log_smooth_part + slack < abs(rational_norm).bit_length():
            continue

        algebraic_norm = homogeneous_norm(f, a, b)
        if algebraic_norm == 0 or algebraic[i] + slack < abs(algebraic_norm).bit_length():
            continue

        yield a, rational_norm, algebraic_norm

def _symmetric(g: Polynomial, modulus: int) -> Polynomial:

    return [c - modulus if c > modulus // 2 else c for c in g]

def product_mod_f(elements: list[Polynomial], f: Polynomial) -> Polynomial:
    """The product of elements of Z[alpha], multiplied pairwise so that the factors stay balanced"""

    elements = list(elements) or [[1]]
    while len(elements) > 1:
        elements = [
            _mulmod(elements[i], elements[i + 1], f) if i + 1 < len(elements) else elements[i]
            for i in range(0, len(elements), 2)
        ]

    return _mod_f(elements[0], f)

def algebraic_square_root(gamma: Polynomial, f: Polynomial, p: int) -> Polynomial | None:
    """beta in Z[alpha] with beta^2 = gamma, or None if gamma is not a square

    p must be a prime = 3 (mod 4) modulo which f, of odd degree, is irreducible. A square root is found
    in the field F_p[x]/(f), with p^d = 3 (mod 4), and is then lifted modulo p^2, p^4, ... until its
    coefficients are those of beta.
    """

    d = len(f) - 1
    gamma = _mod_f(gamma, f)
    field_size = p**d

    beta = _powmod(gamma, (field_size + 1) // 4, f, p)
    if _mulmod(beta, beta, f, p) != _mod_f(gamma, f, p):
        return None

    # newton's iteration for 1/sqrt(gamma) doubles the number of correct p-adic digits each time
    x = _powmod(beta, field_size - 2, f, p)

    f_bits = max(abs(c) for c in f).bit_length()
    bound = max(abs(c) for c in gamma).bit_length() + 2 * d * f_bits + 64

    modulus = p
    while modulus.bit_length() <= 2 * bound:

        modulus *= modulus
        half = (modulus + 1) // 2
        gamma_x_squared = _mulmod(gamma, _mulmod(x, x, f, modulus), f, modulus)
        three_minus = [(3 if i == 0 else 0) - c for i, c in enumerate(gamma_x_squared)]
        x = _mulmod(x, [c * half for c in three_minus], f, modulus)

        beta = _symmetric(_mulmod(gamma, x, f, modulus), modulus)
        if _mulmod(beta, beta, f) == gamma:
            return beta

    return None

class Relation(typing.NamedTuple):
    a: int
    b: int
    # exponents of -1 and of each prime of the rational factor base in a - b*m
    rational_exponents: list[int]
    # the row of the matrix, mod 2
    row: list[int]

def make_relation(
        a: int,
        b: int,
        rational_norm: int,
        algebraic_norm: int,
        rational_base: list[int],
        algebraic_primes: list[int],
        algebraic_columns: dict[tuple[int, int], int],
        characters: list[tuple[int, int]],
    ) -> Relation | None:
    """The relation for (a, b), or None if either norm is not smooth after all"""

    rational_exponents, cofactor = partial_vector_factorization(abs(rational_norm), rational_base)
    if cofactor != 1:
        return None

    prime_exponents, cofactor = partial_vector_factorization(abs(algebraic_norm), algebraic_primes)
    if cofactor != 1:
        return None

    # p divides the norm of a - b*alpha through the prime ideal (p, r) with a = b*r (mod p)
    algebraic_exponents = [0] * len(algebraic_columns)
    for p, exponent in zip(algebraic_primes, prime_exponents):
        if exponent:
            if b % p == 0:
                return None
            r = (a * pow(b, -1, p)) % p
            algebraic_exponents[algebraic_columns[(p, r)]] = exponent

    rational_exponents = [int(rational_norm < 0)] + rational_exponents

    row = (
        [e % 2 for e in rational_exponents]
        + [int(algebraic_norm < 0)]
        + [e % 2 for e in algebraic_exponents]
        + [int(legendre_symbol(a - b * s, q) == -1) for q, s in characters]
    )

    return Relation(a, b, rational_exponents, row)

def factor_from_dependencies(
        n: int,
        f: Polynomial,
        m: int,
        inert_prime: int,
        relations: list[Relation],
        rational_base: list[int],
    ) -> int | None:
    """Returns a non trivial factor of n from a set of relations whose product is a square on both sides"""

    f_prime = derivative(f)
    f_prime_squared = _mulmod(f_prime, f_prime, f)
    f_prime_m = evaluate(f_prime, m, n)
    primes = [-1] + rational_base

    def square_roots(dependency: list[int]) -> tuple[int, int] | None:

        # the f'(alpha)^2 makes sure the square root of the product lies in Z[alpha]
        gamma = product_mod_f(
            [f_prime_squared] + [[relations[i].a, -relations[i].b] for i in dependency],
            f,
        )

        beta = algebraic_square_root(gamma, f, inert_prime)
        if beta is None:
            return None

        # x^2 = phi(gamma) = f'(m)^2 * prod (a - b*m) = y^2 (mod n)
        exponents = [sum(column) for column in zip(*(relations[i].rational_exponents for i in dependency))]
        return evaluate(beta, m, n), (f_prime_m * square_root_of_product(primes, exponents, n)) % n

    return factor_from_squares(n, [relation.row for relation in relations], square_roots)

def number_field_sieve(
        n: int,
        polynomial: tuple[Polynomial, int] | None = None,
        degree: int | None = None,
        b: int | None = None,
        a_range: int | None = None,
        tolerance: int = 10,
        characters: int = CHARACTERS,
        max_lines: int = 10_000,
        max_attempts: int = 5,
    ) -> int | None:
    """Returns a non trivial factor of n, or None if it fails to find one

    polynomial: (f, m), the coefficients of f lowest degree first, with f monic of odd degree and
        f(m) = 0 (mod n). This is how the special number field sieve is run, for instance x^3 - 2 with
        m = 2^k for a factor of 2^(3k) - 2. By default f is chosen by select_polynomial.
    degree: the degree of f when it is chosen by select_polynomial
    b: the bound on the primes of both factor bases
    a_range: the sieve covers -a_range <= a <= a_range on each line b = 1, 2, ...
    """

    if b is None:
        b = calculate_b(n)

    if a_range is None:
        a_range = A_PER_B * b

    rational_base = primes_less_than_n(b)

    for p in rational_base:
        if n % p == 0:
            return p if p != n else None

    if polynomial is None:
        f, m = select_polynomial(n, degree or calculate_degree(n))
    else:
        f, m = polynomial
        if evaluate(f, m, n) != 0:
            raise ValueError("f(m) must be 0 (mod n)")

    if f[-1] != 1 or len(f) < 4 or len(f) % 2:
        if polynomial is not None:
            raise ValueError("f must be monic, of odd degree at least 3")
        return None

    # a common factor with n is as good as the sieve
    for value in (m, evaluate(derivative(f), m)):
        factor = math.gcd(value, n)
        if 1 < factor < n:
            return factor

    inert_prime = find_inert_prime(f)
    if inert_prime is None:
        return None

    algebraic_base = build_algebraic_base(f, rational_base)
    algebraic_primes = sorted({p for p, _ in algebraic_base})
    algebraic_columns = {pair: column for column, pair in enumerate(algebraic_base)}
    quadratic_characters = build_characters(f, b, characters)

    columns = 1 + len(rational_base) + 1 + len(algebraic_base) + len(quadratic_characters)
    slack = SIEVE_SLACK

    relations: list[Relation] = []
    relations_needed = columns + tolerance
    line = 1

    for _ in range(max_attempts):

        while len(relations) < relations_needed and line <= max_lines:

            for a, rational_norm, algebraic_norm in sieve_line(f, m, line, a_range, rational_base, algebraic_base, slack):
                relation = make_relation(
                    a, line, rational_norm, algebraic_norm,
                    rational_base, algebraic_primes, algebraic_columns, quadratic_characters,
                )
                if relation is not None:
                    relations.append(relation)

            line += 1

        if not relations:
            return None

        if factor := factor_from_dependencies(n, f, m, inert_prime, relations, rational_base):
            return factor

        if line > max_lines:
            return None

        relations_needed = len(relations) + tolerance

    return None
