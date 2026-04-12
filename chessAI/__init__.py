from network import Network
import numpy as np
from config import INFO, ACTIVATOR, NORMALIZER, FACTOR_RANGE, BIAS_RANGE, ALPHA, CYCLES
from positionClass import Position
from notation.square import BoardMove, move_decode
from data import position_encode

class ChessAI(Network):
    def process(self, position: Position) -> BoardMove:
        move = super().process(position_encode(position))
        return move_decode(''.join(str(bit) for bit in move))