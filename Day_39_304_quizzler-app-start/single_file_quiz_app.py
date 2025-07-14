import requests
import html
from tkinter import *
from typing import List, Callable


# ==================================
# 1. 데이터 모델 (Recipe Card)
# ==================================
class Question:
    """문제 텍스트와 정답을 한 쌍으로 묶어주는 데이터 상자"""

    def __init__(self, q_text: str, q_answer: str):
        self.text = q_text
        self.answer = q_answer


# ==================================
# 2. 퀴즈 로직 (Kitchen Staff)
# ==================================
class QuizBrain:
    """퀴즈의 모든 핵심 규칙과 논리를 처리하는 두뇌"""

    def __init__(self, q_list: List[Question]):
        self.question_number = 0
        self.score = 0
        self.question_list = q_list
        self.current_question: Question = None

    def still_has_questions(self) -> bool:
        return self.question_number < len(self.question_list)

    def next_question(self) -> str:
        self.current_question = self.question_list[self.question_number]
        self.question_number += 1
        q_text = html.unescape(self.current_question.text)
        return f"Q.{self.question_number}: {q_text}"

    def check_answer(self, user_answer: str) -> bool:
        correct_answer = self.current_question.answer
        if user_answer.lower() == correct_answer.lower():
            self.score += 1
            return True
        return False


# ==================================
# 3. 사용자 인터페이스 (Front-of-House)
# ==================================
class QuizInterface:
    """모든 화면 요소를 만들고 사용자와 상호작용하는 역할"""

    THEME_COLOR = "#375362"

    def __init__(self, quiz_brain: QuizBrain, restart_callback: Callable[[], None]):
        self.quiz = quiz_brain
        self.restart_callback = restart_callback

        self.window = Tk()
        self.window.title("Quizzler")
        self.window.config(padx=20, pady=20, bg=self.THEME_COLOR)

        self.score_label = Label(text="Score: 0", fg="white", bg=self.THEME_COLOR)
        self.score_label.grid(row=0, column=1)

        self.canvas = Canvas(width=300, height=250, bg="white")
        self.question_text = self.canvas.create_text(
            150,
            125,
            width=280,
            text="Question text",
            fill=self.THEME_COLOR,
            font=("Arial", 20, "italic"),
        )
        self.canvas.grid(row=1, column=0, columnspan=2, pady=50)

        true_image = PhotoImage(
            file="self_study/Day_39_304_quizzler-app-start/images/true.png"
        )
        self.true_button = Button(
            image=true_image, highlightthickness=0, command=self.true_pressed
        )
        self.true_button.grid(row=2, column=0)

        false_image = PhotoImage(
            file="self_study/Day_39_304_quizzler-app-start/images/false.png"
        )
        self.false_button = Button(
            image=false_image, highlightthickness=0, command=self.false_pressed
        )
        self.false_button.grid(row=2, column=1)

        # '다시 시작' 버튼 생성 (나중에 표시)
        self.restart_button = Button(text="다시 시작", command=self.restart_quiz)
        self.restart_button_window = None

        self.get_next_question()
        self.window.mainloop()

    def get_next_question(self):
        self.canvas.config(bg="white")
        if self.quiz.still_has_questions():
            q_text = self.quiz.next_question()
            self.canvas.itemconfig(self.question_text, text=q_text)
        else:
            self.canvas.itemconfig(self.question_text, text="퀴즈가 끝났습니다!")
            self.true_button.config(state="disabled")
            self.false_button.config(state="disabled")
            # 다시 시작 버튼을 캔버스 위에 표시
            self.restart_button_window = self.canvas.create_window(
                150, 220, window=self.restart_button
            )

    def true_pressed(self):
        self.give_feedback(self.quiz.check_answer("True"))

    def false_pressed(self):
        self.give_feedback(self.quiz.check_answer("False"))

    def give_feedback(self, is_right):
        if is_right:
            self.canvas.config(bg="green")
        else:
            self.canvas.config(bg="red")
        self.score_label.config(text=f"Score: {self.quiz.score}")
        self.window.after(1000, self.get_next_question)

    def restart_quiz(self):
        # UI 리셋
        self.true_button.config(state="normal")
        self.false_button.config(state="normal")
        self.canvas.delete(self.restart_button_window)  # 다시 시작 버튼 숨기기

        # 콜백 함수를 실행해 새로운 퀴즈 로직으로 교체
        self.quiz = self.restart_callback()
        self.score_label.config(text=f"Score: {self.quiz.score}")
        self.get_next_question()


# ==================================
# 4. 앱 실행 (Head Chef)
# ==================================
def get_new_quiz_brain() -> QuizBrain:
    """API에서 새 질문을 가져와 새로운 QuizBrain 객체를 생성"""
    response = requests.get(
        "https://opentdb.com/api.php", params={"amount": 10, "type": "boolean"}
    )
    response.raise_for_status()
    question_data = response.json()["results"]

    question_bank = [
        Question(q["question"], q["correct_answer"]) for q in question_data
    ]
    return QuizBrain(question_bank)


def start_app():
    """앱을 처음 시작하는 함수"""
    initial_quiz = get_new_quiz_brain()
    QuizInterface(initial_quiz, restart_callback=get_new_quiz_brain)


# 프로그램 시작점
if __name__ == "__main__":
    start_app()
