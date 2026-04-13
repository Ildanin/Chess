from network import Network
from positionClass import Position
from notation.square import BoardMove, move_decode
from chessAI.data import position_encode

class ChessAI(Network):    
    def get_move(self, position: Position) -> BoardMove:
        move = super().process(position_encode(position))
        return move_decode(''.join(str(round(bit)) for bit in move))