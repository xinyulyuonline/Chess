import pygame
import os
import time
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
history_font = pygame.font.Font(None, 30)


def _draw_player_times():
    pygame.draw.rect(screen, (45, 45, 45), (800, 0, 400, 800))

    def _to_minutes_seconds(total_seconds: int) -> tuple[int, int]:
        safe_seconds = max(0, total_seconds)
        return safe_seconds // 60, safe_seconds % 60

    elapsed_seconds = 0 if game.winner != 0 else int(time.time() - game.turn_start_time)

    if game.winner == 0:
        if game.cur_player == False and game.remaining_time_player1 - elapsed_seconds <= 0:
            game.remaining_time_player1 = 0
            game.winner = 2
            elapsed_seconds = 0
        elif game.cur_player == True and game.remaining_time_player2 - elapsed_seconds <= 0:
            game.remaining_time_player2 = 0
            game.winner = 1
            elapsed_seconds = 0

    black_seconds = max(0, game.remaining_time_player2)
    if game.cur_player:
        black_seconds = max(0, black_seconds - elapsed_seconds)
    black_minutes, black_remaining_seconds = _to_minutes_seconds(black_seconds)

    white_seconds = max(0, game.remaining_time_player1)
    if not game.cur_player:
        white_seconds = max(0, white_seconds - elapsed_seconds)
    white_minutes, white_remaining_seconds = _to_minutes_seconds(white_seconds)

    black_text = time_font.render(f"Black: {black_minutes:02d}:{black_remaining_seconds:02d}", True, (240, 240, 240))
    white_text = time_font.render(f"White: {white_minutes:02d}:{white_remaining_seconds:02d}", True, (240, 240, 240))
    screen.blit(white_text, (840, 30))
    screen.blit(black_text, (840, 740))


def _draw_step_history():
    title_text = history_font.render("Step History", True, (240, 240, 240))
    screen.blit(title_text, (840, 120))

    recent_steps = game.step_history[-20:]
    start_index = len(game.step_history) - len(recent_steps)
    for index, step in enumerate(recent_steps):
        from_pos, to_pos = step
        from_x, from_y = from_pos
        to_x, to_y = to_pos
        from_text = f"{from_x + 1}{chr(ord('a') + from_y)}"
        to_text = f"{to_x + 1}{chr(ord('a') + to_y)}"
        player_text = "White" if (start_index + index) % 2 == 0 else "Black"
        step_text = f"{player_text}: {from_text} - {to_text}"
        rendered_text = history_font.render(step_text, True, (240, 240, 240))
        screen.blit(rendered_text, (840, 150 + index * 28))
 
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
    sprite_selected = False
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

                if not sprite_selected:
                    selected_sprite = game.select_sprite(board_pos)
                    if selected_sprite:
                        sprite_selected = True
                        selected_pos = board_pos
                    else:
                        sprite_selected = False
                        selected_pos = None
                else:
                    if selected_sprite and game.move_sprite(board_pos, selected_sprite):
                        sprite_selected = False
                        selected_sprite = None
                        selected_pos = None
                    else:
                        selected_sprite = game.select_sprite(board_pos)
                        if selected_sprite:
                            sprite_selected = True
                            selected_pos = board_pos
                        else:
                            sprite_selected = False
                            selected_pos = None


        screen.blit(board, (0, 0))

        _init_chess_game()
        _draw_player_times()
        _draw_step_history()

        if sprite_selected and selected_pos is not None:
            pygame.draw.rect(screen, (92, 64, 32), (selected_pos[0]*square_size, selected_pos[1]*square_size, square_size, square_size), 5)

        pygame.display.flip()
        clock.tick(60)

def calculate_mouse_pos_to_board_pos(mouse_pos: tuple[int, int]) -> tuple[int, int]:
    x, y = mouse_pos
    board_x = x // square_size
    board_y = y // square_size
    return (board_x, board_y)