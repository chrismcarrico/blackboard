from mathlib.eratoshenes import eratosthenes_generator

def test_first_10_primes():
    sieve = eratosthenes_generator(100)
    
    first_10 = [2,3,5,7,11,13,17,19,23,29]
    
    assert first_10 == [next(sieve) for _ in range(10)]
    
