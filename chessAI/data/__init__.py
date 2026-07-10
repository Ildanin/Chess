from notation.fen import ForsythEdwardsNotation
import numpy as np
import os
import torch as torch

datasets_path = os.path.dirname(__file__)

def position_encode_start(position_array: list[str]) -> np.ndarray:
    encoded = np.zeros((12, 8, 8))
    channel = 0
    for i, piece in enumerate(position_array):
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
    return encoded

def position_encode_target(position_array: list[str], square_id: int) -> np.ndarray:
    encoded = position_encode_start(position_array)
    start_matrix = np.zeros((1,8,8))
    start_matrix[0, square_id//8, square_id%8] = 1
    encoded = np.append(encoded, start_matrix, axis=0)
    return encoded

class Games(torch.utils.data.Dataset):
    def __init__(self, filename: str, start: int = 0, stop: int | None = None, color_filter: bool | None = None, first_move: int = 0, last_move: int | None = None, isstart: bool = True) -> None:
        file = open(os.path.join(datasets_path, filename))
        self.positions: list[torch.Tensor] = []  
        self.squares: list[int] = []        
        for i, info in enumerate(file):
            if i < start:
                continue
            elif stop != None and i >= stop:
                break
            position_FEN, start_id, target_id, color, fullmove_number = info.split()
            if first_move > int(fullmove_number):
                continue
            if last_move != None and last_move < int(fullmove_number):
                continue
            if color_filter != None and color_filter != int(color):
                continue
            pos_array = ForsythEdwardsNotation(position_FEN).get_position_array()
            if isstart:
                self.positions.append(torch.tensor(position_encode_start(pos_array), dtype=torch.float))
                self.squares.append(int(start_id))
            else:
                self.positions.append(torch.tensor(position_encode_target(pos_array, int(start_id)), dtype=torch.float))
                self.squares.append(int(target_id))
        file.close()
    
    def __len__(self):
        return len(self.positions)
    
    def __getitem__(self, index) -> tuple[torch.Tensor, int]:
        return self.positions[index], self.squares[index]