import pytest

from mathlib.tonelli_shanks import (
    tonelli_shanks, 
    _seperate_powers_of_2, 
    _find_first_z_st_non_qr_mod_p,
    _least_i_st_t2_i_is_1
)


@pytest.mark.parametrize(
    "n,s,q",
    [
        (1,0,1),
        (4,2,1),
        (6,1,3),
        (2**3*3*5,3,3*5),

    ]
)
def test_seperate_powers_of_2(n,s,q):
    assert _seperate_powers_of_2(n) == (s,q)


@pytest.mark.parametrize(
        "p,z",
        [
            (7,3),
            (13, 2),
            (17, 3)

        ]
)
def test_find_first_z_st_non_qr_mod_p(p,z):
    assert _find_first_z_st_non_qr_mod_p(p) == z


@pytest.mark.parametrize(
        "t,p,m,i",
        [
            (9,41,3,2),

        ]
)
def test_least_i_st_t2_i_is_1(t,p,m,i):
    assert _least_i_st_t2_i_is_1(t,p,m) == i


@pytest.mark.parametrize(
    "n,p,result", 
    [
        (5, 41, 28),
        (10, 13, 7), 
        (56, 101, 37), 
        (1030, 10009, 1632), 
        (44402, 100049, 30468), 
        (665820697, 1000000009, 378633312), 
        (881398088036, 1000000000039, 791399408049), 
    ]
)
def test_tonelli_shanks(n, p, result):
    assert tonelli_shanks(n, p) == result