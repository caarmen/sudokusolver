# Sudoku solver
Python module which solves a sudoku puzzle

## Usage
The module reads sudoku strings in sdm format.

```python
from sudokusolver.board import Board
from sudokusolver.solver import solve

board = Board("450109780027400013080627040805301200002095400314070000000000325030702194040503076")
solution = solve(board)
print(solution.to_ss())
```
This prints the following:
``` 
456|139|782
927|458|613
183|627|549
------------
895|341|267
672|895|431
314|276|958
------------
761|984|325
538|762|194
249|513|876
```

## Disclaimer
Many sudoku solver packages are already available on [PyPI](https://pypi.org/search/?q=sudoku+solver).
This project doesn't pretend to compete with them 😉 In fact, PyPI has some solvers which are more advanced than this one, supporting boards of arbitrary size for example.

This project was simply a personal challenge. I made it open source in case any part of it could help anybody in some capacity.
