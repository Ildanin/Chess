from network import Network
import numpy as np
from config import INFO, ACTIVATOR, NORMALIZER, FACTOR_RANGE, BIAS_RANGE, ALPHA, CYCLES
from data import get_games
from notation.pgn import PortableGameNotation
from positionClass import Position

class ChessAI(Network):
    def move_piece(self, position: Position) -> None:
        pass   

    #def PGN_slice(self, PGN: PortableGameNotation) -> list[tuple[np.ndarray, np.ndarray]]:
    #    pass

chessAI = ChessAI(INFO, ACTIVATOR, NORMALIZER, FACTOR_RANGE, BIAS_RANGE)
data = get_games("lichess_db_standard_rated_2013-01txt", 1)
print(data.__sizeof__()/2**20)
print(data[0])