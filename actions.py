from selenium.webdriver.common.by import By




def perform_action(driver, action, d2):
    footer = driver.find_element(By.CLASS_NAME, "table-footer-container-content")
    try:
        if action == 'call':
            try:

                button = footer.find_element(By.XPATH,
                                             ".//div[contains(@class, 'pa-call')]//div[contains(@class, 'SimpleButton__text')]")
                d2.execute_script("arguments[0].click();", button)
            except Exception as ei:
                button = footer.find_element(By.XPATH,
                                             ".//div[contains(@class, 'pa-check')]//div[contains(@class, 'SimpleButton__text')]")
                d2.execute_script("arguments[0].click();", button)

        elif action == 'raise':
            try:
                button = footer.find_element(By.XPATH,
                                             ".//div[contains(@class, 'raise_group_actions')]//div[contains(@class, 'SimpleButton__text')]")
                d2.execute_script("arguments[0].click();", button)
            except Exception as ei:
                try:
                    button = footer.find_element(By.XPATH,
                                                 ".//div[contains(@class, 'pa-call')]//div[contains(@class, 'SimpleButton__text')]")
                    d2.execute_script("arguments[0].click();", button)
                except Exception as ei:
                    try:
                        button = footer.find_element(By.XPATH,
                                                     ".//div[contains(@class, 'pa-check')]//div[contains(@class, 'SimpleButton__text')]")
                        d2.execute_script("arguments[0].click();", button)
                    except Exception as ei:
                        try:
                            button = footer.find_element(By.XPATH,
                                                         ".//div[contains(@class, 'pa-all-in')]//div[contains(@class, 'SimpleButton__text')]")
                            d2.execute_script("arguments[0].click();", button)
                        except Exception as ei:
                                button = footer.find_element(By.XPATH,
                                                             ".//div[contains(@class, 'pa-fold')]//div[contains(@class, 'SimpleButton__text')]")
                                d2.execute_script("arguments[0].click();", button)

        elif action == 'bet':
            try:
                button = footer.find_element(By.XPATH,
                                             ".//div[contains(@class, 'raise_group_actions')]//div[contains(@class, 'SimpleButton__text')]")
                d2.execute_script("arguments[0].click();", button)
            except Exception as ei:
                try:
                    button = footer.find_element(By.XPATH,
                                                 ".//div[contains(@class, 'pa-call')]//div[contains(@class, 'SimpleButton__text')]")
                    d2.execute_script("arguments[0].click();", button)
                except Exception as ei:
                    try:
                        button = footer.find_element(By.XPATH, '//div[starts-with(text(), "Subir")]')
                        d2.execute_script("arguments[0].click();", button)
                    except Exception as ei:
                        button = footer.find_element(By.XPATH,
                                                     ".//div[contains(@class, 'pa-check')]//div[contains(@class, 'SimpleButton__text')]")
                        d2.execute_script("arguments[0].click();", button)

        elif action == 'fold':
            try:
                button = footer.find_element(By.XPATH,
                                             ".//div[contains(@class, 'pa-check')]//div[contains(@class, 'SimpleButton__text')]")
                d2.execute_script("arguments[0].click();", button)
            except Exception as ei:
                button = footer.find_element(By.XPATH,
                                             ".//div[contains(@class, 'pa-fold')]//div[contains(@class, 'SimpleButton__text')]")
                d2.execute_script("arguments[0].click();", button)
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
        button = footer.find_element(By.CLASS_NAME, f"im-back-button")
        button.click()
        print(f"Accion generada: sentarme")
    except Exception as e:
        pass
