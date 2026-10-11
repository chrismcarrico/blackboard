import argparse

import pytest

from mathlib.factorization.cli import THRESHOLD_HELP, build_parser, format_factors, integer, main

def test_integer():
    assert integer("360") == 360

def test_integer_expression():
    assert integer("2**89 - 1") == 2**89 - 1
    assert integer("10^40 + 121") == 10**40 + 121
    assert integer("(3 + 4) * 5") == 35

@pytest.mark.parametrize("string", ["abc", "1.5", "0", "-7", "7 / 2", "__import__('os')", "2**(10**9)", "2**-1", ""])
def test_integer_invalid(string):
    with pytest.raises(argparse.ArgumentTypeError):
        integer(string)

def test_format_factors():
    assert format_factors({2: 3, 3: 2, 5: 1}) == "2^3 * 3^2 * 5"
    assert format_factors({7: 1}) == "7"
    assert format_factors({}) == "1"

def test_main(capsys):
    assert main(["360"]) == 0
    assert capsys.readouterr().out == "360 = 2^3 * 3^2 * 5\n"

def test_main_several(capsys):
    assert main(["15", "1", "2**10", "1000003*1000033"]) == 0
    assert capsys.readouterr().out.splitlines() == [
        "15 = 3 * 5",
        "1 = 1",
        "1024 = 2^10",
        "1000036000099 = 1000003 * 1000033",
    ]

def test_main_method(capsys):
    assert main(["-m", "quadratic_sieve", "87463"]) == 0
    assert capsys.readouterr().out == "87463 = 149 * 587\n"

def test_main_thresholds(capsys):
    assert main(["87463", "--small-prime-bound", "0", "--pollard-rho-max-bits", "0", "--fermat-steps", "0"]) == 0
    assert capsys.readouterr().out == "87463 = 149 * 587\n"

def test_main_timed(capsys):
    assert main(["-t", "15"]) == 0
    out = capsys.readouterr().out
    assert out.startswith("15 = 3 * 5\t(") and out.endswith(" seconds)\n")

def test_main_invalid_integer(capsys):
    with pytest.raises(SystemExit) as error:
        main(["abc"])
    assert error.value.code == 2
    assert "'abc' is not an integer" in capsys.readouterr().err

def test_main_invalid_method(capsys):
    with pytest.raises(SystemExit) as error:
        main(["-m", "magic", "15"])
    assert error.value.code == 2

def test_main_no_integers():
    with pytest.raises(SystemExit) as error:
        main([])
    assert error.value.code == 2

def test_main_split_failure(capsys, monkeypatch):
    import mathlib.factorization.cli as cli

    def failing_factor(n, **options):
        if n == 21:
            raise RuntimeError("fermat could not split 21")
        return {3: 1, 5: 1}

    monkeypatch.setattr(cli, "factor", failing_factor)
    assert main(["21", "15"]) == 1
    captured = capsys.readouterr()
    assert captured.out == "15 = 3 * 5\n"
    assert captured.err == "21: fermat could not split 21\n"

def test_every_threshold_has_an_option_and_help():
    import inspect

    from mathlib.factorization.factor import factor

    thresholds = [name for name, parameter in inspect.signature(factor).parameters.items() if parameter.kind is inspect.Parameter.KEYWORD_ONLY]
    assert sorted(thresholds) == sorted(THRESHOLD_HELP)

    args = vars(build_parser().parse_args(["15"]))
    for name in thresholds:
        assert args[name] == inspect.signature(factor).parameters[name].default
