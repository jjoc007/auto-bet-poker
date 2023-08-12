from selenium import webdriver
from game import *
import random
import ast
import requests
import json

from players import *
from deteccion_fase import *
from probabilities import *
from actions import *
from evaluator.card import *
from evaluator.hand_evaluator import *

import time

my_player = 'jjoc007'
my_friends = ['pmass']

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

cards_df = pd.read_csv('cards64/cards.csv')

iframe = driver.find_element(By.CSS_SELECTOR, 'iframe[_ngcontent-serverapp-c94]')
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
    soy_ciega_pequena = False
    my_cards_published = False
    all_friend_cards = []
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
        r_n = 0
        s_n = 0
        present_friends = []
        for pi in players_action_information:
            # impresion de acciones
            insert_action(game_id, phase, cards, pi)
            # Contando acciones
            if pi.action == 'Retirarse' and pi.player.me is False:
                r_n += 1
            elif pi.action in ['Subir', 'Apostar'] and pi.player.me is False:
                s_n += 1

            if pi.player.name in my_friends:
                print(f"Amigo presente: {pi.player.name}")
                present_friends.append({
                    "name": pi.player.name,
                    "hand": None,
                    "force": None
                })

        print(f"---------------------------------")
        print(f"Retirarse: {r_n}")
        print(f"Subir: {s_n}")
        print(f"---------------------------------")
        # detectar juego completo y generar probabilidad

        me, me_action = find_me(players_action_information)
        if me is not None and me.card_1 is not None and me.card_2 is not None:
            if not my_cards_published:
                url_post = "https://xnf9a82pmf.execute-api.us-east-1.amazonaws.com/pro/postresource"

                payload = json.dumps({
                    "game_id": game_id,
                    "player_name": my_player,
                    "hand": f"['{me.card_1}','{me.card_2}']"
                })
                headers = {
                    'Content-Type': 'application/json'
                }

                response = requests.request("POST", url_post, headers=headers, data=payload)
                print(f"respuesta de publicacion de cartas: {response.status_code}")
                if response.status_code == 200:
                    my_cards_published = True

            print(f'hand cards: c1: {me.card_1} c2: {me.card_2} table cards: {cards}')
            if phase != 'Pre-Flop' and len(cards) < 3:
                continue

            for friend in present_friends:
                if friend['hand'] is None:
                    #hacer llamado a api para obtener cartas
                    url_get = f"https://xnf9a82pmf.execute-api.us-east-1.amazonaws.com/pro/getresource?game_id={game_id}&player_name={friend['name']}"
                    payload = {}
                    headers = {}
                    response = requests.request("GET", url_get, headers=headers, data=payload)
                    response_json = response.json()
                    friend_cards = ast.literal_eval(response_json["hand"])
                    all_friend_cards.extend(friend_cards)
                    friend['hand'] = friend_cards

                    print(f"Friend: {friend} cards: {friend_cards} type: {type(friend_cards)}")
                    # calcular fuerza de la mano de cada amigo

            # guardar accion
            if phase == 'Pre-Flop':
                force = HandEvaluator.evaluate_hand([translate_card(me.card_1), translate_card(me.card_2)], board=[], friend_cards=all_friend_cards)
            else:
                force = HandEvaluator.evaluate_hand([translate_card(me.card_1), translate_card(me.card_2)],
                                                    board=translate_cards(cards), friend_cards=all_friend_cards)

            # calcular fuerza de amigos

            pozo_total = detect_pozo(driver)
            required_bet = get_current_bet(driver)
            my_cash = me_action.actual_cash
            cash_total = my_cash
            # calcular accion con base en la fuerza de cada amigo
            accion = determine_simple_action(s_n > 0, phase, force)

            print(f"FM: {force} A: {accion}  RB: {required_bet} MC: {my_cash}")
            perform_action(driver, accion)

        new_game_id = detect_game(driver)
        print("**********************************************************************")
        if new_game_id != game_id:
            print(f"juego nuevo id: {new_game_id}")
            break  # hay un juego nuevo
        time.sleep(0.5)

driver.quit()

