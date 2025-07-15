# -*- coding: utf-8 -*-

# 필요한 라이브러리들을 가져옵니다.
# requests: HTTP 요청을 쉽게 보낼 수 있게 해주는 라이브러리
# datetime: 날짜와 시간 관련 작업을 처리하는 라이브러리
# os: 운영체제와 상호작용하여 환경 변수 등을 가져오는 라이브러리
# dotenv: .env 파일에서 환경 변수를 불러오는 라이브러리
import requests
from datetime import datetime
import os
from dotenv import load_dotenv


def setup_environment():
    """
    .env 파일로부터 환경 변수를 불러와 설정합니다.
    이 함수는 프로그램 실행 시 가장 먼저 호출되어야 합니다.
    성공적으로 변수를 불러오면 설정 값들을 담은 딕셔너리를 반환합니다.
    """
    # .env 파일에 정의된 키-값 쌍을 현재 환경으로 불러옵니다.
    load_dotenv()

    # .env 파일에서 필요한 설정 값들을 가져옵니다.
    # os.getenv()를 사용하여 키가 없을 경우 None을 반환하여 오류를 방지합니다.
    config = {
        "app_id": os.getenv("NT_APP_ID"),
        "api_key": os.getenv("NT_API_KEY"),
        "sheet_endpoint": os.getenv("SHEET_ENDPOINT"),
        "token": os.getenv("TOKEN"),
        "gender": os.getenv("GENDER"),
        "weight_kg": os.getenv("WEIGHT_KG"),
        "height_cm": os.getenv("HEIGHT_CM"),
        "age": os.getenv("AGE"),
    }

    # 필수 환경 변수 중 하나라도 없는 경우, 프로그램을 중단시킵니다.
    if not all(
        [config["app_id"], config["api_key"], config["sheet_endpoint"], config["token"]]
    ):
        print(
            "오류: .env 파일에 필수 환경 변수(NT_APP_ID, NT_API_KEY, SHEET_ENDPOINT, TOKEN)가 설정되지 않았습니다."
        )
        exit()  # 프로그램 종료

    return config


def get_exercise_data(config, user_query):
    """
    Nutritionix API를 호출하여 사용자가 입력한 운동 정보를 분석합니다.

    Args:
        config (dict): API 키, 사용자 정보 등이 담긴 설정 딕셔너리
        user_query (str): 사용자가 입력한 운동 내용 (예: "ran 3 miles and walked for 20 minutes")

    Returns:
        list: 분석된 각 운동의 상세 정보가 담긴 리스트. 오류 발생 시 None을 반환합니다.
    """
    # Nutritionix API의 자연어 처리 엔드포인트 주소
    exercise_endpoint = "https://trackapi.nutritionix.com/v2/natural/exercise"

    # API 요청 시 헤더에 인증 정보를 담습니다.
    headers = {
        "x-app-id": config["app_id"],
        "x-app-key": config["api_key"],
    }

    # API에 보낼 파라미터들을 딕셔너리 형태로 구성합니다.
    parameters = {
        "query": user_query,
        "gender": config["gender"],
        "weight_kg": config["weight_kg"],
        "height_cm": config["height_cm"],
        "age": config["age"],
    }

    try:
        # requests.post를 사용하여 Nutritionix API에 POST 요청을 보냅니다.
        response = requests.post(exercise_endpoint, json=parameters, headers=headers)
        # HTTP 응답 코드가 200(성공)이 아닐 경우, 예외를 발생시킵니다.
        response.raise_for_status()
        # 응답 받은 JSON 데이터를 파싱하여 'exercises' 키에 해당하는 값을 반환합니다.
        return response.json().get("exercises")
    except requests.exceptions.RequestException as e:
        # 네트워크 오류, HTTP 오류 등 API 요청 관련 문제가 발생했을 경우
        print(f"Nutritionix API 요청 오류: {e}")
        return None
    except Exception as e:
        # 기타 예외 처리
        print(f"데이터 처리 중 알 수 없는 오류 발생: {e}")
        return None


def record_workout_to_sheet(config, exercise_data):
    """
    분석된 운동 데이터를 Sheety API를 통해 구글 시트에 기록합니다.

    Args:
        config (dict): Sheety 엔드포인트, 토큰 등이 담긴 설정 딕셔너리
        exercise_data (dict): 기록할 단일 운동의 상세 정보
    """
    # 현재 날짜와 시간을 구글 시트에 맞는 형식으로 변환합니다.
    today_date = datetime.now().strftime("%d/%m/%Y")
    now_time = datetime.now().strftime("%X")

    # Sheety API로 보낼 데이터를 딕셔너리 형태로 구성합니다.
    # 구글 시트의 열 이름(date, time 등)과 일치해야 합니다.
    sheet_inputs = {
        "workout": {
            "date": today_date,
            "time": now_time,
            "exercise": exercise_data[
                "name"
            ].title(),  # 운동 이름을 첫 글자 대문자로 변경
            "duration": exercise_data["duration_min"],
            "calories": exercise_data["nf_calories"],
        }
    }

    # Bearer Token 인증 방식을 위한 헤더 설정
    bearer_headers = {"Authorization": f"Bearer {config['token']}"}

    try:
        # Sheety API에 POST 요청을 보내 데이터를 추가합니다.
        sheet_response = requests.post(
            config["sheet_endpoint"], json=sheet_inputs, headers=bearer_headers
        )
        # HTTP 응답 코드가 200(성공)이 아닐 경우, 예외를 발생시킵니다.
        sheet_response.raise_for_status()
        print(f"'{exercise_data['name'].title()}' 운동 기록 완료!")
    except requests.exceptions.RequestException as e:
        # Sheety API 요청 관련 문제가 발생했을 경우
        print(f"Sheety API 요청 오류: {e}")
        print("Sheety 응답 내용:", sheet_response.text)


def main():
    """
    프로그램의 메인 로직을 실행하는 함수입니다.
    """
    # 1. 환경 변수 설정
    config = setup_environment()

    # 2. 사용자로부터 운동 내용 입력받기
    user_query = input(
        "오늘 어떤 운동을 하셨나요? (예: ran 2km and walked for 15 minutes): "
    )

    # 3. Nutritionix API를 통해 운동 데이터 분석
    exercises = get_exercise_data(config, user_query)

    # 4. 분석된 운동 데이터를 구글 시트에 기록
    if exercises:  # 분석된 운동 데이터가 있을 경우에만 실행
        print(f"\n총 {len(exercises)}개의 운동을 기록합니다...")
        for exercise in exercises:
            record_workout_to_sheet(config, exercise)
        print("\n모든 운동 기록이 성공적으로 완료되었습니다. 🎉")
    else:
        print("\n분석된 운동이 없으므로 구글 시트에 기록하지 않습니다.")


# 이 스크립트 파일이 직접 실행될 때만 main() 함수를 호출합니다.
# 다른 파일에서 이 파일을 모듈로 불러올 경우에는 실행되지 않습니다.
if __name__ == "__main__":
    main()
