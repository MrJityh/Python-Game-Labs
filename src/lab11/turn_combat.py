# From https://codereview.stackexchange.com/questions/237601/simple-python-turn-based-battle-game
import random
import pygame
import sys
from pathlib import Path
from typing import List, Tuple

sys.path.append(str((Path(__file__) / ".." / "..").resolve().absolute()))
from lab4.rock_paper_scissor import Player

weapons: List[str] = ["Sword", "Arrow", "Fire"]


class CombatPlayer(Player):
    def __init__(self, name: str) -> None:
        super().__init__(name)
        self.name = name
        self.health = 100
        self.weapon = 0
        self.current_env_state = None

    def selectAction(self, percept: Tuple) -> None:
        """
        > The function takes in the opponent's last move, updates the player's history of opponent's moves,
         and then updates the player's history of their own moves

        :param percept: Tuple of (environment state, opponent's last move)
        """
        env_state = percept
        # ** Previous round update **
        if percept is not None:
            self.current_env_state = env_state

        # ** Current round update **
        self._action = self.weapon_selecting_strategy()
        self.weapon = self._action
        self.my_choices.append(self.action)

    def damage(self) -> None:
        points = 10
        self.health -= points

    def weapon_selecting_strategy(self) -> int:
        choice = input("Choose your weapon s-Sword, a-Arrow or f-Fire:  ")
        choice = {"s": 1, "a": 2, "f": 3}[choice]
        self.weapon = choice - 1
        return self.weapon


class ComputerCombatPlayer(CombatPlayer):
    def __init__(self, name: str) -> None:
        super().__init__(name)

    def weapon_selecting_strategy(self) -> int:
        choice = random.randint(1, 3)
        self.weapon = choice - 1
        return self.weapon


class Combat:
    def __init__(self) -> None:
        self.gameOver = False
        self.round = 0

    def newRound(self) -> None:
        self.round += 1
        print("\n***   Round: %d   ***\n" % (self.round))

    # Check if either or both Players is below zero health
    def checkWin(self, player: CombatPlayer, opponent: CombatPlayer) -> None:
        if player.health < 1 and opponent.health > 0:
            self.gameOver = True
            print("You Lose")
            return -1
        elif opponent.health < 1 and player.health > 0:
            self.gameOver = True
            print("You Win")
            return 1
        elif player.health < 1 and opponent.health < 1:
            self.gameOver = True
            print("*** Draw ***")
            return 0
        return 0

    def displayResult(self, player: CombatPlayer, opponent: CombatPlayer) -> None:
        print(
            "%s used a %s, %s used a %s \n"
            % (
                player.name,
                weapons[player.weapon],
                opponent.name,
                weapons[opponent.weapon],
            )
        )
        print("%s caused damage to %s\n" % (player.name, opponent.name))

    def takeTurn(self, player: CombatPlayer, opponent: CombatPlayer) -> None:

        # Decision Array
        #
        #           Sword |  Arrow |  Fire
        #           ______|________|_______
        # Sword:    False |  False  |  True
        # Arrow:    True  |  True |  False
        # Fire :    False  |  True  |  True

        decisionArray = [  # Sword   Arrow   Fire
            [False, False, True],  # Sword
            [True, True, False],  # Arrow
            [False, True, True],  # Fire
        ]
        print(
            f"\n{player.name} used {weapons[player.weapon]}, {opponent.name} used {weapons[opponent.weapon]}"
        )
        if decisionArray[player.weapon][opponent.weapon]:
            opponent.damage()

        if decisionArray[opponent.weapon][player.weapon]:
            player.damage()


def run_console_combat():
    # Setup Combat Objects
    currentGame = Combat()
    human = Player("Mark")
    computer = ComputerCombatPlayer("Computer")

    players = [human, computer]

    # Main Combat Loop
    while not currentGame.gameOver:
        for player in players:
            player.selectWeapon()
        currentGame.newRound()
        currentGame.takeTurn(human, computer)
        print("%s's health = %d" % (human.name, human.health))
        print("%s's health = %d" % (computer.name, computer.health))
        currentGame.checkWin(human, computer)
