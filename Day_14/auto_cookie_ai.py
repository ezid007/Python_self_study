from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import StaleElementReferenceException
import time
import os

os.system('cls')

# --- 1. 기본 설정 및 드라이버 실행 ---
chrome_option = webdriver.ChromeOptions()
chrome_option.add_experimental_option("excludeSwitches", ["enable-automation"])
# chrome_option.add_experimental_option("detach", True) # 테스트 시 브라우저를 닫지 않으려면 주석 해제

driver = webdriver.Chrome(options=chrome_option)
driver.get("https://orteil.dashnet.org/experiments/cookie/")

# --- 2. 게임에 필요한 요소 찾기 ---
cookie = driver.find_element(By.ID, 'cookie')
money = driver.find_element(By.ID, 'money')
cps = driver.find_element(By.ID, 'cps')

# --- 3. 게임 시간 및 업그레이드 주기 설정 ---
# time.time() = time(시간) + time(시간): 1970년 1월 1일 0시 0분 0초부터 현재까지 흐른 시간을 초 단위로 반환
game_duration_seconds = 60 * 5  # 5분
check_interval_seconds = 5      # 5초마다 업그레이드 확인

# 게임 종료 시간과 다음 업그레이드 확인 시간 초기화
timeout = time.time() + game_duration_seconds
next_check_time = time.time() + check_interval_seconds



print("--- 쿠키 클리커 자동화를 시작합니다 (5분) ---")

# --- 4. 메인 게임 루프 ---
while True:
    # 4-1. 게임 종료 시간 확인
    if time.time() > timeout:
        break

    # 4-2. 무한 쿠키 클릭
    cookie.click()

    # 4-3. 업그레이드 확인 시간이 되었는지 체크
    if time.time() > next_check_time:
        try:
            # 현재 쿠키 수 확인 (쉼표(,) 제거 후 정수로 변환)
            my_cookies = int(money.text.replace(",", ""))

            # 상점의 모든 아이템과 가격을 딕셔너리로 저장
            # item_prices = {아이템_ID: 가격, ...}
            item_prices = {}
            store_items = driver.find_elements(By.CSS_SELECTOR, "#store > div")
            for item in store_items:
                item_id = item.get_attribute("id")
                # 가격 정보가 있는 b 태그가 없을 수도 있으므로 확인
                price_elements = item.find_elements(By.CSS_SELECTOR, "b")
                if price_elements:
                    price_text = price_elements[0].text.split("-")[-1].strip().replace(",", "")
                    if price_text:
                        item_prices[item_id] = int(price_text)

            # 구매 가능한 아이템들만 필터링 (딕셔너리 컴프리헨션 사용)
            affordable_upgrades = {
                price: item_id
                for item_id, price in item_prices.items()
                if my_cookies >= price
            }

            # 구매 가능한 아이템이 있다면
            if affordable_upgrades:
                # 그중 가장 비싼 아이템의 가격을 찾음
                highest_price = max(affordable_upgrades.keys())
                # 해당 아이템의 ID를 가져옴
                item_to_buy_id = affordable_upgrades[highest_price]

                # 해당 아이템을 자바스크립트로 클릭하여 구매
                item_to_buy = driver.find_element(By.ID, item_to_buy_id)
                driver.execute_script("arguments[0].click();", item_to_buy)

                print(f"아이템 구매 완료: {item_to_buy_id} (가격: {highest_price})")

            # 다음 업그레이드 확인 시간 재설정
            next_check_time = time.time() + check_interval_seconds

        except StaleElementReferenceException:
            # 아이템 구매 후 페이지 요소가 변경될 때 발생하는 에러를 무시하고 다음 루프 진행
            continue
        except Exception as e:
            print(f"에러 발생: {e}")


# --- 5. 게임 종료 및 결과 출력 ---
final_cps = cps.text
print("\n--- 게임 종료 ---")
print(f"최종 CPS (초당 쿠키 생산량): {final_cps}")

driver.quit()
