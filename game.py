from selenium.webdriver.common.by import By
import re
import json


def detect_game(driver):
    try:
        game = driver.find_elements(By.CLASS_NAME, 'game-id')
        if len(game) > 0:
            matches = re.findall(r'#(\d+)', game[0].text)
            return int(matches[0])
        else:
            return 0
    except Exception as e:  # Esto captura cualquier tipo de excepción
        print(f"An error occurred: {e}")
        return 0


def detect_pozo(driver):
    try:
        bank_text = driver.find_elements(By.CLASS_NAME, 'bank-container-content')
        bank_value = bank_text[0].text.replace('Pozo:', '').replace('$', '').replace(',', '').strip()
        bank_value = bank_value.split('.')[0]
        bank_value = int(bank_value)
        return bank_value
    except Exception as e:  # Esto captura cualquier tipo de excepción
        print(f"An error occurred detect_pozo: {e}")
        return 0

def detect_blinds(driver):
    try:
        bank_text = driver.find_elements(By.CLASS_NAME, 'tournament_table_name')
        patron = r"Niveles:\s*(\d+)\s*/\s*(\d+)(?:\s*ante\s*(\d+))?"
        match = re.search(patron, bank_text[0].text)

        if match:
            bb = int(match.group(2))
            ante = int(match.group(3)) if match.group(3) else 0  # Si no hay ante, asignamos 0
            return {
                "big_blind": bb,
                "ante": ante
            }
        else:
            return None, None
    except Exception as e:  # Esto captura cualquier tipo de excepción
        print(f"An error occurred detect_blinds: {e}")
        return {
                "big_blind": 10000,
                "ante": 0
            }


def get_current_bet(driver):
    try:
        footer = driver.find_element(By.CLASS_NAME, "table-footer-container")
        call_component = footer.find_element(By.XPATH, '//div[starts-with(text(), "Igualar")]')

        text = call_component.text
        bet_value_text = text.split('$')[-1]
        bet_value_text = bet_value_text.split('.')[0]
        bet_value = bet_value_text.replace('K', '00')
        bet_value = float(bet_value.replace(',', ''))  # Removemos las comas en caso de que existan (ej. "1,000")
        return bet_value
    except Exception as e:
        return 0


def read_blinds():
    with open('config.json', 'r') as archivo_json:
        contenido = archivo_json.read()
        return json.loads(contenido)
