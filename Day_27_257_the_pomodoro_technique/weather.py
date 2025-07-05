import requests
from datetime import datetime, timedelta

# pomodoro_weather.py에 있는 상수와 변수를 그대로 활용합니다.
KMA_API_KEY = "Qm%2BeM3tI2A%2FndGQSlFsYDJhFeHx7FfFLbfNGSRzxNzEtemy3O%2BK4pncX%2FbgykEhQEmr%2FLhQP7aLBXctq6vbznw%3D%3D"  # 본인의 API 키로 교체하세요.
CITY_GRID_COORDS = {
    "Seoul": (60, 127),
    "Seongnam": (62, 123),
    # ... 다른 도시들
}

def get_kma_forecast(city: str):
    """기상청 초단기예보 API로 앞으로의 날씨 예보를 가져옵니다."""
    if KMA_API_KEY == "YOUR_KMA_API_KEY":
        return "API 키 필요"

    # 도시 이름으로 격자 좌표를 찾습니다. 없으면 서울을 기본값으로 사용합니다.
    nx, ny = CITY_GRID_COORDS.get(city, CITY_GRID_COORDS["Seoul"])

    # --- API 요청을 위한 base_date, base_time 계산 ---
    now = datetime.now()
    # 초단기예보는 매시 30분에 생성되어 45분부터 API로 제공됩니다.
    # 안정적인 데이터 수신을 위해 현재 시간에서 1시간을 빼고, 분은 30분으로 고정합니다.
    base_time_dt = now - timedelta(hours=1)
    base_date = base_time_dt.strftime('%Y%m%d')
    base_time = base_time_dt.strftime('%H30')

    # API 요청 URL
    api_url = (
        "http://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getUltraSrtFcst"
        f"?serviceKey={KMA_API_KEY}&pageNo=1&numOfRows=60&dataType=JSON"
        f"&base_date={base_date}&base_time={base_time}&nx={nx}&ny={ny}"
    )

    try:
        response = requests.get(api_url, timeout=10)
        response.raise_for_status()  # 요청이 실패하면 예외를 발생시킵니다.
        
        items = response.json()["response"]["body"]["items"]["item"]
        
        # 예보 시간별로 데이터를 정리할 딕셔너리
        forecast_data = {}
        for item in items:
            fcst_time = item["fcstTime"]
            # 예보 시간(fcstTime)을 키로 사용하여 데이터 그룹화
            if fcst_time not in forecast_data:
                forecast_data[fcst_time] = {}
            forecast_data[fcst_time][item["category"]] = item["fcstValue"]

        # 가장 빠른 예보 시간의 데이터를 가져옵니다.
        first_forecast_time = sorted(forecast_data.keys())[0]
        weather = forecast_data[first_forecast_time]

        # --- 날씨 정보 해석 ---
        temp = f"{weather.get('T1H')}°C"
        pty_code = weather.get("PTY", "0") # 강수형태
        sky_code = weather.get("SKY", "1") # 하늘상태

        # PTY(강수형태) 코드: 없음(0), 비(1), 비/눈(2), 눈(3), 빗방울(5), 빗방울/눈날림(6), 눈날림(7)
        pty_map = {"0": "", "1": "비", "2": "비/눈", "3": "눈", "5": "빗방울", "6": "빗방울눈날림", "7": "눈날림"}
        
        # SKY(하늘상태) 코드: 맑음(1), 구름많음(3), 흐림(4)
        sky_map = {"1": "맑음", "3": "구름많음", "4": "흐림"}

        # 강수 정보(비, 눈)가 있으면 하늘 상태보다 우선하여 표시합니다.
        if pty_code != "0":
            weather_status = pty_map.get(pty_code, "정보없음")
        else:
            weather_status = sky_map.get(sky_code, "정보없음")
            
        return f"{weather_status} {temp}"

    except requests.exceptions.RequestException:
        return "날씨 로드 실패"
    except (KeyError, TypeError, IndexError):
        return "정보 파싱 오류"


# --- 함수 사용 예제 ---
if __name__ == "__main__":
    # 현재 위치인 성남시의 날씨 예보를 가져옵니다.
    current_city = "Seongnam" 
    forecast = get_kma_forecast(current_city)
    print(f"'{current_city}'의 날씨 예보: {forecast}")
    
    # 서울의 날씨 예보
    forecast_seoul = get_kma_forecast("Seoul")
    print(f"'Seoul'의 날씨 예보: {forecast_seoul}")