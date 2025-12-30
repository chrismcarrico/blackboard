from mathlib.fibonacci_sequence import fibonacci_sequence_generator
from project_euler.solution_set.solution_set import SolutionSet

solution_set = SolutionSet(2, "Find the sum of all fibonacci numbers less than 4_000_000")

@solution_set.register()
def solution():
    
    n = 4_000_000
    sum = 0
    i = 0
    sequence = fibonacci_sequence_generator()

    while i < n:
        i = next(sequence)
        if i % 2 == 0:
            sum += i
            
    return sum
