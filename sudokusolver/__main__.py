"""
Entry point to the sudoku solver program
"""
import argparse
from sudokusolver.board import Board
from sudokusolver.solver import solve

parser = argparse.ArgumentParser()
parser.add_argument("sdm", help="Sudoku puzzle in sdm format")
options = parser.parse_args()
board = Board(options.sdm)
solution = solve(board)
print(solution.to_ss())
