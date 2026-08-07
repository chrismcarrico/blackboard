from mathlib.zellers_algorithm import zellers_algorithm
from project_euler.problem.problem import Problem

problem = Problem(19, "How many Sundays fell on the first of the month during the twentieth century (1 Jan 1901 to 31 Dec 2000)")

@problem.register()
def solution():

    sundays = 0

    for month in range(1,13):
        for year in range(1901, 2001):
            if zellers_algorithm(month, 1, year) == 1:
                sundays += 1

    return sundays

if __name__ == "__main__":
    problem.main()