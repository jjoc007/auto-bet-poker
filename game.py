import json
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
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


def detect_blinds(driver):
    try:
        # Buscar elementos con cada clase por separado
        element = None
        try:
            element = WebDriverWait(driver, 0.1).until(
                EC.presence_of_element_located((By.CLASS_NAME, 'table-name'))
            )
        except Exception:
            element = WebDriverWait(driver, 0.1).until(
                EC.presence_of_element_located((By.CLASS_NAME, 'tournament_table_name'))
            )

        # Obtener el texto del elemento encontrado
        if element:
            bank_text = element.text

            # Patrón para extraer los blinds y ante
            patron = r"Niveles(?: de apuestas)?:\s*\$?(\d+)\s*/\s*\$?(\d+)(?:\s*ante\s*\$?(\d+))?"
            match = re.search(patron, bank_text)

            if match:
                bb = int(match.group(2))
                ante = int(match.group(3)) if match.group(3) else 0  # Si no hay ante, asignamos 0
                return {
                    "big_blind": bb,
                    "ante": ante
                }
            else:
                print('No se detectaron blinds en el texto proporcionado.')
                return read_blinds()
        else:
            print('No se encontró ningún elemento con las clases especificadas.')
            return read_blinds()
    except Exception as e:
        print(f"An error occurred in detect_blinds: {e}")
        return read_blinds()


def get_current_bet(driver):
    try:
        footer = driver.find_element(By.CLASS_NAME, "table-footer-container")
        call_component = footer.find_element(By.XPATH,
                                     ".//div[contains(@class, 'pa-call')]//div[contains(@class, 'SimpleButton__text')]")

        text = call_component.text
        print(f"require bet text: {text}")
        bet_value_text = text.split('$')[-1]

        if 'K' in bet_value_text:
            bet_str = bet_value_text.replace('K', '')  # elimina la 'K'
            value = float(bet_str)  # convierte a número
            value *= 1000  # multiplica por 1000
            return value
        else:
            # Si no hay 'K', se convierte directamente
            return float(bet_value_text)
    except Exception as e:
        return 0


def read_blinds():
    with open('config.json', 'r') as archivo_json:
        contenido = archivo_json.read()
        return json.loads(contenido)

def extract_table_info(driver):
    """
    Extrae la información de la mesa (torneo o juego en efectivo) utilizando Selenium y la devuelve como un diccionario.
    """
    table_info = {}

    try:
        # Esperar a que el contenedor principal esté presente
        wait = WebDriverWait(driver, 0.1)  # Tiempo máximo de espera: 10 segundos
        container = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "TableInfoContainer__page_content")))

        # Localizar todos los campos dentro del contenedor
        fields = container.find_elements(By.CLASS_NAME, "table-info-field")

        for field in fields:
            try:
                # Extraer el label y el valor de cada campo
                label_element = field.find_element(By.CLASS_NAME, "table-info-field-label")
                value_element = field.find_element(By.CLASS_NAME, "table-info-field-value")

                # Normalizar el label para usarlo como clave
                label = label_element.text.strip()
                key = label.lower().replace(' ', '_')

                # Obtener el valor
                value = value_element.text.strip()

                # Guardar en el diccionario
                table_info[key] = value
            except Exception as e:
                print(f"Error procesando un campo: {e}")

    except Exception as e:
        print(f"Error al extraer información de la mesa")

    return table_info