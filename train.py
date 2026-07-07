from chessAI import ChessAI, load_chessAI
from chessAI.data import get_data
from config import INFO, ACTIVATOR, NORMALIZER, FACTOR_RANGE, BIAS_RANGE, ALPHA, MOMENTUM_RATE, CYCLES

ai = ChessAI(INFO, ACTIVATOR, NORMALIZER, FACTOR_RANGE, BIAS_RANGE)
#ai = load_chessAI("ChessAI_C2.txt")

train_x, train_y = get_data("data.txt", 0, 12000, False)

ai.train_stochastic_momentum(train_x, train_y, ALPHA, MOMENTUM_RATE, CYCLES, 1000, True)

#ai.train_vanilla(train_x, train_y, 0.04, 5, True)

ai.save("ChessAI_A1.txt")