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
board_state = []



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

time_font = pygame.font.Font(None, 48)


def _draw_player_times():
    black_seconds = max(0, game.remaining_time_player2)
    black_minutes = black_seconds // 60
    black_remaining_seconds = black_seconds % 60

    white_seconds = max(0, game.remaining_time_player1)
    white_minutes = white_seconds // 60
    white_remaining_seconds = white_seconds % 60

    black_text = time_font.render(f"Black: {black_minutes:02d}:{black_remaining_seconds:02d}", True, (20, 20, 20))
    white_text = time_font.render(f"White: {white_minutes:02d}:{white_remaining_seconds:02d}", True, (20, 20, 20))
    screen.blit(black_text, (840, 30))
    screen.blit(white_text, (840, 740))
 
def _init_chess_game(reset: bool = False):
    """Visualize the position of chess sprites on the board.

    If reset=True, start a new game first. Otherwise, just draw the current state.
    """
    global game, board_state
    if reset:
        game = Chess_Game()
        board_state = game.new_game()
    else:
        board_state = game.board

    for y in range(8):
        for x in range(8):
            sprite = board_state[y][x]
            if sprite is None:
                continue
            img = piece_images[(sprite.color, sprite.name)]
            screen.blit(img, (x * square_size, y * square_size))


def run():
    sprite_Selected = False
    selected_sprite = None
    selected_pos = None

    _init_chess_game(reset=True)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                board_pos = calculate_mouse_pos_to_board_pos(mouse_pos)
                if board_pos[0] not in range(8) or board_pos[1] not in range(8):
                    continue

                if not sprite_Selected:
                    selected_sprite = game.select_sprite(board_pos)
                    if selected_sprite:
                        sprite_Selected = True
                        selected_pos = board_pos
                    else:
                        sprite_Selected = False
                        selected_pos = None
                else:
                    if selected_sprite and game.move_sprite(board_pos, selected_sprite):
                        game.step_history.append((selected_pos, board_pos))
                        sprite_Selected = False
                        selected_sprite = None
                        selected_pos = None
                    else:
                        selected_sprite = game.select_sprite(board_pos)
                        if selected_sprite:
                            sprite_Selected = True
                            selected_pos = board_pos
                        else:
                            sprite_Selected = False
                            selected_pos = None


        screen.blit(board, (0, 0))

        _init_chess_game()
        _draw_player_times()

        if sprite_Selected and selected_pos is not None:
            pygame.draw.rect(screen, (92, 64, 32), (selected_pos[0]*square_size, selected_pos[1]*square_size, square_size, square_size), 5)

        pygame.display.flip()
        clock.tick(60)

def calculate_mouse_pos_to_board_pos(mouse_pos: tuple[int, int]) -> tuple[int, int]:
    x, y = mouse_pos
    board_x = x // square_size
    board_y = y // square_size
    return (board_x, board_y)