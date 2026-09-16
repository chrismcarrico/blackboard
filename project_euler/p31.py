from project_euler.problem.problem import Problem

problem = Problem(31)


p1 = (1, 200)
p2 = (2, 100)
p5 = (5, 40)
p10 = (10, 20)
p20 = (20, 10)
p50 = (50, 4)
e1 = (100, 2)
e2 = (200, 1)

@problem.register()
def solution():
    pass

if __name__ == "__main__":
    problem.main()