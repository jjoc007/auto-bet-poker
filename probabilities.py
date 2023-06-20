import csv
from db_poker import *

def get_hand_probability(card_1, card_2, players):
    probability = get_hand(card_1, card_2, players)
    if probability is None:
        probability = get_hand(card_2, card_1, players)

    if probability is not None:
        return probability[3], probability[0], probability[1]
    else:
        return None, None, None
def calculate_flop_pro(c1, c2, c3, c4, c5, p):
    _, c1, c2 = get_hand_probability(c1, c2, p)
    if c1 is None or c2 is None:
        return None

    prob = get_flop(c1, c2, c3, c4, c5, p)
    if prob is not None:
        return prob[6]

    prob = get_flop(c1, c2, c3, c5, c4, p)
    if prob is not None:
        return prob[6]

    prob = get_flop(c1, c2, c4, c5, c3, p)
    if prob is not None:
        return prob[6]

    prob = get_flop(c1, c2, c5, c3, c4, p)
    if prob is not None:
        return prob[6]

    prob = get_flop(c1, c2, c5, c4, c3, p)
    if prob is not None:
        return prob[6]

    if prob is None:
        return None




def load_probabilities_from_csv(file_name):
    probabilities = {}
    with open(file_name, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            # Asume que las cartas se representan como tuplas
            card1 = row['card_1']  # Convierte la cadena de texto a una tupla
            card2 = row['card_2']  # Convierte la cadena de texto a una tupla
            probabilities[(card1, card2)] = float(row['Win Probability'])
    return probabilities