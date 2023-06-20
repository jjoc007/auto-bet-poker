from posible_games import *

# Single test cases
print(evaluate_complete_hand([('D', 'K'), ('C', 'K')]))  # Pair of Kings, hand only
print(evaluate_complete_hand([('D', 'K'), ('C', 'K'), ('T', '7')]))  # Pair of Kings, after flop
print(evaluate_complete_hand([('D', 'K'), ('C', 'K'), ('T', '7'), ('C', '7')]))  # Two Pair, after turn
print(evaluate_complete_hand([('D', 'K'), ('C', 'K'), ('T', '7'), ('C', '7'), ('P', 'K')]))  # Full House, after river
print(evaluate_complete_hand([('D', 'K'), ('C', 'K'), ('T', '7'), ('C', '7'), ('P', 'K'), ('D', '2'), ('C', 'A')]))  # Full House, complete game

# Multiple test cases
hands = [
    [('D', 'K'), ('C', 'K')],  # Pair of Kings, hand only
    [('D', 'K'), ('C', 'K'), ('T', '7')],  # Pair of Kings, after flop
    [('D', 'K'), ('C', 'K'), ('T', '7'), ('C', '7')],  # Two Pair, after turn
    [('D', 'K'), ('C', 'K'), ('T', '7'), ('C', '7'), ('P', 'K')],  # Full House, after river
    [('D', 'K'), ('C', 'K'), ('T', '7'), ('C', '7'), ('P', 'K'), ('D', '2'), ('C', 'A')],  # Full House, complete game
]

for hand in hands:
    print(evaluate_complete_hand(hand))