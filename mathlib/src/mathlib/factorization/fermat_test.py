from mathlib.factorization.fermat import fermat_factorization

def test_small_psuedo():

    assert fermat_factorization(79*113) == 79


def test_prime():

    assert fermat_factorization(79) is None

def test_large_psuedo():

    assert fermat_factorization(7867*887) == 887

def test_square():

    assert fermat_factorization(17*17) == 17

def test_out_of_steps():

    assert fermat_factorization(3 * 1000003, max_steps=10) is None

def test_large_close_factors():

    p, q = 10**30 + 57, 10**30 + 1281
    assert fermat_factorization(p * q) == p
