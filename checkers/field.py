class Field:
    def draw(self):
        pass
    
    def is_empty(self):
        return True
    
    def is_white(self):
        return False

    def is_blue(self):
        return False
    
    def toogle_mark(self):    
        pass
    
    def is_move_mark(self):
        return False    
    
    def is_marked(self):
        return False       

    def __str__(self):
        return "."