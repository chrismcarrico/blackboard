from mathlib.triangular_numbers import nth_triangular_number, triangular_number_generator

def test_nth_triangular_number_7():
    assert nth_triangular_number(7) == 28
    
def test_generator_7():
    
    generator = triangular_number_generator()
    
    while True:
        a,b = next(generator)
        
        if a == 7:
            break
        
    assert b == 28