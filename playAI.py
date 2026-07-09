from chessBoard import ChessBoard, BoardMove, BoardSquare
import pygame as pg
from config import WIN_WIDTH, WIN_HEIGHT, BOARD_X, BOARD_Y
from time import perf_counter
from random import randrange
from chessAI import load
from chessAI.data import position_encode_start, position_encode_target, torch
import numpy as np

screen = pg.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
clock = pg.Clock()
board = ChessBoard(screen, BOARD_X, BOARD_Y)
start_ai = load("start2.pt")
target_ai = load("target1.pt", False)

while True:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            exit()
        elif event.type == pg.MOUSEBUTTONDOWN:
            board.process_left_click(*pg.mouse.get_pos())
            board.draw()
            if not board.position.white_move:
                with torch.no_grad():
                    start_id = start_ai(torch.tensor(np.array([position_encode_start(board.position).numpy()]))).argmax()
                    target_id = target_ai(torch.tensor(np.array([position_encode_target(board.position, BoardSquare(start_id%8, start_id//8)).numpy()]))).argmax()
                board.show_move(BoardMove(BoardSquare(start_id%8, start_id//8), BoardSquare(target_id%8, target_id//8)))
        elif event.type == pg.KEYDOWN:
            key = event.key
            if key == pg.K_SPACE:
                board.reset()
    
    pg.display.flip()

    clock.tick(20)