from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

# 크롬 옵션을 생성합니다.
chrome_options = webdriver.ChromeOptions()

# detach 옵션을 True로 설정하여 스크립트 종료 후에도 브라우저가 꺼지지 않게 합니다.
chrome_options.add_experimental_option("detach", True)

# webdriver-manager가 자동으로 버전에 맞는 드라이버를 관리합니다.
service = ChromeService(executable_path=ChromeDriverManager().install())

# Service와 Options를 함께 적용하여 드라이버를 실행합니다.
driver = webdriver.Chrome(service=service, options=chrome_options)

# 원하는 웹사이트로 이동합니다.
driver.get("https://www.amazon.com")

# 이 라인이 실행되고 스크립트가 종료되어도 브라우저 창은 그대로 남아있게 됩니다.
print("스크립트 실행이 완료되었습니다. 브라우저는 수동으로 닫아주세요.")
