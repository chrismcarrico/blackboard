from mathlib.zellers_algorithm import zellers_algorithm

def test_day_in_the_far_past():
    assert zellers_algorithm(11, 11, 1918) == 2

def test_day_in_the_past():
    assert zellers_algorithm(10, 15, 2025) == 4


def test_day_in_the_future():
    assert zellers_algorithm(7, 4, 2026) == 0

def test_day_in_the_far_future():
    assert zellers_algorithm(1, 14, 3000) == 3

