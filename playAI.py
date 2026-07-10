from chessBoard import ChessBoard
import pygame as pg
from config import WIN_WIDTH, WIN_HEIGHT, BOARD_X, BOARD_Y
from chessAI import load_chessAI

screen = pg.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
clock = pg.Clock()
board = ChessBoard(screen, BOARD_X, BOARD_Y)
chessAI = load_chessAI("start_opn.pt", "target_opn.pt", 
                       "start_mid.pt", "target_mid.pt", 
                       "start_end.pt", "target_end.pt")

while True:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            exit()
        elif event.type == pg.MOUSEBUTTONDOWN:
            board.process_left_click(*pg.mouse.get_pos())
            board.draw()
            if not board.position.white_move:
                move = chessAI.predict(board.position)
                print(board.position.fullmove_number)
                board.show_move(move)
        elif event.type == pg.KEYDOWN:
            key = event.key
            if key == pg.K_SPACE:
                board.reset()
    
    pg.display.flip()

    clock.tick(20)