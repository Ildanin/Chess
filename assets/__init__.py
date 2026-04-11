from pygame import image
import os

assets_path = os.path.dirname(__file__)

BB = image.load(os.path.join(assets_path, "black_bishop.png"))
BK = image.load(os.path.join(assets_path, "black_king.png"))
BN = image.load(os.path.join(assets_path, "black_knight.png"))
BP = image.load(os.path.join(assets_path, "black_pawn.png"))
BQ = image.load(os.path.join(assets_path, "black_queen.png"))
BR = image.load(os.path.join(assets_path, "black_rook.png"))
WB = image.load(os.path.join(assets_path, "white_bishop.png"))
WK = image.load(os.path.join(assets_path, "white_king.png"))
WN = image.load(os.path.join(assets_path, "white_knight.png"))
WP = image.load(os.path.join(assets_path, "white_pawn.png"))
WQ = image.load(os.path.join(assets_path, "white_queen.png"))
WR = image.load(os.path.join(assets_path, "white_rook.png"))