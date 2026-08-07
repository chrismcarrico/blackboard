from project_euler.problem.problem import Problem

problem = Problem(28, "Starting with the number 1 and moving to the right in a clockwise direction, a 5 by 5 spiral is formed as follows:")

# +2, +4, +6, +10

@problem.register()
def solution():
    N = 1001

    i = 1
    total = 0
    step = 2
    c = 0
    
    while step < N:
        problem.debug(f"i: {i}")
        total += i
        c += 1
        if c % 5 == 0:
            c = 1
            step += 2
        i += step
        problem.debug(f"step: {step}")

    return total

if __name__ == "__main__":
    problem.main()