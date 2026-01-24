def berechne_power(input: int, exponent: int) -> int:
    if exponent < 0:
        raise ValueError("Expontent darf nicht kleiner als 0 sein!!")
    if exponent == 0:
        return 1
    else:
        result = 1
        for i in range(exponent):
            result = result * input

        return result


def test_berechne_power_2_4():
    assert berechne_power(2, 4) == 16


def test_berechne_power_2_0():
    assert berechne_power(2, 0) == 1


def test_berechne_power_2_1():
    assert berechne_power(2, 1) == 2


import pytest


@pytest.mark.xfail(raises=ValueError)
def test_berechne_power_error():
    berechne_power(2, -1)


#### test vom Chess King ###
from data_model import Sprite_King

## Testdaten für Sprite_King: (start_pos, target_pos, expectation)

test_data_king = [
    ((1, 1), (2, 2), True),
    ((2, 2), (1, 1), True),
    ((4, 4), (5, 5), True),
    ((0, 0), (1, 1), True),
    ((7, 7), (6, 6), True),
    ((3, 3), (3, 4), True),
    ((3, 3), (4, 3), True),
    ((5, 5), (5, 6), True),
    ((5, 5), (4, 5), True),
    ((1, 1), (3, 3), False),
    ((1, 1), (1, 3), False),
    ((1, 1), (1, 2), True),
    ((1, 1), (-1, 0), False),
    ((2, 2), (2, 1), True),
    ((6, 6), (7, 5), True),
]


@pytest.mark.parametrize("start_pos, target_pos, expectation", test_data_king)
def test_move_king(start_pos, target_pos, expectation):
    my_king = Sprite_King(cur_pos=start_pos)
    assert my_king.move(target_pos) == expectation


def test_calculate_mouse_pos_to_board_pos():
    from chess_ui import calculate_mouse_pos_to_board_pos

    assert calculate_mouse_pos_to_board_pos((0, 0)) == (0, 0)
    assert calculate_mouse_pos_to_board_pos((100, 100)) == (1, 1)
    assert calculate_mouse_pos_to_board_pos((799, 799)) == (7, 7)
    assert calculate_mouse_pos_to_board_pos((450, 350)) == (4, 3)