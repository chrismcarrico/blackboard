"""Find the largest factor of 600851475143"""

import mathlib.factorization as factorization
from solution_set.solution_set import SolutionSet

solution_set = SolutionSet(3, "Find the largest factor of 600851475143")

@solution_set.register()
def solution():
    n = 600851475143
    return max(factorization.naive_factorization(n))


if __name__ == "__main__":
    solution_set.main()
