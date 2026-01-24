import pygame
import os
from data_model import Chess_Game
 
pygame.init()
width, height = 1200, 800
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()
 
square_size = 100
 
board = pygame.image.load(os.path.join(os.path.dirname(__file__), "Images", "chess_board.png"))
board = pygame.transform.scale(board, (800, 800))
 
game = Chess_Game()
board_state = game.new_game()
 
piece_files = {
    ("white", "King"): os.path.join(os.path.dirname(__file__), "Images", "king_white.png"),
    ("white", "Queen"): os.path.join(os.path.dirname(__file__), "Images", "queen_white.png"),
    ("white", "Tower"): os.path.join(os.path.dirname(__file__), "Images", "tower_white.png"),
    ("white", "Bishop"): os.path.join(os.path.dirname(__file__), "Images", "bishop_white.png"),
    ("white", "Horse"): os.path.join(os.path.dirname(__file__), "Images", "horse_white.png"),
    ("white", "Pawn"): os.path.join(os.path.dirname(__file__), "Images", "pawn_white.png"),
    ("black", "King"): os.path.join(os.path.dirname(__file__), "Images", "king_black.png"),
    ("black", "Queen"): os.path.join(os.path.dirname(__file__), "Images", "queen_black.png"),
    ("black", "Tower"): os.path.join(os.path.dirname(__file__), "Images", "tower_black.png"),
    ("black", "Bishop"): os.path.join(os.path.dirname(__file__), "Images", "bishop_black.png"),
    ("black", "Horse"): os.path.join(os.path.dirname(__file__), "Images", "horse_black.png"),
    ("black", "Pawn"): os.path.join(os.path.dirname(__file__), "Images", "pawn_black.png"),
}
 
piece_images = {
    key: pygame.transform.scale(pygame.image.load(path), (100, 100))
    for key, path in piece_files.items()
}
 
 
def run():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
 
        screen.blit(board, (0, 0))
 
        for y in range(8):
            for x in range(8):
                sprite = board_state[y][x]
                if sprite is None:
                    continue
                img = piece_images[(sprite.color, sprite.name)]
                screen.blit(img, (x * square_size, (7 - y) * square_size))
 
        pygame.display.flip()
        clock.tick(60)

def calculate_mouse_pos_to_board_pos(mouse_pos: tuple[int, int]) -> tuple[int, int]:
    x, y = mouse_pos
    board_x = x // square_size
    board_y = (y // square_size)
    return (board_x, board_y)