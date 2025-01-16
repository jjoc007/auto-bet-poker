import undetected_chromedriver as uc
from game import *

from players import *
import os
from deteccion_fase import *
from probabilities import *
from actions import *
from evaluator.card import *
from evaluator.hand_evaluator import *
import time
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


my_player = os.environ.get('MY_PLAYER')
cache = {}
session_time = 3600

def decide_action(score, required_bet, phase):
    # Definir umbrales según la fase del juego
    if phase == 'pre-flop':
        thresholds = {'fold': 0.6, 'call': 0.8, 'bet': 0.9}
    elif phase == 'flop':
        thresholds = {'fold': 0.5, 'call': 0.7, 'bet': 0.85}
    else:  # river
        thresholds = {'fold': 0.4, 'call': 0.6, 'bet': 0.8}

    # Tomar decisión basada en el score y la apuesta requerida
    if score < thresholds['fold']:
        return 'fold'
    elif score < thresholds['call']:
        return 'call'
    elif score < thresholds['bet']:
        # Si no hay apuesta previa, inicia una apuesta (bet)
        return 'bet' if required_bet == 0 else 'call'
    else:
        # Si ya hay una apuesta previa, entonces 'raise'
        return 'raise' if required_bet > 0 else 'bet'


def make_decision(game_id, force, phase, required_bet, pot, player_data, blinds, my_cash, my_cards, community_cards, t_info, table_players, active_players):
    M = (my_cash / (blinds['big_blind'] + (blinds['big_blind']/2) + blinds['ante']))
    pot_odds_fraction = required_bet / (pot + required_bet)  # en forma de fracción

    # Ponderaciones
    w_f = 0.6  # Peso de fuerza
    w_p = 0.3  # Peso de pot odds
    w_n = 0.1  # Peso de jugadores restantes

    if phase == 'Pre-flop':
        w_f, w_p, w_n = 0.7, 0.3, 0.4
    elif phase == 'Flop':
        w_f, w_p, w_n = 0.8, 0.2, 0.3
    elif phase == 'Turn':
        w_f, w_p, w_n = 0.9, 0.2, 0.3
    elif phase == 'River':
        w_f, w_p, w_n = 0.9, 0.1, 0.1

    # Calcular componentes
    force_component = w_f * force
    pot_odds_component = w_p * (1 - pot_odds_fraction)
    players_component = w_n * (1 - active_players / table_players)

    # Score final
    SD = force_component + pot_odds_component + players_component

    print(f"FORCE: {force} POT: {pot} RB: {required_bet} POT ODDS: {pot_odds_fraction} SD: {SD}  MYCASH: {my_cash}")
    # print(f"big_blind:{blinds['big_blind']} small: {blinds['big_blind']/2}  ante: {blinds['ante']} M: {M}")

    return decide_action(SD, required_bet, phase)

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


def start_driver():
    options = uc.ChromeOptions()
    #options.add_argument("--remote-debugging-port=9222")  # Puerto para DevTools Protocol
    options.add_argument("--disable-gpu")
    # options.add_argument("--proxy-server=127.0.0.1:8083")
    options.add_argument("--no-sandbox")

    return uc.Chrome(options=options)

def run_poker_bot():
    driver = start_driver()
    try:
        #driver.execute_cdp_cmd("Network.enable", {})
        driver.get("https://betplay.com.co/poker")

        time.sleep(5)

        # Ingresar credenciales
        username_field = driver.find_element(By.ID, "userName")
        password_field = driver.find_element(By.ID, "password")
        username_field.send_keys(os.environ.get('USER_LOGIN'))  # Reemplaza con usuario real
        password_field.send_keys(os.environ.get('USER_PASSWORD'))  # Reemplaza con contraseña real
        time.sleep(2)
        login_button = driver.find_element(By.ID, "btnLoginPrimary")
        login_button.click()

        time.sleep(15)

        juega_ya_button = driver.find_element(By.CLASS_NAME, "play-btn")
        juega_ya_button.click()

        # Esperar suficiente tiempo mientras se abre la página de poker
        for i in range(3):
            print(f"esperando lapso: {i}")
            time.sleep(15)

        iframe = driver.find_element(By.CSS_SELECTOR, 'iframe[_ngcontent-serverapp-c3285601390]')
        driver.switch_to.frame(iframe)

        start_time = time.time()
        while time.time() - start_time < session_time:
            # iterar sobre mesas
            games = driver.find_elements(By.CLASS_NAME, 'single_table_container')
            print(f"cantidad de juegos detectado: {len(games)}")

            for game in games:
                gi = detect_game(game)
                if gi == 0:
                    continue

                try:
                    # listen_to_websocket(driver)
                    perform_blinds(game)
                    sentarme(game)
                    pozo_total = detect_pozo(game)
                    blinds = detect_blinds(game)

                    phase, cards = phase_detect(game, cards_df)
                    if phase is None or cards is None:
                        continue

                    table_information = get_players_action(game, my_player, cards_df)
                    players_action_information = table_information["player_info"]
                    me, me_action = find_me(players_action_information)

                    if me and me.card_1 and me.card_2:
                        #insert_friend_cards(gi, my_player, me.card_1, me.card_2)
                        #friend_cards = get_friend_cards_by_game(gi, my_player)
                        # print(f"friend Cards: {friend_cards}")
                        if phase == 'Pre-Flop':
                            force = HandEvaluator.evaluate_hand(
                                [translate_card(me.card_1), translate_card(me.card_2)],
                                board=[],
                                friend_cards=translate_cards([])
                            )
                        else:
                            force = HandEvaluator.evaluate_hand(
                                [translate_card(me.card_1), translate_card(me.card_2)],
                                board=translate_cards(cards),
                                friend_cards=translate_cards([])
                            )

                        required_bet = get_current_bet(game)
                        my_cash = me_action.actual_cash

                        #print(f"FORCE of my hand: {force} RB: {required_bet}")
                        #t_info = extract_table_info(game)

                        accion = make_decision(
                            gi, force, phase, required_bet, pozo_total,
                            players_action_information, blinds, my_cash,
                            f"{me.card_1}, {me.card_2}", ", ".join(cards), {}, table_information["total_players"], table_information["active_players"]
                        )

                        if accion:
                            perform_action(game, accion, driver)
                        else:
                            perform_action(game, 'fold', driver)

                        print("------------------------------------------------------------")

                    time.sleep(0.1)
                except Exception as e:
                    print(f"Skip Error: {e}")

                if time.time() - start_time >= session_time:
                    print("reiniciando el driver.")
                    break

    finally:
        driver.quit()



cards_df = pd.read_csv('cards64/cards.csv')
# Bucle principal
while True:
    try:
        run_poker_bot()
    except Exception as e:
        print(f"Error en el bot: {e}")