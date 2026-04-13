from chessAI import ChessAI
from chessAI.data import get_data
from positionClass import Position
from config import INFO, ACTIVATOR, NORMALIZER, FACTOR_RANGE, BIAS_RANGE, ALPHA, CYCLES

ai = ChessAI(INFO, ACTIVATOR, NORMALIZER, FACTOR_RANGE, BIAS_RANGE)

train_x, train_y = get_data("data.txt")