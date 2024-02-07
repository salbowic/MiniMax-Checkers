from config import *
from field import Field
from pawn import Pawn
from king import King
from move import Move

class Board:
    def __init__(self, window): # row, col
        self.board = []
        self.window = window
        self.marked_piece = None 
        self.something_is_marked=False
        self.white_turn = True
        self.white_fig_left = 12
        self.blue_fig_left = 12
        self.moves_after_capture_or_new_king = 0 # Defined to check for a draw

        self.__set_pieces()
        
    def __deepcopy__(self, memo):
        cls = self.__class__
        result = cls.__new__(cls)
        memo[id(self)] = result
        result.__dict__.update(self.__dict__)
        result.board= deepcopy(self.board )
        return result  

    def __str__(self):
        to_ret=""
        for row in range(8):
            for col in range(8):
                to_ret+=str(self.board[row][col])
            to_ret+="\n"
        return to_ret
        
    def __set_pieces(self):
        for row in range(8):
            self.board.append([])
            for col in range(8):
                self.board[row].append( Field() )

        for row in range(3):
            for col in range((row+1) % 2, BOARD_WIDTH, 2):
                self.board[row][col] = Pawn(False, self.window, row, col, self)

        for row in range(5, 8):
            for col in range((row+1) % 2, BOARD_WIDTH, 2):
                self.board[row][col] = Pawn(True, self.window, row, col, self)

    def get_piece_moves(self, piece):
        pos_moves=[]
        row = piece.row
        col = piece.col
        if piece.is_blue():
            enemy_is_white = True
        else:
            enemy_is_white = False

        if piece.is_white() or (piece.is_blue() and piece.is_king()):            
            dir_y = -1
            if row > 0:
                new_row=row+dir_y
                if col > 0:
                    new_col=col-1
                    if self.board[new_row][new_col].is_empty():
                        pos_moves.append(Move(piece, new_row, new_col))  
                        # When move is a capture
                    elif self.board[new_row][new_col].is_white()==enemy_is_white and new_row+dir_y>=0 and new_col-1>=0 and self.board[new_row+dir_y][new_col-1].is_empty():
                        pos_moves.append(Move(piece,new_row+dir_y, new_col-1, self.board[new_row][new_col]))  
                        
                if col < BOARD_WIDTH-1:
                    new_col=col+1
                    if self.board[new_row][new_col].is_empty():
                        pos_moves.append(Move(piece,new_row, new_col))    
                        # When move is a capture
                    elif self.board[new_row][new_col].is_white()==enemy_is_white and new_row+dir_y>=0 and new_col+1<BOARD_WIDTH and self.board[new_row+dir_y][new_col+1].is_empty():
                        pos_moves.append(Move(piece,new_row+dir_y, new_col+1, self.board[new_row][new_col]))  

        if piece.is_blue() or (piece.is_white() and self.board[row][col].is_king()):
            dir_y = 1
            if row<BOARD_WIDTH-1:
                new_row=row+dir_y
                if col > 0:
                    new_col=col-1
                    if self.board[new_row][new_col].is_empty():
                        pos_moves.append(Move(piece,new_row, new_col))    
                    elif self.board[new_row][new_col].is_white()==enemy_is_white and new_row+dir_y<BOARD_WIDTH and new_col-1>=0 and self.board[new_row+dir_y][new_col-1].is_empty():
                        pos_moves.append(Move(piece,new_row+dir_y, new_col-1, self.board[new_row][new_col]))  
                        
                if col < BOARD_WIDTH-1:
                    new_col=col+1
                    if self.board[new_row][new_col].is_empty():
                        pos_moves.append(Move(piece,new_row, new_col))    
                        #ruch zwiazany z biciem
                    elif self.board[new_row][new_col].is_white()==enemy_is_white and new_row+dir_y<BOARD_WIDTH and new_col+1<BOARD_WIDTH and self.board[new_row+dir_y][new_col+1].is_empty():
                        pos_moves.append(Move(piece,new_row+dir_y, new_col+1, self.board[new_row][new_col]))  
        return pos_moves
    
    def payoff(self):
        '''Payoff function w(s)'''
        if self.white_fig_left==0:
            return 1000
        elif self.blue_fig_left==0:
            return -1000
        elif len(self.get_possible_moves(not self.white_turn)) == 0:
            return -1000
        elif len(self.get_possible_moves(self.white_turn)) == 0:
            return 1000
        elif self.moves_after_capture_or_new_king >= 50 or self.kings_draw(): # Draw requirements
            return 0
        
    def evaluate(self):
        if self.end():
            return self.payoff()
        else:
            h = 0
            for row in range(BOARD_WIDTH):
                for col in range((row+1) % 2, BOARD_WIDTH, 2):
                    field = self.board[row][col]

                    if field.is_white():
                        if isinstance(field, Pawn):
                            if isinstance(field, King):
                                h -= 10
                            else:
                                h -= 1

                    elif field.is_blue():
                        if isinstance(field, Pawn):
                            if isinstance(field, King):
                                h += 10
                            else:
                                h += 1
            return h

    def tight_evaluate (self, is_blue_turn):
        h = self.evaluate()
        possible_moves = self.get_possible_moves(not is_blue_turn)
        for move in possible_moves:
            if move.captures:
                return h
        for row in range(BOARD_WIDTH):
            for col in range((row+1) % 2, BOARD_WIDTH, 2):
                field = self.board[row][col]
                
                neighbors = []
                if row + 1 < BOARD_WIDTH and col + 1 < BOARD_WIDTH:
                    neighbors.append(self.board[row + 1][col + 1])
                if row - 1 >= 0 and col + 1 < BOARD_WIDTH:
                    neighbors.append(self.board[row - 1][col + 1])
                if row + 1 < BOARD_WIDTH and col - 1 >= 0:
                    neighbors.append(self.board[row + 1][col - 1])
                if row - 1 >= 0 and col - 1 >= 0:
                    neighbors.append(self.board[row - 1][col - 1])

                for neighbor in neighbors:
                    if field.is_white():
                        if neighbor.is_white():
                            h+=0.15
                    elif field.is_blue():
                        if neighbor.is_blue():
                            h-=0.15
        return h
    
    def half_evaluate(self):
        if self.end():
            return self.payoff()
        else:
            h=0
            for row in range(BOARD_WIDTH):
                for col in range((row+1) % 2, BOARD_WIDTH, 2):
                    field = self.board[row][col]

                    if isinstance(field, Pawn):
                        if field.is_white():
                            if isinstance(field, King):
                                h -= 10

                            else:
                                if row < 4:
                                    h -= 7
                                else:
                                    h -= 5

                        elif field.is_blue():
                            if isinstance(field, King):
                                h += 10

                            else:
                                if row > 3:
                                    h += 7
                                else:
                                    h += 5    
            return h
        
    def closer_better_evaluate(self):
        if self.end():
            return self.payoff()
        else:
            h=0
            for row in range(BOARD_WIDTH):
                for col in range((row+1) % 2, BOARD_WIDTH, 2):
                    field = self.board[row][col]
                    
                    if isinstance(field, Pawn):
                        if field.is_white():
                            if isinstance(field, King):
                                h -= 15
                            else:
                                h -= 5 + (7 - row + 1) # (top row is 0, and the bottom one is 7)
                        elif field.is_blue():
                            if isinstance(field, King):
                                h += 15
                            else:
                                h += 5 + ((row + 1))

            return h

    def get_possible_moves(self, is_blue_turn):
        pos_moves = []
        for row in range(BOARD_WIDTH):
            for col in range((row+1) % 2, BOARD_WIDTH, 2):
                if not self.board[row][col].is_empty():
                    if (is_blue_turn and self.board[row][col].is_blue()) or (not is_blue_turn and self.board[row][col].is_white()):                        
                        pos_moves.extend(self.get_piece_moves(self.board[row][col]))
        return pos_moves
                        
    def draw(self):
        self.window.fill(WHITE)
        for row in range(BOARD_WIDTH):
            for col in range((row+1) % 2, BOARD_WIDTH, 2):
                y = row*FIELD_SIZE
                x = col*FIELD_SIZE
                pygame.draw.rect(self.window, BLACK, (x, y , FIELD_SIZE, FIELD_SIZE))
                self.board[row][col].draw()
                            
    def move(self, field):
        self.moves_after_capture_or_new_king += 1
        d_row = field.row
        d_col = field.col
        row_from = field.row_from
        col_from = field.col_from
        self.board[row_from][col_from].toogle_mark()
        self.something_is_marked = False
        self.board[d_row][d_col]=self.board[row_from][col_from]
        self.board[d_row][d_col].row=d_row
        self.board[d_row][d_col].col=d_col
        self.board[row_from][col_from]=Field()     

        if field.pos_move.captures:
            self.moves_after_capture_or_new_king = 0
            fig_to_del = field.pos_move.captures
            
            self.board[fig_to_del.row][fig_to_del.col]=Field()
            if self.white_turn:
                self.blue_fig_left -= 1
            else:
                self.white_fig_left -= 1
            
        if self.white_turn and d_row==0:#
            if not isinstance(self.board[d_row][d_col], King):
                self.moves_after_capture_or_new_king = 0
                self.board[d_row][d_col] = King(self.board[d_row][d_col])
            

        if not self.white_turn and d_row==BOARD_WIDTH-1:#damka
            if isinstance(self.board[d_row][d_col], King):
                self.moves_after_capture_or_new_king = 0
                self.board[d_row][d_col] = King(self.board[d_row][d_col])
            
        self.white_turn = not self.white_turn
    
    def kings_draw(self):
        white_kings = 0
        blue_kings = 0
        white_pawns = 0
        blue_pawns = 0
        for row in range(BOARD_WIDTH):
            for col in range((row + 1) % 2, BOARD_WIDTH, 2):
                field = self.board[row][col]

                if field.is_white() and isinstance(field, King):
                    white_kings += 1
                elif field.is_white() and isinstance(field, Pawn):
                    white_pawns += 1
                elif field.is_blue() and isinstance(field, King):
                    blue_kings += 1
                elif field.is_blue() and isinstance(field, Pawn):
                    blue_pawns += 1
        
        if white_pawns == 0 and blue_pawns == 0 and abs(white_kings - blue_kings) < 2:
            return True
        else:
            return False

    def end(self):
        return (
            len(self.get_possible_moves(not self.white_turn))==0
            or len(self.get_possible_moves(self.white_turn))==0
            or self.moves_after_capture_or_new_king >= 50
            or self.kings_draw()
        )
                
    def clicked_at(self, row, col):
        field = self.board[row][col]
        if field.is_move_mark():
            self.move(field)
        if (field.is_white() and self.white_turn and not self.something_is_marked) or (field.is_blue() and not self.white_turn and not self.something_is_marked):
            field.toogle_mark()
            self.something_is_marked = True
        elif self.something_is_marked and field.is_marked():
            field.toogle_mark()
            self.something_is_marked = False

    # similar to move         
    def make_ai_move(self, move):
        self.moves_after_capture_or_new_king +=1      
        d_row = move.dest_row
        d_col = move.dest_col
        row_from = move.piece.row
        col_from = move.piece.col

        self.board[d_row][d_col]=self.board[row_from][col_from]
        self.board[d_row][d_col].row=d_row
        self.board[d_row][d_col].col=d_col
        self.board[row_from][col_from]=Field()  

        if move.captures:
            # Counting moves after capture
            self.moves_after_capture_or_new_king = 0
            fig_to_del = move.captures
            
            self.board[fig_to_del.row][fig_to_del.col]=Field()
            if self.white_turn:
                self.blue_fig_left -= 1
            else:
                self.white_fig_left -= 1
            
        if self.white_turn and d_row==0:#
            if not isinstance(self.board[row_from][col_from], King):
                self.moves_after_capture_or_new_king = 0
                self.board[d_row][d_col] = King(self.board[d_row][d_col])

        if not self.white_turn and d_row==BOARD_WIDTH-1: # Queen
            if not isinstance(self.board[row_from][col_from], King):
                self.moves_after_capture_or_new_king = 0
                self.board[d_row][d_col] = King(self.board[d_row][d_col])
            
        self.board[row_from][col_from]=Field() 
        self.white_turn = not self.white_turn
    
