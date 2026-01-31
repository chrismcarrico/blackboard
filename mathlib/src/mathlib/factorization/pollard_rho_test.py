from mathlib.factorization.pollard_rho import pollard_rho

def test_pollard_rho():
    assert pollard_rho(8051) == 97