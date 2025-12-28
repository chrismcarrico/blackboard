import itertools

from solution_set.solution_set import SolutionSet


solution_set = SolutionSet(24, "What is the millionth lexicographic permutation of the digits 0, 1, 2, 3, 4, 5, 6, 7, 8 and 9?")

@solution_set.register()
def solution():

    permutations = list(itertools.permutations(["0","1","2","3","4","5","6","7","8","9"]))
    return int("".join(permutations[999_999]))


if __name__ == "__main__":
    solution_set.main()