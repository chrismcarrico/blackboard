from mathlib.factorization.pollard_rho import pollard_rho

def test_pollard_rho():
    assert pollard_rho(8051) == 97
def test_pollard_rho_out_of_steps():
    assert pollard_rho(1000003 * 1000033, max_steps=5) is None

def test_pollard_rho_cycle():
    assert pollard_rho(4) is None

def test_pollard_rho_starting_value():
    assert pollard_rho(8051, starting_value=2) == 97

def test_pollard_rho_tries_other_starting_values():
    n = 3 * 23
    assert pollard_rho(n, starting_value=2) is None
    assert pollard_rho(n) in (3, 23)
