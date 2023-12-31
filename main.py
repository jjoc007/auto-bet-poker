from selenium import webdriver
from game import *
import ast
import requests
import pandas as pd

from players import *
from deteccion_fase import *
from probabilities import *
from actions import *
from evaluator.card import *
from evaluator.hand_evaluator import *

import time

my_player = os.environ.get('MY_PLAYER')
my_friends = [os.environ.get('MY_FRIEND')]

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
# url = "file:///Users/jorjuela/Documents/bets/poker-chat/examples/players.html"


driver = webdriver.Chrome(executable_path='/Users/jorjuela/Documents/bets/poker-chat/chromedriver')
driver.get(url)

# esperar suficiente tiempo mientras abro la pagina de poker
for i in range(0, 5):
    print(f"esperando lapso : {i}")
    time.sleep(15)

templates = load_cards()

cards_df = pd.read_csv('cards64/cards.csv')

iframe = driver.find_element(By.CSS_SELECTOR, 'iframe[_ngcontent-serverapp-c92]')
driver.switch_to.frame(iframe)


def calculate_friends_force(players_in_game, friends_in_game, friends_active, my_hand, my_force, board_cards, phase):
    # todos los jugadores son amigos
    if friends_active >= players_in_game - 1:  # menos 1 excluyendome
        print('Accion FOLD - solo amigos')
        return 'fold'
    else:
        print('fuerza conjunta: *******************************')
        print(f'mi mano: {my_hand} mi fuerza: {my_force} board: {board_cards}')
        other_friend_cards = [my_hand[0], my_hand[1]]
        forces = [my_force]
        # valida si hay un amigo
        if len(friends_in_game) > 0 and friends_in_game[0]['hand'] is not None:
            if len(friends_in_game) > 1 and friends_in_game[1]['hand'] is not None:
                other_friend_cards.append(friends_in_game[1]['hand'][0])
                other_friend_cards.append(friends_in_game[1]['hand'][1])
            force_f1 = HandEvaluator.evaluate_hand([translate_card(friends_in_game[0]['hand'][0]),
                                                    translate_card(friends_in_game[0]['hand'][1])],
                                                   board=translate_cards(board_cards),
                                                   friend_cards=translate_cards(other_friend_cards))
            print(f"amigo 1 mano: {friends_in_game[0]['hand'][0]} {friends_in_game[0]['hand'][1]} \n"
                  f"a1 fuerza: {force_f1} \n"
                  f"fcards: {other_friend_cards} \n"
                  f"board: {board_cards} \n")
            forces.append(force_f1)

        other_friend_cards = [my_hand[0], my_hand[1]]
        if len(friends_in_game) > 1 and friends_in_game[1]['hand'] is not None:
            other_friend_cards.append(friends_in_game[0]['hand'][0])
            other_friend_cards.append(friends_in_game[0]['hand'][1])
            force_f2 = HandEvaluator.evaluate_hand([translate_card(friends_in_game[1]['hand'][0]),
                                                    translate_card(friends_in_game[1]['hand'][1])],
                                                   board=translate_cards(board_cards),
                                                   friend_cards=translate_cards(other_friend_cards))
            forces.append(force_f2)

        # calcula accion segun fuerza conjunta
        print(f'fuerzas: {forces}')

        if friends_active > 0 and phase == 'Pre-Flop' and len(forces) > 1:
            if forces[1] > my_force >= 0.75 and forces[1] >= 0.9:
                print('accion conjunta: call')
                return 'call'

        if friends_active > 0 and phase in ['Flop', 'Turn', 'River'] and len(forces) > 1:
            if forces[1] > my_force >= 0.6 and forces[1] >= 0.8:
                print('accion conjunta: bet')
                return 'bet'

        print('fuerza conjunta: *******************************')
        return None


