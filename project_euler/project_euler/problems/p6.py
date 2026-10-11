"""Find (1 + 2 + ... + 100)**2 - (1**2 + 2**2 + ... + 100**2)"""
from project_euler.problem.problem import Problem

problem = Problem(6, "Find (1 + 2 + ... + 100)**2 - (1**2 + 2**2 + ... + 100**2)")

@problem.register()
def solution():
    natural_numbers = range(1,101)
    return (sum(natural_numbers)**2) - sum([i**2 for i in natural_numbers])


problem.register_answer(25164150)

if __name__ == "__main__":
    raise SystemExit(problem.main())
