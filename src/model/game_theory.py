import numpy as np
import nashpy as nash

def get_nash_equilibrium(player_name=None, bowler_name=None):
    # Strategy names
    bowler_labels = ["Yorker", "Bouncer"]
    batsman_labels = ["Defend", "Attack", "Rotate Strike"]

    #  Customize payoff matrix based on selected player/bowler
    if player_name == "V Kohli" and bowler_name == "JJ Bumrah":
        bowler_matrix = np.array([
            [0.4, 0.4, 0.2],
            [0.3, 0.5, 0.2]
        ])
    elif player_name == "MS Dhoni":
        bowler_matrix = np.array([
            [0.2, 0.6, 0.2],
            [0.1, 0.8, 0.1]
        ])
    else:
        # Default matrix
        bowler_matrix = np.array([
            [0.6, 0.3, 0.1],
            [0.2, 0.7, 0.1]
        ])

    batsman_matrix = 1 - bowler_matrix

    # Create game and calculate equilibrium
    game = nash.Game(bowler_matrix, batsman_matrix)
    equilibria = list(game.support_enumeration())

    return bowler_labels, batsman_labels, bowler_matrix, equilibria


