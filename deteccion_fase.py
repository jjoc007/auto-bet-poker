import uuid

import cv2
import numpy as np
import pandas as pd
import os, re

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


def load_cards():
    templates = {}
    for file in os.listdir('cards'):
        if file.endswith('.png'):
            card_name = os.path.splitext(file)[0]
            template = cv2.imread(os.path.join('cards', file), cv2.IMREAD_GRAYSCALE)
            template = cv2.normalize(template, None, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_8U)
            card_value = card_name.split('_')[1]
            card_suit = card_name.split('_')[0]
            card_key = (card_suit, card_value)
            if card_key in templates:
                templates[card_key].append(template)
            else:
                templates[card_key] = [template]
    return templates


def detect_cards(img, templates, threshold=0.99):
    detected_cards = []
    for name, template_list in templates.items():
        for template in template_list:
            w, h = template.shape[::-1]

            # Aplica la coincidencia de plantillas
            res = cv2.matchTemplate(img, template, cv2.TM_CCOEFF_NORMED)

            # Encuentra todas las ubicaciones donde la coincidencia es lo suficientemente fuerte
            _, max_val, _, max_loc = cv2.minMaxLoc(res)

            if max_val >= threshold:
                detected_cards.append(name)
                cv2.rectangle(img, max_loc, (max_loc[0] + w, max_loc[1] + h), 0, 2)
                break

    return detected_cards, determine_poker_phase(len(detected_cards))


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
                    cards_df = cards_df.append({'card': url_base64, 'value': str(uuid.uuid4())}, ignore_index=True)
        cards_df.to_csv('cards64/cards.csv', index=False)

        return phase, detected_cards
    except StaleElementReferenceException:
        print("No se encontró el div con la información de cartas.")
        return None, None


