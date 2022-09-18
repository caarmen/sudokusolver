"""
A Sudoku board solver
"""
from copy import deepcopy
from dataclasses import dataclass
from enum import Enum
from itertools import product
from typing import Iterable, List, Optional

from sudokusolver.board import Board


class Algorithm(str, Enum):
    """
    Algorithm to use when solving
    """

    RECURSIVE = "recursive"
    ITERATIVE = "iterative"

    def __str__(self):
        return self.value


class State(str, Enum):
    """
    The state of a Board
    """

    VALID = "valid"
    HAS_DUPLICATES = "has_duplicates"
    INCOMPLETE = "incomplete"
    UNKNOWN = "unknown"


@dataclass
class Cell:
    """
    A position in the board
    """

    row: int
    col: int


full_group = {"1", "2", "3", "4", "5", "6", "7", "8", "9"}


def _remove_none(data: set) -> set:
    return {item for item in data if item is not None}


def _get_state(items: Iterable[str]) -> State:
    non_none_items = [item for item in items if item is not None]
    if len(set(non_none_items)) != len(non_none_items):
        return State.HAS_DUPLICATES
    if len(non_none_items) != len(items):
        return State.INCOMPLETE
    if set(non_none_items) == full_group:
        return State.VALID
    return State.UNKNOWN


def get_state(board: Board) -> State:
    """
    :return: the state of the board
    """
    # check the rows and columns
    for i in range(9):
        state_row = _get_state(board.get_row(i))
        if state_row != State.VALID:
            return state_row

        state_col = _get_state(board.get_col(i))
        if state_col != State.VALID:
            return state_col

    # check the squares
    for i, j in product(range(0, 9, 3), range(0, 9, 3)):
        state_square = _get_state(board.get_square(i, j))
        if state_square != State.VALID:
            return state_square
    return State.VALID


def _get_possible_numbers_for_cell(board: Board, cell: Cell) -> List[str]:
    """
    :return: the possible numbers for the cell
    based on the numbers in the other cells of its row, column, and square
    """
    numbers_in_row = set(board.get_row(cell.row))
    numbers_in_col = set(board.get_col(cell.col))
    numbers_in_square = set(board.get_square(cell.row, cell.col))
    used_numbers = _remove_none(
        numbers_in_row.union(numbers_in_col).union(numbers_in_square)
    )
    return sorted(full_group.difference(used_numbers))


def _resolve_unambiguous_cells_one_pass(board: Board) -> bool:
    """
    Traverses the board once, filling in any empty cells for which only
    one value is possible.
    :return: True if the board changed.
    """
    has_changed = False
    for row_index, col_index in product(range(9), range(9)):
        if not board.data[row_index][col_index]:
            possible_numbers = _get_possible_numbers_for_cell(
                board, Cell(row_index, col_index)
            )
            if len(possible_numbers) == 1:
                board.data[row_index][col_index] = possible_numbers[0]
                has_changed = True
    return has_changed


def _resolve_unambiguous_cells(board):
    """
    In all the empty cells, look for cases where only one number is possible.
    Fill in all these cases.
    Then repeat.
    Stop when a pass over the board didn't change anything.
    """
    should_try_again = True
    while should_try_again:
        should_try_again = _resolve_unambiguous_cells_one_pass(board)


def _find_first_empty_cell(board: Board) -> Optional[Cell]:
    for row, col in product(range(9), range(9)):
        if board.data[row][col] is None:
            return Cell(row, col)
    return None


def solve(board: Board, algorithm: Algorithm = Algorithm.RECURSIVE) -> Board:
    """
    :return: the board in its solved state, or in an incomplete or invalid state if we
    weren't able to solve it.
    """
    if algorithm == Algorithm.RECURSIVE:
        return _solve_recursive(board)
    return _solve_iterative(board)


def _solve_recursive(board: Board) -> Board:
    cell = _find_first_empty_cell(board)
    if not cell:
        return board

    possible_numbers = _get_possible_numbers_for_cell(board, cell)
    if not possible_numbers:
        return board

    for number in possible_numbers:
        board_copy = deepcopy(board)
        board_copy.data[cell.row][cell.col] = number
        _resolve_unambiguous_cells(board_copy)
        state = get_state(board_copy)
        if state == State.VALID:
            return board_copy
        if state == State.INCOMPLETE:
            board_copy = solve(board_copy)
        if get_state(board_copy) == State.VALID:
            return board_copy
        # else INVALID state.
        # Maybe we'll have better luck with the next possible number

    return board


def _solve_iterative(board: Board) -> Board:
    boards_stack: List[Board] = [board]
    while boards_stack:
        board_to_test = boards_stack.pop()

        cell = _find_first_empty_cell(board_to_test)
        if not cell:
            continue

        possible_numbers = _get_possible_numbers_for_cell(board_to_test, cell)
        if not possible_numbers:
            continue

        for number in possible_numbers:
            board_copy = deepcopy(board_to_test)
            board_copy.data[cell.row][cell.col] = number
            _resolve_unambiguous_cells(board_copy)
            state = get_state(board_copy)
            if state == State.VALID:
                return board_copy
            if state == State.INCOMPLETE:
                boards_stack.append(board_copy)
            # else INVALID state.
            # Maybe we'll have better luck with the next possible number

    # If we get here, this means we couldn't find a solution. Return the original board.
    return board
