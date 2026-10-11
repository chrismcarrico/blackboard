import functools
import typing

from mathlib.eratoshenes import primes_less_than_n
from mathlib.factorization.fermat import fermat_factorization
from mathlib.factorization.pollard_rho import pollard_rho
from mathlib.factorization.qs import quadratic_sieve
from mathlib.factorization.shors import find_factor
from mathlib.factorization.trial_division import trial_division
from mathlib.perfect_power import perfect_power
from mathlib.primality.miller_rabin import miller_rabin

Method = typing.Literal["auto", "trial_division", "fermat", "pollard_rho", "quadratic_sieve", "shors"]

METHODS: tuple[Method, ...] = typing.get_args(Method)

# every splitting algorithm takes n and returns a non trivial factor of it, or None if it fails
Splitter = typing.Callable[[int], int | None]

# defaults for the keyword arguments of factor, which describes them
SMALL_PRIME_BOUND = 10_000
POLLARD_RHO_MAX_BITS = 44
FERMAT_STEPS = 100
POLLARD_RHO_STEPS = 1_000
POLLARD_RHO_STEPS_LARGE = 20_000
LARGE_BITS = 80
MILLER_RABIN_TRIALS = 20

SPLITTERS: dict[str, Splitter] = {
    "trial_division": trial_division,
    "fermat": fermat_factorization,
    "pollard_rho": pollard_rho,
    "quadratic_sieve": quadratic_sieve,
    "shors": find_factor,
}

def plan(
        n: int,
        *,
        pollard_rho_max_bits: int = POLLARD_RHO_MAX_BITS,
        fermat_steps: int = FERMAT_STEPS,
        pollard_rho_steps: int = POLLARD_RHO_STEPS,
        pollard_rho_steps_large: int = POLLARD_RHO_STEPS_LARGE,
        large_bits: int = LARGE_BITS,
    ) -> list[tuple[str, Splitter]]:
    """The splitting algorithms worth trying on n, best first

    n is assumed to be odd, composite, not a perfect power, and to have no small prime factors.
    The keyword arguments are described in factor.
    """

    if n.bit_length() <= pollard_rho_max_bits:
        return [
            ("pollard_rho", pollard_rho),
            ("quadratic_sieve", quadratic_sieve),
            ("trial_division", trial_division),
        ]

    max_steps = pollard_rho_steps if n.bit_length() <= large_bits else pollard_rho_steps_large

    return [
        # instant when the two factors are close together, hopeless otherwise
        ("fermat", functools.partial(fermat_factorization, max_steps=fermat_steps)),
        # cost depends on the size of the smallest factor rather than on the size of n
        ("pollard_rho", functools.partial(pollard_rho, starting_value=2, max_steps=max_steps)),
        # cost depends only on the size of n
        ("quadratic_sieve", quadratic_sieve),
        ("pollard_rho", pollard_rho),
    ]

def split(n: int, method: Method = "auto", **plan_options: int) -> int:
    """A non trivial factor of n, which must be odd, composite and not a perfect power

    Any keyword arguments are passed on to plan
    """

    if method == "auto":
        splitters = plan(n, **plan_options)
    else:
        splitters = [(method, SPLITTERS[method])]

    for _, splitter in splitters:
        factor = splitter(n)
        if factor is not None and 1 < factor < n and n % factor == 0:
            return factor

    raise RuntimeError(f"{', '.join(name for name, _ in splitters)} could not split {n}")

def _factor(n: int, multiplicity: int, factors: dict[int, int], method: Method, miller_rabin_trials: int, plan_options: dict[str, int]) -> None:
    """Adds the prime factors of n, which must be odd, to factors"""

    if n == 1:
        return

    if miller_rabin(n, miller_rabin_trials):
        factors[n] = factors.get(n, 0) + multiplicity
        return

    # none of the splitting algorithms can be relied on to split a power of a single prime
    if power := perfect_power(n):
        root, exponent = power
        _factor(root, multiplicity * exponent, factors, method, miller_rabin_trials, plan_options)
        return

    divisor = split(n, method, **plan_options)
    _factor(divisor, multiplicity, factors, method, miller_rabin_trials, plan_options)
    _factor(n // divisor, multiplicity, factors, method, miller_rabin_trials, plan_options)

def factor(
        n: int,
        method: Method = "auto",
        *,
        small_prime_bound: int = SMALL_PRIME_BOUND,
        pollard_rho_max_bits: int = POLLARD_RHO_MAX_BITS,
        fermat_steps: int = FERMAT_STEPS,
        pollard_rho_steps: int = POLLARD_RHO_STEPS,
        pollard_rho_steps_large: int = POLLARD_RHO_STEPS_LARGE,
        large_bits: int = LARGE_BITS,
        miller_rabin_trials: int = MILLER_RABIN_TRIALS,
    ) -> dict[int, int]:
    """The prime factorization of n, as a mapping from each prime factor to its exponent

    By default each composite that turns up along the way is handed to whichever algorithm suits it,
    see plan. Passing a method does all of the splitting with that one algorithm instead.

    The keyword arguments are the thresholds that decide which algorithm gets which integer:

    small_prime_bound: every prime below this is divided out before anything cleverer is tried
    pollard_rho_max_bits: up to this many bits pollard rho is tried before the quadratic sieve
    fermat_steps: how long to look for close factors before falling back on the quadratic sieve
    pollard_rho_steps: how long to look for small factors before falling back on the quadratic sieve
    pollard_rho_steps_large: the same, for integers of more than large_bits bits
    large_bits: the size past which the quadratic sieve is slow enough to make a longer look worthwhile
    miller_rabin_trials: bases tried by the primality test once n is too big for it to be deterministic
    """

    if n < 1:
        raise ValueError("n must be greater than or equal to 1")

    if method not in METHODS:
        raise ValueError(f"method must be one of {', '.join(METHODS)}")

    plan_options = {
        "pollard_rho_max_bits": pollard_rho_max_bits,
        "fermat_steps": fermat_steps,
        "pollard_rho_steps": pollard_rho_steps,
        "pollard_rho_steps_large": pollard_rho_steps_large,
        "large_bits": large_bits,
    }

    factors: dict[int, int] = {}

    # fermat and shors both need n to be odd, so 2 is always divided out
    small_primes = primes_less_than_n(max(small_prime_bound, 3)) if method == "auto" else [2]

    for p in small_primes:

        if p * p > n:
            break

        while n % p == 0:
            factors[p] = factors.get(p, 0) + 1
            n //= p

    _factor(n, 1, factors, method, miller_rabin_trials, plan_options)

    return dict(sorted(factors.items()))
