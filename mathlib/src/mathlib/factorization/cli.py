import argparse
import ast
import inspect
import operator
import sys
import time
import typing

from mathlib.factorization.factor import METHODS, factor

MAX_EXPONENT = 100_000

OPERATORS: dict[type, typing.Callable[[int, int], int]] = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Pow: operator.pow,
}

THRESHOLD_HELP = {
    "small_prime_bound": "Divide out every prime below N before trying anything cleverer",
    "pollard_rho_max_bits": "Try pollard rho before the quadratic sieve on integers of up to N bits",
    "fermat_steps": "Look for close factors for N steps before falling back on the quadratic sieve",
    "pollard_rho_steps": "Look for small factors for N steps before falling back on the quadratic sieve",
    "pollard_rho_steps_large": "The same, for integers of more than --large-bits bits",
    "large_bits": "Size past which --pollard-rho-steps-large is used",
    "miller_rabin_trials": "Bases tried by the primality test on large integers",
}

def _evaluate(node: ast.expr) -> int:

    if isinstance(node, ast.Constant) and type(node.value) is int:
        return node.value

    if isinstance(node, ast.UnaryOp) and isinstance(node.op, ast.USub):
        return -_evaluate(node.operand)

    if isinstance(node, ast.BinOp) and type(node.op) in OPERATORS:
        left, right = _evaluate(node.left), _evaluate(node.right)
        if isinstance(node.op, ast.Pow) and not 0 <= right <= MAX_EXPONENT:
            raise ValueError
        return OPERATORS[type(node.op)](left, right)

    raise ValueError

def integer(string: str) -> int:
    """Parses an integer, or an expression such as 2**89 - 1 or 10^40 + 121"""

    try:
        n = _evaluate(ast.parse(string.replace("^", "**").strip(), mode="eval").body)
    except (ValueError, SyntaxError, RecursionError):
        raise argparse.ArgumentTypeError(f"{string!r} is not an integer") from None

    if n < 1:
        raise argparse.ArgumentTypeError(f"{string!r} is less than 1")

    return n

def format_factors(factors: dict[int, int]) -> str:

    if not factors:
        return "1"

    return " * ".join(str(p) if e == 1 else f"{p}^{e}" for p, e in factors.items())

def build_parser() -> argparse.ArgumentParser:

    parser = argparse.ArgumentParser(
        prog="python -m mathlib.factorization",
        description="Find the prime factorization of one or more integers",
    )

    parser.add_argument(
        "integers",
        metavar="n",
        nargs="+",
        type=integer,
        help="Integer to factor, which may be written as an expression such as '2**89 - 1'"
    )
    parser.add_argument(
        "-m", "--method",
        choices=METHODS,
        default="auto",
        help="Algorithm to do the splitting with, auto picks one to suit each integer"
    )
    parser.add_argument(
        "-t", "--timed",
        action="store_true",
        default=False,
        help="Time each factorization"
    )

    # one option for each of the thresholds factor takes as a keyword argument
    thresholds = parser.add_argument_group("thresholds", "These decide which algorithm auto gives each integer to")
    for name, parameter in inspect.signature(factor).parameters.items():
        if parameter.kind is inspect.Parameter.KEYWORD_ONLY:
            thresholds.add_argument(
                f"--{name.replace('_', '-')}",
                type=int,
                default=parameter.default,
                metavar="N",
                help=f"{THRESHOLD_HELP.get(name, '')} (default: {parameter.default})".strip()
            )

    return parser

def main(argv: typing.Sequence[str] | None = None) -> int:

    args = vars(build_parser().parse_args(argv))

    integers = args.pop("integers")
    timed = args.pop("timed")

    status = 0
    for n in integers:

        st = time.time()
        try:
            factors = factor(n, **args)
        except RuntimeError as error:
            print(f"{n}: {error}", file=sys.stderr)
            status = 1
            continue
        se = time.time()

        line = f"{n} = {format_factors(factors)}"
        if timed:
            line += f"\t({se-st:.6f} seconds)"
        print(line)

    return status
