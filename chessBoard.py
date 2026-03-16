import pygame as pg
from settings import *
import os
from math import copysign
from typing import Literal
from time import perf_counter


BB = pg.image.load(os.path.join("assets", "black_bishop.png "))
BK = pg.image.load(os.path.join("assets", "black_king.png "))
BN = pg.image.load(os.path.join("assets", "black_knight.png "))
BP = pg.image.load(os.path.join("assets", "black_pawn.png "))
BQ = pg.image.load(os.path.join("assets", "black_queen.png "))
BR = pg.image.load(os.path.join("assets", "black_rook.png "))

WB = pg.image.load(os.path.join("assets", "white_bishop.png "))
WK = pg.image.load(os.path.join("assets", "white_king.png "))
WN = pg.image.load(os.path.join("assets", "white_knight.png "))
WP = pg.image.load(os.path.join("assets", "white_pawn.png "))
WQ = pg.image.load(os.path.join("assets", "white_queen.png "))
WR = pg.image.load(os.path.join("assets", "white_rook.png"))

class ChessBoard:
    def __init__(self, screen: pg.Surface, x: int, y: int, size: int = BOARD_SIZE, init_FEN_position = INIT_POSITION,
                 white_color: tuple = WHITE_COLOR, black_color: tuple = BLACK_COLOR, highlight_clor: tuple = HIGHLIGHT_COLOR, higlight_moves: bool = HIGHLIGHT_MOVES) -> None:
        self.screen = screen
        self.x = x
        self.y = y
        self.square_size = size//8
        self.size = self.square_size*8
        self.white_color = white_color
        self.black_color = black_color
        self.highlight_clor = highlight_clor
        self.higlight_moves = higlight_moves

        self.init_FEN_position = init_FEN_position
        self.position = self.get_position(init_FEN_position)
        self.history = [init_FEN_position]
        self.position_handler = self.Position_handler(self.position)

        self.prev_pos: tuple[int, int] | None = None
        self.higlighted_squares: list[tuple[int, int]] | None = None
        self.promotion = None

        self.piece_assets = {
            'b': pg.transform.scale(BB.convert_alpha(), (self.square_size, self.square_size)),
            'k': pg.transform.scale(BK.convert_alpha(), (self.square_size, self.square_size)),
            'n': pg.transform.scale(BN.convert_alpha(), (self.square_size, self.square_size)),
            'p': pg.transform.scale(BP.convert_alpha(), (self.square_size, self.square_size)),
            'q': pg.transform.scale(BQ.convert_alpha(), (self.square_size, self.square_size)),
            'r': pg.transform.scale(BR.convert_alpha(), (self.square_size, self.square_size)),

            'B': pg.transform.scale(WB.convert_alpha(), (self.square_size, self.square_size)),
            'K': pg.transform.scale(WK.convert_alpha(), (self.square_size, self.square_size)),
            'N': pg.transform.scale(WN.convert_alpha(), (self.square_size, self.square_size)),
            'P': pg.transform.scale(WP.convert_alpha(), (self.square_size, self.square_size)),
            'Q': pg.transform.scale(WQ.convert_alpha(), (self.square_size, self.square_size)),
            'R': pg.transform.scale(WR.convert_alpha(), (self.square_size, self.square_size))
            }
        self.draw()
        
    def __str__(self) -> str: #todo
        return 'TODO'

    def get_position(self, notation: str) -> list[str]: #move to dedicated class
        "Returns the position as an array of strings(chars) given the FEN notation"
        position: list[str] = []
        for c in notation:
            if c == '/':
                pass
            elif c.isdigit():
                position += ['' for _ in range(int(c))]
            else:
                position.append(c)
        return(position)
    
    def get_notation(self) -> str: #move to dedicated class
        "Returns the FEN notation of the current positon"
        notation = ''
        for i, piece in enumerate(self.position):
            if (i)%8 == 0:
                notation += '/'
            if piece == '':
                if notation[-1].isdigit():
                    notation = notation[:-1] + str(int(notation[-1]) + 1)
                else:
                    notation += '1'
            else:
                notation += piece
        return notation[1:]

    def get_square(self, mouse_x: int, mouse_y: int) -> tuple[int, int]: #add flip
        "Returns the coordinates of the square relative to its position on the screen"
        xid = (mouse_x-self.x) // self.square_size
        yid = (mouse_y-self.y) // self.square_size
        return xid, yid

    def get_piece(self, board_x: int, board_y: int) -> str:
        "Returns the piece located in the given coordinates"
        if 0 <= board_x < 8 and 0 <= board_y < 8:
            return self.position[board_x + 8*board_y]
        return ''
    
    def process_left_click(self, mouse_x: int, mouse_y: int) -> None:
        "Handles user's lmb press"
        board_x, board_y = self.get_square(mouse_x, mouse_y)
        if not(0 <= board_x < 8 and 0 <= board_y < 8):
            return None
        if self.prev_pos == None:
            self.pick(board_x, board_y)
        elif self.promotion != None:
            self.pick_promotion(board_x, board_y)
            self.unpick()
        elif (board_x, board_y) == self.prev_pos:
            self.unpick()
        elif self.position_handler.is_move_possible(*self.prev_pos, board_x, board_y, self.higlighted_squares):
            if self.position_handler.ispromotion(board_y, self.get_piece(*self.prev_pos)):
                self.position_handler.set_piece(*self.prev_pos, '')
                self.promotion = (board_x, board_y)
                self.higlighted_squares = [self.promotion]
            else:
                self.move_piece(*self.prev_pos, board_x, board_y, available_squares=self.higlighted_squares)
                self.unpick()
        else:
            self.pick(board_x, board_y)
    
    def pick(self, board_x: int, board_y: int) -> None:
        self.prev_pos = (board_x, board_y)
        if self.higlight_moves:
            self.higlighted_squares = self.position_handler.get_highlights(board_x, board_y)

    def unpick(self) -> None:
        self.prev_pos = None
        self.higlighted_squares = None

    def pick_promotion(self, board_x: int, board_y: int) -> None:
        "Handles user's clicks on the screen during a pawn promotion"
        if self.promotion == None or self.prev_pos == None:
            raise ValueError("no pawn promotion is present")
        if self.promotion[1] == 0:
            if self.promotion[0] == board_x and (0 <= board_y < 4):
                self.move_piece(*self.prev_pos, *self.promotion, ['Q', 'N', 'R', 'B'][board_y], self.higlighted_squares)
            else:
                self.position_handler.set_piece(*self.prev_pos, 'P')
        elif self.promotion[1] == 7:
            if self.promotion[0] == board_x and (4 <= board_y < 8):
                self.move_piece(*self.prev_pos, *self.promotion, ['q', 'n', 'r', 'b'][7 - board_y], self.higlighted_squares)
            else:
                self.position_handler.set_piece(*self.prev_pos, 'p')
        self.promotion = None        
    
    def draw(self) -> None: #add flip
        "Draws board with pieces to the screen"
        self.draw_board()
        self.higlight()
        self.draw_pieces()
        self.draw_promotion_screen()

    def draw_board(self) -> None: #add flip
        "Draws the board to the screen"
        for board_y in range(0, 8):
            for board_x in range(0, 8):
                if (board_x % 2 == 0) ^ (board_y % 2 == 0):
                    pg.draw.rect(self.screen, 
                                 self.black_color, 
                                 pg.Rect(self.square_size * board_x + self.x, 
                                         self.square_size * board_y + self.y, 
                                         self.square_size, self.square_size))
                else:
                    pg.draw.rect(self.screen, 
                                 self.white_color, 
                                 pg.Rect(self.square_size * board_x + self.x, 
                                         self.square_size * board_y + self.y, 
                                         self.square_size, self.square_size))
        
    def draw_pieces(self) -> None: #add flip
        "Draws pieces to the screen"
        for i, piece in enumerate(self.position):
            if piece != '':
                self.screen.blit(self.piece_assets[piece], 
                                 (self.x + (i%8)*self.square_size, 
                                  self.y + (i//8)*self.square_size))

    def higlight(self) -> None: #add flip
        "Highlights all the squares that can be accessed by the picked piece"
        if self.higlighted_squares == None:
            return None
        for x, y in self.higlighted_squares:
            pg.draw.rect(self.screen, self.highlight_clor, 
                        pg.Rect(self.x + x * self.square_size, 
                                self.y + y * self.square_size, 
                                self.square_size, self.square_size))
    
    def draw_promotion_screen(self) -> None: #add flip
        if self.promotion == None:
            return None
        if self.promotion[1] == 0:
            pg.draw.rect(self.screen, (255, 255, 255), 
                            pg.Rect(self.x + self.promotion[0]*self.square_size, 
                                    self.y + self.promotion[1]*self.square_size, 
                                    self.square_size, 4*self.square_size))
            for y, piece in zip(range(self.promotion[1], self.promotion[1]+4, 1), ['Q', 'N', 'R', 'B']):
                self.screen.blit(self.piece_assets[piece], 
                                (self.x + self.promotion[0]*self.square_size, 
                                    self.y + y*self.square_size))
        elif self.promotion[1] == 7:
            pg.draw.rect(self.screen, (255, 255, 255), 
                            pg.Rect(self.x + self.promotion[0]*self.square_size, 
                                    self.y + (self.promotion[1] - 3)*self.square_size, 
                                    self.square_size, 4*self.square_size))
            for y, piece in zip(range(self.promotion[1], self.promotion[1]-4, -1), ['q', 'n', 'r', 'b']):
                self.screen.blit(self.piece_assets[piece], 
                                (self.x + self.promotion[0]*self.square_size, 
                                    self.y + y*self.square_size))

    def ischekmate(self) -> bool:
        "Returns True if position is a checkmate, False otherwise"
        return self.position_handler.ischeckmate()
    
    def isdraw(self) -> bool:
        "Returns True if position is a draw, False otherwise"
        return self.position_handler.isdraw()
    
    def move_piece(self, board_x1: int, board_y1: int, board_x2: int, board_y2: int, 
                   promote_to: str | None = None, available_squares: list[tuple[int, int]] | None = None) -> bool:
        "Moves the piece if it is posible. Returns True if moved successfully, False otherwise"
        if self.position_handler.move(board_x1, board_y1, board_x2, board_y2, promote_to, available_squares):
            self.history.append(self.get_notation())
            return True
        return False
    
    def reset(self) -> list[str]:
        "Returns the board to its originall state"
        out = self.history.copy()
        self.history.clear()
        self.position = self.get_position(self.init_FEN_position)
        self.position_handler.__init__(self.position)
        self.prev_pos = None
        self.higlighted_squares = None
        self.draw()
        return(out)
        
    class Position_handler:
        def __init__(self, board_position: list[str]):
            self.position = board_position
            self.white_to_move = True
            self.en_passant: tuple | None = None
            self.white_long_castle = True
            self.white_short_castle = True
            self.black_long_castle = True
            self.black_short_castle = True

        def get_piece(self, board_x: int, board_y: int) -> str:
            "Returns the piece given the coordinates"
            return self.position[board_x + 8*board_y]
        
        def get_location(self, piece: str) -> tuple[int, int]:
            "Return first occurring coordinate of the piece"
            ind = self.position.index(piece)
            return ind%8, ind//8
        
        def set_piece(self, board_x: int, board_y: int, piece: str = '') -> None:
            self.position[board_x + 8*board_y] = piece
        
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
            if self.position.count('') == 62:
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
            saved_position = self.position.copy() #saves the state of the game
            saved_states = self.en_passant, self.white_long_castle, self.white_short_castle, self.black_long_castle, self.black_short_castle
            self.raw_move(board_x1, board_y1, board_x2, board_y2) #makes a move
            if self.white_to_move:
                king_x, king_y = self.get_location('K')
            else:
                king_x, king_y = self.get_location('k')
            ischecked = self.isattacked(king_x, king_y) #checks if the king is attacked
            self.position.clear() #return position to its initial state
            self.position += saved_position
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