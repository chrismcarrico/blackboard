import time
import functools
import argparse
import logging
import typing

logging.basicConfig(level=logging.INFO, format='%(message)s')
_logger = logging.getLogger(__name__)

class SolutionSet:

    def __init__(self, number: int, problem_description: str):
        self.number = number
        self.description = problem_description
        self._solutions: dict[str, typing.Callable] = {}
        self.default: str | None = None

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

    def run_solution(self, solution_name: str | None = None):
        
        if solution_name is None:
            solution_name = self.default

        if solution_name is None:
            solution_name = list(self._solutions.keys())[0]

        return self._solutions[solution_name]()
    
    def run(self, solution_name: str | None = None, timed: bool = False, verbose: int = 0):

        if verbose > 0:
            _logger.setLevel(logging.DEBUG)
        
        _logger.info(f"Problem {self.number}:")
        
        st = time.time()
        result = self.run_solution(solution_name)
        se = time.time()

        _logger.info(f"\tAnswer: {result}")
        if timed:
            _logger.info(f"\tTime: {se-st:.6f} seconds")

    def list_solutions(self) -> list[str]:
        return list(self._solutions.keys())

    def list(self, verbose: int = 0) -> None:
        del verbose # unused for now 
        _logger.info(f"Available solutions for problem {self.number}")
        for solution_name in self.list_solutions():
            _logger.info(f"\t{solution_name}")

    def main(self) -> None:
        args = self.cli.parse_args()
        
        match args.command:

            case "run":
                self.run(args.solution, args.timed, args.verbose)
            
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

        list_parser = subparsers.add_parser(
            "list",
            parents=[parent_parser],
            help=f"List available solutions for problem {self.number}"
        )

        
        return parser
