from pydantic import BaseModel
import time
 
 
 
class Chess_Sprite(BaseModel):
    color: str = "white" # or "black"
    cur_pos: tuple = (0,0) # possible values x in range(8) and y in range(8)
    next_possible_pos: list[tuple] = []
    name: str = "King" # possible values: ["Tower", "Queen", "Horse", "Bishop", "Pawn"]
    status: bool = True
 
 
 
    def move(self, target_pos: tuple) -> bool:
        pass
 
 
 
class Sprite_King(Chess_Sprite):
   
    def move(self, target_pos: tuple):
        # rule check of king
        cur_x, cur_y = self.cur_pos
        target_x, target_y = target_pos
        if abs(cur_x - target_x) <= 1 and abs(cur_y - target_y) <= 1 and (cur_x != target_x or cur_y != target_y) and target_x in range(8) and target_y in range(8):
            self.cur_pos = target_pos
            return True
        else:
            return False
 
class Sprite_Queen(Chess_Sprite):
 
    def move(self, target_pos: tuple):
        cur_x, cur_y = self.cur_pos
        target_x, target_y = target_pos
 
        if (cur_x == target_x or cur_y == target_y or abs(cur_x - target_x) == abs(cur_y - target_y)) and (cur_x != target_x or cur_y != target_y) and target_x in range(8) and target_y in range(8):
            self.cur_pos = target_pos
            return True
        else:
            return False
 
class Sprite_Tower(Chess_Sprite):
 
    def move(self, target_pos: tuple):
        cur_x, cur_y = self.cur_pos
        target_x, target_y = target_pos
 
        if(cur_x == target_x and cur_y != target_y or cur_x != target_x and cur_y == target_y) and target_x in range(8) and target_y in range(8):
            self.cur_pos = target_pos
            return True
        else:
            return False
 
class Sprite_Bishop(Chess_Sprite):
 
    def move(self, target_pos: tuple):
        cur_x, cur_y = self.cur_pos
        target_x, target_y = target_pos
 
        if abs(cur_x - target_x) == abs(cur_y - target_y) and (cur_x != target_x or cur_y != target_y) and target_x in range(8) and target_y in range(8):
            self.cur_pos = target_pos
            return True
        else:
            return False
       
class Sprite_Horse(Chess_Sprite):
 
    def move(self, target_pos: tuple):
        cur_x, cur_y = self.cur_pos
        target_x, target_y = target_pos
        if (abs(cur_x - target_x) == 2 and abs(cur_y - target_y) == 1 or abs(cur_x - target_x) == 1 and abs(cur_y - target_y) == 2) and target_x in range(8) and target_y in range(8):
            self.cur_pos = target_pos
            return True
        else:
            return False
   
class Sprite_Pawn(Chess_Sprite):
    def move(self, target_pos: tuple, target_sprite: Chess_Sprite | None = None, middle_square_empty: bool = True):
        cur_x, cur_y = self.cur_pos
        target_x, target_y = target_pos
        direction = 1 if self.color == "white" else -1
        start_row = 1 if self.color == "white" else 6
        horizontal_distance = target_x - cur_x
        vertical_distance = target_y - cur_y

        if target_x not in range(8) or target_y not in range(8):
            return False

        if horizontal_distance == 0 and vertical_distance == direction and target_sprite is None:
            self.cur_pos = target_pos
            return True
        elif horizontal_distance == 0 and vertical_distance == 2 * direction and cur_y == start_row and target_sprite is None and middle_square_empty:
            self.cur_pos = target_pos
            return True
        elif abs(horizontal_distance) == 1 and vertical_distance == direction and target_sprite is not None and target_sprite.color != self.color:
            self.cur_pos = target_pos
            return True
        else:
            return False
 
