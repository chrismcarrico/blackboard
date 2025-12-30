"""Find the 10_001th prime"""

from mathlib.eratoshenes import primes_less_than_n_generator
from project_euler.solution_set.solution_set import SolutionSet

solution_set = SolutionSet(7, "Find the 10_001th prime")

@solution_set.register()
def solution():
    
    sieve = primes_less_than_n_generator(10_000_000)
    discovered_primes = []
    
    while len(discovered_primes) != 10_001:
        discovered_primes.append(next(sieve))
        
    return discovered_primes[-1]

if __name__ == "__main__":
    solution_set.main()
    