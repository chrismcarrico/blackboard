from project_euler.solution_set.solution_set import SolutionSet

solution_set = SolutionSet(1, "Find all numbers less than 1000 that are divisible by 3 or 5")

@solution_set.register()
def solution():
    n = 1000
    return sum([i for i in range(n) if i % 5 == 0 or i % 3 == 0])

if __name__ == "__main__":
    solution_set.main()     