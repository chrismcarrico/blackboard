from project_euler.problem.problem import Problem

from mathlib.perfect_number import is_abundent

problem = Problem(23, "Find the sum of all the positive integers which cannot be written as the sum of two abundant numbers.")


@problem.register()
def solution():

    n = 28123
    found = [0]*n
    abundant_numbers = []

    for i in range(1, n):
        if is_abundent(i):
            abundant_numbers.append(i)


    for i in abundant_numbers:
        for j in abundant_numbers:
            k = i + j
            if k < n:
                found[k] = 1

    return sum(i for i,value in enumerate(found) if value == 0)


if __name__ == "__main__":
    problem.main()