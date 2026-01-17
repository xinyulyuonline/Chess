import pytest
from data_model import (
    Sprite_Horse,
    Sprite_Bishop,
    Sprite_King,
    Sprite_Queen,
    Sprite_Tower,
    Sprite_Pawn,
)

horse_test_data = [
    ((4, 4), (6, 5), True),
    ((4, 4), (5, 6), True),
    ((4, 4), (3, 2), True),
    ((4, 4), (5, 5), False),
    ((4, 4), (4, 6), False),
]

@pytest.mark.parametrize("start_pos, target_pos, expected", horse_test_data)
def test_horse_move(start_pos, target_pos, expected):
    horse = Sprite_Horse(cur_pos=start_pos)
    assert horse.move(target_pos) == expected



bishop_test_data = [
    ((4, 4), (6, 6), True),
    ((4, 4), (2, 2), True),
    ((4, 4), (7, 1), True),
    ((4, 4), (4, 6), False),
    ((4, 4), (5, 4), False),
]

@pytest.mark.parametrize("start_pos, target_pos, expected", bishop_test_data)
def test_bishop_move(start_pos, target_pos, expected):
    bishop = Sprite_Bishop(cur_pos=start_pos)
    assert bishop.move(target_pos) == expected



king_test_data = [
    ((4, 4), (5, 5), True),
    ((4, 4), (4, 5), True),
    ((4, 4), (3, 4), True),
    ((4, 4), (6, 4), False),
    ((4, 4), (4, 7), False),
]

@pytest.mark.parametrize("start_pos, target_pos, expected", king_test_data)
def test_king_move(start_pos, target_pos, expected):
    king = Sprite_King(cur_pos=start_pos)
    assert king.move(target_pos) == expected



queen_test_data = [
    ((4, 4), (4, 7), True),
    ((4, 4), (7, 4), True),
    ((4, 4), (7, 7), True),
    ((4, 4), (1, 7), True),
    ((4, 4), (5, 6), False),
]

@pytest.mark.parametrize("start_pos, target_pos, expected", queen_test_data)
def test_queen_move(start_pos, target_pos, expected):
    queen = Sprite_Queen(cur_pos=start_pos)
    assert queen.move(target_pos) == expected


tower_test_data = [
    ((4, 4), (4, 0), True),
    ((4, 4), (4, 7), True),
    ((4, 4), (0, 4), True),
    ((4, 4), (7, 4), True),
    ((4, 4), (6, 6), False),
]

@pytest.mark.parametrize("start_pos, target_pos, expected", tower_test_data)
def test_tower_move(start_pos, target_pos, expected):
    tower = Sprite_Tower(cur_pos=start_pos)
    assert tower.move(target_pos) == expected


pawn_test_data = [
    ((4, 1), (4, 2), True),
    ((4, 1), (4, 3), False),
    ((4, 1), (5, 2), False),
    ((4, 6), (4, 5), True),
    ((4, 6), (4, 4), False),
]

@pytest.mark.parametrize("start_pos, target_pos, expected", pawn_test_data)
def test_pawn_move(start_pos, target_pos, expected):

    color = "white" if start_pos[1] <= 1 else "black"

    pawn = Sprite_Pawn(cur_pos=start_pos, color=color)
    assert pawn.move(target_pos) == expected