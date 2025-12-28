from mathlib.factorization.fermat import fermat_factorization

def test_small_psuedo():

    assert fermat_factorization(79*113) == [113, 79]


def test_prime():

    assert fermat_factorization(79) == [79]

def test_large_psuedo():

    assert fermat_factorization(7867*887) == [7867, 887]

def test_square():

    assert fermat_factorization(17*17) == [17]
