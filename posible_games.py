from collections import Counter
from itertools import combinations

def evaluate_hand(hand):
    values = [card[2] for card in hand]
    suits = [card[0] for card in hand]
    count_values = Counter(values)
    count_suits = Counter(suits)

    # Check for Poker (four of a kind)
    if 4 in count_values.values():
        return 0.8

    # Check for Full House
    if 2 in count_values.values() and 3 in count_values.values():
        return 0.7

    # Check for Flush
    if 5 in count_suits.values():
        return 0.6

    # Check for Straight
    values_order = list('23456789TJQKA')
    sorted_values = sorted(count_values, key=values_order.index)
    for i in range(len(sorted_values) - 4):
        if ''.join(values_order).find(''.join(sorted_values[i:i + 5])) != -1:
            return 0.5

    # Check for Three of a Kind
    if 3 in count_values.values():
        return 0.4

    # Determinar cuál es el valor del par
    pair_value = [key for key, value in count_values.items() if value == 2]

    # Asegurarse de que se encontró un par
    if len(pair_value) == 1:
        print(f'El par es de {pair_value[0]}')
        if pair_value[0] in values[:2]:
            print('El par está en las dos primeras cartas.')
            if pair_value[0] in ['A', 'T', 'J', 'Q', 'K']:
                return 0.25
            else:
                return 0.2
        else:
            print('El par no está en las dos primeras cartas.')
            return 0.1
    elif len(pair_value) == 2:
        return 0.3

    # If none of the above, it's a High Card
    return 0.01

def evaluate_complete_hand(complete_hand):
    return max(evaluate_hand(hand) for hand in combinations(complete_hand, 5))

