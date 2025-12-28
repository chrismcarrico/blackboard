"""Find the smallest number divisible by 2...20"""

import math

from mathlib.factorization.vector import vector_factorization
from solution_set.solution_set import SolutionSet

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
    
    unique_primes = {}
    for i in range(2,21):
        e = vector_factorization(i)
        for k in e:
            unique_primes[k[0]] = max(unique_primes.get(k[0],0), k[1])
                
    return math.prod([i**k for i,k in unique_primes.items()])
    
if __name__ == "__main__":
    solution_set.main()
