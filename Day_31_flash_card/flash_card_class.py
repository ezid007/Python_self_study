import tkinter as tk
import pandas as ps
import random

# --- 상수 정의 ---
# 자주 사용되는 값들은 맨 위에 상수로 빼두면 관리하기 편합니다.
BACKGROUND_COLOR = "#B1DDC6"
FONT_LANGUAGE = ("Ariel", 40, "italic")
FONT_WORD = ("Ariel", 60, "bold")
CSV_PATH_ORIGINAL = "self_study/Day_31_flash_card/data/eng_words.csv"
CSV_PATH_TO_LEARN = "self_study/Day_31_flash_card/data/words_to_learn.csv"
IMG_PATH_FRONT = "self_study/Day_31_flash_card/images/card_front.png"
IMG_PATH_BACK = "self_study/Day_31_flash_card/images/card_back.png"
IMG_PATH_RIGHT = "self_study/Day_31_flash_card/images/right.png"
IMG_PATH_WRONG = "self_study/Day_31_flash_card/images/wrong.png"


# --- 플래시 카드 애플리케이션 클래스 ---
# 모든 변수와 함수를 하나의 클래스로 묶어 관리합니다.
class FlashCardApp:
    def __init__(self, window):
        """
        클래스가 처음 생성될 때 실행되는 초기화 함수입니다.
        앱에 필요한 모든 변수를 설정하고 UI를 생성합니다.
        """
        # 1. 기본 윈도우 설정
        self.window = window
        self.window.title("Flashy")
        self.window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

        # 2. 클래스 내부 변수 초기화 (global 키워드 불필요)
        self.to_learn = self._load_data()  # 학습할 단어 목록
        self.current_card = {}  # 현재 화면에 표시된 카드
        self.flip_timer = None  # 카드 뒤집기 타이머 ID

        # 3. UI 위젯 생성
        self._create_widgets()

        # 4. 창 닫기 버튼('X')을 눌렀을 때의 동작 설정 (최적화 1)
        self.window.protocol("WM_DELETE_WINDOW", self.on_closing)

        # 5. 첫 카드 표시
        self.next_card()

    def _load_data(self):
        """
        학습할 단어 데이터를 CSV 파일에서 불러옵니다.
        학습 기록이 있으면 그 파일을, 없으면 원본 파일을 사용합니다.
        """
        try:
            data = ps.read_csv(CSV_PATH_TO_LEARN)
        except FileNotFoundError:
            data = ps.read_csv(CSV_PATH_ORIGINAL)
        # 클래스 내부 함수이므로 self를 통해 접근합니다.
        return data.to_dict(orient="records")

    def _create_widgets(self):
        """
        화면에 필요한 모든 UI 요소(캔버스, 버튼 등)를 생성하고 배치합니다.
        """
        # 캔버스 및 배경 이미지 설정
        self.canvas = tk.Canvas(
            width=800, height=526, bg=BACKGROUND_COLOR, highlightthickness=0
        )
        self.card_front_img = tk.PhotoImage(file=IMG_PATH_FRONT)
        self.card_back_img = tk.PhotoImage(file=IMG_PATH_BACK)
        self.card_background = self.canvas.create_image(
            400, 263, image=self.card_front_img
        )
        self.canvas.grid(row=0, column=0, columnspan=2)

        # 텍스트 설정
        self.card_title = self.canvas.create_text(400, 150, text="", font=FONT_LANGUAGE)
        self.card_word = self.canvas.create_text(400, 263, text="", font=FONT_WORD)

        # 버튼 설정
        wrong_img = tk.PhotoImage(file=IMG_PATH_WRONG)
        self.wrong_button = tk.Button(
            image=wrong_img, highlightthickness=0, command=self.next_card
        )
        self.wrong_button.image = wrong_img  # 참조 유지
        self.wrong_button.grid(row=1, column=0)

        right_img = tk.PhotoImage(file=IMG_PATH_RIGHT)
        self.right_button = tk.Button(
            image=right_img, highlightthickness=0, command=self.is_known
        )
        self.right_button.image = right_img  # 참조 유지
        self.right_button.grid(row=1, column=1)

    def next_card(self):
        """다음 카드를 보여주는 함수"""
        # 최적화 3: 학습 완료 시 예외 처리
        if not self.to_learn:
            self.show_completion_message()
            return

        # self.flip_timer처럼 클래스 변수로 접근합니다.
        if self.flip_timer:
            self.window.after_cancel(self.flip_timer)

        self.current_card = random.choice(self.to_learn)
        self.canvas.itemconfig(self.card_title, text="English", fill="black")
        self.canvas.itemconfig(
            self.card_word, text=self.current_card["English"], fill="black"
        )
        self.canvas.itemconfig(self.card_background, image=self.card_front_img)
        self.flip_timer = self.window.after(3000, self.flip_card)

    def flip_card(self):
        """카드를 뒤집어 한국어 뜻을 보여주는 함수"""
        self.canvas.itemconfig(self.card_title, text="Korean", fill="white")
        self.canvas.itemconfig(
            self.card_word, text=self.current_card["Korean"], fill="white"
        )
        self.canvas.itemconfig(self.card_background, image=self.card_back_img)

    def is_known(self):
        """'아는 단어' 처리 함수"""
        # 최적화 1: 이제 메모리에서만 제거하고 파일 저장은 하지 않습니다.
        if self.current_card in self.to_learn:
            self.to_learn.remove(self.current_card)

        self.next_card()

    def on_closing(self):
        """
        최적화 1: 창이 닫힐 때 남은 단어들을 파일에 한 번만 저장합니다.
        """
        data_to_save = ps.DataFrame(self.to_learn)
        data_to_save.to_csv(CSV_PATH_TO_LEARN, index=False)
        self.window.destroy()

    def show_completion_message(self):
        """최적화 3: 모든 단어 학습 완료 시 메시지를 표시하는 함수"""
        self.canvas.itemconfig(self.card_background, image=self.card_front_img)
        self.canvas.itemconfig(self.card_title, text="Congratulations!", fill="blue")
        self.canvas.itemconfig(
            self.card_word, text="You've learned all the words.", fill="blue"
        )
        # 버튼 비활성화
        self.right_button.config(state="disabled")
        self.wrong_button.config(state="disabled")


# --- 프로그램 실행 ---
# 이 스크립트 파일이 직접 실행될 때만 아래 코드가 동작하도록 합니다.
if __name__ == "__main__":
    # 1. 메인 윈도우 생성
    root = tk.Tk()
    # 2. 우리 앱 클래스의 인스턴스(실체)를 생성
    app = FlashCardApp(root)
    # 3. 윈도우의 이벤트 루프 시작
    root.mainloop()
