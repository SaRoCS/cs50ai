"""
Tic Tac Toe Player
"""

import math
import copy


X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY], [EMPTY, EMPTY, EMPTY], [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """

    # count how many time each player has gone
    x_count = 0
    o_count = 0

    for row in board:
        for cell in row:
            if cell == X:
                x_count += 1
            elif cell == O:
                o_count += 1

    # use the count to determine turns
    if x_count > o_count:
        return O
    if x_count == o_count:
        return X

    raise ValueError("Invalid State")


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """

    moves = set()

    for i, row in enumerate(board):
        for j, cell in enumerate(row):
            if cell == EMPTY:
                moves.add((i, j))

    return moves


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """

    new_board = copy.deepcopy(board)
    turn = player(new_board)

    # double check that the space is empty
    if new_board[action[0]][action[1]] == EMPTY:
        new_board[action[0]][action[1]] = turn
        return new_board

    raise ValueError("Invalid Action")


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """

    # get coords of all plays
    x_coords = set()
    o_coords = set()

    for i, row in enumerate(board):
        for j, cell in enumerate(row):
            if cell == X:
                x_coords.add((i, j))
            elif cell == O:
                o_coords.add((i, j))

    # create list of winning patterns
    wins = (
        {(0, 0), (0, 1), (0, 2)},
        {(1, 0), (1, 1), (1, 2)},
        {(2, 0), (2, 1), (2, 2)},
        {(0, 0), (1, 0), (2, 0)},
        {(0, 1), (1, 1), (2, 1)},
        {(0, 2), (1, 2), (2, 2)},
        {(0, 0), (1, 1), (2, 2)},
        {(0, 2), (1, 1), (2, 0)},
    )

    # check if each pattern is a subset of plays
    for win in wins:
        if win.issubset(x_coords):
            return X
        if win.issubset(o_coords):
            return O
    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """

    # if there is a winner the board is terminal
    if winner(board):
        return True

    # if there is an open space the board if not terminal
    for row in board:
        if EMPTY in row:
            return False

    # board is full and therefore terminal
    return True


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """

    win = winner(board)

    if win == X:
        return 1
    if win == O:
        return -1
    return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """

    # no moves to make
    if terminal(board):
        return None

    # if board is empty return a corner
    if board == initial_state():
        return (0, 0)

    # get who's turn it is, possible moves, and a list for their resulting boards
    turn = player(board)
    moves = list(actions(board))
    moves.sort()
    boards = []

    # depending on whose turn it is run minimax on the possible resulting boards to
    # get their scores then pick the highest/lowest possible move and return the move to get there
    if turn == X:
        for move in moves:
            boards.append(min_value(result(board, move)))
        index_of_max = boards.index(max(boards))
        return moves[index_of_max]
    if turn == O:
        for move in moves:
            boards.append(max_value(result(board, move)))
        index_of_min = boards.index(min(boards))
        return moves[index_of_min]

    raise ValueError("Invalid State")


def min_value(board):
    # follows minimax min_value algorithm
    if terminal(board):
        return utility(board)
    v = 2
    for action in actions(board):
        v = min(v, max_value(result(board, action)))
    return v


def max_value(board):
    # follows minimax max_value algorithm
    if terminal(board):
        return utility(board)
    v = -2
    for action in actions(board):
        v = max(v, min_value(result(board, action)))
    return v
