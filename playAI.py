from chessBoard import ChessBoard
import pygame as pg
from chessAI import load_chessAI
from config import WIN_WIDTH, WIN_HEIGHT, BOARD_X, BOARD_Y
from time import perf_counter
from random import randrange

screen = pg.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
clock = pg.Clock()
board = ChessBoard(screen, BOARD_X, BOARD_Y)
ai = load_chessAI("ChessAI_A1.txt")

while True:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            exit()
        elif event.type == pg.MOUSEBUTTONDOWN:
            board.process_left_click(*pg.mouse.get_pos())
            board.draw()
            if not board.position.white_move:
                move = ai.move(board.position, True)
                board.show_move(move)
        elif event.type == pg.KEYDOWN:
            key = event.key
            if key == pg.K_SPACE:
                board.reset()
                pass
    
    '''print(board.position.history[-1])
    legal_moves = list(board.position.get_legal_moves())
    if board.position.move(legal_moves[randrange(0, len(legal_moves))]):
        board.draw()
    if board.ischekmate():
        print('Checkmate')
        exit()
    elif board.position.isdraw():
        print('Draw')
        exit()'''
    
    pg.display.flip()

    clock.tick(20)