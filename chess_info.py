from fastapi import FastAPI
from data_model import Chess_Game,Sprite_King, Sprite_Queen, Sprite_Tower,Sprite_Bishop, Sprite_Horse, Sprite_Pawn

app = FastAPI()


@app.get("/chess_names")
def read_root():
    return {
        "chess_names": ["King", "Queen", "Tower", "Bishop", "Horse", "Pawn"]
    }


@app.get("/{chess_name}/init_position")
def get_init_position(chess_name: str, color: str = "white"):

    valid_names = ["King", "Queen", "Tower", "Bishop", "Horse", "Pawn"]

    if chess_name not in valid_names:
        return {"error": "Chess name not found"}

    game = Chess_Game()
    board = game.new_game()

    positions = []

    for y in range(8):
        for x in range(8):
            sprite = board[y][x]
            if sprite and sprite.name == chess_name and sprite.color == color:
                positions.append((x + 1, y))

    return {
        "chess_name": chess_name,
        "color": color,
        "positions": positions
    }


@app.get("/{chess_name}/possible_moves")
def get_possible_moves(chess_name: str, color: str = "white"):

    sprite_classes = {
        "King": Sprite_King,
        "Queen": Sprite_Queen,
        "Tower": Sprite_Tower,
        "Bishop": Sprite_Bishop,
        "Horse": Sprite_Horse,
        "Pawn": Sprite_Pawn
    }

    if chess_name not in sprite_classes:
        return {"error": "Chess name not found"}

    game = Chess_Game()
    board = game.new_game()

    results = []

    for y in range(8):
        for x in range(8):
            sprite = board[y][x]
            if sprite and sprite.name == chess_name and sprite.color == color:

                moves = []
                for ty in range(8):
                    for tx in range(8):
                        test_sprite = sprite.copy()
                        if test_sprite.move((tx, ty)):
                            moves.append((tx + 1, ty))

                results.append({
                    "start_position": (x + 1, y),
                    "possible_moves": moves
                })

    return {
        "chess_name": chess_name,
        "color": color,
        "results": results
    }
