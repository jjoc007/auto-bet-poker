from selenium import webdriver
from actions import *
import undetected_chromedriver as uc

url = "file:///Users/juanorjuela/Documents/dev/auto-bet-poker/examples/buttons2.html"

driver = uc.Chrome()
driver.implicitly_wait(10)
driver.get(url)

action = 'call'
perform_action(driver, action)


