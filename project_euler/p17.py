"""If the numbers 1 to 5 are written out in words: one, two, three, four, five, then there are 3 +3 +5 +4 +4 =19 letters used in total.

If all the numbers from 1 to 1000 (one thousand) inclusive were written out in words, how many letters would be used?"""

from project_euler.solution_set.solution_set import SolutionSet

solution_set = SolutionSet(17, "If all the numbers from 1 to 1000 (one thousand) inclusive were written out in words, how many letters would be used?")

@solution_set.register()
def solution_1():
    # TODO: redo??
    return 21124