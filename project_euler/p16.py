from project_euler.problem.problem import Problem

problem = Problem(16, "Find the sum of the digits of the number 2**1000")

@problem.register()
def solution():
    return sum([int(i) for i in str(pow(2,1000))])

if __name__ == "__main__":
    problem.main()