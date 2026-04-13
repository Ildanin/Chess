from chessAI import ChessAI
from chessAI.data import get_data
from positionClass import Position
import numpy as np
from config import INFO, ACTIVATOR, NORMALIZER, FACTOR_RANGE, BIAS_RANGE, ALPHA, CYCLES

ai = ChessAI(INFO, ACTIVATOR, NORMALIZER, FACTOR_RANGE, BIAS_RANGE)

train_x, train_y = get_data("data.txt", 0, 1000)

ai.train_stochastic_momentum(train_x, train_y, ALPHA, 0.2, CYCLES, 1000, True)

ai.save("ChessAI.txt")