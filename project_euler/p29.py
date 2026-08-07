from project_euler.problem.problem import Problem

problem = Problem(29)


@problem.register()
def solution():
    
    a_b = []
    for a in range(2,101):
        for b in range(2, 101):
            a_b.append(a**b)
    
    return len(set(a_b))
            

if __name__ == "__main__":
    problem.main()