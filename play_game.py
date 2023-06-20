from probabilities import *
from db_poker import *
from pot_odds import *

'''
1. digito la mano inicial y los jugadores
2. con base a la mano inicial decido si seguir o no con el juego
3. colocar cartas de flop y calcular fuerza de la mano
4. pendiente calcular probabilidad de ganancia en cada fase
'''

def calculate_flop_pro(c1,c2,c3,c4,c5,p):
    prob = get_flop(c1, c2, c3, c4, c5, p)
    if prob is not None:
        return prob

    prob = get_flop(c1, c2, c3, c5, c4, p)
    if prob is not None:
        return prob

    prob = get_flop(c1, c2, c4, c5, c3, p)
    if prob is not None:
        return prob

    prob = get_flop(c1, c2, c5, c3, c4, p)
    if prob is not None:
        return prob

    prob = get_flop(c1, c2, c5, c4, c3, p)
    if prob is not None:
        return prob
'''

(3, 2, 1)
'''

players = input("cantidad de jugadores: ")
initial_hand = input("mano inicial: ")
initial_hand = initial_hand.upper()
card_1 = initial_hand[0]+'_'+initial_hand[1]
card_2 = initial_hand[2]+'_'+initial_hand[3]

probability = get_hand(card_1, card_2, players)
if probability is None:
    probability = get_hand(card_2, card_1, players)

print(f'card1: {card_1} card2: {card_2} player: {players} pro: { probability[3]}')

# hay flop
flop = input("flop: ")
flop = flop.upper()
card_3 = flop[0]+'_'+flop[1]
card_4 = flop[2]+'_'+flop[3]
card_5 = flop[4]+'_'+flop[5]

probability_with_flop = calculate_flop_pro(probability[0], probability[1], card_3, card_4, card_5, players)
if probability_with_flop is not None:
    print(f'card1: {card_1} card2: {card_2} card3: {card_3} card4: {card_4} card5: {card_5} player: {players} pro: {probability_with_flop[6]}')
else:
    print('no hay probabilidad')




