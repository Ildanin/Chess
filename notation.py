#nbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1
#rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR b KQkq e3 0 1
#rnbqkbnr/pp1ppppp/8/2p5/4P3/8/PPPP1PPP/RNBQKBNR w KQkq c6 0 2
#rnbqkbnr/pp1ppppp/8/2p5/4P3/5N2/PPPP1PPP/RNBQKB1R b KQkq - 1 2


def board_to_algebraic(board_x: int, board_y: int) -> str:
    x_comp = 'abcdefgh'[board_x]
    y_comp = str(8 - board_y)
    return x_comp + y_comp

def algebraic_to_board(algebraic: str) -> tuple[int, int]:
    x_comp = algebraic[0]
    y_comp = algebraic[1]
    board_x = 'abcdefgh'.index(x_comp)
    board_y = 8 - int(y_comp)
    return board_x, board_y

class ForsythEdwardsNotation:
    def __init__(self, FEN_notation: str) -> None:
        self.FEN_notation = FEN_notation
        self.FEN_list = FEN_notation.split()
    
    def __str__(self) -> str:
        return self.FEN_notation
    
    def get_FEN(self) -> str:
        return self.FEN_notation
    
    def get_position_array(self) -> list[str]:
        position: list[str] = []
        for c in self.FEN_list[0]:
            if c.isdigit():
                position += ['' for _ in range(int(c))]
            elif c != '/':
                position.append(c)
        return(position)
    
    def get_is_white_to_move(self) -> bool:
        if self.FEN_list[1] == 'w':
            return True
        else:
            return False
    
    def get_castles(self) -> dict[str, bool]:
        return {'K': 'K' in self.FEN_list[2], 
                'Q': 'Q' in self.FEN_list[2], 
                'k': 'k' in self.FEN_list[2], 
                'q': 'q' in self.FEN_list[2]}
    
    def get_en_passant(self) -> tuple | None:
        if self.FEN_list[3] != '-':
            return algebraic_to_board(self.FEN_list[3])
    
    def get_halfmove_clock(self) -> int:
        return int(self.FEN_list[4])
    
    def get_fullmove_number(self) -> int:
        return int(self.FEN_list[5])

'''#pgn notation
#1. e4 e6 2. d4 b6 3. a3 Bb7 4. Nc3 Nh6 5. Bxh6 gxh6 6. Be2 Qg5 7. Bg4 h5 8. Nf3 Qg6 9. Nh4 Qg5 10. Bxh5 Qxh4 11. Qf3 Kd8 12. Qxf7 Nc6 13. Qe8# 1-0
class PortableGameNotation:
    def __init__(self, PGN_notation: str) -> None:
        self.PGN = PGN_notation
    
    def __str__(self) -> str:
        return self.PGN

    def append(self) -> None:
        pass

    def as_FEN_list(self) -> list[ForsythEdwardsNotation]: #todo
        pass

    def as_FEN(self, move: int) -> ForsythEdwardsNotation: #todo
        pass

    def as_position_array(self, move: int) -> list[str]: #todo
        pass'''