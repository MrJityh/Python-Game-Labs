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

from src.lab11.pygame_combat import (
    Combat,
    PyGameAICombatPlayer,
    PyGameComputerCombatPlayer,
    run_turn,
)


def run_turn(currentGame, player, opponent):
    players = [player, opponent]
    states = list(reversed([(player.health, player.weapon) for player in players]))

    for current_player, state in zip(players, states):
        current_player.selectAction(state)

    currentGame.newRound()
    currentGame.takeTurn(player, opponent)

    observation = (player.health, opponent.health)
    action = player.weapon
    reward = currentGame.checkWin(player, opponent)

    return observation, action, reward


def run_episode(player1, player2):
    currentGame = Combat()
    episode_data = []

    while not currentGame.gameOver:
        observation, action, reward = run_turn(currentGame, player1, player2)
        episode_data.append((observation, action, reward))

    return episode_data


if __name__ == "__main__":
    player1 = PyGameAICombatPlayer("Legolas")
    player2 = PyGameComputerCombatPlayer("Computer")

    print(run_episode(player1, player2))