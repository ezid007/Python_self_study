from rich import print
import requests
from datetime import datetime
import os


# 이전에 사용한 API 키와 좌표를 그대로 사용합니다.
OWM_Endpoint = "https://api.openweathermap.org/data/2.5/forecast"
WEATHER_API_KEY = os.environ.get("WEATHER_API_KEY")

weather_params = {
    "lat": 37.4432147832698,
    "lon": 127.13859949509914,
    "appid": WEATHER_API_KEY,
    "units": "metric",  # 온도를 섭씨(℃)로 받기 위해 추가
    "lang": "kr",  # 날씨 설명을 한국어로 받기 위해 추가
}

# API 요청 보내기
api_session = requests.Session()
response = api_session.get(OWM_Endpoint, params=weather_params)
response.raise_for_status()  # 요청이 실패하면 에러를 발생시킴
weather_data = response.json()

# 오늘 날짜를 'YYYY-MM-DD' 형식의 문자열로 가져옵니다.
today_date_str = datetime.now().strftime("%Y-%m-%d")
print(f"[bold green]오늘({today_date_str})의 3시간 간격 날씨 예보[/bold green]")

# 받아온 예보 목록(list)에서 오늘 날짜에 해당하는 예보만 필터링하여 출력
for forecast in weather_data.get("list", []):
    # 예보 시간(dt_txt)이 오늘 날짜로 시작하는 경우에만 출력
    if forecast["dt_txt"].startswith(today_date_str):
        forecast_time = forecast["dt_txt"]
        temp = forecast["main"]["temp"]
        description = forecast["weather"][0]["description"]
        print(
            f"  - [cyan]{forecast_time}[/cyan] | 온도: [bold yellow]{temp}°C[/bold yellow] | 날씨: [bold sky_blue1]{description}[/bold sky_blue1]"
        )
