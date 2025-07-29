import os
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By


# --- 함수 정의 ---
def print_elements(description, elements):
    """
    찾아낸 요소들을 보기 좋게 출력하는 함수입니다.

    Args:
        description (str): 현재 어떤 선택자를 테스트하는지에 대한 설명
        elements (list): find_elements로 찾아낸 웹 요소들의 리스트
    """
    print(f"\n--- {description} ---")
    if elements:
        print(f"✅ 총 {len(elements)}개의 요소를 찾았습니다.")
        for index, el in enumerate(elements):
            # 요소의 태그 이름과 텍스트 내용을 출력합니다.
            print(f"  [{index+1}] <{el.tag_name}> {el.text.strip()}")
    else:
        print("❌ 해당하는 요소를 찾지 못했습니다.")


# --- 메인 코드 실행 ---
# with 문을 사용하여 드라이버를 안전하게 관리합니다.
with webdriver.Chrome(service=Service(ChromeDriverManager().install())) as driver:
    # 현재 파이썬 파일의 위치를 기준으로 practice.html 파일의 절대 경로를 계산합니다.
    # 이렇게 하면 어떤 컴퓨터에서 실행해도 파일 경로가 올바르게 설정됩니다.
    html_file_path = (
        Path(__file__).parent / "practice.html"
    )

    # 로컬 HTML 파일을 엽니다. 'file://' 프로토콜을 사용합니다.
    driver.get(html_file_path.as_uri())

    print("=" * 50)
    print("CSS 선택자 실습을 시작합니다.")
    print("=" * 50)

    # 1. 기본 선택자 실습
    print_elements(
        "타입 선택자: 모든 <li> 요소 찾기", driver.find_elements(By.CSS_SELECTOR, "li")
    )
    print_elements(
        "클래스 선택자: 'title' 클래스를 가진 모든 요소 찾기",
        driver.find_elements(By.CSS_SELECTOR, ".title"),
    )
    print_elements(
        "ID 선택자: 'login-form-area' ID를 가진 요소 찾기",
        driver.find_elements(By.CSS_SELECTOR, "#login-form-area"),
    )

    # 2. 관계 선택자 실습
    print_elements(
        "후손 선택자: 'article-list' 안에 있는 모든 <a> 요소 찾기",
        driver.find_elements(By.CSS_SELECTOR, "#article-list a"),
    )
    print_elements(
        "자식 선택자: 'input-group'의 직계 자식인 <label> 요소 찾기",
        driver.find_elements(By.CSS_SELECTOR, ".input-group > label"),
    )
    print_elements(
        "인접 형제 선택자: <h2> 바로 다음에 오는 <p> 요소 찾기",
        driver.find_elements(By.CSS_SELECTOR, "h2 + p"),
    )

    # 3. 속성 선택자 실습
    print_elements(
        "속성 존재 선택자: 'placeholder' 속성을 가진 모든 <input> 찾기",
        driver.find_elements(By.CSS_SELECTOR, "input[placeholder]"),
    )
    print_elements(
        "속성 값 일치 선택자: type이 'password'인 <input> 찾기",
        driver.find_elements(By.CSS_SELECTOR, "input[type='password']"),
    )
    print_elements(
        "속성 값 포함 선택자: class에 'btn'이 포함된 <button> 찾기",
        driver.find_elements(By.CSS_SELECTOR, "button[class*='btn']"),
    )
    print_elements(
        "속성 값 시작 선택자: data-category가 'news'로 시작하는 <li> 찾기",
        driver.find_elements(By.CSS_SELECTOR, "li[data-category^='news']"),
    )

    # 4. 가상 클래스 선택자 실습
    print_elements(
        "첫 번째 자식 선택자: 'article-list'의 첫 번째 <li> 찾기",
        driver.find_elements(By.CSS_SELECTOR, "#article-list li:first-child"),
    )
    print_elements(
        "n번째 자식 선택자: 'article-list'의 3번째 <li> 찾기",
        driver.find_elements(By.CSS_SELECTOR, "#article-list li:nth-child(3)"),
    )

    # 5. 복합 선택자 실습
    print_elements(
        "복합 선택자: 'article-item'이면서 'special' 클래스도 가진 <li> 찾기",
        driver.find_elements(By.CSS_SELECTOR, "li.article-item.special"),
    )

    print("\n" + "=" * 50)
    print("실습이 모두 종료되었습니다.")
    print("=" * 50)
