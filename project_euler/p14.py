"""Which Collatz chain under 1_000_000 is the longest"""

from mathlib.collatz import collatz_chain_length
from project_euler.problem.problem import Problem

problem = Problem(14, "Which Collatz chain under 1_000_000 is the longest")

@problem.register()
def solution():
    
    n_limit = 1_000_000
    largest_n = 0
    largest_chain = 0
    
    for n in range(1, n_limit+1):
        current_chain = collatz_chain_length(n)
        if largest_chain < current_chain:
            largest_n = n
            largest_chain = current_chain
            
    return largest_n

if __name__ == "__main__":
    problem.main()