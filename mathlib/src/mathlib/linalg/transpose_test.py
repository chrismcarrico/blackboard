import pytest

from mathlib.linalg.transpose import transpose

@pytest.fixture
def identity():
    return [[1,0,0], [0,1,0], [0,0,1]]

@pytest.fixture()
def m1():
    return [[1,2], [3,4], [5,6]]

@pytest.fixture()
def m2():
    return [[1,3,5], [2,4,6]]

def test_identity(identity):
    assert transpose(identity) == identity

def test_m1_t(m1, m2):
    assert transpose(m1) == m2

def test_m2_t(m1, m2):
    assert transpose(m2) == m1

def test_double_transpose(m1):
    assert transpose(transpose(m1)) == m1