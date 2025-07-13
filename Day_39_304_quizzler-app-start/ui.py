from tkinter import *
from quiz_brain import QuizBrain
from typing import Callable

THEME_COLOR = "#375362"


class QuizInterface:
    def __init__(self, quiz_brain: QuizBrain, restart_callback: Callable[[], None]):
        self.quiz = quiz_brain
        self.restart_callback = restart_callback

        self.window = Tk()
        self.window.title("Quizzler")
        self.window.config(padx=20, pady=20, bg=THEME_COLOR)

        self.score_label = Label(
            text="Score: 0", fg="white", bg=THEME_COLOR, font=("Arial", 12)
        )
        self.score_label.grid(row=0, column=1)

        self.canvas = Canvas(width=300, height=250, bg="white")
        self.question_text = self.canvas.create_text(
            150,
            125,
            width=280,
            text="질문 텍스트",
            fill=THEME_COLOR,
            font=("Arial", 16, "italic"),
        )
        self.canvas.grid(row=1, column=0, columnspan=2, pady=50)

        # 이미지 버튼 로드 (경로 수정 금지)
        try:
            true_image = PhotoImage(
                file="self_study/Day_39_304_quizzler-app-start/images/true.png"
            )
            self.true_button = Button(
                image=true_image, highlightthickness=0, command=self.true_pressed
            )
            false_image = PhotoImage(
                file="self_study/Day_39_304_quizzler-app-start/images/false.png"
            )
            self.false_button = Button(
                image=false_image, highlightthickness=0, command=self.false_pressed
            )
        except TclError:
            print("이미지 파일을 찾을 수 없습니다. 텍스트 버튼을 사용합니다.")
            self.true_button = Button(
                text="True", command=self.true_pressed, width=10, height=3
            )
            self.false_button = Button(
                text="False", command=self.false_pressed, width=10, height=3
            )

        self.true_button.grid(row=2, column=0)
        self.false_button.grid(row=2, column=1)

        # '다시 시작' 버튼 생성
        self.restart_button = Button(
            text="다시 시작", font=("Arial", 10, "bold"), command=self.restart_quiz
        )
        self.restart_button_window = None  # 캔버스에 생성될 버튼의 ID 저장 변수

        self.get_next_question()
        self.window.mainloop()

    def get_next_question(self):
        """다음 문제를 가져와 화면에 표시합니다."""
        self.canvas.config(bg="white")
        if self.quiz.still_has_questions():
            q_text = self.quiz.next_question()
            self.canvas.itemconfig(self.question_text, text=q_text)
        else:
            self.show_final_score()

    def show_final_score(self):
        """퀴즈 종료 시 최종 점수를 표시하고 재시작 버튼을 활성화합니다."""
        final_text = (
            f"퀴즈 끝!\n최종 점수: {self.quiz.score}/{self.quiz.question_number}"
        )
        self.canvas.itemconfig(self.question_text, text=final_text)
        self.true_button.config(state="disabled")
        self.false_button.config(state="disabled")
        self.restart_button_window = self.canvas.create_window(
            150, 225, window=self.restart_button
        )

    def true_pressed(self):
        """'True' 버튼을 눌렀을 때 호출됩니다."""
        self.give_feedback(self.quiz.check_answer("True"))

    def false_pressed(self):
        """'False' 버튼을 눌렀을 때 호출됩니다."""
        self.give_feedback(self.quiz.check_answer("False"))

    def give_feedback(self, is_right: bool):
        """정답/오답 여부에 따라 시각적 피드백을 줍니다."""
        self.canvas.config(bg="green" if is_right else "red")
        self.score_label.config(text=f"Score: {self.quiz.score}")
        self.window.after(1000, self.get_next_question)

    def restart_quiz(self):
        """퀴즈를 내부적으로 초기화하고 UI를 리셋합니다."""
        # 1. main.py의 콜백 함수를 호출하여 QuizBrain을 리셋합니다.
        self.restart_callback()

        # 2. UI 요소들을 초기 상태로 리셋합니다.
        self.score_label.config(text="Score: 0")
        self.true_button.config(state="normal")
        self.false_button.config(state="normal")

        # 3. 캔버스에서 '다시 시작' 버튼을 제거합니다.
        if self.restart_button_window:
            self.canvas.delete(self.restart_button_window)
            self.restart_button_window = None

        # 4. 새 퀴즈의 첫 번째 문제를 가져옵니다.
        self.get_next_question()
