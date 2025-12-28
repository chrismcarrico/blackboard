from solution_set.solution_set import SolutionSet

from mathlib.perfect_number import is_abundent

solution_set = SolutionSet(23, "Find the sum of all the positive integers which cannot be written as the sum of two abundant numbers.")


@solution_set.register()
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
    solution_set.main()