while True:
    # detectar juego
    game_id = detect_game(driver)
    cards_df = pd.read_csv('cards64/cards.csv')
    if game_id == 0:
        continue
    # detectar jugadores y cargar informacion de jugadores
    players_information = get_players_info(driver)

    # guardar juego con jugadores
    insert_game(game_id, players_information)
    my_cards_published = False
    all_friend_cards = []
    while True:
        # detectar fase
        perform_blinds(driver)
        sentarme(driver)

        phase, cards = phase_detect(driver, cards_df)
        if phase is None or cards is None:
            continue

        # detectar acciones de los jugadores
        players_action_information = get_players_action(driver, my_player, cards_df)
        active_players = len(players_action_information)

        r_n = 0
        s_n = 0
        active_friends = 0
        present_friends = []
        for pi in players_action_information:
            # impresion de acciones
            insert_action(game_id, phase, cards, pi)
            # Contando acciones
            if pi.action == 'Retirarse' and pi.player.me is False:
                r_n += 1
                active_players = active_players - 1
            elif pi.action in ['Subir', 'Apostar'] and pi.player.me is False:
                s_n += 1

            if pi.player.name in my_friends:
                friend_active = False
                if pi.action != "Retirarse":
                    friend_active = True
                    active_friends = active_friends + 1
                print(f"Amigo presente: {pi.player.name}")
                present_friends.append({
                    "name": pi.player.name,
                    "hand": None,
                    "force": None,
                    "active": friend_active
                })

        print(f"counts: ---------------------------------")
        print(f"active players: {active_players} Active Friends: {active_friends} Retirarse: {r_n} Subir: {s_n}")

        # detectar juego completo y generar probabilidad
        me, me_action = find_me(players_action_information)
        if me is not None and me.card_1 is not None and me.card_2 is not None:
            if False: # por el momento no es necesario publicar cartas not my_cards_published:
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

            print("my games status: ---------------------------------------")
            print(f'hand cards: c1: {me.card_1} c2: {me.card_2} table cards: {cards}')
            if phase != 'Pre-Flop' and len(cards) < 3:
                continue

            for friend in present_friends:
                if friend['hand'] is None:
                    # hacer llamado a api para obtener cartas
                    url_get = f"https://xnf9a82pmf.execute-api.us-east-1.amazonaws.com/pro/getresource?game_id={game_id}&player_name={friend['name']}"
                    payload = {}
                    headers = {}
                    response = requests.request("GET", url_get, headers=headers, data=payload)
                    if response.text == "":
                        continue
                    response_json = response.json()
                    friend_cards = ast.literal_eval(response_json["hand"])
                    all_friend_cards.extend(friend_cards)
                    friend['hand'] = friend_cards

                    # calcular fuerza de la mano de cada amigo

            # guardar accion
            if phase == 'Pre-Flop':
                force = HandEvaluator.evaluate_hand([translate_card(me.card_1), translate_card(me.card_2)], board=[],
                                                    friend_cards=translate_cards(all_friend_cards))
            else:
                force = HandEvaluator.evaluate_hand([translate_card(me.card_1), translate_card(me.card_2)],
                                                    board=translate_cards(cards),
                                                    friend_cards=translate_cards(all_friend_cards))

            accion = None
            if len(present_friends) > 0:
                accion = calculate_friends_force(active_players, present_friends, active_friends, [me.card_1, me.card_2], force, cards, phase)

            pozo_total = detect_pozo(driver)
            required_bet = get_current_bet(driver)
            my_cash = me_action.actual_cash
            cash_total = my_cash
            # calcular accion con base en la fuerza de cada amigo
            if accion is None:
                accion = determine_simple_action(s_n > 0, phase, force)

            if force < 0.7 and phase == 'Pre-Flop':
                perform_action(driver, 'fold')
            else:
                if force >= 0.9:
                    if phase == 'Pre-Flop':
                        perform_custom_action(driver, '3BB')
                    else:
                        perform_custom_action(driver, 'pozo')
                elif force >= 0.8:
                    if phase == 'Pre-Flop':
                        perform_action(driver, 'call')
                    else:
                        perform_custom_action(driver, 'pozo')
                elif force >= 0.7:
                    if phase == 'Pre-Flop' and required_bet <= 500:
                        perform_action(driver, 'call')
                    elif phase == 'Pre-Flop' and required_bet > 500:
                        perform_action(driver, 'fold')
                    elif phase != 'Pre-Flop' and required_bet <= 1500:
                        perform_action(driver, 'call')
                    elif phase != 'Pre-Flop' and required_bet > 1500:
                        perform_action(driver, 'fold')
                    else:
                        perform_action(driver, 'fold')
                else:
                    print(f"No hay acciones")
                    perform_action(driver, 'fold')

            print(f"FM: {force} RB: {required_bet} MC: {my_cash}")

        new_game_id = detect_game(driver)
        print("**********************************************************************")
        if new_game_id != game_id:
            print(f"juego nuevo id: {new_game_id}")
            break  # hay un juego nuevo
        time.sleep(3)

driver.quit()
