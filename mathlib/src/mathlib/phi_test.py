from mathlib.phi import phi

def test_phi_1():
    assert phi(1) == 1

def test_phi_prime():
    assert phi(2) == 1
    assert phi(3) == 2
    assert phi(5) == 4
    assert phi(7) == 6
    assert phi(11) == 10
    assert phi(13) == 12
    assert phi(17) == 16
    assert phi(19) == 18
    
def test_phi_powers_of_prime():
    assert phi(4) == 2
    assert phi(8) == 4
    assert phi(9) == 6
    assert phi(16) == 8
    assert phi(25) == 20
    assert phi(27) == 18
    assert phi(32) == 16
    assert phi(49) == 42
    
def test_phi_highly_composite():
    assert phi(12) == 4
    assert phi(18) == 6
    assert phi(20) == 8
    assert phi(24) == 8
    assert phi(36) == 12
    assert phi(48) == 16
