from chessAI import ChessAI
from chessAI.data import get_data
from config import INFO, ACTIVATOR, NORMALIZER, FACTOR_RANGE, BIAS_RANGE, ALPHA, MOMENTUM_RATE, CYCLES

ai = ChessAI(INFO, ACTIVATOR, NORMALIZER, FACTOR_RANGE, BIAS_RANGE)

train_x, train_y = get_data("data.txt", 0, 1000)

ai.train_vanilla(train_x, train_y, ALPHA, CYCLES, True)

test_x, test_y = get_data("data.txt", 1000, 1010)

cost = 0
for x, y in zip(test_x, test_y):
    move = ai.process(x)
    cost += ai.cost(y)
print(cost/len(test_x))

ai.save("ChessAI3.txt")