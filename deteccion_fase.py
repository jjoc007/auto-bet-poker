import re
import pandas as pd
import uuid
from selenium.common import StaleElementReferenceException
from selenium.webdriver.common.by import By

palos = {
    'C': 1,
    'T': 2,
    'P': 3,
    'D': 4
}

cartas = {
    '2': 2,
    '3': 3,
    '4': 4,
    '5': 5,
    '6': 6,
    '7': 7,
    '8': 8,
    '9': 9,
    '10': 10,
    'J': 11,
    'Q': 12,
    'K': 13,
    'A': 14,
}



def determine_poker_phase(total_cards):
    # Determina la fase del juego basada en el número total de cartas
    if total_cards == 0:
        return "Pre-Flop"
    elif total_cards == 3:
        return "Flop"
    elif total_cards == 4:
        return "Turn"
    elif total_cards == 5:
        return "River"
    else:
        return "Indeterminado"


def phase_detect(driver, cards_df):
    try:
        detected_cards = []
        container = driver.find_element(By.CSS_SELECTOR, '.r-table-cards.max-cards-5')
        cards = container.find_elements(By.CLASS_NAME, 'r-card')
        phase = determine_poker_phase(len(cards))
        for c in cards:
            element = c.find_element(By.CSS_SELECTOR, '.face')
            style = element.get_attribute('style')
            match = re.search(r'url\("(.+)"\)', style)
            if match is not None:
                url_base64 = match.group(1)  # La URL en base64 está en el primer grupo capturado
                if url_base64 in cards_df['card'].values:
                    existing_value = cards_df.loc[cards_df['card'] == url_base64, 'value'].values[0]
                    detected_cards.append(existing_value)
                else:
                    new_row = pd.DataFrame({'card': [url_base64], 'value': [str(uuid.uuid4())]})
                    cards_df = pd.concat([cards_df, new_row], ignore_index=True)
        cards_df.to_csv('cards64/cards.csv', index=False)

        return phase, detected_cards
    except StaleElementReferenceException:
        print("No se encontró el div con la información de cartas.")
        return None, None


