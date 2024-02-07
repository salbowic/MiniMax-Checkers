from config import *
from field import Field
from pos_move_field import PosMoveField

class Pawn(Field):
    def __init__(self, is_white, window, row, col, board):
        self.__is_white=is_white
        self.__is_marked =False 
        self.window = window
        self.row = row
        self.col = col
        self.board = board
        
    def __deepcopy__(self, memo):
        cls = self.__class__
        result = cls.__new__(cls)
        memo[id(self)] = result
        result.__dict__.update(self.__dict__)
        return result  

    def __str__(self):
        if self.is_white():
            return "w"
        return "b"
            
    def is_king(self):
        return False
    
    def is_empty(self):
        return False
    
    def is_white(self):
        return self.__is_white

    def is_blue(self):
        return not self.__is_white
    
    def is_marked(self):
        return self.__is_marked
    
    def toogle_mark(self):
        if self.__is_marked:
            for pos_move in self.pos_moves: #remove possible moves
                row = pos_move.dest_row
                col = pos_move.dest_col
                self.board.board[row][col] = Field()
            self.pos_moves=[]
        else:#self.is_marked
            self.pos_moves = self.board.get_piece_moves(self)
            for pos_move in self.pos_moves:
                row = pos_move.dest_row
                col = pos_move.dest_col
                self.board.board[row][col] = PosMoveField(False, self.window, row, col, self.board, self.row, self.col, pos_move)
            
        self.__is_marked = not self.__is_marked
    
    def draw(self):
        if self.__is_white:
            cur_col = WHITE
        else:
            cur_col = BLUE
        x = self.col*FIELD_SIZE
        y = self.row*FIELD_SIZE
        pygame.draw.circle(self.window, cur_col, (x+FIELD_SIZE/2, y+FIELD_SIZE/2), PIECE_SIZE)

        if self.__is_marked:
            pygame.draw.circle(self.window, RED, (x+FIELD_SIZE/2, y+FIELD_SIZE/2), PIECE_SIZE+MARK_THICK, MARK_THICK)