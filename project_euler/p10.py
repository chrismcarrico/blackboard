"""Find the sum of all primes less than 2_000_000"""

from mathlib.eratoshenes import primes_less_than_n_generator
from project_euler.problem.problem import Problem

problem = Problem(10, "Find the sum of all primes less than 2_000_000")

@problem.register()
def solution():
    sieve = primes_less_than_n_generator(1_000_000_000)
    
    sum = 0
    
    while True:
        prime = next(sieve)
        if prime > 2_000_000:
            break
        sum += prime
        
    return sum
