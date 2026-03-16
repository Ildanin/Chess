from math import copysign
from notationClass import Notation

class Position:
    def __init__(self, init_position: Notation | list[str]):
        if type(init_position) == Notation:
            self.pos_array = init_position.as_position_array()
        elif type(init_position) == list[str]:
            self.pos_array = init_position
        self.white_to_move = True
        self.en_passant: tuple | None = None
        self.white_long_castle = True
        self.white_short_castle = True
        self.black_long_castle = True
        self.black_short_castle = True

    def __iter__(self):
        return iter(self.pos_array)

    def get_piece(self, board_x: int, board_y: int) -> str:
        "Returns the piece given the coordinates"
        return self.pos_array[board_x + 8*board_y]
    
    def get_location(self, piece: str) -> tuple[int, int]:
        "Return first occurring coordinate of the piece"
        ind = self.pos_array.index(piece)
        return ind%8, ind//8
    
    def set_piece(self, board_x: int, board_y: int, piece: str = '') -> None:
        self.pos_array[board_x + 8*board_y] = piece
    
    def get_highlights(self, board_x: int, board_y: int) -> list[tuple[int, int]]:
        "Returns a list of coordinates to which the piece can move"
        squares = []
        for y in range(8):
            for x in range(8):
                if self.is_move_possible(board_x, board_y, x, y):
                    squares.append((x, y))
        return squares
    
    def get_possible_moves(self) -> list[tuple[int, int, int, int]]:
        moves = []
        for x1 in range(0,8):
            for y1 in range(0,8):
                for y2 in range(0, 8):
                    for x2 in range(0, 8):
                        if self.is_move_possible(x1, y1, y2, x2) == True:
                            moves.append((x1, y1, y2, x2))
        return moves

    def raw_move(self, board_x1: int, board_y1: int, board_x2: int, board_y2: int, promote_to: str | None = None) -> None:
        "Makes a move without any checks and does not pass the move"
        piece = self.get_piece(board_x1, board_y1)
        self.set_piece(board_x2, board_y2, piece)
        self.set_piece(board_x1, board_y1, '')
        self.handle_en_passant(board_x1, board_y1, board_x2, board_y2, piece)
        self.handle_castling(board_x1, board_x2, piece)
        self.handle_promotion(board_x2, board_y2, promote_to)
    
    def move(self, board_x1: int, board_y1: int, board_x2: int, board_y2: int, 
                promote_to: str | None = None, available_squares: list[tuple[int, int]] | None = None) -> bool:
        "Moves the piece if it is posible. Returns True if moved successfully, False otherwise"
        if self.is_move_possible(board_x1, board_y1, board_x2, board_y2, available_squares):
            self.raw_move(board_x1, board_y1, board_x2, board_y2, promote_to)
            self.white_to_move = not self.white_to_move
            return True
        return False
    
    def handle_en_passant(self, board_x1: int, board_y1: int, board_x2: int, board_y2: int, piece: str) -> None:
        if piece == 'P':
            if (board_x2, board_y2) == self.en_passant:
                self.set_piece(board_x2, board_y2 + 1)
            elif board_y2 - board_y1 == -2:
                self.en_passant = (board_x1, 5)
                return None
        elif piece == 'p':
            if (board_x2, board_y2) == self.en_passant:
                self.set_piece(board_x2, board_y2 - 1)
            elif board_y2 - board_y1 == 2:
                self.en_passant = (board_x1, 2)
                return None
        self.en_passant = None

    def handle_castling(self, board_x1: int, board_x2: int, piece: str) -> None:
        if piece == 'R':
            if board_x1 == 0:
                self.white_long_castle = False
            elif board_x1 == 7:
                self.white_short_castle = False
        elif piece == 'r':
            if board_x1 == 0:
                self.black_long_castle = False
            elif board_x1 == 7:
                self.black_short_castle = False
        elif piece == 'K':
            self.white_long_castle = False
            self.white_short_castle = False
            if board_x1 == 4:
                if board_x2 == 2:
                    self.set_piece(3, 7, 'R')
                    self.set_piece(0, 7, '')
                elif board_x2 == 6:
                    self.set_piece(5, 7, 'R')
                    self.set_piece(7, 7, '')
        elif piece == 'k':
            self.black_long_castle = False
            self.black_short_castle = False
            if board_x1 == 4:
                if board_x2 == 2:
                    self.set_piece(3, 0, 'r')
                    self.set_piece(0, 0, '')
                elif board_x2 == 6:
                    self.set_piece(5, 0, 'r')
                    self.set_piece(7, 0, '')

    def handle_promotion(self, board_x2: int, board_y2: int, promote_to: str | None) -> None:
        if promote_to != None:
            self.set_piece(board_x2, board_y2, promote_to)

    def ischeckmate(self) -> bool:
        if self.white_to_move:
            king_x, king_y = self.get_location('K')
        else:
            king_x, king_y = self.get_location('k')
        if not self.isattacked(king_x, king_y):
            return False
        for x1 in range(0,8):
            for y1 in range(0,8):
                for y2 in range(0, 8):
                    for x2 in range(0, 8):
                        if self.is_move_possible(x1, y1, y2, x2) == True:
                            return False
        return True
    
    def isdraw(self) -> bool:
        if self.pos_array.count('') == 62:
            return True
        if self.white_to_move:
            king_x, king_y = self.get_location('K')
        else:
            king_x, king_y = self.get_location('k')
        if self.isattacked(king_x, king_y): 
            return False
        for x1 in range(0,8):
            for y1 in range(0,8):
                for y2 in range(0, 8):
                    for x2 in range(0, 8):
                        if self.is_move_possible(x1, y1, y2, x2) == True:
                            return False 
        return True

    def is_move_possible(self, board_x1: int, board_y1: int, board_x2: int, board_y2: int, available_squares: list[tuple[int, int]] | None = None) -> bool:
        "Returns True if the move can be made, False otherwise"
        if available_squares != None:
            return ((board_x2, board_y2) in available_squares)
        if not(0 <= board_x1 < 8 and 0 <= board_y1 < 8 and 0 <= board_x2 < 8 and 0 <= board_y2 < 8):
            return False
        piece = self.get_piece(board_x1, board_y1)
        if piece == '':
            return False
        if piece.isupper() != self.white_to_move:
            return False
        if (self.get_piece(board_x2, board_y2) != '' and 
            self.white_to_move == self.get_piece(board_x2, board_y2).isupper()):
            return False
        match piece:
            case 'P':       movable = self.ismovable_wpawn(board_x1, board_y1, board_x2, board_y2)
            case 'p':       movable = self.ismovable_bpawn(board_x1, board_y1, board_x2, board_y2)
            case 'N' | 'n': movable = self.ismovable_knight(board_x1, board_y1, board_x2, board_y2)
            case 'B' | 'b': movable = self.ismovable_bishop(board_x1, board_y1, board_x2, board_y2)
            case 'R' | 'r': movable = self.ismovable_rook(board_x1, board_y1, board_x2, board_y2)
            case 'Q' | 'q': movable = self.ismovable_queen(board_x1, board_y1, board_x2, board_y2)
            case 'K' | 'k': movable = self.ismovable_king(board_x1, board_y1, board_x2, board_y2)
        if movable and not(self.ischecked(board_x1, board_y1, board_x2, board_y2)):
            return True
        return False
    
    def ispromotion(self, board_y2: int, piece: str) -> bool:
        return (board_y2 == 0 and piece == 'P' or 
                board_y2 == 7 and piece == 'p')

    def ischecked(self, board_x1: int, board_y1: int, board_x2: int, board_y2: int) -> bool:
        "Returns True if the king will be in check after the given move, False otherwise"
        saved_position = self.pos_array.copy() #saves the state of the game
        saved_states = self.en_passant, self.white_long_castle, self.white_short_castle, self.black_long_castle, self.black_short_castle
        self.raw_move(board_x1, board_y1, board_x2, board_y2) #makes a move
        if self.white_to_move:
            king_x, king_y = self.get_location('K')
        else:
            king_x, king_y = self.get_location('k')
        ischecked = self.isattacked(king_x, king_y) #checks if the king is attacked
        self.pos_array.clear() #return pos_array to its initial state
        self.pos_array += saved_position
        self.en_passant, self.white_long_castle, self.white_short_castle, self.black_long_castle, self.black_short_castle = saved_states
        return ischecked

    "'ismovable' functions return True if the piece can make the given move, False otherwise"
    def ismovable_wpawn(self, board_x1: int, board_y1: int, board_x2: int, board_y2: int) -> bool:
        if board_x1 == board_x2 and self.get_piece(board_x2, board_y2) == '':
            if board_y2 - board_y1 == -1: 
                return True
            elif board_y1 == 6 and board_y2 == 4 and self.get_piece(board_x2, 5) == '': 
                return True
        elif (board_y2 - board_y1 == -1 and abs(board_x2 - board_x1) == 1):
            if self.get_piece(board_x2, board_y2) != '': 
                return True
            elif (board_x2, board_y2) == self.en_passant: 
                return True
        return False

    def ismovable_bpawn(self, board_x1: int, board_y1: int, board_x2: int, board_y2: int) -> bool:
        if board_x1 == board_x2 and self.get_piece(board_x2, board_y2) == '':
            if board_y2 - board_y1 == 1: 
                return True
            elif board_y1 == 1 and board_y2 == 3 and self.get_piece(board_x2, 2) == '': 
                return True
        elif (board_y2 - board_y1 == 1 and abs(board_x2 - board_x1) == 1):
            if self.get_piece(board_x2, board_y2) != '': 
                return True
            elif (board_x2, board_y2) == self.en_passant: 
                return True
        return False

    def ismovable_knight(self, board_x1: int, board_y1: int, board_x2: int, board_y2: int) -> bool:
        if ((abs(board_x2 - board_x1) == 1 and abs(board_y2 - board_y1) == 2) or 
            (abs(board_y2 - board_y1) == 1 and abs(board_x2 - board_x1) == 2)):
            return True
        return False

    def ismovable_bishop(self, board_x1: int, board_y1: int, board_x2: int, board_y2: int) -> bool:
        if abs(board_x2 - board_x1) != abs(board_y2 - board_y1): 
            return False
        x_direction = int(copysign(1, board_x2-board_x1))
        y_direction = int(copysign(1, board_y2-board_y1))
        for x, y in zip(range(board_x1 + x_direction, board_x2, x_direction), 
                        range(board_y1 + y_direction, board_y2, y_direction)):
            if self.get_piece(x, y) != '': 
                return False
        return True

    def ismovable_rook(self, board_x1: int, board_y1: int, board_x2: int, board_y2: int) -> bool:
        if board_x1 == board_x2:
            y_direction = int(copysign(1, board_y2-board_y1))
            for y in range(board_y1 + y_direction, board_y2, y_direction):
                if self.get_piece(board_x1, y) != '': 
                    return False
            return True
        elif board_y1 == board_y2:
            x_direction = int(copysign(1, board_x2-board_x1))
            for x in range(board_x1 + x_direction, board_x2, x_direction):
                if self.get_piece(x, board_y1) != '': 
                    return False
            return True
        return False

    def ismovable_queen(self, board_x1: int, board_y1: int, board_x2: int, board_y2: int) -> bool:
        if (self.ismovable_rook(board_x1, board_y1, board_x2, board_y2) or 
            self.ismovable_bishop(board_x1, board_y1, board_x2, board_y2)):
            return True
        return False

    def ismovable_king(self, board_x1: int, board_y1: int, board_x2: int, board_y2: int) -> bool: #rewrite add attack checks
        if (-1 <= board_x2 - board_x1 <= 1) and (-1 <= board_y2 - board_y1 <= 1): 
            return True
        if self.white_to_move and self.get_piece(4, 7) == 'K' and board_y2 == 7:
            if (board_x2 == 2 and self.white_long_castle and self.get_piece(0, 7) == 'R' and 
                self.get_piece(1, 7) == '' and self.get_piece(3, 7) == ''): 
                return True
            elif (board_x2 == 6 and self.white_short_castle and self.get_piece(7, 7) == 'R' and 
                    self.get_piece(5, 7) == ''): 
                return True
        elif not(self.white_to_move) and self.get_piece(4, 0) == 'k' and board_y2 == 0:
            if (board_x2 == 2 and self.black_long_castle and self.get_piece(0, 0) == 'r' and
                self.get_piece(1, 0) == '' and self.get_piece(3, 0) == ''): 
                return True
            elif (board_x2 == 6 and self.black_short_castle and self.get_piece(7, 0) == 'r' and 
                    self.get_piece(5, 0) == ''): 
                return True
        return False

    "'isatacked' functions return True if the given square is attacked by an enemy piece, False otherwise"
    def isattacked(self, board_x: int, board_y: int) -> bool:
        return (self.isattacked_by_pawn(board_x, board_y) or 
                self.isattacked_by_knight(board_x, board_y) or 
                self.isattacked_by_bishop_queen(board_x, board_y) or 
                self.isattacked_by_rook_queen(board_x, board_y) or 
                self.isattacked_by_king(board_x, board_y))
    
    def isattacked_by_pawn(self, board_x: int, board_y: int) -> bool:
        if self.white_to_move:
            return self.isattacked_by_bpawn(board_x, board_y)
        else:
            return self.isattacked_by_wpawn(board_x, board_y)

    def isattacked_by_wpawn(self, board_x: int, board_y: int) -> bool:
        if board_y == 7:
            return False
        if board_x - 1 >= 0 and self.get_piece(board_x-1, board_y+1) == 'P':
            return True
        if board_x + 1 <= 7 and self.get_piece(board_x+1, board_y+1) == 'P':
            return True
        return False

    def isattacked_by_bpawn(self, board_x: int, board_y: int) -> bool:
        if board_y == 0:
            return False
        if board_x - 1 >= 0 and self.get_piece(board_x-1, board_y-1) == 'p':
            return True
        if board_x + 1 <= 7 and self.get_piece(board_x+1, board_y-1) == 'p':
            return True
        return False

    def isattacked_by_knight(self, board_x: int, board_y: int) -> bool:
        if self.white_to_move:
            knight = 'n'
        else:
            knight = 'N'
        for dy in [-2, -1, 1, 2]:
            for dx in [-2, -1, 1, 2]:
                if (abs(dx) != abs(dy) and 
                    0 <= board_x + dx < 8 and 0 <= board_y + dy < 8 and
                    self.get_piece(board_x + dx, board_y + dy) == knight):
                    return True
        return False

    def isattacked_by_bishop_queen(self, board_x: int, board_y: int) -> bool:
        if self.white_to_move:
            bishop = 'b'
            queen = 'q'
        else:
            bishop = 'B'
            queen = 'Q'
        for x, y in zip(range(board_x-1, -1, -1), 
                        range(board_y-1, -1, -1)):
            piece = self.get_piece(x, y)
            if piece == bishop or piece == queen:
                return True
            elif piece != '':
                break
        for x, y in zip(range(board_x+1, 8, 1), 
                        range(board_y-1, -1, -1)):
            piece = self.get_piece(x, y)
            if piece == bishop or piece == queen:
                return True
            elif piece != '':
                break
        for x, y in zip(range(board_x-1, -1, -1), 
                        range(board_y+1, 8, 1)):
            piece = self.get_piece(x, y)
            if piece == bishop or piece == queen:
                return True
            elif piece != '':
                break
        for x, y in zip(range(board_x+1, 8, 1), 
                        range(board_y+1, 8, 1)):
            piece = self.get_piece(x, y)
            if piece == bishop or piece == queen:
                return True
            elif piece != '':
                break
        return False

    def isattacked_by_rook_queen(self, board_x: int, board_y: int) -> bool:
        if self.white_to_move:
            rook = 'r'
            queen = 'q'
        else:
            rook = 'R'
            queen = 'Q'
        for y in range(board_y+1, 8, 1):
            piece = self.get_piece(board_x, y)
            if piece == rook or piece == queen:
                return True
            elif piece != '':
                break
        for y in range(board_y-1, -1, -1):
            piece = self.get_piece(board_x, y)
            if piece == rook or piece == queen:
                return True
            elif piece != '':
                break
        for x in range(board_x+1, 8, 1):
            piece = self.get_piece(x, board_y)
            if piece == rook or piece == queen:
                return True
            elif piece != '':
                break
        for x in range(board_x-1, -1, -1):
            piece = self.get_piece(x, board_y)
            if piece == rook or piece == queen:
                return True
            elif piece != '':
                break
        return False

    def isattacked_by_king(self, board_x: int, board_y: int) -> bool:
        if self.white_to_move:
            king = 'k'
        else:
            king = 'K'
        for y in range(max(0, board_y-1), min(board_y + 1, 7) + 1):
            for x in range(max(0, board_x-1), min(board_x + 1, 7) + 1):
                if self.get_piece(x, y) == king:
                    return True
        return False