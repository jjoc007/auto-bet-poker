from selenium import webdriver
from game import *

url = "file:///Users/jorjuela/Documents/bets/poker-chat/examples/bank-container.html"

driver = webdriver.Chrome(executable_path='/Users/jorjuela/Documents/bets/poker-chat/chromedriver')
driver.get(url)

bb, ante = detect_blinds(driver)
print(bb)
print(ante)


