"""
Unit tests for the sudoku solver
"""
import pytest

from sudokusolver.solver import solve, get_state, State, Algorithm
from sudokusolver.board import Board


@pytest.mark.parametrize("algorithm", Algorithm)
def test_already_solved(algorithm: Algorithm):
    """
    Check that a sudoku which is already fully completed is valid
    """
    _test_sudoku(
        "589314276726859341341276895197432658238965714654781932412693587863547129975128463",
        algorithm=algorithm,
    )


@pytest.mark.parametrize("algorithm", Algorithm)
def test_no_guessing_needed(algorithm: Algorithm):
    """
    Tests a sudoku for which we can find, over several iterations, one unique value for
    each empty cell that satisfies the rules. We never have a situation where all empty
    cells can have multiple values
    """
    _test_sudoku(
        "509304070726059040040276005107030050208905000050000032002693507060540009975028003",
        algorithm=algorithm,
    )


@pytest.mark.parametrize("algorithm", Algorithm)
def test_guessing_needed(algorithm: Algorithm):
    """
    After several iterations of finding unambiguous answers for some cells, we end up in
    a situation where all the remaining empty cells have multiple possible values. We have
    to, at this point, take a guess and continue.
    """
    _test_sudoku(
        "450109780027400013080627040805301200002095400314070000000000325030702194040503076",
        algorithm=algorithm,
    )


@pytest.mark.parametrize("algorithm", Algorithm)
def test_few_initial_values_provided(algorithm: Algorithm):
    """
    Test a sudoku which has many empty cells to begin with.
    """
    _test_sudoku(
        "123456789000000000000000000000000000000000000000000000000000000000000000000000000",
        algorithm=algorithm,
    )


@pytest.mark.parametrize("algorithm", Algorithm)
def test_has_duplicates1(algorithm: Algorithm):
    """
    Test a sudoku which is already invalid
    """
    _test_sudoku_has_duplicates(
        "123456789234567891345678912456789123567891234678912345789123456891234567912345678",
        algorithm=algorithm,
    )


@pytest.mark.parametrize("algorithm", Algorithm)
def test_has_duplicates2(algorithm: Algorithm):
    """
    Test a sudoku which is isn't solvable
    """
    _test_sudoku_has_duplicates(
        "110000000000000000000000000000000000000000000000000000000000000000000000000000000",
        algorithm=algorithm,
    )


@pytest.mark.parametrize("algorithm", Algorithm)
def test_unsolvable2(algorithm: Algorithm):
    """
    Test a sudoku which is isn't solvable
    https://www.sudokudragon.com/unsolvable.htm
    """
    _test_incomplete_sudoku(
        "516849732307605000809700065135060907472591006968370050253186074684207500791050608",
        algorithm=algorithm,
    )


# The following come from
# http://forum.enjoysudoku.com/the-master-collection-sdm-format-t39722.html
# https://drive.google.com/drive/folders/1e_hQNQiJVxhHP_5WBQhBNur9dnS5ml3E


@pytest.mark.parametrize("algorithm", Algorithm)
def test_easy_1(algorithm: Algorithm):
    """
    Easy sudoku from the master sdm collection
    """
    _test_sudoku(
        "050703060007000800000816000000030000005000100730040086906000204840572093000409000",
        algorithm=algorithm,
    )


@pytest.mark.parametrize("algorithm", Algorithm)
def test_easy_2(algorithm: Algorithm):
    """
    Easy sudoku from the master sdm collection
    """
    _test_sudoku(
        "302401809001000300000000000040708010780502036000090000200609003900000008800070005",
        algorithm=algorithm,
    )


@pytest.mark.parametrize("algorithm", Algorithm)
def test_easy_3(algorithm: Algorithm):
    """
    Easy sudoku from the master sdm collection
    """
    _test_sudoku(
        "000823001003000400070000052300960010000102000010038006830000040002000900600789000",
        algorithm=algorithm,
    )


