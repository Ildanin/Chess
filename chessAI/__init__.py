from network import Network
from positionClass import Position
from notation.square import BoardMove, BoardSquare, move_decode
from chessAI.data import position_encode
import os

saved_networks_path = os.path.join(os.path.dirname(__file__), "networks")

class ChessAI(Network):
    def get_move(self, position: Position) -> BoardMove:
        square = super().process(position_encode(position))
        square = BoardSquare(int(square[:8].argmax()), int(square[8:].argmax()))
        return BoardMove(square, square)
    
    def move(self, position: Position, skip_check: bool = False) -> BoardMove:
        move = self.get_move(position)
        position.move(move, skip_check=skip_check)
        return move
    
    def save(self, filename: str) -> None:
        return super().save(os.path.join(saved_networks_path, filename))


def load_chessAI(filename: str) -> ChessAI:
    ai = ChessAI([], 'linear')
    ai.load(os.path.join(saved_networks_path, filename))
    return ai