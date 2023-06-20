from selenium.webdriver.common.by import By
import re


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


def get_current_bet(driver):
    try:
        footer = driver.find_element(By.CLASS_NAME, "table-footer-container")
        call_component = footer.find_element(By.XPATH,
                                             ".//div[contains(@class, 'pa-call')]//div[contains(@class, 'SimpleButton__text')]")

        text = call_component.text
        bet_value_text = text.split('$')[-1]
        bet_value = float(bet_value_text.replace(',', ''))  # Removemos las comas en caso de que existan (ej. "1,000")
        return bet_value
    except Exception as e:
        return 0