@pytest.mark.parametrize("algorithm", Algorithm)
def test_easy_4(algorithm: Algorithm):
    """
    Easy sudoku from the master sdm collection
    """
    _test_sudoku(
        "500700032100326000000000000020070058010803040890040070000000000000654001230009005",
        algorithm=algorithm,
    )


@pytest.mark.parametrize("algorithm", Algorithm)
def test_easy_5(algorithm: Algorithm):
    """
    Easy sudoku from the master sdm collection
    """
    _test_sudoku(
        "760000053020080040005000900000000000040010070603000104100304009000000000006827300",
        algorithm=algorithm,
    )


@pytest.mark.parametrize("algorithm", Algorithm)
def test_easy_6(algorithm: Algorithm):
    """
    Easy sudoku from the master sdm collection
    """
    _test_sudoku(
        "140000050700200000000300204200080400080090020006050001809001000000006007050000069",
        algorithm=algorithm,
    )


@pytest.mark.parametrize("algorithm", Algorithm)
def test_easy_7(algorithm: Algorithm):
    """
    Easy sudoku from the master sdm collection
    """
    _test_sudoku(
        "002009000015008760040000051620407000000010000000206074170000090098500610000700800",
        algorithm=algorithm,
    )


@pytest.mark.parametrize("algorithm", Algorithm)
def test_easy_8(algorithm: Algorithm):
    """
    Easy sudoku from the master sdm collection
    """
    _test_sudoku(
        "060010030830605029000000000006030900092000570000409000285000716000000000470000095",
        algorithm=algorithm,
    )


@pytest.mark.parametrize("algorithm", Algorithm)
def test_easy_9(algorithm: Algorithm):
    """
    Easy sudoku from the master sdm collection
    """
    _test_sudoku(
        "600002305000970016021000009070643000000000000000891040200000530310064000904700001",
        algorithm=algorithm,
    )


@pytest.mark.parametrize("algorithm", Algorithm)
def test_easy_10(algorithm: Algorithm):
    """
    Easy sudoku from the master sdm collection
    """
    _test_sudoku(
        "007020850200516000400000006070648090930102068060953020700000005000495002029060100",
        algorithm=algorithm,
    )


@pytest.mark.parametrize("algorithm", Algorithm)
def test_medium_1(algorithm: Algorithm):
    """
    Medium sudoku from the master sdm collection
    """
    _test_sudoku(
        "020900000048000031000063020009407003003080200400105600030570000250000180000006050",
        algorithm=algorithm,
    )


@pytest.mark.parametrize("algorithm", Algorithm)
def test_medium_2(algorithm: Algorithm):
    """
    Medium sudoku from the master sdm collection
    """
    _test_sudoku(
        "100800570000009210090040000300900050007000300020006008000020040071400000064007003",
        algorithm=algorithm,
    )


@pytest.mark.parametrize("algorithm", Algorithm)
def test_medium_3(algorithm: Algorithm):
    """
    Medium sudoku from the master sdm collection
    """
    _test_sudoku(
        "002000800005020100460000029130060052009080400000302000006070200700000008020519070",
        algorithm=algorithm,
    )


@pytest.mark.parametrize("algorithm", Algorithm)
def test_medium_4(algorithm: Algorithm):
    """
    Medium sudoku from the master sdm collection
    """
    _test_sudoku(
        "802600009000058000006000401090406005020000040600203090205000900000970000100002804",
        algorithm=algorithm,
    )


@pytest.mark.parametrize("algorithm", Algorithm)
def test_medium_5(algorithm: Algorithm):
    """
    Medium sudoku from the master sdm collection
    """
    _test_sudoku(
        "070000120100000067000200004200040070710030049090070001300009000950000006067000080",
        algorithm=algorithm,
    )


@pytest.mark.parametrize("algorithm", Algorithm)
def test_medium_6(algorithm: Algorithm):
    """
    Medium sudoku from the master sdm collection
    """
    _test_sudoku(
        "054608003700004000800000020690000102000010000203000047070000006000500008900306410",
        algorithm=algorithm,
    )


