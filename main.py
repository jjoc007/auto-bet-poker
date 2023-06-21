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

        for pi in players_action_information:
            insert_action(game_id, phase, cards, pi)
        # detectar juego completo y generar probabilidad
        me, me_action = find_me(players_action_information)
        if me is not None and me.card_1 is not None and me.card_2 is not None:
            print(f'hand cards: c1: {me.card_1} c2: {me.card_2} table cards: {cards}')
            if phase != 'Pre-Flop' and len(cards) < 3:
                continue

            # guardar accion


            if phase == 'Pre-Flop':
                force = HandEvaluator.evaluate_hand([translate_card(me.card_1), translate_card(me.card_2)], [])
            else:
                force = HandEvaluator.evaluate_hand([translate_card(me.card_1), translate_card(me.card_2)],
                                                    translate_cards(cards))
            points = 0.0

            pozo_total = detect_pozo(driver)
            required_bet = get_current_bet(driver)
            my_cash = me_action.actual_cash
            percentage_required = (required_bet / my_cash) * 100

            accion = determine_action(players_action_information, phase, force, percentage_required)

            print(f"FM: {force} A: {accion} PR:{percentage_required}% RB: {required_bet} MC: {my_cash}")
            perform_action(driver, accion)

        new_game_id = detect_game(driver)
        print("**********************************************************************")
        if new_game_id != game_id:
            print(f"juego nuevo id: {new_game_id}")
            break  # hay un juego nuevo
        time.sleep(0.5)

driver.quit()

