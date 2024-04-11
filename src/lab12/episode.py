''' 
Lab 12: Beginnings of Reinforcement Learning

Create a function called run_episode that takes in two players
and runs a single episode of combat between them. 
As per RL conventions, the function should return a list of tuples
of the form (observation/state, action, reward) for each turn in the episode.
Note that observation/state is a tuple of the form (player1_health, player2_health).
Action is simply the weapon selected by the player.
Reward is the reward for the player for that turn.

Monte-Carlo Method (next week's lab)
Initialize for all s within S, a within A(s):
    Q(s,a) <- arbitrary
    pi(s) <- arbitrary
    Returns(s,a) <- empty list

Repeat forever:
    (a) Generate an episode using exploring starts and pi
    (b) For each pair s,a appearing in the episode:
        R <- reutrn following the first occurence of s,a
        Append R to Returns(s,a)
        Q(s,a) <- average(Returns(s,a))
    (c) For each s in the episode

'''
import sys
from pathlib import Path

sys.path.append(str((Path(__file__) / ".." / ".." / "..").resolve().absolute()))

from src.lab11.pygame_combat import run_turn
from src.lab11.turn_combat import Combat


def run_episode(playerOne, playerTwo):
    currentGame = Combat()
    endResult = []
    temp = run_turn(currentGame, playerOne, playerTwo)
    endResult.append(temp)
    while 2 > 1:
        if(temp[0][0] == 0 or temp[0][1] == 0):
            return endResult
        else:
            temp = run_turn(currentGame, playerOne, playerTwo)
            endResult.append(temp)
    return endResult