import undetected_chromedriver as uc
from game import *

from players import *
from genrative_prediction import *
from deteccion_fase import *
from probabilities import *
from actions import *
from evaluator.card import *
from evaluator.hand_evaluator import *
import time

my_player = os.environ.get('MY_PLAYER')
cache = {}

def make_decision(game_id, force, phase, required_bet, pot, player_data, blinds, my_cash, my_cards, community_cards, t_info):
    M = (my_cash / (blinds['big_blind'] + (blinds['big_blind']/2) + blinds['ante']))
    # print(f"big_blind:{blinds['big_blind']} small: {blinds['big_blind']/2}  ante: {blinds['ante']} M: {M}")

    if force < 0.8:
        return 'fold'

    data = {
        'game_id': game_id,
        'players': list_players(player_data),
        'phase': phase,
        'big_blind': blinds['big_blind'],
        'small_blind': blinds['big_blind']/2,
        'ante': blinds['ante'],
        'm': M,
        'my_cash': my_cash,
        'pot': pot,
        'required_bet': required_bet,
        'force': force,
        'my_cards':my_cards,
        'community_cards': community_cards
    }

    decision = get_strategy_from_model(data, t_info)

    return decision

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
    options.add_argument("--remote-debugging-port=9222")  # Puerto para DevTools Protocol
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    return uc.Chrome(options=options)

def run_poker_bot():
    driver = start_driver()
    try:
        driver.execute_cdp_cmd("Network.enable", {})
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

        # Control de tiempo: 20 minutos
        start_time = time.time()
        while time.time() - start_time < 1200:  # 1200 segundos = 20 minutos
            game_id = detect_game(driver)
            if game_id == 0:
                continue

            cards_df = pd.read_csv('cards64/cards.csv')
            players_information = get_players_info(driver)
            insert_game(game_id, players_information)

            while True:
                try:

                    perform_blinds(driver)
                    sentarme(driver)
                    pozo_total = detect_pozo(driver)
                    blinds = detect_blinds(driver)

                    phase, cards = phase_detect(driver, cards_df)
                    if phase is None or cards is None:
                        continue

                    players_action_information = get_players_action(driver, my_player, cards_df)
                    me, me_action = find_me(players_action_information)

                    if me and me.card_1 and me.card_2:
                        insert_friend_cards(game_id, my_player, me.card_1, me.card_2)
                        friend_cards = get_friend_cards_by_game(game_id, my_player)
                        print(f"friend Cards: {friend_cards}")
                        if phase == 'Pre-Flop':
                            force = HandEvaluator.evaluate_hand(
                                [translate_card(me.card_1), translate_card(me.card_2)],
                                board=[],
                                friend_cards=translate_cards(friend_cards)
                            )
                        else:
                            force = HandEvaluator.evaluate_hand(
                                [translate_card(me.card_1), translate_card(me.card_2)],
                                board=translate_cards(cards),
                                friend_cards=translate_cards(friend_cards)
                            )

                        required_bet = get_current_bet(driver)
                        my_cash = me_action.actual_cash

                        print(f"FORCE of my hand: {force} RB: {required_bet}")
                        t_info = extract_table_info(driver)

                        accion = make_decision(
                            game_id, force, phase, required_bet, pozo_total,
                            players_action_information, blinds, my_cash,
                            f"{me.card_1}, {me.card_2}", ", ".join(cards), t_info
                        )

                        if accion:
                            perform_action(driver, accion)
                        else:
                            perform_action(driver, 'fold')

                        print("------------------------------------------------------------")

                    new_game_id = detect_game(driver)
                    if new_game_id != game_id:
                        break

                    time.sleep(8)
                except Exception as e:
                    print(f"Skip Error")

            if time.time() - start_time >= 1200:
                print("20 minutos cumplidos, reiniciando el driver.")
                break
    finally:
        driver.quit()



# Bucle principal
while True:
    try:
        run_poker_bot()
    except Exception as e:
        print(f"Error en el bot: {e}")