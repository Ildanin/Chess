from notation.fen import ForsythEdwardsNotation
from notation.square import BoardMove, BoardSquare, algebraic_to_board
from positionClass import Position, WHITE_KING_SQUARE, BLACK_KING_SQUARE, WHITE_BACK_RANK, BLACK_BACK_RANK
from typing import Generator


def get_board_move(alg_move: str, position: Position) -> BoardMove:
    if alg_move == 'O-O':
        if position.white_move:
            return BoardMove(WHITE_KING_SQUARE, BoardSquare(6, WHITE_BACK_RANK))
        else:
            return BoardMove(BLACK_KING_SQUARE, BoardSquare(6, BLACK_BACK_RANK))
    if alg_move == 'O-O-O':
        if position.white_move:
            return BoardMove(WHITE_KING_SQUARE, BoardSquare(2, WHITE_BACK_RANK))
        else:
            return BoardMove(BLACK_KING_SQUARE, BoardSquare(2, BLACK_BACK_RANK))
    if alg_move[-2] == '=':
        promote_to = alg_move[-1]
        alg_move = alg_move[:-2]
    else:
        promote_to = 'Q'
    target = algebraic_to_board(alg_move[-2:])
    add_info = alg_move[1:-2]
    if len(add_info) == 2:
        return BoardMove(algebraic_to_board(add_info), target, promote_to)
    if position.white_move:
        legal_starts = list(position.getcandidates(target, alg_move[0]))
    else:
        legal_starts = list(position.getcandidates(target, alg_move[0].lower()))
    if len(legal_starts) == 1:
        return BoardMove(legal_starts[0], target, promote_to)
    if add_info.isdigit():
        rank = 8 - int(add_info)
        for start in legal_starts:
            if start.rank == rank:
                return BoardMove(start, target, promote_to)
    else:
        file = 'abcdefgh'.index(add_info)
        for start in legal_starts:
            if start.file == file:
                return BoardMove(start, target, promote_to)
    if len(legal_starts) > 1:
        for start in legal_starts:
            move = BoardMove(start, target, promote_to)
            if position.is_king_safe(move):
                return move
    print(position.get_FEN(), alg_move, *legal_starts)
    raise ValueError("Incorrect algebraic notation")



class PortableGameNotation:
    def __init__(self, PGN: str, init_position: ForsythEdwardsNotation = ForsythEdwardsNotation()) -> None:
        self.string = PGN
        self.init_position = init_position
    
    def __str__(self) -> str:
        return self.string
    
    def get_results(self) -> str:
        return self.string.split()[-1]
    
    def get_alg_moves(self) -> list[str]:
        unfiltered_list = self.string.split()
        filtered_list: list[str] = []
        for alg_move in unfiltered_list[:-1]:
            if not(alg_move[0].isdigit()):
                filtered_list.append(alg_move)
        return filtered_list
    
    def get_formatted_alg_moves(self) -> list[str]:
        formatted_move_list: list[str] = []
        for alg_move in self.get_alg_moves():
            alg_move = alg_move.replace('x', '')
            alg_move = alg_move.replace('+', '')
            alg_move = alg_move.replace('#', '')
            if alg_move[0].islower():
                alg_move = 'P' + alg_move
            formatted_move_list.append(alg_move)
        return formatted_move_list
    
    def get_moves(self) -> Generator[BoardMove]:
        alg_moves = self.get_formatted_alg_moves()
        position = Position(self.init_position)
        for alg_move in alg_moves:
            move = get_board_move(alg_move, position)
            yield move
            position.move(move, [move.target])
    
    def get_FENs(self) -> Generator[ForsythEdwardsNotation]:
        alg_moves = self.get_formatted_alg_moves()
        position = Position(self.init_position)
        for alg_move in alg_moves:
            yield position.get_FEN()
            move = get_board_move(alg_move, position)
            position.move(move, [move.target])
    
    def get_position(self) -> Position:
        alg_moves = self.get_formatted_alg_moves()
        position = Position(self.init_position)
        for alg_move in alg_moves:
            move = get_board_move(alg_move, position)
            position.move(move, [move.target])
        return position


def get_PGN(moves: list[BoardMove], init_position: ForsythEdwardsNotation = ForsythEdwardsNotation(), results: str | None = None) -> PortableGameNotation:
    position = Position(init_position)
    pgn = ''
    for i, move in enumerate(moves):
        if i%2 == 0:
            pgn += f"{1 + i//2}. "
        target = move.target.get_algebraic()
        piece = position.get_piece(move.start)
        take = ''
        if position.get_piece(move.target) != '':
            take = 'x'
        add_info = ''
        if piece == 'P' or piece == 'p':
            if take == 'x' or position.en_passant == move.target:
                add_info = 'abcdefgh'[move.start.file] + 'x'
            pgn += add_info + target
            if move.target.rank == 0 or move.target.rank == 7:
                pgn += f"={move.promote_to}"
        elif piece == 'K' or piece == 'k':
            if (piece == 'K' and position.castles['Q'] and target == 'c1' or 
                piece == 'k' and position.castles['q'] and target == 'c8'):
                pgn += 'O-O-O'
            elif (piece == 'K' and position.castles['K'] and target == 'g1' or 
                  piece == 'k' and position.castles['k'] and target == 'g8'):
                pgn += 'O-O'
            else:
                pgn += 'K' + take + target
        else:
            legal_starts = list(position.getcandidates(move.target, piece))
            if len(legal_starts) != 1:
                files = [start.file for start in legal_starts]
                if files.count(move.start.file) == 1:
                    add_info += 'abcdefgh'[move.start.file]
                else:
                    add_info = move.start.get_algebraic()
            pgn += piece.upper() + add_info + take + target
        position.move(move, [move.target])
        if position.ischeckmate():
            pgn += '#'
        elif position.ischecked():
            pgn += '+'
        pgn += ' '
    if results != None:
        pgn += results
        return PortableGameNotation(pgn, init_position)
    if pgn[-2] == '#':
        if position.white_move:
            results = '0-1'
        else:
            results = '1-0'
    else:
        results = '1/2-1/2'
    pgn += results
    return PortableGameNotation(pgn, init_position)