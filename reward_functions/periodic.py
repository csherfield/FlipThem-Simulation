import math
import reward_functions.renewal


def calculate_periodic_equilibrium(defender_costs, attacker_costs):

    if defender_costs[0] < attacker_costs[0]:
        return 1 / (2 * attacker_costs[0]), defender_costs[0] / (2 * attacker_costs[0] ** 2)
    elif defender_costs[0] == attacker_costs[0]:
        return 1 / (2 * defender_costs[0]), 1 / (2 * defender_costs[0])
    else:
        return attacker_costs[0] / (2 * defender_costs[0] ** 2), 1 / (2 * defender_costs[0])


def periodic_opt_response(player, opponent):
    move_cost = player.get_player_properties()['move_costs'][0]
    test = 1 / (2 * move_cost)
    opponent_rate = opponent.get_player_properties()['rates'][0]
    if opponent_rate < test:
        return math.sqrt(opponent_rate * test)
    else:
        return 0


def age_density(z, rate):

    if z < 1/rate:
        return rate
    else:
        return 0

def age_distribution(z, rate):
    if z < 1/rate:
        return rate * z
    else:
        return 1


if __name__ == '__main__':


    # print(calculate_periodic_equilibrium((0.2,), (0.2,)))

    print(reward_functions.renewal.reward(1, ((age_density,),(age_distribution,)), ((age_density,),(age_distribution,)),
                                         (1.8,), (1.8,), (0.2,), (0.2,)))

    print(
        reward_functions.renewal.reward(1, ((age_density,), (age_distribution,)), ((age_density,), (age_distribution,)),
                                        (2.0,), (1.8,), (0.2,), (0.2,)))

    print(
        reward_functions.renewal.reward(1, ((age_density,), (age_distribution,)), ((age_density,), (age_distribution,)),
                                        (2.2,), (1.8,), (0.2,), (0.2,)))

    print(
        reward_functions.renewal.reward(1, ((age_density,), (age_distribution,)), ((age_density,), (age_distribution,)),
                                        (2.5,), (1.8,), (0.2,), (0.2,)))

    print(
        reward_functions.renewal.reward(1, ((age_density,), (age_distribution,)), ((age_density,), (age_distribution,)),
                                        (2.0,), (2.0,), (0.2,), (0.2,)))