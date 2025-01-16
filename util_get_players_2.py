from selenium import webdriver
from players import *

url = "file:///Users/jorjuela/Documents/dev/bets/auto-bet-poker/examples/players-2.html"
driver = webdriver.Chrome()
driver.get(url)

table_information = get_players_action(driver, "jjoc007", None)
print(table_information)