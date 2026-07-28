from mathlib.cycles import find_longest_cycle

def test_no_cycle():
    assert find_longest_cycle([1,2,3,4,5]) == []

def test_find_longest_cycle():
    assert find_longest_cycle([1,2,3,1,2,3]) == [1,2,3]
    assert find_longest_cycle([1,2,1,2,1]) == [1,2]
    assert find_longest_cycle([1,2,3,4,5,6]*3) == [1,2,3,4,5,6]
    
def test_repeating_single_digit():
    assert find_longest_cycle([3,3,3,3,3]) == [3]

def test_partial_repeat():
    assert find_longest_cycle([1,6,6,6,6,1,6,6,6,6,1,6,6]) == [1,6,6,6,6]
    