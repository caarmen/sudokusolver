from copy import deepcopy
from dataclasses import dataclass
from enum import Enum
from itertools import product
from typing import List, Optional
from sudokusolver.board import Board


class State(str, Enum):
    VALID = "valid"
    HAS_DUPLICATES = "has_duplicates"
    INCOMPLETE = "incomplete"
    UNKNOWN = "unknown"


@dataclass
class Cell:
    row: int
    col: int


full_group = {"1", "2", "3", "4", "5", "6", "7", "8", "9"}


def _remove_none(data: set) -> set:
    return {item for item in data if item is not None}


def _get_state(items: List) -> State:
    non_none_items = [item for item in items if item is not None]
    if len(set(non_none_items)) != len(non_none_items):
        return State.HAS_DUPLICATES
    if len(non_none_items) != len(items):
        return State.INCOMPLETE
    if set(non_none_items) == full_group:
        return State.VALID
    return State.UNKNOWN


def get_state(board: Board) -> State:
    for row in board.rows:
        state = _get_state(row)
        if state != State.VALID:
            return state
    for col in board.cols:
        state = _get_state(col)
        if state != State.VALID:
            return state
    for square in board.squares:
        state = _get_state(square)
        if state != State.VALID:
            return state
    return State.VALID


def _get_possible_numbers_for_cell(board: Board, cell: Cell) -> List[int]:
    """
    :return: the possible numbers for the cell
    based on the numbers in the other cells of its row, column, and square
    """
    numbers_in_row = set(board.data[cell.row : cell.row + 1, 0:9].flatten())
    numbers_in_col = set(board.data[0:9, cell.col : cell.col + 1].flatten())
    square_begin_row = cell.row - cell.row % 3
    square_begin_col = cell.col - cell.col % 3
    numbers_in_square = set(
        board.data[
            square_begin_row : square_begin_row + 3,
            square_begin_col : square_begin_col + 3,
        ].flatten()
    )
    used_numbers = _remove_none(
        numbers_in_row.union(numbers_in_col).union(numbers_in_square)
    )
    return sorted(full_group.difference(used_numbers))


def _calculate_number_for_cell(board: Board, cell: Cell) -> Optional[chr]:
    """
    :return: the number for the cell if there's only one possible number it may have,
    based on the numbers in the other cells of its row, column, and square
    """
    possible_numbers = _get_possible_numbers_for_cell(board, cell)
    return possible_numbers.pop() if len(possible_numbers) == 1 else None


def _resolve_unambiguous_cells_one_pass(board: Board) -> bool:
    """
    Traverses the board once, filling in any empty cells for which only
    one value is possible.
    :return: True if the board changed.
    """
    has_changed = False
    for row_index, col_index in product(range(9), range(9)):
        if not board.data[row_index][col_index]:
            number = _calculate_number_for_cell(board, Cell(row_index, col_index))
            if number:
                board.data[row_index][col_index] = number
                has_changed = True
    return has_changed


def _resolve_unambiguous_cells(board):
    """
    In all the empty cells, look for cases where only one number is possible. Fill in all these cases.
    Then repeat.
    Stop when a pass over the board didn't change anything.
    """
    should_try_again = True
    while should_try_again:
        should_try_again = _resolve_unambiguous_cells_one_pass(board)


def _find_first_ambiguous_cell(board: Board) -> Optional[Cell]:
    for row, col in product(range(9), range(9)):
        if board.data[row][col] is None:
            return Cell(row, col)
    return None


def solve(board: Board) -> Board:
    cell = _find_first_ambiguous_cell(board)
    if not cell:
        return board
    possible_numbers = _get_possible_numbers_for_cell(board, cell)
    if not possible_numbers:
        return board
    snapshot = deepcopy(board)
    for number in possible_numbers:
        board = deepcopy(snapshot)
        board.data[cell.row][cell.col] = number
        _resolve_unambiguous_cells(board)
        state = get_state(board)
        if state == State.VALID:
            return board
        elif state == State.INCOMPLETE:
            board = solve(board)
            if get_state(board) == State.VALID:
                return board
    return board
