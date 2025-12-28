import pytest

from mathlib.tonelli_shanks import tonelli_shanks

@pytest.mark.parametrize(
    "n,p,result", 
    [
        (10, 13, (7,6)), 
        (56, 101, (37, 64)), 
        (1030, 10009, (1632, 8377)), 
        (44402, 100049, (30468, 69581)), 
        (665820697, 1000000009, (378633312, 621366697)), 
        (881398088036, 1000000000039, (791399408049, 208600591990)), 
    ]
)
def test_tonelli_shanks(n, p, result):
    assert tonelli_shanks(n, p) == result