from typing import Iterator

class BoardSquare:
    def __init__(self, file: int, rank: int) -> None:
        self.file = file
        self.rank = rank
        self.id = file + 8*rank
    
    def __str__(self) -> str:
        return f"({self.file} {self.rank})"

    def __iter__(self) -> Iterator[int]:
        return iter((self.file, self.rank))
    
    def __eq__(self, square: object) -> bool:
        if square == None:
            return False
        elif type(square) != BoardSquare:
            raise ValueError(f"BoardSquare object cannot be compared with {type(square)} object")
        return (self.file == square.file and self.rank == square.rank)

    def isinrange(self, lower_bound: int = 0, upper_bound: int = 8) -> bool:
        return(lower_bound <= self.file < upper_bound and 
               lower_bound <= self.rank < upper_bound)

    def shift(self, dx: int = 0, dy: int = 0):
        return BoardSquare(self.file + dx, self.rank + dy)
    
    def get_algebraic(self) -> str:
        x_comp = 'abcdefgh'[self.file]
        y_comp = str(8 - self.rank)
        return x_comp + y_comp

class BoardMove:
    def __init__(self, start_square: BoardSquare, target_square: BoardSquare) -> None:
        self.start_square = start_square
        self.target_square = target_square
        self.file1 = start_square.file
        self.rank1 = start_square.rank
        self.file2 = target_square.file
        self.rank2 = target_square.rank
        self.dx = None
        self.dy = None
    
    def __str__(self) -> str:
        return f"({self.start_square} {self.target_square})"
    
    def __iter__(self) -> Iterator[int]:
        return iter((*self.start_square, *self.target_square))
    
    def __eq__(self, move: object) -> bool:
        if move == None:
            return False
        elif type(move) != BoardMove:
            raise ValueError(f"BoardSquare object cannot be compared with {type(move)} object")
        return (self.start_square == move.start_square and self.target_square == move.target_square)
    
    def get_dx(self) -> int:
        if self.dx == None:
            self.dx = self.target_square.file - self.start_square.file
        return self.dx
    
    def get_dy(self) -> int:
        if self.dy == None:
            self.dy = self.target_square.rank - self.start_square.rank
        return self.dy

def algebraic_to_board(algebraic: str) -> BoardSquare:
    x_comp = algebraic[0]
    y_comp = algebraic[1]
    file = 'abcdefgh'.index(x_comp)
    rank = 8 - int(y_comp)
    return BoardSquare(file, rank)