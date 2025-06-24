from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import StaleElementReferenceException
import time
import os


os.system('cls')

chrome_option = webdriver.ChromeOptions()
chrome_option.add_experimental_option("excludeSwitches", ["enable-automation"])

driver = webdriver.Chrome(chrome_option)
driver.get("https://orteil.dashnet.org/experiments/cookie/")

cookie = driver.find_element(By.ID, "cookie")
money = driver.find_element(By.ID, "money")
cps = driver.find_element(By.ID, "cps")

game_duration_seconds = 60 * 5
check_interval_seconds = 5

timeout = time.time() + game_duration_seconds
next_check_time = time.time() + check_interval_seconds

while timeout > time.time():

    cookie.click()

    if time.time() > next_check_time:
        try:
            my_cookies = int(money.text.replace(",", ""))

            item_prices = {}
            store_items = driver.find_elements(By.CSS_SELECTOR, "#store > div")
            for item in store_items:
                item_id = item.get_attribute("id")
                price_elements = item.find_elements(By.CSS_SELECTOR, "b")
                if price_elements:
                    price_text = price_elements[0].text.split("-")[-1].strip().replace(",","")
                    if price_text:
                        item_prices[item_id] = int(price_text)

            affordable_upgrades = {
                price: item_id
                for item_id, price in item_prices.items()
                if my_cookies >= price
            }

            if affordable_upgrades:
                highest_price = max(affordable_upgrades.keys())
                item_to_buy_id = affordable_upgrades[highest_price]

                item_to_buy = driver.find_element(By.ID, item_to_buy_id)
                driver.execute_script("arguments[0].click()", item_to_buy)

            next_check_time = time.time() + check_interval_seconds

        except StaleElementReferenceException:
            continue

        except Exception as e:
            print(f"에러 발생: {e}")

final_cps = cps.text
print("\n--- 게임 종료 ---")
print(f"최종 CPS (초당 쿠키 생산량): {final_cps}")

driver.quit()