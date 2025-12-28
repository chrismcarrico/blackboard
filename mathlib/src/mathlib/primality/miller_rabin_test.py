import pytest

from mathlib.primality.miller_rabin import is_known_prime, seperate_powers_of_two, miller_rabin


@pytest.mark.parametrize("n,test_result", [(13, True), (26, False), (1000, False)])
def test_is_known_prime_true(n, test_result):
    assert is_known_prime(n) == test_result


@pytest.mark.parametrize(
        "n,result", 
        [
            (2*2*2*13*5, (3, 13*5)), 
            (17*3, (0, 17*3)), 
            (5*3, (0, 15)),
            (2*5*3, (1, 15))
        ]
)
def test_seperate_powers_of_two(n, result):

    assert seperate_powers_of_two(n) == result


miller_rabin_trials = [
        (17, True),
        (4463, True),
        (2, True),
        (20753, True),
        (20753*3, False),
        (2**16, False),
        (20753*4463, False),
        (840, False)
    ]

@pytest.mark.parametrize("n,result", miller_rabin_trials)
def test_miller_rabin(n, result):
    assert miller_rabin(n, 5) == result
