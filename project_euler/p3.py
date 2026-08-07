"""Find the largest factor of 600851475143"""

from mathlib.factorization.naive import naive_factorization
from project_euler.problem.problem import Problem

problem = Problem(3, "Find the largest factor of 600851475143")

@problem.register()
def solution():
    n = 600851475143
    return max(naive_factorization(n))


if __name__ == "__main__":
    problem.main()
