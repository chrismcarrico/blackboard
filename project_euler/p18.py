"""By starting at the top of the triangle below and moving to adjacent numbers on the row below, the maximum total from top to bottom is 23.

3
7 4
2 4 6
8 5 9 3

That is, 3 + 7 + 4 + 9 = 23.

Find the maximum total from top to bottom in the triangle saved in data/p18_input.txt"""

from project_euler.solution_set.solution_set import SolutionSet
from project_euler.data import load

solution_set = SolutionSet(18, "Find the maximum total from top to bottom in the triangle saved in data/p18_input.txt")

@solution_set.register()
def solution():
    data = load("p18_input").splitlines()
    data = [[int(j) for j in i.split()] for i in data]

    num_lines = len(data)
    current_line_index = num_lines - 2

    while current_line_index > -1:
        for i, num in enumerate(data[current_line_index]):
            data[current_line_index][i] = max(num + data[current_line_index+1][i], num + data[current_line_index+1][i+1])
        current_line_index = current_line_index - 1

    return data[0][0]

if __name__ == "__main__":
    solution_set.main()