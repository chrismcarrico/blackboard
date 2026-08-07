import math

from project_euler.problem.problem import Problem

problem = Problem(20, "Find the sum of the digits in the number 100!")

@problem.register()
def solution():
    return sum([int(i) for i in str(math.factorial(100))])

if __name__ == "__main__":
    problem.main()