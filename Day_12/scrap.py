from bs4 import BeautifulSoup
from rich import print
import requests
import pandas as pd
import os

os.system('cls')

# 1. 웹페이지 요청 및 파싱 (기존과 동일)
url = requests.get('https://news.ycombinator.com/news')
# .text 속성은 requests가 추측한 인코딩으로 디코딩해주므로 더 편리합니다.
soup = BeautifulSoup(url.text, 'lxml')

# 2. '행' 데이터를 담을 비어있는 리스트로 초기화
article_rows = []

# 3. 각 게시물의 제목/링크가 담긴 tr 태그(class='athing')를 모두 찾습니다.
item_rows = soup.find_all('tr', class_='athing')

# 4. 각 게시물 정보(tr)를 순회합니다.
for row in item_rows:
    # 제목과 링크 추출
    title_tag = row.find('span', class_='titleline').find('a')
    if not title_tag:
        continue # 'a' 태그가 없는 경우는 건너뜁니다.
    
    title = title_tag.get_text()
    href = title_tag.get('href')

    # 점수 추출 (바로 다음 형제 tr 태그에서 찾아야 함)
    # .find_next_sibling()을 사용해 해당 게시물의 점수 정보를 담은 tr을 찾습니다.
    metadata_row = row.find_next_sibling('tr')
    score = 0  # 기본값을 0으로 설정
    if metadata_row:
        score_tag = metadata_row.find('span', class_='score')
        # 점수가 있는 게시물(score_tag가 발견된 경우)에만 값을 추출합니다.
        if score_tag:
            score = int(score_tag.get_text().split()[0])

    # 5. 추출한 정보를 하나의 딕셔너리로 묶습니다.
    article_dict = {
        'title': title,
        'href': href,
        'score': score
    }

    # 6. 완성된 딕셔너리를 리스트에 추가합니다.
    article_rows.append(article_dict)

# 결과 확인 (딕셔너리의 리스트를 판다스 데이터프레임으로 변환하여 출력)
df = pd.DataFrame(article_rows)
print(df)