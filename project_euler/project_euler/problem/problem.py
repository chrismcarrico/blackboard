import time
import functools
import argparse
import logging
import signal
import typing

logging.basicConfig(level=logging.INFO, format='%(message)s')


class SolutionTimeoutError(Exception):
    pass


def _alarm_handler(signum, frame):
    del signum, frame
    raise SolutionTimeoutError()


class Problem:

    def __init__(self, number: int, problem_description: str | None = None):
        self.number = number
        self.description = problem_description
        self._solutions: dict[str, typing.Callable] = {}
        self.default: str | None = None
        self.logger = logging.getLogger(f"project_euler.p{number}")
        
    def debug(self, log:object):
        self.logger.debug(str(log))    
    
    def info(self, log:object):
        self.logger.info(str(log))

    @property
    def solutions(self):
        return self._solutions.keys()

    @property
    def len(self):
        return len(self._solutions)

    def register(self, solution_name: str | None = None, default: bool = False):
        def wrapper(fn):
            key = solution_name if solution_name is not None else fn.__name__
            self._solutions[key] = fn
            if default:
                self.default = key
            return fn
        return wrapper

    def _resolve_solution_name(self, solution_name: str | None) -> str:

        if solution_name is None:
            solution_name = self.default

        if solution_name is None:
            solution_name = list(self._solutions.keys())[0]

        return solution_name

    def run_solution(self, solution_name: str | None = None, timeout: int | None = None):

        solution_name = self._resolve_solution_name(solution_name)
        fn = self._solutions[solution_name]

        if timeout is None:
            return fn()

        previous_handler = signal.signal(signal.SIGALRM, _alarm_handler)
        signal.alarm(timeout)
        try:
            return fn()
        finally:
            signal.alarm(0)
            signal.signal(signal.SIGALRM, previous_handler)

    def run(self, solution_name: str | None = None, timed: bool = False, verbose: int = 0, timeout: int | None = None):

        self.logger.setLevel(logging.DEBUG if verbose > 0 else logging.INFO)

        resolved_name = self._resolve_solution_name(solution_name)

        self.logger.info(f"Problem {self.number}:")

        st = time.time()
        try:
            result = self.run_solution(resolved_name, timeout=timeout)
        except SolutionTimeoutError:
            se = time.time()
            self.logger.error(f"\tSolution '{resolved_name}' timed out after {se-st:.6f} seconds")
            return

        se = time.time()

        self.logger.info(f"\tAnswer: {result}")
        if timed:
            self.logger.info(f"\tTime: {se-st:.6f} seconds")

    def list_solutions(self) -> list[str]:
        return list(self._solutions.keys())

    def list(self, verbose: int = 0) -> None:
        self.logger.setLevel(logging.DEBUG if verbose > 0 else logging.INFO)
        self.logger.info(f"Available solutions for problem {self.number}")
        for solution_name in self.list_solutions():
            self.logger.info(f"\t{solution_name}")

    def main(self) -> None:
        args = self.cli.parse_args()

        match args.command:

            case "run":
                self.run(args.solution, args.timed, args.verbose, args.timeout)

            case "list":
                self.list(args.verbose)

            case _:
                raise ValueError
    
    @functools.cached_property
    def cli(self):

        parent_parser = argparse.ArgumentParser(add_help=False) # Important: Disable help on the parent
        parent_parser.add_argument(
            '-v', '--verbose',
            action='count', # 'count' will track the number of times -v is used (e.g., -v, -vv, -vvv)
            default=0,
            help='Increase output verbosity. Use multiple times for more detail (e.g., -vv).'
        )

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

        run_parser.add_argument(
            "-s", "--solution", 
            choices=list(self._solutions.keys()),
            default=self.default,
            help="Solution to run"
        )
        run_parser.add_argument(
            "-t", "--timed",
            action="store_true",
            default=False,
            help="Time the solution"
        )
        run_parser.add_argument(
            "-T", "--timeout",
            type=int,
            default=None,
            help="Abort the solution if it runs longer than this many seconds"
        )

        list_parser = subparsers.add_parser(
            "list",
            parents=[parent_parser],
            help=f"List available solutions for problem {self.number}"
        )

        
        return parser
