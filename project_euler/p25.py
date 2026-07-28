from mathlib.fib import get_next_fib

from project_euler.solution_set.solution_set import SolutionSet

solution_set = SolutionSet(25, "What is the index of the first term in the Fibonacci sequence to contain 1000 digits?")


@solution_set.register()
def solution():

    fib_gen = get_next_fib()
    i = 1
    while True:
        n = next(fib_gen)
        
        if len(str(n)) >= 1000:
            break
        
        i += 1
        
    return i


if __name__ == "__main__":
    solution_set.main()