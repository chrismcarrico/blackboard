import time
import functools
import argparse
import dataclasses
import logging
import signal
import typing


class SolutionTimeoutError(Exception):
    pass


def _alarm_handler(signum, frame):
    del signum, frame
    raise SolutionTimeoutError()


def configure_logging() -> None:
    logging.basicConfig(level=logging.INFO, format='%(message)s')


def _positive_seconds(value: str) -> float:
    seconds = float(value)
    if seconds <= 0:
        raise argparse.ArgumentTypeError("must be greater than 0")
    return seconds


def add_verbose_argument(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(
        '-v', '--verbose',
        action='count', # 'count' will track the number of times -v is used (e.g., -v, -vv, -vvv)
        default=0,
        help='Increase output verbosity. Use multiple times for more detail (e.g., -vv).'
    )


def add_timeout_argument(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(
        "-T", "--timeout",
        type=_positive_seconds,
        default=None,
        help="Abort a solution if it runs longer than this many seconds"
    )


def add_run_arguments(parser: argparse.ArgumentParser, solutions: list[str] | None = None, default: str | None = None) -> None:
    parser.add_argument(
        "-s", "--solution",
        choices=solutions,
        default=default,
        help="Solution to run"
    )
    parser.add_argument(
        "-t", "--timed",
        action="store_true",
        default=False,
        help="Time the solution"
    )
    add_timeout_argument(parser)


def add_check_arguments(parser: argparse.ArgumentParser) -> None:
    add_timeout_argument(parser)
    parser.add_argument(
        "--slow",
        action="store_true",
        default=False,
        help="Include solutions registered as slow"
    )


@dataclasses.dataclass(frozen=True)
class Result:
    problem: int
    solution: str
    answer: object
    expected: object
    seconds: float
    status: typing.Literal["ok", "wrong", "unchecked", "timeout", "error"]
    error: Exception | None = None

    @property
    def ok(self) -> bool:
        return self.status in ("ok", "unchecked")

    @property
    def detail(self) -> str:

        match self.status:

            case "wrong":
                return f"got {self.answer}, expected {self.expected}"

            case "unchecked":
                return f"got {self.answer}, no expected answer"

            case "error":
                return f"{type(self.error).__name__}: {self.error}"

            case _:
                return ""


class Problem:

    def __init__(self, number: int, problem_description: str | None = None):
        self.number = number
        self.description = problem_description
        self.answer: object = None
        self._solutions: dict[str, typing.Callable] = {}
        self.default: str | None = None
        self.slow: set[str] = set()
        self.logger = logging.getLogger(f"project_euler.p{number}")

    def debug(self, log:object):
        self.logger.debug(str(log))

    def info(self, log:object):
        self.logger.info(str(log))

    @property
    def solutions(self) -> list[str]:
        return list(self._solutions.keys())

    def register(self, solution_name: str | None = None, default: bool = False, slow: bool = False):
        def wrapper(fn):
            key = solution_name if solution_name is not None else fn.__name__
            if key in self._solutions:
                raise ValueError(f"Problem {self.number} already has a solution named '{key}'")
            self._solutions[key] = fn
            if default:
                self.default = key
            if slow:
                self.slow.add(key)
            return fn
        return wrapper

    def register_answer(self, answer: object) -> None:
        if self.answer is not None:
            raise ValueError(f"Problem {self.number} already has a registered answer")
        self.answer = answer

    def resolve_solution_name(self, solution_name: str | None = None) -> str:

        if not self._solutions:
            raise LookupError(f"Problem {self.number} has no registered solutions")

        if solution_name is None:
            solution_name = self.default

        if solution_name is None:
            solution_name = self.solutions[0]

        if solution_name not in self._solutions:
            raise LookupError(
                f"Problem {self.number} has no solution named '{solution_name}' "
                f"(available: {', '.join(self.solutions)})"
            )

        return solution_name

    def run_solution(self, solution_name: str | None = None, timeout: float | None = None):

        solution_name = self.resolve_solution_name(solution_name)
        fn = self._solutions[solution_name]

        if timeout is None:
            return fn()

        previous_handler = signal.signal(signal.SIGALRM, _alarm_handler)
        signal.setitimer(signal.ITIMER_REAL, timeout)
        try:
            return fn()
        finally:
            signal.setitimer(signal.ITIMER_REAL, 0)
            signal.signal(signal.SIGALRM, previous_handler)

    def execute(self, solution_name: str | None = None, timeout: float | None = None) -> Result:

        solution_name = self.resolve_solution_name(solution_name)

        answer = None
        error = None

        st = time.perf_counter()
        try:
            answer = self.run_solution(solution_name, timeout=timeout)
        except SolutionTimeoutError:
            status = "timeout"
        except Exception as e:  # noqa: BLE001 - any failure of a solution is reported as a Result
            status = "error"
            error = e
        else:
            if self.answer is None:
                status = "unchecked"
            elif answer == self.answer:
                status = "ok"
            else:
                status = "wrong"
        se = time.perf_counter()

        return Result(self.number, solution_name, answer, self.answer, se-st, status, error)

    def run(self, solution_name: str | None = None, timed: bool = False, verbose: int = 0, timeout: float | None = None) -> int:

        self.logger.setLevel(logging.DEBUG if verbose > 0 else logging.INFO)

        solution_name = self.resolve_solution_name(solution_name)

        self.logger.info(f"Problem {self.number}:")

        result = self.execute(solution_name, timeout=timeout)

        match result.status:

            case "timeout":
                self.logger.error(f"\tSolution '{result.solution}' timed out after {result.seconds:.6f} seconds")

            case "error":
                self.logger.error(f"\tSolution '{result.solution}' failed", exc_info=result.error)

            case "ok":
                self.logger.info(f"\tAnswer: {result.answer} (correct)")

            case "wrong":
                self.logger.error(f"\tAnswer: {result.answer} (expected {result.expected})")

            case _:
                self.logger.info(f"\tAnswer: {result.answer}")

        if timed and result.status not in ("timeout", "error"):
            self.logger.info(f"\tTime: {result.seconds:.6f} seconds")

        return 0 if result.ok else 1

    def check(self, timeout: float | None = None, slow: bool = False, verbose: int = 0) -> int:

        self.logger.setLevel(logging.DEBUG if verbose > 0 else logging.INFO)
        self.logger.info(f"Problem {self.number}:")

        width = max((len(name) for name in self.solutions), default=0)
        failed = False

        for solution_name in self.solutions:

            if solution_name in self.slow and not slow:
                self.logger.info(f"\t{solution_name:<{width}}  skipped (slow)")
                continue

            result = self.execute(solution_name, timeout=timeout)
            failed = failed or not result.ok

            self.logger.info(f"\t{solution_name:<{width}}  {result.status:<9}  {result.seconds:.6f}s  {result.detail}".rstrip())

        return 1 if failed else 0

    def list(self, verbose: int = 0) -> None:
        self.logger.setLevel(logging.DEBUG if verbose > 0 else logging.INFO)
        self.logger.info(f"Available solutions for problem {self.number}")
        for solution_name in self.solutions:
            self.logger.info(f"\t{solution_name}")

    def main(self, argv: typing.Sequence[str] | None = None) -> int:

        configure_logging()

        args = self.cli.parse_args(argv)

        match args.command:

            case "run":
                return self.run(args.solution, args.timed, args.verbose, args.timeout)

            case "check":
                return self.check(args.timeout, args.slow, args.verbose)

            case "list":
                self.list(args.verbose)
                return 0

            case _:
                raise ValueError

    @functools.cached_property
    def cli(self):

        parent_parser = argparse.ArgumentParser(add_help=False) # Important: Disable help on the parent
        add_verbose_argument(parent_parser)

        parser = argparse.ArgumentParser(
            prog=f"Problem {self.number}",
            description=self.description,
        )

        subparsers = parser.add_subparsers(
            title='Available Commands',
            description='Use one of the following commands:',
            # Set a default value if no subcommand is given
            required=True,
            # The 'dest' argument will hold the name of the subcommand executed
            dest='command'
        )

        run_parser = subparsers.add_parser(
            "run",
            parents=[parent_parser],
            help=f"Run solution for problem {self.number}"
        )
        add_run_arguments(run_parser, self.solutions, self.default)

        check_parser = subparsers.add_parser(
            "check",
            parents=[parent_parser],
            help=f"Run every solution for problem {self.number} and compare against the expected answer"
        )
        add_check_arguments(check_parser)

        subparsers.add_parser(
            "list",
            parents=[parent_parser],
            help=f"List available solutions for problem {self.number}"
        )

        return parser
