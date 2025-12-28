from solution_set.solution_set import SolutionSet

solution_set = SolutionSet(16, "Find the sum of the digits of the number 2**1000")

@solution_set.register()
def solution():
    return sum([int(i) for i in str(pow(2,1000))])

if __name__ == "__main__":
    solution_set.main()