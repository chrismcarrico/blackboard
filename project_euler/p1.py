from project_euler.problem.problem import Problem

problem = Problem(1, "Find all numbers less than 1000 that are divisible by 3 or 5")

@problem.register()
def solution():
    n = 1000
    return sum([i for i in range(n) if i % 5 == 0 or i % 3 == 0])

if __name__ == "__main__":
    problem.main()     