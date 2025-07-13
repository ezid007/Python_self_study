from question_model import Question
from quiz_brain import QuizBrain
from ui import QuizInterface
import requests
import html

QUESTION_AMOUNT = 3
parameters = {
    "amount": QUESTION_AMOUNT,
    "type": "boolean",
}


def get_new_quiz_brain():
    """
    API에서 새 질문들을 가져와 새로운 QuizBrain 객체를 생성하고 반환합니다.
    이 함수는 퀴즈를 새로 시작할 때마다 호출됩니다.
    """
    try:
        response = requests.get("https://opentdb.com/api.php", params=parameters)
        response.raise_for_status()
        data = response.json()["results"]
    except requests.exceptions.RequestException as e:
        print(f"API 요청 중 오류가 발생했습니다: {e}")
        data = []

    question_bank = []
    for question in data:
        question_text = html.unescape(question["question"])
        question_answer = question["correct_answer"]
        new_question = Question(question_text, question_answer)
        question_bank.append(new_question)

    return QuizBrain(question_bank)


def start_app():
    """
    애플리케이션을 처음 시작합니다.
    초기 퀴즈 객체를 만들고 GUI를 실행합니다.
    """
    # 첫 퀴즈를 위한 QuizBrain 객체 생성
    initial_quiz = get_new_quiz_brain()

    # QuizInterface를 생성할 때, 'get_new_quiz_brain' 함수를 콜백으로 전달합니다.
    # 이렇게 하면 ui.py에서 '다시 시작'이 필요할 때 이 함수를 호출할 수 있습니다.
    quiz_ui = QuizInterface(initial_quiz, restart_callback=get_new_quiz_brain)


# 이 파일이 직접 실행될 때만 start_app() 함수를 호출합니다.
if __name__ == "__main__":
    start_app()
