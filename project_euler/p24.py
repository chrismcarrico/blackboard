import itertools

from project_euler.problem.problem import Problem


problem = Problem(24, "What is the millionth lexicographic permutation of the digits 0, 1, 2, 3, 4, 5, 6, 7, 8 and 9?")


@problem.register()
def solution():

    numbers = [str(i) for i in range(10)]
    permutations = list(itertools.permutations(numbers))
    return int("".join(permutations[999_999]))


if __name__ == "__main__":
    problem.main()