@pytest.mark.parametrize("algorithm", Algorithm)
def test_medium_7(algorithm: Algorithm):
    """
    Medium sudoku from the master sdm collection
    """
    _test_sudoku(
        "000159000015000790000000000100405008280000067500728001000896000098010420000000000",
        algorithm=algorithm,
    )


@pytest.mark.parametrize("algorithm", Algorithm)
def test_medium_8(algorithm: Algorithm):
    """
    Medium sudoku from the master sdm collection
    """
    _test_sudoku(
        "000000000340000091701060408800000006010000020600205009060107050005020100030090060",
        algorithm=algorithm,
    )


@pytest.mark.parametrize("algorithm", Algorithm)
def test_medium_9(algorithm: Algorithm):
    """
    Medium sudoku from the master sdm collection
    """
    _test_sudoku(
        "206008309001002000700004012942060000000407000000080423620700004000200500309800206",
        algorithm=algorithm,
    )


@pytest.mark.parametrize("algorithm", Algorithm)
def test_medium_10(algorithm: Algorithm):
    """
    Medium sudoku from the master sdm collection
    """
    _test_sudoku(
        "100009570798040000600002000012000008000000000500000320000300005000070416061200003",
        algorithm=algorithm,
    )


@pytest.mark.parametrize("algorithm", Algorithm)
def test_hard_1(algorithm: Algorithm):
    """
    Hard sudoku from the master sdm collection
    """
    _test_sudoku(
        "080200400570000100002300000820090005000715000700020041000006700003000018007009050",
        algorithm=algorithm,
    )


@pytest.mark.parametrize("algorithm", Algorithm)
def test_hard_2(algorithm: Algorithm):
    """
    Hard sudoku from the master sdm collection
    """
    _test_sudoku(
        "600050007030000000080409200015300000008000300000007590009501030000000080200070004",
        algorithm=algorithm,
    )


@pytest.mark.parametrize("algorithm", Algorithm)
def test_hard_3(algorithm: Algorithm):
    """
    Hard sudoku from the master sdm collection
    """
    _test_sudoku(
        "210950004090060037000700000000000308920000015805000000000002000680010040100047096",
        algorithm=algorithm,
    )


@pytest.mark.parametrize("algorithm", Algorithm)
def test_hard_4(algorithm: Algorithm):
    """
    Hard sudoku from the master sdm collection
    """
    _test_sudoku(
        "024000650100000007008010900000000000260090083080501070600903008002854700000070000",
        algorithm=algorithm,
    )


@pytest.mark.parametrize("algorithm", Algorithm)
def test_hard_5(algorithm: Algorithm):
    """
    Hard sudoku from the master sdm collection
    """
    _test_sudoku(
        "000050000000206000064000390045000810000020000000107000053000980090804060100030004",
        algorithm=algorithm,
    )


@pytest.mark.parametrize("algorithm", Algorithm)
def test_hard_6(algorithm: Algorithm):
    """
    Hard sudoku from the master sdm collection
    """
    _test_sudoku(
        "108500406000070900530004007001060008090408070800050600700100069006080000904006205",
        algorithm=algorithm,
    )


@pytest.mark.parametrize("algorithm", Algorithm)
def test_hard_7(algorithm: Algorithm):
    """
    Hard sudoku from the master sdm collection
    """
    _test_sudoku(
        "970306042805000109000050000207000304010020080400738001000905000000000000100847003",
        algorithm=algorithm,
    )


@pytest.mark.parametrize("algorithm", Algorithm)
def test_hard_8(algorithm: Algorithm):
    """
    Hard sudoku from the master sdm collection
    """
    _test_sudoku(
        "040000000086100034001500260000305840000040000058902000095008300160009450000000010",
        algorithm=algorithm,
    )


@pytest.mark.parametrize("algorithm", Algorithm)
def test_hard_9(algorithm: Algorithm):
    """
    Hard sudoku from the master sdm collection
    """
    _test_sudoku(
        "045900000000710205020003009008301026010000050360805100200100030801057000000009510",
        algorithm=algorithm,
    )


