from mathlib.reciprocal import calculate_reciprocal_long

def test_reciprocal_7():
    assert calculate_reciprocal_long(7, 12) == [1,4,2,8,5,7,1,4,2,8,5,7]
    
def test_reciprocal_2():
    assert calculate_reciprocal_long(2) == [5]
    
def test_reciprocal_3():
    assert calculate_reciprocal_long(3, 10) == [3,3,3,3,3,3,3,3,3,3]