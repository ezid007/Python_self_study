from rich import print
import csv
import pandas as pd


# 요청하신 대로 기존 데이터 스타일을 그대로 사용합니다.
weather_data = [
    ['day', 'temp', 'condition'],
    ['Monday', 12, 'Sunny'],
    ['Tuesday', 14, 'Rain'],
    ['Wednesday', 15, 'Rain'],
    ['Thursday', 14, 'Cloudy'],
    ['Friday', 21, 'Sunny'],
    ['Saturday', 22, 'Sunny'],
    ['Sunday', 24, 'Sunny']
]

# 1. 리스트 데이터를 사용하여 DataFrame을 생성합니다.
#    - 데이터 부분: 리스트의 첫 번째 요소를 제외한 나머지 (weather_data[1:])
#    - 컬럼(열) 이름: 리스트의 첫 번째 요소 (weather_data[0])
df = pd.DataFrame(data=weather_data[1:], columns=weather_data[0])

# 2. DataFrame을 CSV 파일로 저장합니다.
file_name = 'weather_from_list.csv'
df.to_csv(file_name, index=False, encoding='utf-8')

print(f"'{file_name}' 파일이 리스트 데이터를 직접 사용하여 성공적으로 생성되었습니다.")

# (참고) 생성된 DataFrame 확인
print("\n--- 생성된 DataFrame ---")
print(df)
