# From https://codereview.stackexchange.com/questions/237601/simple-python-turn-based-battle-game
import random
from player import Player


weapons = ["Rock", "Paper", "Scissor"]

def console_weapon_select():
    """
    It takes a list of weapons, prints them out, and returns the user's choice
    :return: The weapon that the user has chosen.
    """
    weapons_list = [f'{i+1}-{w}' for i, w in enumerate(weapons)]
    choice = int(input(f'Choose your weapon {", ".join(weapons_list)}:  '))
    weapon = choice - 1
    return weapon

def random_weapon_select():
    return random.randint(0, 2)

    

# Child class of player with override methods for weapon
class ComputerPlayer(Player):
    def __init__(self, name, computer_agent=-1):
        super().__init__(name)
        if computer_agent == -1:
            self.agent = random.randint(0, 2)
        else:
            self.agent = computer_agent
        self.initial_weapon = random_weapon_select()
        self.print_agent()

    def print_agent(self):
        if self.agent == 0:
            print("Agent: Single")
        elif self.agent == 1:
            print("Agent: Switch")
        elif self.agent == 2:
            print("Agent: Mimic")

    def agent_single(self):
        return self.initial_weapon

    def agent_switch(self):
        """
        > The agent will switch to a random weapon every 10 turns
        :return: The initial weapon is being returned.
        """
        if len(self.opponent_choices)%10 == 0:
            self.initial_weapon = random_weapon_select()
        return self.initial_weapon

    def agent_mimic(self):
        """
        > The agent will mimic the opponent's last choice
        :return: The last choice of the opponent.
        """
        if len(self.opponent_choices) == 0:
            return self.initial_weapon

        return self.opponent_choices[-1]

    def weapon_selecting_strategy(self):
        if self.agent == 0:
            return self.agent_single()
        if self.agent == 1:
            return self.agent_switch()
        if self.agent == 2:
            return self.agent_mimic()

        raise ValueError("Agent not found")


class Game:
    def __init__(self, players):
        self.gameOver = False
        self.round = 0
        self.players = players
        self.players_tally = {player:0 for player in players}

    def newRound(self):
        self.round += 1
        print(f'\n***   Round: {self.round}   ***\n')  

    def updateWin(self, result):
        if result != 0:
            self.players_tally[result] += 1

    def displayResult(self, player, opponent, winner):
        print(f'{player.name} used a {weapons[player.action]}, {opponent.name} used a {weapons[opponent.action]}')
        if winner == 0:
            print("*** Draw ***")
        else:
            print(f'{weapons[winner.action]} beats {weapons[player.action if opponent == winner else opponent.action]}')

    def takeTurn(self, player, opponent):

        # Decision Array
        #
        #             Rock|  Paper |  Scissor
        #           ______|________|_______
        # Rock:       0   |    2   |   1
        # Paper:      1   |    0   |   2   
        # Scissor:    2   |    1   |   0

        decisionArray = [[0, 2, 1], [1, 0, 2], [2, 1, 0]]
        winner = 0
        if decisionArray[player.action][opponent.action] == 1:
            winner = player
        elif decisionArray[player.action][opponent.action] == 2:
            winner = opponent
        elif decisionArray[player.action][opponent.action] == 0:
            winner = 0
        self.displayResult(player, opponent, winner)
        return winner


# Setup Game Objects
def run_game(player: Player, n_rounds=3, computer_agent=-1):
    """
    > The function `run_game` takes in an agent, number of rounds to play and a computer agent, 
    and plays a game of rock-paper-scissors with them for the specified number of rounds.
    
    :param player: The player you want to play against the computer
    :param n_rounds: The number of rounds to play, defaults to 3 (optional)
    :param computer_agent: The agent that the computer will use, defaults to -1 meaning a randomly selected agent (optional)
    """
    percept = [None, None] 
    computer = ComputerPlayer("Computer", computer_agent)

    players = [player, computer]
    currentGame = Game(players)

    # Main Game Loop
    for _ in range(n_rounds):
        currentGame.newRound()
        for a_player, last_opp_move in zip(players, percept):
            a_player.selectAction(percept=last_opp_move)
        currentGame.updateWin(currentGame.takeTurn(*players))
        percept = [players[1].action, players[0].action]
        print(f'Score: {"-".join([str(score) for _, score in currentGame.players_tally.items()])}')


    # Display Results
    print("\n***   Game Over   ***\n")
    computer.print_agent()
    for a_player, score in currentGame.players_tally.items():
        print(f'{a_player.name} won {score} rounds')

    return currentGame.players_tally.items()
    

if __name__ == '__main__':
    human = Player("Mark", strategy=console_weapon_select)
    run_game(human)
