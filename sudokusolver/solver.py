from itertools import product
from typing import Optional

import numpy

full_group = {'1', '2', '3', '4', '5', '6', '7', '8', '9'}


def _remove_none(data: set) -> set:
    return {item for item in data if item is not None}


class Sudoku:
    def __init__(self, sdm: str):
        self.iteration_count = 0
        if len(sdm) != 81:
            raise ValueError("Invalid sdm input")
        self.data = numpy.zeros(81, dtype=object).reshape((9, 9))
        for row, col in product(range(9), range(9)):
            input_number = sdm[row * 9 + col]
            if 1 <= int(input_number) <= 9:
                self.data[row][col] = input_number
            else:
                self.data[row][col] = None

    @property
    def rows(self):
        # Our data is organized by rows already
        return self.data

    @property
    def cols(self):
        return numpy.transpose(self.data)

    @property
    def squares(self):
        return [
            self.data[0:3, 0:3].flatten(),
            self.data[3:6, 0:3].flatten(),
            self.data[6:9, 0:3].flatten(),
            self.data[0:3, 3:6].flatten(),
            self.data[3:6, 3:6].flatten(),
            self.data[6:9, 3:6].flatten(),
            self.data[0:3, 6:9].flatten(),
            self.data[3:6, 6:9].flatten(),
            self.data[6:9, 6:9].flatten(),
        ]

    def _calculate_number_for_cell(self, row_index: int, col_index: int) -> Optional[chr]:
        """
        :return: the number for the cell if there's only one possible number it may have,
        based on the numbers in the other cells of its row, column, and square
        """
        numbers_in_row = set(self.data[row_index:row_index + 1, 0:9].flatten())
        numbers_in_col = set(self.data[0:9, col_index:col_index + 1].flatten())
        square_begin_row = row_index - row_index % 3
        square_begin_col = col_index - col_index % 3
        numbers_in_square = set(
            self.data[square_begin_row:square_begin_row + 3, square_begin_col:square_begin_col + 3].flatten())
        used_numbers = _remove_none(numbers_in_row.union(numbers_in_col).union(numbers_in_square))
        available_numbers = full_group.difference(used_numbers)
        return available_numbers.pop() if len(available_numbers) == 1 else None

    def _update_all_cells(self):
        has_changed = False
        for row_index, col_index in product(range(9), range(9)):
            if not self.data[row_index][col_index]:
                number = self._calculate_number_for_cell(row_index, col_index)
                if number:
                    self.data[row_index][col_index] = number
                    has_changed = True
        return has_changed

    def resolve_unambiguous_cells(self):
        """
        In all the empty cells, look for cases where only one number is possible. Fill in all these cases.
        Then repeat.
        Stop when either we're finished (we solved the sudoku), or all the empty cells have at least 2
        possible numbers that can be used, based on the numbers of their row, group, and square.
        """
        should_try_again = True
        while should_try_again:
            self.iteration_count += 1
            print(f"iteration {self.iteration_count}")
            has_changed = self._update_all_cells()
            should_try_again = not self.is_valid() and has_changed
            print(self.to_ss())

    def is_valid(self) -> bool:
        are_rows_valid = all(set(row) == full_group for row in self.rows)
        are_cols_valid = all(set(col) == full_group for col in self.cols)
        are_squares_valid = all(set(square) == full_group for square in self.squares)
        return are_rows_valid and are_cols_valid and are_squares_valid

    def to_ss(self) -> str:
        """
        :return: the sudoko formatted in the ss format, like this:

        5.9|3.4|.7.
        726|.59|.4.
        .4.|276|..5
        ------------
        197|.32|.5.
        238|9.5|...
        .54|...|.32
        ------------
        ..2|693|5.7
        .6.|54.|..9
        975|128|.63

        """
        result = ""
        for row, col in product(range(9), range(9)):
            cell = self.data[row, col]
            result += cell if cell else "."
            if col in [2, 5]:
                result += "|"
            elif col == 8:
                result += "\n"
                if row in [2, 5]:
                    result += "------------\n"
        return result
