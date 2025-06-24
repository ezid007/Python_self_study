from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from rich import print
import time
import os

os.system('cls')

chrome_option = webdriver.ChromeOptions()
# --- 탐지 회피 옵션 추가 ---
# 1. "Chrome이 자동화된 테스트 소프트웨어에 의해 제어되고 있습니다." 메시지 제거
chrome_option.add_experimental_option("excludeSwitches", ["enable-automation"])
# 2. 자동화 탐지를 어렵게 하기 위해 User-Agent 변경 (일반적인 윈도우 크롬 브라우저인 척)
user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36"
chrome_option.add_argument(f"user-agent={user_agent}")
# 3. navigator.webdriver 플래그 비활성화
chrome_option.add_argument('--disable-blink-features=AutomationControlled')
# --- 기존 옵션 ---
chrome_option.add_experimental_option("detach", True)

# 위에서 설정한 모든 옵션을 적용하여 드라이버 실행
driver = webdriver.Chrome(options=chrome_option)
#...(이하 코드는 동일)
driver.get("https://en.wikipedia.org/wiki/Main_Page")
id = driver.find_element(By.ID, "mp-tfa-h2").text
print(id)

try:
    price_dollar_element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'a-price-symbol')))
    print(f"찾은 통화 기호: {price_dollar_element.text}")
    price_whole_element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//span[@class="a-price-whole"]')))
    print(price_whole_element.text)

    item_name = WebDriverWait(driver, 10).until(EC.presence_of_element_located)
    event_times = driver.find_element_by_css_selector(".event-widget a")

    for name in event_times:
        print(name.text)

except Exception as e:
    print("요소를 찾는데 실패하였습니다.")
    print(e)
 