import argparse
import json
import logging
import time

from project_euler import registry
from project_euler.problem.problem import (
    Problem,
    add_check_arguments,
    add_run_arguments,
    add_verbose_argument,
    configure_logging,
)

logger = logging.getLogger("project_euler")

TEMPLATE = '''from project_euler.problem.problem import Problem

problem = Problem({arguments})


@problem.register()
def solution():
    pass


if __name__ == "__main__":
    raise SystemExit(problem.main())
'''


def list_problems(problems: dict[int, Problem]) -> int:

    for number, problem in problems.items():

        names = []
        for name in problem.solutions:
            flags = [flag for flag, on in (("default", name == problem.default), ("slow", name in problem.slow)) if on]
            names.append(f"{name} ({', '.join(flags)})" if flags else name)

        state = "solved" if problem.answer is not None else "unsolved"
        logger.info(f"p{number:<4} {state:<9} {', '.join(names)}")
        if problem.description:
            logger.info(f"\t{problem.description}")

    return 0


def check_problems(problems: list[Problem], timeout: float | None, all_solutions: bool, slow: bool, verbose: int) -> int:

    counts = {"ok": 0, "unchecked": 0, "failed": 0}

    st = time.perf_counter()

    for problem in problems:

        problem.logger.setLevel(logging.DEBUG if verbose > 0 else logging.INFO)

        if all_solutions:
            names = [name for name in problem.solutions if slow or name not in problem.slow]
        else:
            names = [problem.resolve_solution_name()]

        for name in names:
            result = problem.execute(name, timeout=timeout)
            counts[result.status if result.ok else "failed"] += 1
            logger.info(f"p{problem.number:<4} {name:<20} {result.status:<9} {result.seconds:10.6f}s  {result.detail}".rstrip())

    se = time.perf_counter()

    logger.info(f"{counts['ok']} ok, {counts['failed']} failed, {counts['unchecked']} unchecked in {se-st:.2f}s")

    return 1 if counts["failed"] else 0


def new_problem(number: int, description: str | None = None) -> int:

    path = registry.PROBLEMS_DIR / f"p{number}.py"

    if path.exists():
        logger.error(f"{path} already exists")
        return 1

    arguments = str(number) if description is None else f"{number}, {json.dumps(description)}"
    path.write_text(TEMPLATE.format(arguments=arguments))
    logger.info(f"Created {path}")

    return 0


def build_parser() -> argparse.ArgumentParser:

    parent_parser = argparse.ArgumentParser(add_help=False)
    add_verbose_argument(parent_parser)

    parser = argparse.ArgumentParser(
        prog="project_euler",
        description="Run and check Project Euler solutions",
    )

    subparsers = parser.add_subparsers(
        title='Available Commands',
        required=True,
        dest='command'
    )

    subparsers.add_parser(
        "list",
        parents=[parent_parser],
        help="List every problem and its solutions"
    )

    run_parser = subparsers.add_parser(
        "run",
        parents=[parent_parser],
        help="Run one problem's solution"
    )
    run_parser.add_argument("number", type=int, help="Problem number")
    add_run_arguments(run_parser)

    check_parser = subparsers.add_parser(
        "check",
        parents=[parent_parser],
        help="Run solutions and compare against the expected answers"
    )
    check_parser.add_argument("numbers", type=int, nargs="*", help="Problem numbers (default: all)")
    check_parser.add_argument(
        "-a", "--all-solutions",
        action="store_true",
        default=False,
        help="Check every registered solution rather than just the default"
    )
    add_check_arguments(check_parser)

    new_parser = subparsers.add_parser(
        "new",
        parents=[parent_parser],
        help="Create the solution file for a new problem"
    )
    new_parser.add_argument("number", type=int, help="Problem number")
    new_parser.add_argument("-d", "--description", default=None, help="Problem description")

    return parser


def main(argv: list[str] | None = None) -> int:

    configure_logging()

    parser = build_parser()
    args = parser.parse_args(argv)

    if args.command == "new":
        return new_problem(args.number, args.description)

    problems = registry.discover()

    match args.command:
        case "run":
            numbers = [args.number]
        case "check":
            numbers = args.numbers
        case _:
            numbers = []

    missing = [number for number in numbers if number not in problems]
    if missing:
        parser.error(f"no such problem: {', '.join(map(str, missing))}")

    match args.command:

        case "list":
            return list_problems(problems)

        case "run":
            try:
                return problems[args.number].run(args.solution, args.timed, args.verbose, args.timeout)
            except LookupError as e:
                parser.error(str(e))

        case "check":
            selected = [problems[number] for number in numbers] if numbers else list(problems.values())
            return check_problems(selected, args.timeout, args.all_solutions, args.slow, args.verbose)

        case _:
            raise ValueError