@pytest.mark.parametrize("algorithm", Algorithm)
def test_hard_10(algorithm: Algorithm):
    """
    Hard sudoku from the master sdm collection
    """
    _test_sudoku(
        "900801005000607000870000069490000057080000020000375000040000070008060900109000603",
        algorithm=algorithm,
    )


@pytest.mark.parametrize("algorithm", Algorithm)
def test_diabolical_1(algorithm: Algorithm):
    """
    Diabolical sudoku from the master sdm collection
    """
    _test_sudoku(
        "083020090000800100029300008000098700070000060006740000300006980002005000010030540",
        algorithm=algorithm,
    )


@pytest.mark.parametrize("algorithm", Algorithm)
def test_diabolical_2(algorithm: Algorithm):
    """
    Diabolical sudoku from the master sdm collection
    """
    _test_sudoku(
        "200050006010000090600801003007090600000703000900080002100000005060902010003060200",
        algorithm=algorithm,
    )


@pytest.mark.parametrize("algorithm", Algorithm)
def test_diabolical_3(algorithm: Algorithm):
    """
    Diabolical sudoku from the master sdm collection
    """
    _test_sudoku(
        "590000007040010083008034900001402000069000820000109300004670200980040030700000016",
        algorithm=algorithm,
    )


@pytest.mark.parametrize("algorithm", Algorithm)
def test_diabolical_4(algorithm: Algorithm):
    """
    Diabolical sudoku from the master sdm collection
    """
    _test_sudoku(
        "006000200900000004243000896000591000002080300400203001300000007000907000010408020",
        algorithm=algorithm,
    )


@pytest.mark.parametrize("algorithm", Algorithm)
def test_diabolical_5(algorithm: Algorithm):
    """
    Diabolical sudoku from the master sdm collection
    """
    _test_sudoku(
        "000000000560000032230040079000060000070501090000708000053000920009806500700000004",
        algorithm=algorithm,
    )


@pytest.mark.parametrize("algorithm", Algorithm)
def test_diabolical_6(algorithm: Algorithm):
    """
    Diabolical sudoku from the master sdm collection
    """
    _test_sudoku(
        "000310000060097040001420300030000502786000139502000060003059700020680010000074000",
        algorithm=algorithm,
    )


@pytest.mark.parametrize("algorithm", Algorithm)
def test_diabolical_7(algorithm: Algorithm):
    """
    Diabolical sudoku from the master sdm collection
    """
    _test_sudoku(
        "076009400000801007300000009610307080000090000020108034500000006900204000001600790",
        algorithm=algorithm,
    )


@pytest.mark.parametrize("algorithm", Algorithm)
def test_diabolical_8(algorithm: Algorithm):
    """
    Diabolical sudoku from the master sdm collection
    """
    _test_sudoku(
        "103070002000000040090005001020100503007000200405002060200800030050000000800020709",
        algorithm=algorithm,
    )


@pytest.mark.parametrize("algorithm", Algorithm)
def test_diabolical_9(algorithm: Algorithm):
    """
    Diabolical sudoku from the master sdm collection
    """
    _test_sudoku(
        "850000031000070000000809000003000600970301052000020000100407006205000307000080000",
        algorithm=algorithm,
    )


@pytest.mark.parametrize("algorithm", Algorithm)
def test_diabolical_10(algorithm: Algorithm):
    """
    Diabolical sudoku from the master sdm collection
    """
    _test_sudoku(
        "031006009000040060008007300184070020000000000090020148005800400040060000300500780",
        algorithm=algorithm,
    )


def _test_sudoku(sdm: str, algorithm: Algorithm):
    board = Board(sdm)
    board = solve(board, algorithm=algorithm)
    assert get_state(board) == State.VALID


def _test_sudoku_has_duplicates(sdm: str, algorithm: Algorithm):
    board = Board(sdm)
    board = solve(board, algorithm=algorithm)
    assert get_state(board) == State.HAS_DUPLICATES


def _test_incomplete_sudoku(sdm: str, algorithm: Algorithm):
    board = Board(sdm)
    board = solve(board, algorithm=algorithm)
    assert get_state(board) == State.INCOMPLETE
