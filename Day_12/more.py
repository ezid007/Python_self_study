import requests
from bs4 import BeautifulSoup
import pandas as pd
from rich import print
from urllib.parse import urljoin  # URL을 안전하게 조합하기 위해 import
import time  # 서버에 부담을 주지 않기 위해 import

# --- 설정 변수 ---
BASE_URL = "https://news.ycombinator.com/"
# 시작 페이지 URL
current_page_url = urljoin(BASE_URL, "news") 
# 몇 페이지를 크롤링할지 지정
PAGES_TO_SCRAPE = 5

# 모든 페이지의 게시물을 담을 리스트
all_article_rows = []


# --- 메인 크롤링 루프 ---
for page_num in range(1, PAGES_TO_SCRAPE + 1):
    print(f"----- [ {page_num}페이지 크롤링 중... ] URL: {current_page_url} -----")

    # 1. 현재 페이지 요청 및 파싱
    response = requests.get(current_page_url)
    if response.status_code != 200:
        print(f"페이지를 가져오는 데 실패했습니다: {current_page_url}")
        break
    
    soup = BeautifulSoup(response.text, 'lxml')
    
    # 2. 현재 페이지의 게시물 정보를 수집 (이전 코드와 동일한 로직)
    item_rows = soup.find_all('tr', class_='athing')
    for row in item_rows:
        title_tag = row.find('span', class_='titleline').find('a')
        if not title_tag:
            continue
        
        title = title_tag.get_text()
        href = title_tag.get('href')

        metadata_row = row.find_next_sibling('tr')
        score = 0
        if metadata_row:
            score_tag = metadata_row.find('span', class_='score')
            if score_tag:
                score = int(score_tag.get_text().split()[0])

        all_article_rows.append({
            'title': title,
            'href': href,
            'score': score
        })

    # 3. 다음 페이지로 넘어갈 'More' 링크를 찾습니다.
    more_link_tag = soup.find('a', class_='morelink')

    # 4. 'More' 링크가 있으면 다음 페이지 URL을 업데이트, 없으면 루프 종료
    if more_link_tag:
        # 'news?p=2' 와 같은 상대 경로를 가져옵니다.
        next_relative_path = more_link_tag.get('href')
        # 기본 URL과 상대 경로를 조합하여 다음 페이지의 전체 URL을 만듭니다.
        current_page_url = urljoin(BASE_URL, next_relative_path)
        
        # ※ 예의 바른 크롤링: 다음 페이지를 요청하기 전에 잠시 기다립니다. (1초)
        print("1초 대기...")
        time.sleep(1)
    else:
        print("마지막 페이지입니다. 크롤링을 종료합니다.")
        break


# --- 최종 결과 출력 ---
# 수집된 모든 데이터를 데이터프레임으로 변환
df = pd.DataFrame(all_article_rows)

print("\n----- 최종 크롤링 결과 -----")
print(df)
print(f"\n총 {len(df)}개의 게시물을 수집했습니다.")