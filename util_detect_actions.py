from selenium import webdriver
from actions import *

url = "file:///Users/jorjuela/Documents/bets/poker-chat/examples/buttons.html"

driver = webdriver.Chrome()
driver.implicitly_wait(10)
driver.get(url)

action = 'raise'
perform_action(driver, action)


