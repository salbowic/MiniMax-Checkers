import random
from copy import deepcopy


def successor(board):
    possible_moves = board.get_possible_moves(not board.white_turn) 
    U = []
    for p_move in possible_moves:
            new_board = deepcopy(board)
            new_board.make_ai_move(p_move)
            U.append((deepcopy(new_board), p_move))
    return U

def minimax_a_b(board, depth):
    board = deepcopy(board)
    U = successor(board)
    a = -1000
    b = 1000
    moves = []

    for u, p_move in U:
        h_s = minimax_a_b_recurr(u, depth - 1, board.white_turn, a, b)
        moves.append((p_move, h_s))

    if board.white_turn:
        min_value = min(moves, key=lambda x: x[1])[1]
        best_moves = [move for move, value in moves if value == min_value]
        best_move = random.choice(best_moves)

    elif not board.white_turn:
        max_value = max(moves, key=lambda x: x[1])[1]
        best_moves = [move for move, value in moves if value == max_value]
        best_move = random.choice(best_moves)

    return best_move   

def minimax_a_b_recurr(board, depth, move_max, a, b):
    if board.end() or depth == 0:
        return board.evaluate()
        # return board.tight_evaluate(not move_max)
        # return board.half_evaluate()
        # return board.closer_better_evaluate()
        
    U = successor(board)

    if move_max:
        for u, p_move in U:
            a_value = minimax_a_b_recurr(u, depth - 1, not move_max, a, b)
            if a_value > a:
                a = a_value
            if a >= b:
                break
        return a
    else:
        for u, p_move in U:
            a_value = minimax_a_b_recurr(u, depth - 1, not move_max, a, b)
            if a_value < b:
                b = a_value
            if a >= b:
                break
        return b

def minimax_a_b_dif_eval(board, depth, h_s):
    board = deepcopy(board)
    U = successor(board)
    a = -1000
    b = 1000
    moves = []

    for u, p_move in U:
        h_s = minimax_a_b_recurr_dif_eval(u, depth - 1, board.white_turn, a, b, h_s)
        moves.append((p_move, h_s))

    if board.white_turn:
        min_value = min(moves, key=lambda x: x[1])[1]
        best_moves = [move for move, value in moves if value == min_value]
        best_move = random.choice(best_moves)

    elif not board.white_turn:
        max_value = max(moves, key=lambda x: x[1])[1]
        best_moves = [move for move, value in moves if value == max_value]
        best_move = random.choice(best_moves)

    return best_move

def minimax_a_b_recurr_dif_eval(board, depth, move_max, a, b, h_s):
    if board.end() or depth == 0:
        if h_s == 1:
            return board.evaluate()
        elif h_s == 2:
            return board.tight_evaluate(not move_max)
        elif h_s == 3:
            return board.half_evaluate()
        elif h_s == 4:
            return board.closer_better_evaluate()
        
    U = successor(board)

    if move_max:
        for u, p_move in U:
            a_value = minimax_a_b_recurr(u, depth - 1, not move_max, a, b)
            if a_value > a:
                a = a_value
            if a >= b:
                break
        return a
    else:
        for u, p_move in U:
            a_value = minimax_a_b_recurr(u, depth - 1, not move_max, a, b)
            if a_value < b:
                b = a_value
            if a >= b:
                break
        return b
