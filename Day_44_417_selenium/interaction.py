from rich import print
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# webdriver-manager가 알아서 드라이버를 관리하고 경로를 설정해줍니다.
with webdriver.Chrome(service=Service(ChromeDriverManager().install())) as driver:
    driver.get("https://en.wikipedia.org/wiki/Main_Page")

    # id="articlecount", title="Special:Statistics"
    active_editors_element = driver.find_element(
        By.CSS_SELECTOR, "#articlecount a[title='Special:Statistics']"
    )
    active_editors_count = active_editors_element.text
    print(active_editors_count)
