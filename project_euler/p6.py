"""Find (1 + 2 + ... + 100)**2 - (1**2 + 2**2 + ... + 100**2)"""
from project_euler.solution_set.solution_set import SolutionSet

solution_set = SolutionSet(6, "Find (1 + 2 + ... + 100)**2 - (1**2 + 2**2 + ... + 100**2)")

@solution_set.register()
def solution():
    natural_numbers = range(1,101)
    return (sum(natural_numbers)**2) - sum([i**2 for i in natural_numbers])

if __name__ == "__main__":
    solution_set.main()
