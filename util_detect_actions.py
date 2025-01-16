from selenium import webdriver
from actions import *
import undetected_chromedriver as uc

url = "file:///Users/juanorjuela/Documents/dev/auto-bet-poker/examples/buttons3.html"

driver = uc.Chrome()
driver.implicitly_wait(10)
driver.get(url)

action = 'call'

games = driver.find_elements(By.CLASS_NAME, 'single_table_container')
print(f"cantidad de juegos detectado: {len(games)}")

for game in games:
    perform_action(game, action, driver)



