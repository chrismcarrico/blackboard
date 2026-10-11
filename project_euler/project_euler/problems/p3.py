"""Find the largest factor of 600851475143"""

from mathlib.factorization.factor import factor
from project_euler.problem.problem import Problem

problem = Problem(3, "Find the largest factor of 600851475143")

@problem.register()
def solution():
    n = 600851475143
    return max(factor(n))


problem.register_answer(6857)

if __name__ == "__main__":
    raise SystemExit(problem.main())
