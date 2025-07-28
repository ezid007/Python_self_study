from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

with webdriver.Chrome(service=Service(ChromeDriverManager().install())) as driver:
    driver.get("https://en.wikipedia.org/wiki/Main_Page")

    # id="articlecount", title="Special:Statistics"
    active_editors_element = driver.find_element(
        By.CSS_SELECTOR, "#articlecount a[title='Special:Statistics']"
    )
    active_editors_count = active_editors_element.text
    print(active_editors_count)

    search = driver.find_element(By.NAME, "search")
    search.send_keys("python")
    time.sleep(2)
    # 4. 검색 버튼 찾아서 클릭하기 (수정된 최종 버전)
    # 제공해주신 버튼 정보에 따르면, 버튼에는 고유한 class 이름이 있습니다.
    # CSS 선택자에서 '.'은 class를 의미합니다.
    # ".cdx-search-input__end-button"는 "cdx-search-input__end-button"이라는 클래스를 가진 요소를 찾으라는 뜻입니다.
    # 이 방법은 type이나 id가 없을 때 class 이름을 이용하는 가장 안정적인 방법 중 하나입니다.
    search_button = driver.find_element(
        By.CSS_SELECTOR, ".cdx-search-input__end-button"
    )
    search_button.click()
    time.sleep(5)
