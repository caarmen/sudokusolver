# Sudoku solver

Python module which solves a sudoku puzzle

[<img src="https://img.shields.io/badge/license-MIT-lightgrey.svg?maxAge=2592000">](https://github.com/caarmen/sudokusolver/blob/main/LICENSE)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[<img src="https://github.com/caarmen/sudokusolver/actions/workflows/tests.yml/badge.svg">](https://github.com/caarmen/sudokusolver/actions?query=workflow%3A%22Run+tests%22++)

## Usage

The module reads sudoku strings in sdm format.

### Program

Invoke the program as follows to solve one puzzle:

```bash
python -m  sudokusolver --sdm 450109780027400013080627040805301200002095400314070000000000325030702194040503076
```

This prints the following:

```
450109780027400013080627040805301200002095400314070000000000325030702194040503076
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

It's also possible to specify a file containing one sdm entry per line:

```
python -m sudokusolver --file /path/to/sudoku.sdm
```

Use `--help` to display full options:

```commandline
% python -m sudokusolver --help
usage: __main__.py [-h] (--sdm SDM | --file FILE) [--mode [{parallel,sequential}]] [--algorithm [{recursive,iterative}]]

options:
  -h, --help            show this help message and exit
  --sdm SDM             Sudoku puzzle in sdm format
  --file FILE           File containing sudoku puzzles in sdm format
  --mode [{parallel,sequential}]
                        How to process multiple boards. Default parallel
  --algorithm [{recursive,iterative}]
                        Default recursive

```

### Package

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
This project doesn't pretend to compete with them 😉 In fact, PyPI has some solvers which are more advanced than this
one, supporting boards of arbitrary size for example.

This project was simply a personal challenge. I made it open source in case any part of it could help anybody in some
capacity.
