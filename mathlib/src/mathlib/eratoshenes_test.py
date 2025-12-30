from mathlib.eratoshenes import primes_less_than_n_generator, primes_less_than_n

def test_first_10_primes_generator():
    sieve = primes_less_than_n_generator(100)
    
    first_10 = [2,3,5,7,11,13,17,19,23,29]
    
    assert first_10 == [next(sieve) for _ in range(10)]
    

def test_first_10_primes():

    assert primes_less_than_n(30) == [2,3,5,7,11,13,17,19,23,29]