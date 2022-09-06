"""
Tic Tac Toe Player
"""

import copy
import random


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
        corners = [(0, 0), (0, 2), (2, 0), (2, 2)]
        return random.choice(corners)

    # get who's turn it is, possible moves, and a list for their resulting boards
    turn = player(board)

    # determine maximum/minimum value and return its move
    if turn == X:
        return max_value(board)[1]
    if turn == O:
        return min_value(board)[1]

    raise ValueError("Invalid State")


def min_value(board, alpha=-2, beta=2, move=None):
    # if the board is terminal return utility and the move to get there
    if terminal(board):
        return utility(board), move

    best = 2
    best_action = None

    # for every option find the max score
    for action in actions(board):
        val, _ = max_value(result(board, action), alpha, beta, action)

        # if current move gets a lower value save it to best
        if val < best:
            best = val
            best_action = action

        beta = min(beta, best)

        # if the best I can do is less than the worst I can do, prune
        if beta <= alpha:
            break

    return best, best_action


def max_value(board, alpha=-2, beta=2, move=None):
    # if the board is terminal return utility and the move to get there
    if terminal(board):
        return utility(board), move

    best = -2
    best_action = None

    # for every option find the min score
    for action in actions(board):
        val, _ = min_value(result(board, action), alpha, beta, action)

        # if current move gets a higher value save it to best
        if val > best:
            best = val
            best_action = action

        alpha = max(alpha, best)

        # if the best I can do is less than the worst I can do, prune
        if beta <= alpha:
            break

    return best, best_action
