from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from rich import print

chrome_option = webdriver.ChromeOptions()
chrome_option.add_experimental_option("detach", True)

driver = webdriver.Chrome(options=chrome_option)
driver.get("https://www.amazon.com/instant-Pot-Plus-60-Programmable/dp/B01NBKTPTS/?th=1")

try:
    price_dollar_element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME,'a-price-symbol')))
    print(f"찾은 통화 기호: {price_dollar_element.text}")

except Exception as e:
    print("요소를 찾는데 실패하였습니다.")
    print(e)