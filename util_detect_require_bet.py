import undetected_chromedriver as uc
from game import *

url = "file:///Users/juanorjuela/Documents/dev/auto-bet-poker/examples/buttons2.html"

driver = uc.Chrome()
driver.get(url)

require_bet = get_current_bet(driver)
print(require_bet)


