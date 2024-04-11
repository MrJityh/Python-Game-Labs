import random
import pygame
from lab11.turn_combat import CombatPlayer

""" Create PyGameAIPlayer class here"""


class PyGameAIPlayer:
    def __init__(self) -> None:
        self.current_city = 0
        pass

    def selectAction(self, state):
        self.current_city = (self.current_city + 1) % 10
        return ord(str(self.current_city))


""" Create PyGameAICombatPlayer class here"""


class PyGameAICombatPlayer(CombatPlayer):
    def __init__(self, name) -> None:
        super().__init__(name)

    def weapon_selecting_strategy(self):
        self.weapon = random.randint(0,2)
        return self.weapon
