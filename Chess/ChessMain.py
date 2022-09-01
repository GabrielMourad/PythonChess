# Main Driver that is responsible for user input and displaying the GameState
# The use of pygame will allow us to display the engine

import pygame as p
from constants import DIM, WIDTH,HEIGHT,SQUARE_SIZE,FPS
import ChessEngine
import ChessAI

p.init()

IMAGES = {}

# initialize the images in the dictionary


def load_images():
    pieces = ['bB', 'bK', 'bN', 'bP', 'bQ',
              'bR', 'wB', 'wK', 'wN', 'wP', 'wQ', 'wR']

    # each piece will be put in to the dictionary based on file name
    # which corresponds to the image needed
    #ex: IMAGES['bB'] = p.image.load("images/bB.png")
    for piece in pieces:
        # we scale the image based on the square size
        IMAGES[piece] = p.transform.scale(p.image.load(
            "images/"+piece+".png"), (SQUARE_SIZE, SQUARE_SIZE))

# Responsible for all the drawings on the board


def draw_game_state(screen, game_state, valid_moves, square_selected):
    draw_board(screen, game_state)
    highlight_squares(screen, game_state, valid_moves, square_selected)

def game_over_text(screen, winner):
    font = p.font.SysFont("Comic Sans", 32, True, False)
    text_obj = font.render(winner, 0, p.Color("Black"))
    text_location = p.Rect(0,0,WIDTH, HEIGHT).move(WIDTH/2 - text_obj.get_width()/2, HEIGHT/2 - text_obj.get_height()/2)
    screen.blit(text_obj, text_location)



#highlights valid moves and selected square
def highlight_squares(screen, game_state, valid_moves, square_selected):
    curr_turn = "w" if game_state.white_turn else "b"
    opponent = "b" if game_state.white_turn else "w"
    if square_selected != ():
        row, column = square_selected

        if game_state.board[row][column][0] == curr_turn: #checks the current selection if it is a valid piece to move

            surface = p.Surface((SQUARE_SIZE, SQUARE_SIZE))
            surface.set_alpha(110)
            surface.fill(p.Color(51,51,255))

            screen.blit(surface, (column * SQUARE_SIZE, row* SQUARE_SIZE))

            
            for move in valid_moves:
                if move.startRow == row and move.startColumn == column:
                    surface.fill(p.Color(255,255,103))
                    screen.blit(surface, (move.endColumn* SQUARE_SIZE, move.endRow * SQUARE_SIZE))
                
                    if game_state.board[move.endRow][move.endColumn][0] == opponent:
                        print("opponent possible")
                        surface.fill(p.Color(255,0,0))
                        screen.blit(surface, (move.endColumn* SQUARE_SIZE, move.endRow * SQUARE_SIZE))

# draws squares on the board


def draw_board(screen, game_state):
    # makes a list of 2 colors, index 0 : light color, index 1: dark color
    colors = [p.Color("navajowhite3"), p.Color("sienna4")]

    # creates an 8x8 board
    for row in range(DIM):
        for column in range(DIM):
            color = colors[((row+column) % 2)]
            p.draw.rect(screen, color, p.Rect(column * SQUARE_SIZE,
                        row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
            piece = game_state.board[row][column]
            # checking if the part of the board is not empty
            if piece != "--":
                screen.blit(IMAGES[piece], p.Rect(column * SQUARE_SIZE,
                                                  row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

# draws pieces on the board




# Main Driver
def main():
    screen = p.display.set_mode((WIDTH, HEIGHT))
    clock = p.time.Clock()
    # gives us access to the board and variables
    game_state = ChessEngine.GameState()
    valid_moves = game_state.get_valid_moves()
    load_images()
    game_on = True
    game_over = False
    square_selected = () #initially, no square is selected
    player_clicks = [] #keeps track of player clicks
    move_made = False
    player_one = True
    player_two = False

    while game_on:
        human_turn = (game_state.white_turn and player_one) or (not game_state.white_turn and player_two)
        

        for event in p.event.get():
            if event.type == p.QUIT:
                game_on = False
            
            elif event.type == p.MOUSEBUTTONDOWN:
                if not game_over and human_turn:
                    location = p.mouse.get_pos() #location of mouse
                    column = location[0]// SQUARE_SIZE
                    row = location[1]// SQUARE_SIZE
                    
                    #checks if user clicked same square twice, will undo if so
                    if square_selected == (row,column):
                        square_selected = ()
                        player_clicks = []
                    else:
                        square_selected = (row,column)
                        player_clicks.append(square_selected)
                        
                    
                    if len(player_clicks) == 2: #checks the second click in order to move the 1st click location into the second click location
                        move = ChessEngine.Move(player_clicks[0], player_clicks[1], game_state.board)
                        print(move.get_chess_notation())
                        print(len(valid_moves))
                        for i in range(len(valid_moves)):
                            if move == valid_moves[i]: #checks if move is in the current valid move in the array
                                move_made = True
                                game_state.make_move(valid_moves[i])

                                square_selected = () #resets user clicks
                                player_clicks =  []
                        
                        if not move_made:
                            player_clicks = [square_selected]
                            
            elif event.type == p.KEYDOWN:
                if event.key == p.K_j:
                    game_state.undo_move()
                    move_made = True

                if event.key == p.K_r:
                    game_state = ChessEngine.GameState()
                    valid_moves = game_state.get_valid_moves()
                    square_selected = ()
                    player_clicks =  []
                    move_made = False

            #AI
            if not game_over and not human_turn:
                AI = ChessAI.random_moves(valid_moves)
                game_state.make_move(AI)
                move_made = True


            if move_made:
                print("making valid moves....")
                valid_moves = game_state.get_valid_moves()
                move_made = False

               
                        





        draw_game_state(screen, game_state, valid_moves, square_selected )

        if game_state.check_mate:
            game_over = True

            if game_state.white_turn:
                game_over_text(screen, "Black Wins")
            
            else:
                game_over_text(screen, "White Wins")
            
        elif game_state.stale_mate:
            game_over = True
            game_over_text(screen, "Stale Mate")

                
        clock.tick(FPS)
        p.display.flip()


if __name__ == "__main__":
    main()
