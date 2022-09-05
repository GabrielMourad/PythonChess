'''
Class responsible for storing the current state of the game
Aswell as determining valid moves based on the state, keeping a move log 
'''
#6.19.52
from constants import DIM


        
class GameState():

    # Color of pieces determined with the first character : "w" = white ,"b" = black
    # Second character represents the type: "K", "Q", "R", "N", "P", "B"
    def __init__(self):
        self.board = [
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bP", "bP", "bP", "bP", "bP", "bP", "bP", "bP"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["wP", "wP", "wP", "wP", "wP", "wP", "wP", "wP"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]
        ]

        self.testBoard = [
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bP", "bP", "bP", "bP", "bP", "bP", "bP", "bP"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["wP", "wP", "wP", "wP", "wP", "wP", "wP", "wP"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]
        ]

        # white_turn determines who's turn it is
        self.white_turn = True
        #tracks kings of both colors positions in case of stalemates and checkmates
        self.white_king_pos = (7,4) #initial pos
        self.black_king_pos = (0,4) #initial pos
        
        self.check_mate = False
        self.stale_mate = False
        self.en_passant_square = ()
        self.curr_castle_rights = CastleRights(True,True,True,True)
        self.castle_rights_log = [CastleRights(self.curr_castle_rights.white_right_castle, self.curr_castle_rights.black_right_castle, 
                                               self.curr_castle_rights.white_left_castle, self.curr_castle_rights.black_left_castle)]
        # Keeps tracks of the move taken place
        self.moveLog = []
        




    def make_move(self, move):
        
        
        #checks pawn promotion
        
        
        self.board[move.startRow][move.startColumn] = "--"
        self.board[move.endRow][move.endColumn] = move.pieceMoved
        self.moveLog.append(move)
        self.white_turn = not self.white_turn

        if move.pieceMoved == "wK":
            self.white_king_pos = (move.endRow, move.endColumn)
        elif move.pieceMoved == "bK":
            self.black_king_pos = (move.endRow, move.endColumn)
           
        #dealing with pawn promotion
        if move.is_pawn_promotion:
            self.board[move.endRow][move.endColumn] = move.pieceMoved[0] + "Q" #this grabs the color of the piece and concatinates the promotion for the pawn

        #dealing with en passant
        if move.is_en_passant:
            self.board[move.startRow][move.endColumn] = "--"

        if move.pieceMoved[1] == "P" and abs(move.startRow - move.endRow) == 2:
            self.en_passant_square = ((move.startRow + move.endRow) //2, move.startColumn)
        else:
            self.en_passant_square = ()
        
        if move.castle_move:
            if move.endColumn - move.startColumn == 2: #right castle
                self.board[move.endRow][move.endColumn-1] = self.board[move.endRow][move.endColumn +1] #sets rook
                self.board[move.endRow][move.endColumn+1] = "--" #removes rook
            else: #left castle
                self.board[move.endRow][move.endColumn+1] = self.board[move.endRow][move.endColumn-2]
                self.board[move.endRow][move.endColumn-2] = "--"

        #dealing with castling
        self.check_castle_rights(move)
        self.castle_rights_log.append(CastleRights(self.curr_castle_rights.white_right_castle, self.curr_castle_rights.black_right_castle, 
                                  self.curr_castle_rights.white_left_castle, self.curr_castle_rights.black_left_castle))
        
        
        
    
    def undo_move(self):
    
       if len(self.moveLog) != 0:
            move = self.moveLog.pop()
            self.board[move.startRow][move.startColumn] = move.pieceMoved
            self.board[move.endRow][move.endColumn] = move.pieceCaptured
            self.white_turn = not self.white_turn
            if move.pieceMoved == "wK":
                self.white_king_pos = (move.startRow, move.startColumn)
        
            elif move.pieceMoved == "bK":
                 self.black_king_pos = (move.startRow, move.startColumn)
            
            #en passant
            if move.is_en_passant:
                self.board[move.endRow][move.endColumn] = "--"
                self.board[move.startRow][move.endColumn] = move.pieceCaptured
                self.en_passant_square = (move.endRow, move.endColumn)
            
            #2 square advance pawn
            if move.pieceMoved == "p" and abs(move.startRow - move.endRow) == 2:
                self.en_passant_square = ()
            
            #dealing with castle
            self.castle_rights_log.pop() #remove the latest castle rights
            updated_rights = self.castle_rights_log[-1] #set the current rights to the last rights in the list
            self.curr_castle_rights = CastleRights(updated_rights.white_right_castle, updated_rights.black_right_castle, updated_rights.white_left_castle, updated_rights.black_left_castle)
            if move.castle_move:
                if move.endColumn - move.startColumn == 2: #right castle
                    self.board[move.endRow][move.endColumn+1] = self.board[move.endRow][move.endColumn-1]
                    self.board[move.endRow][move.endColumn-1] = "--"
                
                else: #left
                    self.board[move.endRow][move.endColumn-2] = self.board[move.endRow][move.endColumn +1]
                    self.board[move.endRow][move.endColumn+1] = "--"
   
   
    def get_valid_moves(self):
        saved_en_passant = self.en_passant_square
        castle_rights = CastleRights(self.curr_castle_rights.white_right_castle, self.curr_castle_rights.black_right_castle, 
                                  self.curr_castle_rights.white_left_castle, self.curr_castle_rights.black_left_castle)
       
        moves = self.get_possible_moves() #generates a list of all possible moves based on the current state
        
        if self.white_turn:
            self.get_castle_moves(self.white_king_pos[0], self.white_king_pos[1], moves)
        else:
            self.get_castle_moves(self.black_king_pos[0], self.black_king_pos[1], moves)
            

        #For each move, make the move
        for i in range(len(moves)-1,-1,-1):
            self.make_move(moves[i])
            
            self.white_turn = not self.white_turn
            if self.in_check():
                moves.remove(moves[i])
            
            self.white_turn = not self.white_turn
            self.undo_move()
        
        if len(moves) == 0:
            if self.in_check():
                self.check_mate = True
            else:
                self.stale_mate = True
        
        else:
            self.check_mate = False
            self.stale_mate = False
       
        self.en_passant_square = saved_en_passant
        self.curr_castle_rights = castle_rights

        return moves
    
    def in_check(self):
        if self.white_turn:
            return self.current_king_danger(self.white_king_pos[0], self.white_king_pos[1])
        else:
            return self.current_king_danger(self.black_king_pos[0], self.black_king_pos[1] )

    def current_king_danger(self, kings_row, kings_column): 
        self.white_turn = not self.white_turn
        enemy_moves = self.get_possible_moves()
        self.white_turn = not self.white_turn
        for enemy_move in enemy_moves:
            if enemy_move.endRow == kings_row and enemy_move.endColumn == kings_column:
                return True
    
        return False
    
    def check_castle_rights(self,move):
        if move.pieceMoved == "wK":
            self.curr_castle_rights.white_left_castle = False
            self.curr_castle_rights.white_right_castle = False
       
        elif move.pieceMoved == "bK":
            self.curr_castle_rights.black_left_castle = False
            self.curr_castle_rights.black_right_castle = False
        
        elif move.pieceMoved == "wR":
            if move.startRow == 7:
                if move.startColumn == 0:
                    self.curr_castle_rights.white_left_castle = False
                elif move.startColumn == 7:
                    self.curr_castle_rights.white_right_castle = False

        elif move.pieceMoved == "bR":
            if move.startRow == 0:
                if move.startColumn == 0:
                    self.curr_castle_rights.black_left_castle = False
                elif move.startColumn == 7:
                    self.curr_castle_rights.black_right_castle = False


    
    def get_possible_moves(self): #returns a list with all possible moves in chess with the current state of our board
        moves = []

        for row in range(DIM): # can use range(len(self.board))
            for column in range(DIM): # can use range(len(self.board[row]))
                turn = self.board[row][column][0] #gets first letter of element (its either 'w' or 'b')
                if (turn == "w" and self.white_turn) or (turn == "b" and not self.white_turn):
                    piece = self.board[row][column][1] #gets second letter (p, k, q, etc..)

                    if piece == "P":
                        self.get_pawn_moves(row, column, moves)
                    elif piece == "R":
                        self.get_rook_moves(row, column, moves)
                    
                    elif piece == "B":
                        self.get_bishop_moves(row, column, moves)
                    
                    elif piece == "K":
                        self.get_king_moves(row,column,moves)
                    
                    elif piece == "N":
                        self.get_knight_moves(row,column,moves)

                    elif piece == "Q":
                        self.get_queen_moves(row, column, moves)
                    
                    

        
        return moves

    def get_pawn_moves(self, row, column, moves):
        
        if self.white_turn: #white's turn
            if self.board[row-1][column] == "--": #if white, we must go up the array, hence minus 1 row
                moves.append(Move((row,column), (row-1, column), self.board))              

                if row == 6 and self.board[row-2][column] == "--":
                    moves.append(Move((row,column), (row-2, column), self.board))

            if (column - 1) >= 0: #captures to left 
                if self.board[row - 1][column-1][0] == "b": #a black piece to capture diagonally from the left
                        moves.append(Move((row, column), (row-1, column -1), self.board))
                
                elif (row-1, column-1) == self.en_passant_square:
                    moves.append(Move((row, column), (row-1, column -1), self.board, en_passant=True))
      

            if (column +1) <= 7: #captures to right
                if self.board[row-1][column + 1][0] == "b":
                        moves.append(Move((row, column), (row-1, column +1), self.board))
               
                elif (row-1, column+1) == self.en_passant_square:
                    moves.append(Move((row, column), (row-1, column +1), self.board, en_passant=True))
        else:
            if self.board[row+1][column] == "--": #if black, we must go down the array, hence plus 1 row
                moves.append(Move((row,column), (row + 1, column), self.board))              

                if row == 1 and self.board[row+2][column] == "--":
                    moves.append(Move((row,column), (row + 2, column), self.board))
                    
            if (column - 1) >= 0: #captures to right 
                if self.board[row + 1][column - 1][0] == "w": #a black piece to capture diagonally from the left
                    moves.append(Move((row, column), (row + 1, column - 1 ), self.board))
               
                elif (row + 1, column-1) == self.en_passant_square:
                    moves.append(Move((row, column), (row + 1, column -1), self.board, en_passant=True))
                       
            if (column + 1) <= 7: #captures to left
                if self.board[row + 1 ][column + 1][0] == "w":
                    moves.append(Move((row, column), (row + 1, column + 1), self.board))
                
                elif (row + 1, column+1) == self.en_passant_square:
                    moves.append(Move((row, column), (row + 1, column+1), self.board, en_passant=True))


   
    def get_rook_moves(self, row, column, moves):
        
        coords = [(-1,0), (0,-1), (1,0), (0,1)] # coordinates of directions that are possible
        enemy_piece = "b" if self.white_turn else "w"

        for coord in coords:
            for i in range(1, 8): # goes through 1-7 as i
                ending_column = column + coord[1] * i #takes starting pos + direction moving in * i
                ending_row = row + coord[0] * i       # ^^

                if 0 <= ending_row <= 7 and  0 <= ending_column <= 7: #still on the board
                    item_on_square = self.board[ending_row][ending_column]

                    if item_on_square == "--" :
                        moves.append(Move((row,column), (ending_row, ending_column), self.board))
                    
                    elif item_on_square[0] == enemy_piece:
                        moves.append(Move((row,column), (ending_row, ending_column), self.board))
                        break
                    else:
                        break
                else: #out of the board
                    break #continues with other directions
    
    
    def get_bishop_moves(self, row,column,moves):
       
        coords = [(-1,-1), (1,-1), (-1,1), (1,1)] # coordinates of directions that are possible
        enemy_piece = "b" if self.white_turn else "w"

        for coord in coords:
            for i in range(1, 8): # goes through 1-7 as i
                ending_column = column + coord[1] * i #takes starting pos + direction moving in * i
                ending_row = row + coord[0] * i       # ^^

                if 0 <= ending_row <= 7 and  0 <= ending_column <= 7: #still on the board
                    item_on_square = self.board[ending_row][ending_column]

                    if item_on_square == "--":
                        moves.append(Move((row,column), (ending_row, ending_column), self.board))
                   
                    elif item_on_square[0] == enemy_piece:
                        moves.append(Move((row,column), (ending_row, ending_column), self.board))
                        break #leaves the loop when finding a enemy piece
                    else:
                        break
                
                else: #out of the board
                    break #continues with other directions
    
    def get_knight_moves(self, row, column, moves):
        coords = [(2,1), (1,2), (-2,1), (2,-1), (-2,-1), (-1,2), (-1,-2), (1,-2)] # coordinates of directions that are possible
        enemy_piece = "b" if self.white_turn else "w"

        for coord in coords:
            for i in range(1, 8): # goes through 1-7 as i
                ending_column = column + coord[1]  #takes starting pos + direction moving in * i
                ending_row = row + coord[0]        # ^^

                if 0 <= ending_row <= 7 and  0 <= ending_column <= 7: #still on the board
                    item_on_square = self.board[ending_row][ending_column]

                    if item_on_square == "--":
                        moves.append(Move((row,column), (ending_row, ending_column), self.board))
                   
                    elif item_on_square[0] == enemy_piece:
                        moves.append(Move((row,column), (ending_row, ending_column), self.board))
                        break #continues the if statements
                    else:
                        break
                
                else: #out of the board
                    break #continues with other directions

    def get_king_moves(self, row, column, moves):
       
        coords = [(1,0), (0,1), (1,1), (-1,0), (0,-1), (1,-1), (-1,1), (-1,-1)] # coordinates of directions that are possible
        enemy_piece = "b" if self.white_turn else "w"

        for i in range(1, 8): # goes through 1-7 as i
            ending_column = column + coords[i][1] #takes starting pos + direction moving in * i
            ending_row = row + coords[i][0]      # ^^

            if 0 <= ending_row <= 7 and  0 <= ending_column <= 7: #still on the board
                item_on_square = self.board[ending_row][ending_column]

                if item_on_square == "--" or item_on_square[0] == enemy_piece:
                    moves.append(Move((row,column), (ending_row, ending_column), self.board))
                   
           


    def get_castle_moves(self, row, column, moves):
        if self.current_king_danger(row,column):
            return
        
        if (self.white_turn and self.curr_castle_rights.white_left_castle) or (not self.white_turn and self.curr_castle_rights.black_left_castle):
            self.get_left_castle_moves(row, column, moves)
        
        if (self.white_turn and self.curr_castle_rights.white_right_castle) or (not self.white_turn and self.curr_castle_rights.black_right_castle):
            self.get_right_castle_moves(row, column, moves)

    def get_right_castle_moves(self, row, column, moves):
        if self.board[row][column+1] == "--" and self.board[row][column+2] == "--":
            if not self.current_king_danger(row,column+1) and not self.current_king_danger(row, column+2):
                moves.append(Move((row,column), (row, column+2), self.board, castle_move=True))

    def get_left_castle_moves(self, row, column, moves):
        if self.board[row][column-1] == "--" and self.board[row][column-2] == "--" and self.board[row][column-3] == "--":
            if not self.current_king_danger(row,column-1) and not self.current_king_danger(row, column-2):
                moves.append(Move((row,column), (row, column-2), self.board, castle_move=True)) 
               

    def get_queen_moves(self,row,column, moves):
       
        self.get_bishop_moves(row,column, moves)
        self.get_rook_moves(row,column, moves)


class CastleRights():
    def __init__(self, white_right_castle, black_right_castle, white_left_castle, black_left_castle):
        self.white_left_castle = white_left_castle
        self.white_right_castle = white_right_castle
        self.black_left_castle = black_left_castle 
        self.black_right_castle = black_right_castle

class Move():
    ranksToRows = {"1": 7, "2": 6, "3": 5, "4": 4,
                   "5": 3, "6": 2, "7": 1, "8": 0}
    rowstoRanks = {v: k for k, v in ranksToRows.items()}
    filesToColumns = {"a": 0, "b": 1, "c": 2, "d": 3,
                      "e": 4, "f": 5, "g": 6, "h": 7}
    columnsToFiles = {v: k for k, v in filesToColumns.items()}

    def __eq__(self, object):
        
        if isinstance(object, Move):

            return self.move_ID == object.move_ID
        
        return False

    def __init__(self, startSquare, endSquare, board, en_passant = False, castle_move = False):
        self.startRow = startSquare[0]
        self.startColumn = startSquare[1]
        self.endRow = endSquare[0]
        self.endColumn = endSquare[1]
        self.pieceMoved = board[self.startRow][self.startColumn]
        self.pieceCaptured = board[self.endRow][self.endColumn]
        self.is_pawn_promotion =  (self.pieceMoved == "wP" and self.endRow == 0) or (self.pieceMoved == "bP" and self.endRow == 7)
        self.is_en_passant = en_passant

        if self.is_en_passant:
            self.pieceCaptured = "wP" if self.pieceMoved == "bP" else "bP"

        self.castle_move = castle_move

        self.move_ID = self.startRow * 1000 + self.startColumn * 100 + self.endRow *10 + self.endColumn
        
        
    
    def get_chess_notation(self):
        return self.get_rank_file(self.startRow, self.startColumn) + self.get_rank_file(self.endRow, self.endColumn)

    def get_rank_file(self, row, column):
        return self.columnsToFiles[column] + self.rowstoRanks[row]