from selenium import webdriver
from players import *

url = "file:///Users/jorjuela/Documents/bets/poker-chat/examples/players.html"

driver = webdriver.Chrome()
driver.get(url)

players_info = get_players_info(driver)
print(players_info)