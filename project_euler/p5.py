"""Find the smallest number divisible by 2...20"""

import math

from mathlib.eratoshenes import primes_less_than_n
from mathlib.factorization.vector import vector_factorization
from project_euler.solution_set.solution_set import SolutionSet

solution_set = SolutionSet(5, "Find the smallest number divisible by 2...20")

@solution_set.register("naive")
def solution_1():
        
    limit = math.prod(range(2, 21))
    
    for i in range(1,limit+1):
        if not any([i%divisor for divisor in range(2, 21)]):
            return i
            
    raise RuntimeError

@solution_set.register(default=True)
def solution_2():
    
    primes = primes_less_than_n(21)

    n = [0]*len(primes)
    for i in range(2,21):
        e = vector_factorization(i, primes)
        assert e
        for i, k in enumerate(e):
            n[i] = max(n[i], k)

                
    return math.prod([i**k for i,k in zip(primes, n)])
    
if __name__ == "__main__":
    solution_set.main()
