"""
Read the user input from the command line, solve tne input, and output the solutions to standard out
"""
import argparse
import multiprocessing
from enum import Enum

from sudokusolver import solver
from sudokusolver.board import Board
from sudokusolver.solver import Algorithm


def run():
    """
    Run the solver on the sudoku puzzles input by the user on the command line
    """
    options = _parse_args()
    sdms = []
    if options.sdm:
        sdms.append(options.sdm)
    else:
        with options.file as file:
            sdms = [line.rstrip() for line in file]

    if options.mode == _Mode.PARALLEL:
        with multiprocessing.Pool() as pool:
            pool.starmap(_solve, [(sdm, options.algorithm) for sdm in sdms])
    else:
        for sdm in sdms:
            _solve(sdm, options.algorithm)


class _Mode(Enum):
    PARALLEL = "parallel"
    SEQUENTIAL = "sequential"

    def __str__(self):
        return self.value


def _parse_args():
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "--sdm",
        help="Sudoku puzzle in sdm format",
    )
    group.add_argument(
        "--file",
        type=argparse.FileType("r"),
        help="File containing sudoku puzzles in sdm format",
    )
    parser.add_argument(
        "--mode",
        choices=list(_Mode),
        type=_Mode,
        default=_Mode.PARALLEL,
        help="How to process multiple boards. Default %(default)s",
        nargs="?",
    )
    parser.add_argument(
        "--algorithm",
        choices=list(Algorithm),
        type=Algorithm,
        default=Algorithm.RECURSIVE,
        help="Default %(default)s",
        nargs="?",
    )
    return parser.parse_args()


def _solve(sdm: str, algorithm: Algorithm):
    board = Board(sdm)
    solution = solver.solve(board, algorithm=algorithm)
    print(sdm)
    print(solution.to_ss())
