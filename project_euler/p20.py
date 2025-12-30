import math

from project_euler.solution_set.solution_set import SolutionSet

solution_set = SolutionSet(20, "Find the sum of the digits in the number 100!")

@solution_set.register()
def solution():
    return sum([int(i) for i in str(math.factorial(100))])

if __name__ == "__main__":
    solution_set.main()