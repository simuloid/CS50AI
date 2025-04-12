"""
Tic Tac Toe Player
"""

import math
from copy import deepcopy

X = "X"
O = "O"
EMPTY = None

infinity = float('inf')

def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    xs = board[0].count(X) + board[1].count(X) + board[2].count(X)
    os = board[0].count(O) + board[1].count(O) + board[2].count(O)
    return X if xs <= os else O


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    return set([(i,j) for i in range(3) for j in range(3) if board[i][j] == None])


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    if action[0] < 0 or action[0] > 2 or action[1] < 0 or action[1] > 2 or board[action[0]][action[1]]:
        raise Exception(str(action) + ' is not a valid move')
    result = deepcopy(board)
    result[action[0]][action[1]] = player(board)
    return result


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    if board[0][0] and board[0][0] == board[0][1] and board[0][1] == board[0][2]:
        return board[0][0]
    if board[1][0] and board[1][0] == board[1][1] and board[1][1] == board[1][2]:
        return board[1][0]
    if board[2][0] and board[2][0] == board[2][1] and board[2][1] == board[2][2]:
        return board[2][0]

    if board[0][0] and board[0][0] == board[1][0] and board[1][0] == board[2][0]:
        return board[0][0]
    if board[0][1] and board[0][1] == board[1][1] and board[1][1] == board[2][1]:
        return board[0][1]
    if board[0][2] and board[0][2] == board[1][2] and board[1][2] == board[2][2]:
        return board[0][2]

    if board[0][0] and board[0][0] == board[1][1] and board[1][1] == board[2][2]:
        return board[0][0]

    if board[0][2] and board[0][2] == board[1][1] and board[1][1] == board[2][0]:
        return board[0][2]

    return None

def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    empty = board[0].count(None) + board[1].count(None) + board[2].count(None)
    victor = winner(board)
    return empty == 0 or victor != None


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    victor = winner(board)
    return 1 if victor == X else (-1 if victor == O else 0)


def min_ply(board):
    if terminal(board):
        return (utility(board), None)
    
    moves = actions(board)
    best_score = infinity
    best_move = None
    for m in moves:
        b = result(board, m)
        score, _ = max_ply(b)
        if score < best_score:
            best_score = score
            best_move = m

    return (best_score, best_move)


def max_ply(board):
    if terminal(board):
        return (utility(board), None)
    
    moves = actions(board)
    best_score = -infinity
    best_move = None
    for m in moves:
        b = result(board, m)
        score, _ = min_ply(b)
        if score > best_score:
            best_score = score
            best_move = m

    return (best_score, best_move)
    
def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board):
        return None
    score, move = max_ply(board) if player(board) == X else min_ply(board)
    return move
