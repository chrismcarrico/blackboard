from mathlib.collatz import collatz_chain_length

def test_chain_length_13():
    assert collatz_chain_length(13) == 10
    
def test_chain_length_1():
    assert collatz_chain_length(1) == 4
    
def test_chain_length_100():
    assert collatz_chain_length(100) == 26
    