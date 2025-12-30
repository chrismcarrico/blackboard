"""Find the greatest product of four adjacent numbers in the same direction"""
import math

from project_euler.data import load
from project_euler.solution_set.solution_set import SolutionSet

solution_set = SolutionSet(11, "Find the greatest product of four adjacent numbers in the same direction")

@solution_set.register()
def solution():
        
    current_max = 0
    
    raw_array = load("p11_input")
    rows = raw_array.splitlines()
    nrows = len(rows)
    ncols = len(rows[0].split())
    array = raw_array.split()
        
    def a(r, c):
        if r < nrows and c < ncols:
            return int(array[ncols*r + c])
        return 0
    
    def right(r, c):
        return math.prod([a(r, c), a(r, c+1), a(r, c+2), a(r, c+3)])

    def down(r, c):
        return math.prod([a(r, c), a(r+1, c), a(r+2, c), a(r+3, c)])

    def diag_right_down(r, c):
        return math.prod([a(r, c), a(r+1, c+1), a(r+2, c+2), a(r+3, c+3)])

    def diag_left_down(r, c):
        return math.prod([a(r, c), a(r+1, c-1), a(r+2, c-2), a(r+3, c-3)])

    for r in range(nrows):
        for c in range(ncols):
            current_max = max([
                current_max, 
                right(r,c), 
                down(r,c), 
                diag_right_down(r,c), 
                diag_left_down(r,c),
            ])
        
    return current_max
    