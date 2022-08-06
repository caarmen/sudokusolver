from itertools import product

import numpy


class Board:
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
