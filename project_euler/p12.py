"""Find the first triangle number with over 500 divisors"""

from mathlib.sigma import sigma
from mathlib.triangular_numbers import nth_triangular_number_formula
from solution_set.solution_set import SolutionSet

solution_set = SolutionSet(12, "Find the first triangle number with over 500 divisors")

@solution_set.register()
def solution():
    
    nfactors = 0
    i = 1
    while nfactors < 500:
        a = nth_triangular_number_formula(i)
        nfactors = sigma(a)
        i += 1

    return a
