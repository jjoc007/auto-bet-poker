from phevaluator import evaluate_cards


'''
def translate_cards(play_cards):
    c = []
    for card in play_cards:
        s, v = card.split("_")
        s_f = 'd'
        if s == "T":
            s_f = 'c'
        elif s == "C":
            s_f = 'h'
        elif s == "P":
            s_f = 's'

        c.append(f"{v}{s_f}")
    return c

test_h = ['C_7','T_5','D_3', 'T_J', 'P_4', 'D_J']
p1 = evaluate_cards(*translate_cards(test_h))
p2 = evaluate_cards("9c", "4c", "4s", "9d", "4h", "2c", "9h")

# Player 2 has a stronger hand
print(f"The rank of the hand in player 1 is {p1}") # 292
print(f"The rank of the hand in player 2 is {p2}") # 236
'''

from pokereval.card import Card
from pokereval.hand_evaluator import HandEvaluator

hole = [Card('Q', 'D'), Card('A', 'S')]
board = []
score = HandEvaluator.evaluate_hand(hole, board)
print(score)