"""Find the sum of all primes less than 2_000_000"""

from mathlib.eratoshenes import eratosthenes_generator
from solution_set.solution_set import SolutionSet

solution_set = SolutionSet(10, "Find the sum of all primes less than 2_000_000")

@solution_set.register()
def solution():
    sieve = eratosthenes_generator(1_000_000_000)
    
    sum = 0
    
    while True:
        prime = next(sieve)
        if prime > 2_000_000:
            break
        sum += prime
        
    return sum
