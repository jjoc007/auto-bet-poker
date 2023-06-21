from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def perform_action(driver, action):
    footer = driver.find_element(By.CLASS_NAME, "table-footer-container-content")
    try:
        if action == 'call':
            try:
                button = footer.find_element(By.XPATH, ".//div[contains(@class, 'pa-call')]//div[contains(@class, 'SimpleButton__text')]")
                driver.execute_script("arguments[0].click();", button)
            except Exception as ei:
                button = footer.find_element(By.XPATH, ".//div[contains(@class, 'pa-check')]//div[contains(@class, 'SimpleButton__text')]")
                driver.execute_script("arguments[0].click();", button)

        if action == 'raise':
            try:
                button = footer.find_element(By.XPATH, '//div[starts-with(text(), "Subir")]')
                driver.execute_script("arguments[0].click();", button)
            except Exception as ei:
                try:
                    button = footer.find_element(By.XPATH,
                                                 ".//div[contains(@class, 'pa-call')]//div[contains(@class, 'SimpleButton__text')]")
                    driver.execute_script("arguments[0].click();", button)
                except Exception as ei:
                    button = footer.find_element(By.XPATH,
                                                 ".//div[contains(@class, 'pa-check')]//div[contains(@class, 'SimpleButton__text')]")
                    driver.execute_script("arguments[0].click();", button)

        if action == 'bet':
            try:
                button = footer.find_element(By.XPATH,
                                             ".//div[contains(@class, 'pa-bet')]//div[contains(@class, 'SimpleButton__text')]")
                driver.execute_script("arguments[0].click();", button)
            except Exception as ei:
                try:
                    button = footer.find_element(By.XPATH,
                                                 ".//div[contains(@class, 'pa-call')]//div[contains(@class, 'SimpleButton__text')]")
                    driver.execute_script("arguments[0].click();", button)
                except Exception as ei:
                    try:
                        button = footer.find_element(By.XPATH, '//div[starts-with(text(), "Subir")]')
                        driver.execute_script("arguments[0].click();", button)
                    except Exception as ei:
                        button = footer.find_element(By.XPATH,
                                                     ".//div[contains(@class, 'pa-check')]//div[contains(@class, 'SimpleButton__text')]")
                        driver.execute_script("arguments[0].click();", button)

        if action == 'fold':
            try:
                button = footer.find_element(By.XPATH, ".//div[contains(@class, 'pa-check')]//div[contains(@class, 'SimpleButton__text')]")
                driver.execute_script("arguments[0].click();", button)
            except Exception as ei:
                button = footer.find_element(By.XPATH, ".//div[contains(@class, 'pa-fold')]//div[contains(@class, 'SimpleButton__text')]")
                driver.execute_script("arguments[0].click();", button)
        print(f"Accion generada: {action}")
    except Exception as e:
        pass



def perform_blinds(driver):
    try:
        footer = driver.find_element(By.CLASS_NAME, "table-footer-container")
        try:
            button = footer.find_element(By.CLASS_NAME, f"pa-big-blind")
            button.click()
            print(f"Accion generada: blinds")
        except Exception as ei:
            button = footer.find_element(By.CLASS_NAME, f"pa-small-blind")
            button.click()
            print(f"Accion generada: blinds")

    except Exception as e:
        pass


def sentarme(driver):
    try:
        footer = driver.find_element(By.CLASS_NAME, "table-footer-container-content")
        try:
            button = footer.find_element(By.CLASS_NAME, f"im-back-button")
            button.click()
            print(f"Accion generada: sentarme")
        except Exception as ei:
            pass

    except Exception as e:
        pass


