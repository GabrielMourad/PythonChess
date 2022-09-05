import random
import time
from constants import CHECKMATE, STALEMATE, DEPTH

values = {"P": 1, "N":3, "B": 3, "R":5, "Q": 9, "K": 0 }
test, test2 = CHECKMATE, STALEMATE


def random_moves(valid_moves):
    return random.choice(valid_moves)


def min_max(game_state, valid_moves):
    time.sleep(1.5)
    global next_moves
    move_min_max(game_state, valid_moves, DEPTH, game_state.white_turn )
    return next_moves



def move_min_max(game_state, valid_moves, depth, white_turn):
    global next_moves
    random.shuffle(valid_moves)
    if depth == 0:
        print(game_state.white_turn)

        return board_score(game_state)
    
    if white_turn:
        max_score = -CHECKMATE
        
        for move in valid_moves:
            
            game_state.make_move(move)
            next_moves = game_state.get_valid_moves()
            total_score = move_min_max(game_state, next_moves, depth-1, False)

            if total_score > max_score:
                max_score = total_score

                if depth == DEPTH:
                    next_moves = move
            
            game_state.undo_move()
            print(game_state.white_turn)

            return max_score
    
    else:
        min_score = CHECKMATE

        for move in valid_moves:
            game_state.make_move(move)
            next_moves = game_state.get_valid_moves()
            total_score = move_min_max(game_state, next_moves, depth -1, True)

            if total_score < min_score:

                min_score = total_score

                if depth == DEPTH:
                    next_moves = move
            
            game_state.undo_move()
            print(game_state.white_turn)
            return min_score
    

    



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
            if piece[0] == "w":
                total_score += values[piece[1]]
            elif piece[0] == "b":
                total_score -= values[piece[1]]
    
    return total_score