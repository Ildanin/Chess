from notation.pgn import PortableGameNotation
from notation.square import BoardMove, BoardSquare
from positionClass import Position
import numpy as np
import os
import torch as torch

datasets_path = os.path.dirname(__file__)

def position_encode_start(position: Position) -> torch.Tensor:
    encoded = np.zeros((12, 8, 8))
    channel = 0
    for i, piece in enumerate(position.pos_array):
        match piece:
            case '' : continue
            case 'P': channel = 0
            case 'N': channel = 1
            case 'B': channel = 2
            case 'R': channel = 3
            case 'Q': channel = 4
            case 'K': channel = 5
            case 'p': channel = 6
            case 'n': channel = 7
            case 'b': channel = 8
            case 'r': channel = 9
            case 'q': channel = 10
            case 'k': channel = 11
        encoded[channel, i//8, i%8] = 1
    return torch.tensor(encoded, dtype= torch.float)

def position_encode_target(position: Position, square: BoardSquare) -> torch.Tensor:
    encoded = position_encode_start(position).numpy()
    start_matrix = np.zeros((1,8,8))
    start_matrix[0, square.file, square.rank] = 1
    encoded = np.append(encoded, start_matrix, axis=0)
    return torch.tensor(encoded, dtype= torch.float)

class Games(torch.utils.data.Dataset):
    def __init__(self, filename: str, start: int, stop: int, color_filter: bool | None = None, isstart: bool = True, min_fullmove: int = 0, max_fullmove: int = -1) -> None:
        file = open(os.path.join(datasets_path, filename))
        self.positions: list[torch.Tensor] = []
        self.resulting_moves: list[int] = []
        for i, game in enumerate(file):
            if i < start:
                continue
            elif i >= stop:
                break
            position = Position()
            moves = PortableGameNotation(game).get_moves()
            for move in moves:
                if color_filter != None and color_filter != position.white_move:
                    position.move(move, skip_check=True)
                    continue
                if isstart:
                    self.positions.append(position_encode_start(position))
                    self.resulting_moves.append(move.start.id)
                else:
                    self.positions.append(position_encode_target(position, move.start))
                    self.resulting_moves.append(move.target.id)
                position.move(move, skip_check=True)
        file.close()
    
    def __len__(self):
        return len(self.positions)
    
    def __getitem__(self, index) -> tuple[torch.Tensor, int]:
        return self.positions[index], self.resulting_moves[index]