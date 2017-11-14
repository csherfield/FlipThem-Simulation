from game import Game
from system import System
import numpy as np

from game import Game
from enum import Enum
from reward_functions.exponential import reward

#
# class TOURNAMENT_TYPE(Enum):
#     STOCHASTIC = 1
#     DETERMINISTIC = 2
#
# example_tournament_properties = {
#     'number_of_rounds': 1,
#     'attacker_threshold': 1,
#     'defender_threshold': 1,
#     'selection_ratio': 0.5,
#     'tournament_type': TOURNAMENT_TYPE.STOCHASTIC
# }

class Tournament(object):
    """
    Takes in any number of strategies, puts each one in the defending position and plays them against the whole population
    of attackers in order to see which is the strongest.
    - Need to set up exactly the same game each time: Time_limit etc.
    - Decide on number of times we play each game
    - Best way to record all results. (Writing to text files, retrieving these files and using Pandas to analyse the data)
    """

    def __init__(self, defender_strategies=None, attacker_strategies=None, tournament_properties=None):
        """
        :param player_strategies: a tuple of players with different (or the same strategies)
        :param game_properties: game properties to be played throughout the tournament
        """
        # Needs to iterate through each strategy, putting them as defence
        # Then iterate through the rest of the strategies in attacking position
        #
        self.attacker_strategies = attacker_strategies
        self.defender_strategies = defender_strategies

        self.tournament_properties = tournament_properties
        number_of_resources = len(attacker_strategies[0].get_strategies())
        self.system = System(number_of_resources)
        self.defender_results = {}
        self.attacker_results = {}
        self.mean_defender_results = {}
        self.mean_attacker_results = {}

        for attacker in self.attacker_strategies:
            self.attacker_results[attacker] = {}
            self.mean_attacker_results[attacker] = {}

        for defender in self.defender_strategies:
            self.defender_results[defender] = {}
            self.mean_defender_results[defender] = {}

    def play_tournament(self):

        total_games = len(self.attacker_strategies) * len(self.defender_strategies)
        games_to_play = total_games * self.tournament_properties['selection_ratio']

        for match in range(0, int(games_to_play)):

            correct_choice = False
            while not correct_choice:
                defender = np.random.choice(self.defender_strategies)
                defender.get_player_properties()['threshold'] = self.tournament_properties['defender_threshold']

                attacker = np.random.choice(self.attacker_strategies)
                attacker.get_player_properties()['threshold'] = self.tournament_properties['attacker_threshold']

                if self.defender_results.get(defender).get(attacker) is None:
                    self.defender_results[defender][attacker] = []
                    self.attacker_results[attacker][defender] = []
                    correct_choice = True

            for i in range(0, self.tournament_properties['number_of_rounds']):
                defenders_reward = None
                attackers_reward = None
                print(self.tournament_properties['tournament_type'])
                print(self.tournament_properties)
                print(self.tournament_properties['tournament_type'] is TOURNAMENT_TYPE.DETERMINISTIC)
                if self.tournament_properties['tournament_type'] is TOURNAMENT_TYPE.STOCHASTIC:
                    g = Game((defender, attacker), self.system, self.tournament_properties['game_properties'])

                    g.play()

                    defenders_reward = self.system.get_system_reward(defender)
                    attackers_reward = self.system.get_system_reward(attacker)

                    g.reset()
                    self.system = System(self.system.get_number_of_servers())
                elif self.tournament_properties['tournament_type'] is TOURNAMENT_TYPE.DETERMINISTIC:
                    defender_rates = [s.get_rate() for s in defender.get_strategies()]
                    attacker_rates = [s.get_rate() for s in attacker.get_strategies()]

                    defender_costs = defender.get_player_properties()['move_costs']
                    attacker_costs = attacker.get_player_properties()['move_costs']

                    threshold = self.tournament_properties['attacker_threshold']
                    defenders_reward, attackers_reward = reward(threshold, defender_rates,
                                                                attacker_rates, defender_costs, attacker_costs)

                self.defender_results[defender][attacker].append((defenders_reward, attackers_reward))

                self.attacker_results[attacker][defender].append((attackers_reward, defenders_reward))

            # Need to calculate the mean of the results for each playoff
            self.mean_defender_results[defender][attacker] = (
            np.mean([x[0] for x in self.defender_results[defender][attacker]]),
            np.mean([x[1] for x in self.defender_results[defender][attacker]]))

            self.mean_attacker_results[attacker][defender] = (
            np.mean([x[0] for x in self.attacker_results[attacker][defender]]),
            np.mean([x[1] for x in self.attacker_results[attacker][defender]]))


    def get_mean_defense(self):
        mean_defense = {}
        for defender in self.defender_strategies:
            mean_defense[defender] = np.mean([self.mean_defender_results[defender][x][0]
                                              for x in self.mean_defender_results[defender]])
        return mean_defense

    def get_mean_attack(self):
        mean_attack = {}
        for attacker in self.attacker_strategies:
            mean_attack[attacker] = np.mean([self.mean_attacker_results[attacker][x][0]
                                             for x in self.mean_attacker_results[attacker]])
        return mean_attack



def convert_tournament_type(type_string):

    values = str.split(type_string, '.')
    t = values[-1]

    for k, v in TOURNAMENT_TYPE.__members__.items():
        if k == t:
            tournament_type = v

    return tournament_type
