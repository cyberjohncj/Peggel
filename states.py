from enum import Enum

### Game States
class GameState(Enum):
    MENU = 0
    PLAYING = 1
    LEVEL_EDITING = 2

class MenuState(Enum):
    MAIN = 0
    LEVEL_SELECT = 1
    EDIT_SELECT = 2
    POWERUP_SELECT = 3
    SETTINGS = 4
    CREDITS = 5

class PlayState(Enum):
    SPAWNING_PEGS = 0
    AIMING = 1
    BALL_DROPPING = 2
    ADJUSTING_SCORE = 3
    GAME_OVER = 4

### Object States
class BallState(Enum):
    SHOT = 0
    ACTIVE = 1

class PegState(Enum):
    WAITING_TO_SPAWN = 0
    SPAWNING = 1
    ACTIVE = 2
    DESPAWNING = 3
    REMOVED = 4

game_state = GameState.MENU
menu_state = MenuState.MAIN
play_state = PlayState.SPAWNING_PEGS