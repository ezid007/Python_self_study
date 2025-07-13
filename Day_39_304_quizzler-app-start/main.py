import requests
import html
from typing import List
from question_model import Question
from quiz_brain import QuizBrain
from ui import QuizInterface

# --- 상수 정의 ---
QUESTION_AMOUNT = 3
API_URL = "https://opentdb.com/api.php"
# Session 객체를 사용하여 여러 요청에 걸쳐 TCP 연결을 재사용합니다.
api_session = requests.Session()


def get_new_questions() -> List[Question]:
    """OpenTDB API에서 새로운 질문 목록을 가져와 Question 객체 리스트로 반환합니다."""
    parameters = {"amount": QUESTION_AMOUNT, "type": "boolean"}
    try:
        response = api_session.get(API_URL, params=parameters)
        response.raise_for_status()  # HTTP 오류가 발생하면 예외를 발생시킵니다.
        data = response.json().get("results", [])
    except requests.exceptions.RequestException as e:
        print(f"API 요청 중 오류가 발생했습니다: {e}")
        # API 요청 실패 시 data.py의 데이터를 대체 사용하거나 빈 리스트를 반환할 수 있습니다.
        # from data import question_data
        # data = question_data
        return []

    return [Question(html.unescape(q["question"]), q["correct_answer"]) for q in data]


def start_app():
    """애플리케이션을 시작하고 GUI를 설정합니다."""
    # 첫 퀴즈를 위한 질문 목록과 QuizBrain 객체 생성
    initial_questions = get_new_questions()
    if not initial_questions:
        print("질문을 가져오는데 실패하여 프로그램을 종료합니다.")
        return

    quiz_brain = QuizBrain(initial_questions)

    def restart_quiz_callback():
        """퀴즈 재시작을 위한 콜백 함수입니다."""
        new_questions = get_new_questions()
        if new_questions:
            quiz_brain.reset(new_questions)
        else:
            print("새로운 질문을 가져오는데 실패했습니다.")

    # QuizInterface를 생성하고, 재시작 콜백 함수를 전달합니다.
    quiz_ui = QuizInterface(quiz_brain, restart_callback=restart_quiz_callback)


if __name__ == "__main__":
    start_app()