class Chess_Game(BaseModel):
    winner: int = 0 # 0 for nobody, 1 for white winner, and 2 for black winner
    gaming_time: int = 0 # unit is second
    board: list[list[Chess_Sprite]] = []
    cur_player: bool = False # False for white and True for black
    #turn: int = 0
    #player_names: list[str, str] = []
    remaining_time_player1: int = 600 # unit is second
    remaining_time_player2: int = 600 # unit is second
    turn_start_time: float = 0.0
    selected_sprite: Chess_Sprite | None = None
    step_history: list[tuple] = []
 
 
    def new_game(self) -> list[list[Chess_Sprite]]:
        self.board = []
        self.step_history.clear()
        self.cur_player = False
        self.remaining_time_player1 = 600
        self.remaining_time_player2 = 600
        self.turn_start_time = time.time()

        for y in range(8):
            row = []
            for x in range(8):
 
                if y == 0:
                    if x == 0 or x == 7:
                        row.append(Sprite_Tower(cur_pos=(x, y), color="white", name="Tower"))
                    elif x == 1 or x == 6:
                        row.append(Sprite_Horse(cur_pos=(x, y), color="white", name="Horse"))
                    elif x == 2 or x == 5:
                        row.append(Sprite_Bishop(cur_pos=(x, y), color="white", name="Bishop"))
                    elif x == 3:
                        row.append(Sprite_Queen(cur_pos=(x, y), color="white", name="Queen"))
                    elif x == 4:
                        row.append(Sprite_King(cur_pos=(x, y), color="white", name="King"))
 
                elif y == 1:
                    row.append(Sprite_Pawn(cur_pos=(x, y), color="white", name="Pawn"))
 
                elif y == 6:
                    row.append(Sprite_Pawn(cur_pos=(x, y), color="black", name="Pawn"))
 
                elif y == 7:
                    if x == 0 or x == 7:
                        row.append(Sprite_Tower(cur_pos=(x, y), color="black", name="Tower"))
                    elif x == 1 or x == 6:
                        row.append(Sprite_Horse(cur_pos=(x, y), color="black", name="Horse"))
                    elif x == 2 or x == 5:
                        row.append(Sprite_Bishop(cur_pos=(x, y), color="black", name="Bishop"))
                    elif x == 3:
                        row.append(Sprite_Queen(cur_pos=(x, y), color="black", name="Queen"))
                    elif x == 4:
                        row.append(Sprite_King(cur_pos=(x, y), color="black", name="King"))
 
                else:
                    row.append(None)
 
            self.board.append(row)
 
        return self.board
    
 
    def select_sprite(self, pos: tuple[int, int]) -> Chess_Sprite | None:
        """
        pos is a tuple of (x, y) coordinates on the board, range of x and y is 0 to 7

        after selecting:
        TODO: move sprite or castling if the move is valid
 


        """
        self.selected_sprite = self.board[pos[1]][pos[0]]
        return self.selected_sprite


    def move_sprite(self, target_pos: tuple, sprite: Chess_Sprite) -> bool:
        """
        move the selected sprite to target position if the move is valid

        before moving, check:
        1. if it's the correct player's turn
        2. if the target position is occupied
            - if occupied by own piece, invalid move
            - if occupied by opponent's piece, capture the piece
        after moving, do the following actions:
        1. after moving, update the board state
        2. change the current player
        3. calculate remaining time for each player
        4. update the step history
        5. check if target is occupied by one piece of opponent, then capture it 
            - if the captured piece is king, update winner status
        6. TODO: check if pawn reaches the other side, then promote it to queen
        """
        cur_x, cur_y = sprite.cur_pos
        target_x, target_y = target_pos

        if self.winner != 0:
            return False

        elapsed_time = int(time.time() - self.turn_start_time)
        if self.cur_player == False and self.remaining_time_player1 - elapsed_time <= 0:
            self.remaining_time_player1 = 0
            self.winner = 2
            return False
        if self.cur_player == True and self.remaining_time_player2 - elapsed_time <= 0:
            self.remaining_time_player2 = 0
            self.winner = 1
            return False

        if (self.cur_player == False and sprite.color != "white") or (self.cur_player == True and sprite.color != "black"):
            return False

        target_sprite = self.board[target_y][target_x]

        if isinstance(sprite, Sprite_King) and isinstance(target_sprite, Sprite_Tower) and target_sprite.color == sprite.color:
            if self.castling(sprite.cur_pos, target_pos):
                if self.cur_player == False:
                    self.remaining_time_player1 = max(0, self.remaining_time_player1 - elapsed_time)
                else:
                    self.remaining_time_player2 = max(0, self.remaining_time_player2 - elapsed_time)
                self.cur_player = not self.cur_player
                self.turn_start_time = time.time()
                return True
            return False

        if target_sprite is not None and target_sprite.color == sprite.color:
            return False
        middle_square_empty = True
        if isinstance(sprite, Sprite_Pawn):
            if cur_x == target_x and abs(target_y - cur_y) == 2:
                direction = 1 if sprite.color == "white" else -1
                middle_y = cur_y + direction
                if middle_y not in range(8):
                    middle_square_empty = False
                else:
                    middle_square_empty = self.board[middle_y][cur_x] is None

        is_valid_move = sprite.move(target_pos, target_sprite, middle_square_empty) if isinstance(sprite, Sprite_Pawn) else sprite.move(target_pos)

        if is_valid_move:
            captured_sprite = target_sprite if target_sprite is not None and target_sprite.color != sprite.color else None
            if captured_sprite is not None:
                captured_sprite.status = False
                if captured_sprite.name == "King":
                    self.winner = 1 if sprite.color == "white" else 2

            if self.cur_player == False:
                self.remaining_time_player1 = max(0, self.remaining_time_player1 - elapsed_time)
            else:
                self.remaining_time_player2 = max(0, self.remaining_time_player2 - elapsed_time)

            self.board[cur_y][cur_x] = None
            self.board[target_y][target_x] = sprite
            self.step_history.append(((cur_x, cur_y), (target_x, target_y)))
            self.cur_player = not self.cur_player
            self.turn_start_time = time.time()
            return True
        else:
            return False
        
    def castling(self, king_pos: tuple, tower_pos: tuple) -> bool:
        king_x, king_y = king_pos
        tower_x, tower_y = tower_pos

        if king_x not in range(8) or king_y not in range(8) or tower_x not in range(8) or tower_y not in range(8):
            return False
        if king_y != tower_y:
            return False

        king = self.board[king_y][king_x]
        tower = self.board[tower_y][tower_x]

        if not isinstance(king, Sprite_King) or not isinstance(tower, Sprite_Tower):
            return False
        if king.color != tower.color:
            return False

        king_has_moved = any(from_pos == king_pos for from_pos, _ in self.step_history)
        tower_has_moved = any(from_pos == tower_pos for from_pos, _ in self.step_history)
        if king_has_moved or tower_has_moved:
            return False

        step = 1 if tower_x > king_x else -1
        for x in range(king_x + step, tower_x, step):
            if self.board[king_y][x] is not None:
                return False

        new_king_x = king_x + 2 * step
        new_tower_x = new_king_x - step
        if new_king_x not in range(8) or new_tower_x not in range(8):
            return False

        self.board[king_y][king_x] = None
        self.board[tower_y][tower_x] = None

        king.cur_pos = (new_king_x, king_y)
        tower.cur_pos = (new_tower_x, tower_y)

        self.board[king_y][new_king_x] = king
        self.board[tower_y][new_tower_x] = tower

        self.step_history.append((king_pos, (new_king_x, king_y)))
        self.step_history.append((tower_pos, (new_tower_x, tower_y)))
        return True