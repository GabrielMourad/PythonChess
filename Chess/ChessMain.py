# Main Driver that is responsible for user input and displaying the GameState
# The use of pygame will allow us to display the engine

import pygame
from pygame import mixer
from constants import DIM, WIDTH, HEIGHT, SQUARE_SIZE, FPS, COLORS
import ChessEngine
import ChessAI


pygame.init()
pygame.display.set_caption("Python CHESS (AI Editon)")

mixer.init()
mixer.music.load("audio/move_sound.mp3")
mixer.music.set_volume(0.7)

IMAGES = {}

# initialize the images in the dictionary


def menu(screen):

    BG = pygame.image.load("images/chessBG.png")
    BG = pygame.transform.scale(BG, (WIDTH, HEIGHT))
    title_font = pygame.font.SysFont("Verdana", 50)
    caption_font = pygame.font.SysFont("Arial", 30)
    caption_font2 = pygame.font.SysFont("Arial", 20)

    title = title_font.render("CHESS", 30, (139, 121, 94), True)
    caption1 = caption_font.render("Versus AI", 50, (16, 78, 139))
    caption2 = caption_font2.render(
        "Click anywhere to start!", 50, (16, 78, 139))

    run = True
    while run:

        screen.blit(BG, (0, 0))

        screen.blit(title, (170, 40))
        screen.blit(caption1, (195, 130))
        screen.blit(caption2, (175, 190))
        pygame.display.update()
        #caption_font = pygame.font.SysFont("Arial", 15)

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                run = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                run = False


def load_images():
    pieces = ['bB', 'bK', 'bN', 'bP', 'bQ',
              'bR', 'wB', 'wK', 'wN', 'wP', 'wQ', 'wR']

    # each piece will be put in to the dictionary based on file name
    # which corresponds to the image needed
    #ex: IMAGES['bB'] = pygame.image.load("images/bB.png")
    for piece in pieces:
        # we scale the image based on the square size
        IMAGES[piece] = pygame.transform.scale(pygame.image.load(
            "images/"+piece+".png"), (SQUARE_SIZE, SQUARE_SIZE))

# Responsible for all the drawings on the board


def draw_game_state(screen, game_state, valid_moves, square_selected):
    draw_board(screen, game_state)
    highlight_squares(screen, game_state, valid_moves, square_selected)


def game_over_text(screen, winner):
    font = pygame.font.SysFont("Comic Sans", 32, True, False)
    text_obj = font.render(winner, 0, pygame.Color("Black"))
    text_location = pygame.Rect(0, 0, WIDTH, HEIGHT).move(
        WIDTH/2 - text_obj.get_width()/2, HEIGHT/2 - text_obj.get_height()/2)
    screen.blit(text_obj, text_location)


# highlights valid moves and selected square
def highlight_squares(screen, game_state, valid_moves, square_selected):
    curr_turn = "w" if game_state.white_turn else "b"
    opponent = "b" if game_state.white_turn else "w"

    if square_selected != ():
        row, column = square_selected

        # checks the current selection if it is a valid piece to move
        if game_state.board[row][column][0] == curr_turn:

            surface = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE))
            surface.set_alpha(110)
            surface.fill(pygame.Color(51, 51, 255))

            screen.blit(surface, (column * SQUARE_SIZE, row * SQUARE_SIZE))

            for move in valid_moves:
                if move.startRow == row and move.startColumn == column:
                    surface.fill(pygame.Color(255, 255, 103))
                    screen.blit(surface, (move.endColumn *
                                SQUARE_SIZE, move.endRow * SQUARE_SIZE))

                    if game_state.board[move.endRow][move.endColumn][0] == opponent:
                        print("opponent possible")
                        surface.fill(pygame.Color(255, 0, 0))
                        screen.blit(surface, (move.endColumn *
                                    SQUARE_SIZE, move.endRow * SQUARE_SIZE))


# draws squares on the board


def draw_board(screen, game_state):
    # makes a list of 2 COLORS, index 0 : light color, index 1: dark color

    # creates an 8x8 board
    surface = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE))
    surface.set_alpha(110)
    for row in range(DIM):
        for column in range(DIM):
            color = COLORS[((row+column) % 2)]
            pygame.draw.rect(screen, color, pygame.Rect(column * SQUARE_SIZE,
                                                        row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
            piece = game_state.board[row][column]
            # checking if the part of the board is not empty
            if piece != "--":
                screen.blit(IMAGES[piece], pygame.Rect(column * SQUARE_SIZE,
                                                       row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

    if len(game_state.moveLog) != 0:
        prev_move_row, prev_move_column = game_state.moveLog[-1].startRow, game_state.moveLog[-1].startColumn
        curr_location_row, curr_location_column = game_state.moveLog[-1].endRow, game_state.moveLog[-1].endColumn
        surface.fill(pygame.Color(127, 255, 0))
        screen.blit(surface, (prev_move_column *
                              SQUARE_SIZE,  prev_move_row * SQUARE_SIZE))

        surface.set_alpha(70)
        screen.blit(surface, (curr_location_column *
                              SQUARE_SIZE,  curr_location_row * SQUARE_SIZE))

# draws pieces on the board


# Main Driver
def main():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    # gives us access to the board and variables
    game_state = ChessEngine.GameState()
    valid_moves = game_state.get_valid_moves()
    load_images()
    game_on = True
    game_over = False
    square_selected = ()  # initially, no square is selected
    player_clicks = []  # keeps track of player clicks
    move_made = False
    player_one = True
    player_two = False

    menu(screen)

    while game_on:

        for event in pygame.event.get():

            human_turn = (game_state.white_turn and player_one) or (
                not game_state.white_turn and player_two)

            if event.type == pygame.QUIT:
                game_on = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if not game_over and human_turn:
                    location = pygame.mouse.get_pos()  # location of mouse
                    column = location[0] // SQUARE_SIZE

                    row = location[1] // SQUARE_SIZE
                    # checks if user clicked same square twice, will undo if so
                    if square_selected == (row, column):
                        square_selected = ()
                        player_clicks = []
                    else:
                        square_selected = (row, column)
                        player_clicks.append(square_selected)

                    # checks the second click in order to move the 1st click location into the second click location
                    if len(player_clicks) == 2:
                        move = ChessEngine.Move(
                            player_clicks[0], player_clicks[1], game_state.board)
                        print(move.get_chess_notation())
                        print(len(valid_moves))
                        for i in range(len(valid_moves)):
                            # checks if move is in the current valid move in the array
                            if move == valid_moves[i]:
                                move_made = True
                                game_state.make_move(valid_moves[i])
                                mixer.music.play()
                                square_selected = ()  # resets user clicks
                                player_clicks = []

                        if not move_made:
                            player_clicks = [square_selected]

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_j:
                    game_state.undo_move()
                    move_made = True

                if event.key == pygame.K_r:
                    game_state = ChessEngine.GameState()
                    valid_moves = game_state.get_valid_moves()
                    square_selected = ()
                    player_clicks = []
                    move_made = False

            # AI
            if not game_over and not human_turn:

                AI_move = ChessAI.get_nega_max(game_state, valid_moves)

                if AI_move is None:
                    AI_move = ChessAI.random_moves(valid_moves)
                game_state.make_move(AI_move)
                mixer.music.play()
                draw_board(screen, game_state)
                move_made = True

            if move_made:

                print("making valid moves....")
                valid_moves = game_state.get_valid_moves()
                move_made = False

        draw_game_state(screen, game_state, valid_moves, square_selected)

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
        pygame.display.flip()


if __name__ == "__main__":
    main()
