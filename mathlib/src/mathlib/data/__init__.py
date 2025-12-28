import functools
import importlib.resources as resources

@functools.cache
def get_known_primes() -> list[int]:
    known_primes = resources.read_text("mathlib.data", "known_primes.txt")
    return [int(i) for i in known_primes.strip().splitlines()]