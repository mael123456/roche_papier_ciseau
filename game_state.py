"""
programme fait par mael chassin de kergommeaux
goupe 123
description : jeu de roche papier ciseau
"""

from enum import Enum


class GameState(Enum):
    ROUND_DONE = 0
    GAME_OVER = 1
    NOT_STARTED = 2
    ROUND_ACTIVE = 3
