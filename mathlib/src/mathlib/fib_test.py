from mathlib.fib import get_next_fib

def test_fib_until_i_12():
    fib_gen = get_next_fib()
    seq = [next(fib_gen) for _ in range(12)]
    assert seq == [1,1,2,3,5,8,13,21,34,55,89,144]