from selenium import webdriver
from game import *
import random

from players import *
from deteccion_fase import *
from probabilities import *
from actions import *
from pokereval.card import Card
from pokereval.hand_evaluator import HandEvaluator

import time

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


url = "https://betplay.com.co/"
#url = "file:///Users/jorjuela/Documents/bets/poker-chat/examples/players.html"


driver = webdriver.Chrome()
driver.get(url)

# esperar suficiente tiempo mientras abro la pagina de poker
for i in range(0, 5):
    print(f"esperando lapso : {i}")
    time.sleep(15)


templates = load_cards()
my_player = 'jjoc007'
cards_df = pd.read_csv('cards64/cards.csv')

iframe = driver.find_element(By.CSS_SELECTOR, 'iframe[_ngcontent-serverapp-c194]')
driver.switch_to.frame(iframe)

while True:
    # detectar juego
    game_id = detect_game(driver)
    if game_id == 0:
        continue
    # detectar jugadores y cargar informacion de jugadores
    players_information = get_players_info(driver)

    # guardar juego con jugadores
    insert_game(game_id, players_information)
    while True:
        # detectar fase
        perform_blinds(driver)
        sentarme(driver)
        cards_df = pd.read_csv('cards64/cards.csv')
        phase, cards = phase_detect(driver, cards_df)
        if phase is None or cards is None:
            continue

        #detectar acciones de los jugadores
        players_action_information = get_players_action(driver, my_player, cards_df)

        # detectar juego completo y generar probabilidad
        me, me_action = find_me(players_action_information)
        if me is not None and me.card_1 is not None and me.card_2 is not None:
            print(f'hand cards: c1: {me.card_1} c2: {me.card_2} table cards: {cards}')

            # calculo de probabilidad
            # si la fase es preflop
            prob = 0.0
            force = 0.0
            points = 0.0
            accion = "check"
            hay_prob = True
            if phase == 'Pre-Flop':
                prob = get_hand_probability(me.card_1, me.card_2, 6)
                prob = prob[0]
                points = ((prob - 0.23) / (0.55 - 0.23)) * 0.5
                force = HandEvaluator.evaluate_hand([translate_card(me.card_1), translate_card(me.card_2)], [])

            # si la fase es flop
            if phase in ['Flop', 'Turn', 'River']:
                prob = calculate_flop_pro(me.card_1, me.card_2, cards[0], cards[1], cards[2], 6)
                if prob is None:
                    print(f"no hay probabilidad: {[me.card_1, me.card_2, cards[0], cards[1], cards[2]]}")
                    prob = 0.2
                    hay_prob = False
                points = ((prob - 0.2) / (0.8 - 0.2)) * 0.5
                force = HandEvaluator.evaluate_hand([translate_card(me.card_1), translate_card(me.card_2)], translate_cards(cards))

            pozo_total = detect_pozo(driver)
            required_bet = get_current_bet(driver)
            my_cash = me_action.actual_cash
            # ratio_apuesta_pozo = required_bet / pozo_total

            if 0 < required_bet <= 100 and phase == 'Pre-Flop':
                accion = "call"
            elif 0 < required_bet <= 400 and force >= 0.9 and phase == 'Pre-Flop':
                accion = "bet"
            elif 0 < required_bet <= 400 and force >= 0.8 and phase == 'Pre-Flop':
                accion = "call"
            elif 0 < required_bet <= 400 and force >=0.7 and phase in ['Flop', 'Turn', 'River']:
                accion = "call"
            else:
                if force >= 0.9 and phase == 'Pre-Flop':
                    accion = "call"
                elif force >= 0.9 and phase in ['Flop', 'Turn', 'River']:
                    accion = 'bet'
                elif force >= 0.8 and phase in ['Flop', 'Turn', 'River']:
                    accion = 'call'
                else:
                    accion = 'fold'

            if accion == 'fold' and phase == 'Pre-Flop' and random.random() < 0.2:
                print('apuesta por azar')
                accion = 'call'


            print(f"FM: {force} points: {points} A: {accion}  RB: {required_bet} P: {pozo_total}")
            perform_action(driver, accion)

        # guardar accion
        for pi in players_action_information:
            insert_action(game_id, phase, cards, pi)

        new_game_id = detect_game(driver)
        print("**********************************************************************")
        if new_game_id != game_id:
            print(f"juego nuevo id: {new_game_id}")
            break  # hay un juego nuevo
        time.sleep(0.1)

driver.quit()

