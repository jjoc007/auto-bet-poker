from selenium.common import NoSuchElementException, StaleElementReferenceException
from selenium.webdriver.common.by import By
from balance import *
import re


class Player:
    def __init__(self, name, cash=0, me=False, card_1=None, card_2=None):
        self.name = name
        self.cash = cash
        self.me = me
        self.card_1 = card_1
        self.card_2 = card_2

    def to_dict(self):
        return {
            'name': self.name,
            'cash': self.cash,
            'me': self.me,
            'card_1': self.card_1,
            'card_2': self.card_2
        }


class BetPlayer:
    def __init__(self, bet):
        self.bet = bet

    def to_dict(self):
        return {
            'bet': self.bet
        }


class ActionPlayer:
    def __init__(self, position, player, action, actual_cash, bet_player):
        self.position = position
        self.player = player
        self.action = action
        self.actual_cash = get_balance(actual_cash)
        if self.action is None:
            self.action = ''
        self.bet_player = bet_player

    def to_dict(self):
        return {
            'p': self.position,
            'player': self.player.to_dict() if self.player is not None else None,
            'action': self.action,
            'actual_cash': self.actual_cash,
            'bet_player': self.bet_player.to_dict() if self.bet_player is not None else None
        }


def get_players_info(driver):
    players = driver.find_elements(By.CLASS_NAME, 'r-seat')
    players_info = []

    for player in players:
        try:
            class_list = player.get_attribute('class')
            classes = class_list.split()  # esto divide la lista de clases en elementos individuales
            seat_class = [s for s in classes if s.startswith('s-')]
            position = -1
            if seat_class:  # comprueba si encontramos una clase que comienza con 's-'
                position = seat_class[0].split('-')[1]  # toma el número después de 's-'

            # busca la clase que comienza con 's-'
            seat_class = [s for s in classes if s.startswith('s-')]

            name = player.find_element(By.CLASS_NAME, 'player-name')
            player_name = name.text

            player_information = Player(player_name)
            players_info.append(player_information)
        except NoSuchElementException:
            pass
        except StaleElementReferenceException:
            pass
    return players_info


def get_players_action(driver, my_user, cards_df):
    players = driver.find_elements(By.CLASS_NAME, 'r-seat')
    players_info = []

    for player in players:
        try:
            # position
            class_list = player.get_attribute('class')
            classes = class_list.split()  # esto divide la lista de clases en elementos individuales
            seat_class = [s for s in classes if s.startswith('s-')]
            position = -1
            if seat_class:  # comprueba si encontramos una clase que comienza con 's-'
                position = seat_class[0].split('-')[1]  # toma el número después de 's-'

            # busca la clase que comienza con 's-'
            seat_class = [s for s in classes if s.startswith('s-')]

            name = player.find_element(By.CLASS_NAME, 'player-name')
            player_name = name.text

            me = False
            card_hand_1 = None
            card_hand_2 = None
            if player_name == my_user:
                me = True
                cards = player.find_elements(By.CLASS_NAME, 'r-card')
                detected_cards = []
                for c in cards:
                    # detectar mis cartas
                    element = c.find_element(By.CSS_SELECTOR, '.face')
                    style = element.get_attribute('style')
                    match = re.search(r'url\("(.+)"\)', style)
                    if match is not None:
                        url_base64 = match.group(1)  # La URL en base64 está en el primer grupo capturado
                        if url_base64 in cards_df['card'].values:
                            existing_value = cards_df.loc[cards_df['card'] == url_base64, 'value'].values[0]
                            detected_cards.append(existing_value)

                if len(detected_cards) == 2:
                    card_hand_1 = detected_cards[0]
                    card_hand_2 = detected_cards[1]

            cash = player.find_element(By.CLASS_NAME, 'player-cash')
            player_cash = cash.text

            player_information = Player(player_name, player_cash, me, card_hand_1, card_hand_2)

            action_elements = player.find_elements(By.CLASS_NAME, 'player-action')
            if action_elements:
                action_text_elements = action_elements[0].find_elements(By.CLASS_NAME, 'text')
                player_action = action_text_elements[0].text if action_text_elements else None
            else:
                player_action = None

            # bets
            # bet
            bet_table = driver.find_element(By.CSS_SELECTOR, ".r-table-chips-layer")

            bet_parent_element = bet_table.find_element(By.CSS_SELECTOR, f".r-player-bet.s-{position}")
            bet_child_element = bet_parent_element.find_element(By.CSS_SELECTOR, ".r-player-bet-content")
            bet = bet_child_element.text

            bets = BetPlayer(bet)

            player_action_information = ActionPlayer(position, player_information, player_action, player_cash, bets)
            players_info.append(player_action_information)
        except Exception as e:
            pass
    return players_info


def find_me(player_information):
    for pi in player_information:
        if pi.player.me:
            return pi.player, pi
    print("No estoy jugando")
    return None, None


def get_position_player(player):
    positions = [
        "BTN",
        "CO",
        "HJ",
        "UTG",
        "BB",
        "SB"
    ]
