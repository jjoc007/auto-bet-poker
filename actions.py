from selenium.webdriver.common.by import By




def perform_custom_action(driver, action):
    footer = driver.find_element(By.CLASS_NAME, "table-footer-container-content")
    try:
        '''
        3BB => 3 ciegas
        pozo => pozo
        
        '''
        if action == '3BB': #TODO encontrar clase que es
            button_3b = footer.find_element(By.XPATH, ".//div[contains(@class, 'fa-bb')]//div[contains(text(), '3BB')]")
            driver.execute_script("arguments[0].click();", button_3b)
            button = footer.find_element(By.XPATH, ".//div[contains(@class, 'pa-bet') or contains(@class, 'pa-raise')]//div[contains(@class, 'SimpleButton__text')]")
            driver.execute_script("arguments[0].click();", button)
            return
        elif action == 'pozo':
            button_pozo = footer.find_element(By.XPATH,
                                         ".//div[contains(@class, 'fa-pot')]//div[contains(@class, 'button-text')]")
            driver.execute_script("arguments[0].click();", button_pozo)
            button = footer.find_element(By.XPATH, ".//div[contains(@class, 'pa-bet') or contains(@class, 'pa-raise')]//div[contains(@class, 'SimpleButton__text')]")
            driver.execute_script("arguments[0].click();", button)
            return

        #Accion por defecto igualar
        try:
            button = footer.find_element(By.XPATH,
                                         ".//div[contains(@class, 'pa-call')]//div[contains(@class, 'SimpleButton__text')]")
            driver.execute_script("arguments[0].click();", button)
            return
        except Exception as ei:
            button = footer.find_element(By.XPATH,
                                         ".//div[contains(@class, 'pa-check')]//div[contains(@class, 'SimpleButton__text')]")
            driver.execute_script("arguments[0].click();", button)
            return

    except Exception as e:
        try:
            button = footer.find_element(By.XPATH,
                                         ".//div[contains(@class, 'pa-check')]//div[contains(@class, 'SimpleButton__text')]")
            driver.execute_script("arguments[0].click();", button)
        except Exception as ei:
            try:
                button = footer.find_element(By.XPATH,
                                             ".//div[contains(@class, 'pa-fold')]//div[contains(@class, 'SimpleButton__text')]")
                driver.execute_script("arguments[0].click();", button)
            except Exception as ei:
                pass



def perform_action(driver, action):
    footer = driver.find_element(By.CLASS_NAME, "table-footer-container-content")
    try:
        if action == 'call':
            try:

                button = footer.find_element(By.XPATH,
                                             ".//div[contains(@class, 'pa-call')]//div[contains(@class, 'SimpleButton__text')]")
                driver.execute_script("arguments[0].click();", button)
            except Exception as ei:
                button = footer.find_element(By.XPATH,
                                             ".//div[contains(@class, 'pa-check')]//div[contains(@class, 'SimpleButton__text')]")
                driver.execute_script("arguments[0].click();", button)

        elif action == 'raise':
            try:
                button = footer.find_element(By.XPATH,
                                             ".//div[contains(@class, 'raise_group_actions')]//div[contains(@class, 'SimpleButton__text')]")
                driver.execute_script("arguments[0].click();", button)
            except Exception as ei:
                try:
                    button = footer.find_element(By.XPATH,
                                                 ".//div[contains(@class, 'pa-call')]//div[contains(@class, 'SimpleButton__text')]")
                    driver.execute_script("arguments[0].click();", button)
                except Exception as ei:
                    try:
                        button = footer.find_element(By.XPATH,
                                                     ".//div[contains(@class, 'pa-check')]//div[contains(@class, 'SimpleButton__text')]")
                        driver.execute_script("arguments[0].click();", button)
                    except Exception as ei:
                        try:
                            button = footer.find_element(By.XPATH,
                                                         ".//div[contains(@class, 'pa-all-in')]//div[contains(@class, 'SimpleButton__text')]")
                            driver.execute_script("arguments[0].click();", button)
                        except Exception as ei:
                                button = footer.find_element(By.XPATH,
                                                             ".//div[contains(@class, 'pa-fold')]//div[contains(@class, 'SimpleButton__text')]")
                                driver.execute_script("arguments[0].click();", button)

        elif action == 'bet':
            try:
                button = footer.find_element(By.XPATH,
                                             ".//div[contains(@class, 'raise_group_actions')]//div[contains(@class, 'SimpleButton__text')]")
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

        elif action == 'fold':
            try:
                button = footer.find_element(By.XPATH,
                                             ".//div[contains(@class, 'pa-check')]//div[contains(@class, 'SimpleButton__text')]")
                driver.execute_script("arguments[0].click();", button)
            except Exception as ei:
                button = footer.find_element(By.XPATH,
                                             ".//div[contains(@class, 'pa-fold')]//div[contains(@class, 'SimpleButton__text')]")
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
        button = footer.find_element(By.CLASS_NAME, f"im-back-button")
        button.click()
        print(f"Accion generada: sentarme")
    except Exception as e:
        pass
