import numpy as np
import pandas as pd
import pygame
import random
from copy import deepcopy

FPS = 20
MINIMAX_DEPTH = 5
WIN_WIDTH = 800
WIN_HEIGHT = 800
BOARD_WIDTH = 8
FIELD_SIZE = WIN_WIDTH/BOARD_WIDTH
PIECE_SIZE = FIELD_SIZE/2 - 8
MARK_THICK = 5
POS_MOVE_MARK_SIZE = PIECE_SIZE/2
WHITE = (255,255,255)
BLACK = (0,0,0)
BLUE = (0,0,255)
RED = (255,0,0)
GREEN = (0,255,0)
