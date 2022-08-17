"""
Tic Tac Toe Player
"""

import math

X = "X"
O = "O"
EMPTY = None


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
    countX = 0
    countO = 0
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] == X:
                countX += 1
            elif board[i][j] == O:
                countO += 1

    if countX > countO:
        return 'O'
    else :
        return 'X'


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    allPossibleActions = []
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] == EMPTY:
                allPossibleActions.append([i, j])

    return allPossibleActions


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    updatedBoard = board
    if updatedBoard[action[0]][action[1]] == EMPTY:
        updatedBoard[action[0]][action[1]] = player(board)
    return updatedBoard


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """

    winner = ''
    for i in range(len(board)):
        if board[i][0] == board[i][1] and board[i][1] == board[i][2]:
            winner = board[i][0]

    for j in range(len(board)):
        if board[0][j] == board[1][j] and board[1][j] == board[2][j]:
            winner = board[0][j]

    if board[0][0] == board[1][1] and  board[1][1] == board[2][2]:
        winner = board[0][0]

    elif board[0][2] == board[1][1] and  board[1][1] == board[2][0]:
        winner = board[0][2]

    return winner or ''


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """

    if winner(board) != '' or actions(board) == []:
        return True
    else:
        return False


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if winner(board) == X:
        return 1
    elif winner(board) == O:
        return -1
    else:
        return 0


def minimax_aux(board):
    if utility(board) == -1:
        return -1

    elif utility(board) == 1:
        return 1

    if terminal(board):
        return 0

    if player(board) == X:
        best = -999
        for action in actions(board):
            board = result(board, action)
            best = max(best, minimax_aux(board))
            board[action[0]][action[1]] =  EMPTY
        return best

    else:
        best = 999
        for action in actions(board):
            board = result(board, action)
            best = min(best, minimax_aux(board))
            board[action[0]][action[1]] =  EMPTY
        return best
    
def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if len(actions(board)) == 9:
        return [0, 0]

    aiPlayer = player(board)
    if aiPlayer == 'X':
        bestValueSoFar = -999
    else:
        bestValueSoFar = 999

    bestMoveSoFar = [-1, -1]

    for action in actions(board):

        board = result(board, action)

        valueNow = minimax_aux(board)

        board[action[0]][action[1]] = EMPTY

        if aiPlayer == 'X' and valueNow > bestValueSoFar:
            move = []
            move.append(action[0])
            move.append(action[1])
            bestMoveSoFar = move
            bestValueSoFar = valueNow

        if aiPlayer == 'O' and valueNow < bestValueSoFar:
            move = []
            move.append(action[0])
            move.append(action[1])
            bestMoveSoFar = move
            bestValueSoFar = valueNow

    return bestMoveSoFar
