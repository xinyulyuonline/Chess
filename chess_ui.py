import pygame

from data_model import Chess_Game

pygame.init()
width, height = 800, 800
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()

square_size = 100

board = pygame.image.load("Images/chess_board.png")
board = pygame.transform.scale(board, (800, 800))

game = Chess_Game()
board_state = game.new_game()

piece_files = {
    ("white", "King"): "Images/king_white.png",
    ("white", "Queen"): "Images/queen_white.png",
    ("white", "Tower"): "Images/tower_white.png",
    ("white", "Bishop"): "Images/bishop_white.png",
    ("white", "Horse"): "Images/horse_white.png",
    ("white", "Pawn"): "Images/pawn_white.png",
    ("black", "King"): "Images/king_black.png",
    ("black", "Queen"): "Images/queen_black.png",
    ("black", "Tower"): "Images/tower_black.png",
    ("black", "Bishop"): "Images/bishop_black.png",
    ("black", "Horse"): "Images/horse_black.png",
    ("black", "Pawn"): "Images/pawn_black.png",
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

