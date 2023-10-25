from evaluator.card import Card
from evaluator.hand_evaluator import HandEvaluator


def translate_card(card_play):
    s, v = card_play.split("_")
    s_f = 'd'
    if s == "T":
        s_f = 'c'
    elif s == "C":
        s_f = 'h'
    elif s == "P":
        s_f = 's'

    return Card(v, s_f)


def translate_cards(play_cards):
    c = []
    for card in play_cards:
        c.append(translate_card(card))
    return c

friend_cards_1 = ['C_A','P_A']

hand_2 = [
    'C_A',
    'P_A',
]

friend_cards_2 = [
    'T_A',
    'C_T'
]

hand_1 = [
    'P_3',
    'C_A'
]

table = [
'C_2',
'T_4',
'P_4',
'D_A'
]



#player 1
force_hand = HandEvaluator.evaluate_hand([translate_card(hand_1[1]), translate_card(hand_1[0])], board=[], friend_cards=[]) # 0.9212244897959184
force_table = HandEvaluator.evaluate_hand([translate_card(hand_1[0]), translate_card(hand_1[1])],
                                          board=translate_cards(table)) #0.8589269195189639
print(force_hand)
print(force_table)









'''
force_table = HandEvaluator.evaluate_hand([translate_card(hand_1[0]), translate_card(hand_1[1])],
                                          board=translate_cards(table)) #0.8589269195189639
print(f"force hand:  {force_hand}")
print(f"force table: {force_table}")

print(f"with friend cards")

force_hand = HandEvaluator.evaluate_hand([translate_card(hand_1[1]), translate_card(hand_1[0])], board=[], friend_cards=translate_cards(friend_cards_1)) # 0.9212244897959184
force_table = HandEvaluator.evaluate_hand([translate_card(hand_1[0]), translate_card(hand_1[1])],
                                          board=translate_cards(table), friend_cards=translate_cards(friend_cards_1)) #0.8589269195189639

print(f"force hand:  {force_hand}")
print(f"force table: {force_table}")



print(f"----------------")
print(f"----------------")
#player 2
force_hand = HandEvaluator.evaluate_hand([translate_card(hand_2[1]), translate_card(hand_2[0])], board=[], friend_cards=[]) # 0.9212244897959184
force_table = HandEvaluator.evaluate_hand([translate_card(hand_2[0]), translate_card(hand_2[1])],
                                          board=translate_cards(table)) #0.8589269195189639

print(f"force hand:  {force_hand}")
print(f"force table: {force_table}")

print(f"with friend cards")

force_hand = HandEvaluator.evaluate_hand([translate_card(hand_2[1]), translate_card(hand_2[0])], board=[], friend_cards=translate_cards(friend_cards_2)) # 0.9212244897959184
force_table = HandEvaluator.evaluate_hand([translate_card(hand_2[0]), translate_card(hand_2[1])],
                                          board=translate_cards(table), friend_cards=translate_cards(friend_cards_2)) #0.8589269195189639

print(f"force hand:  {force_hand}")
print(f"force table: {force_table}")
'''