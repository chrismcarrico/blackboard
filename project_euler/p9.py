"""Find a Pythagorean triple such that a + b + c = 1000"""

from mathlib.pythagorean_triples import is_pythagorean_triple
from project_euler.solution_set.solution_set import SolutionSet

solution_set = SolutionSet(9, "Find a Pythagorean triple such that a + b + c = 1000")

@solution_set.register()
def solution():
    
    for i in range(1,1000):
        for k in range(1, 1000):
            for j in range(1, 1000):
                
                if i < j and j < k and (i + k + j) == 1000 and is_pythagorean_triple(i, j, k):
                    return i*j*k
