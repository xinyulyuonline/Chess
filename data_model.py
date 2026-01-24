from pydantic import BaseModel
 
 
 
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
    def move(self, target_pos: tuple):
        cur_x, cur_y = self.cur_pos
        target_x, target_y = target_pos
        if cur_x == target_x and abs(cur_y - target_y) == 1:
            self.cur_pos = target_pos
            return True
        else:
            return False
 
class Chess_Game(BaseModel):
    winner: int = 0 # 0 for nobody, 1 for white winner, and 2 for black winner
    gaming_time: int = 0 # unit is second
    board: list[list[Chess_Sprite]] = []
    cur_player: bool = False # False for white and True for black
    turn: int = 0
    player_names: list[str, str] = []
    remaining_time_player1: int = 0
    remaining_time_player2: int = 0
    selected_sprite: Chess_Sprite | None = None
    step_history: list[tuple] = []
 
 
    def new_game(self) -> list[list[Chess_Sprite]]:
        self.board = []
 
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
        """
        self.selected_sprite = self.board[pos[1]][pos[0]]
        return self.selected_sprite


    def move_sprite(self, target_pos: tuple, sprite: Chess_Sprite) -> bool:
        """
        move the selected sprite to target position if the move is valid
        """
        cur_x, cur_y = sprite.cur_pos
        target_x, target_y = target_pos
 
 
        if sprite.move(target_pos):
            self.board[cur_y][cur_x] = None
            self.board[target_y][target_x] = sprite
            return True
        else:
            return False