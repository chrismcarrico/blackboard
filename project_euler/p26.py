from mathlib.reciprocal import calculate_reciprocal_long
from mathlib.cycles import find_longest_cycle

from project_euler.problem.problem import Problem

problem = Problem(26, "Find the value of d < 1000 for which d contains the longest recurring cycle in its decimal fraction part.")


@problem.register()
def solution():
    
    max_d = 0
    max_cycle_length = 0
    
    for d in range(2, 1000):
        digits = calculate_reciprocal_long(d)
        for i in range(len(digits)):
 
            cycle = find_longest_cycle(digits[i:])
            
            if len(cycle) > max_cycle_length:
                max_d = d
                max_cycle_length = len(cycle)
                

    return max_d

if __name__ == "__main__":
    problem.main()