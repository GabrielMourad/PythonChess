import random
import time
from constants import CHECKMATE, STALEMATE, DEPTH

values = {"P": 1, "N":3, "B": 3, "R":5, "Q": 9, "K": 0 }


def random_moves(valid_moves):
    return random.choice(valid_moves)


def get_nega_max(game_state, valid_moves):
    time.sleep(0.5)
    global next_move, counter
    next_move = None
    counter = 0
    print(counter)
    random.shuffle(valid_moves)
    #move_min_max(game_state, valid_moves, DEPTH, game_state.white_turn )
    nega_max(game_state, valid_moves, DEPTH, -CHECKMATE, CHECKMATE, 1 if game_state.white_turn else -1 )
    
    return next_move




def nega_max(game_state, valid_moves, depth, alpha, beta, turn_multiplier): #nega max with alpha beta pruning
    global next_move,counter
    counter += 1
    if depth == 0:
        return turn_multiplier * board_score(game_state)
        
    #

    max_score = -CHECKMATE
    for move in valid_moves:
        game_state.make_move(move)
        next_moves = game_state.get_valid_moves()
        total_score = -nega_max(game_state, next_moves, depth - 1, -beta, -alpha, -turn_multiplier)
        
        if total_score > max_score:
            max_score = total_score

            if depth == DEPTH:
                next_move = move
        game_state.undo_move()

        if max_score > alpha:
            alpha = max_score
        
        if alpha >= beta:
            break

    
    return max_score


def board_score(game_state):
    if game_state.check_mate:

        if game_state.white_turn:
            return -CHECKMATE
        else:
            return CHECKMATE
        
    elif game_state.stale_mate:
        return STALEMATE

    total_score = 0

    for row in game_state.board:
        for piece in row:

            if piece[0] == 'w':
                total_score += values[piece[1]]

            elif piece[0] == 'b':
                total_score -= values[piece[1]]

    return total_score
    