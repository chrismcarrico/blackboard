from mathlib.amicable_numbers import d
from project_euler.solution_set.solution_set import SolutionSet

solution_set = SolutionSet(21, "Evaluate the sum of all the amicable numbers under 10000.")

@solution_set.register()
def solution():

    bound = 10_000
    amicable_numbers = []

    for i in range(bound):

        if i not in amicable_numbers:
            possible = d(i)

            if possible < bound and possible != i:
                if d(possible) == i:
                    amicable_numbers.append(i)
                    amicable_numbers.append(possible)

    return sum(amicable_numbers)


if __name__ == "__main__":
    solution_set.main()
