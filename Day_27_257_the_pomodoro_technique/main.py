"""
Pomodoro Technique Timer
이 프로그램은 Tkinter를 사용하여 만든 간단한 뽀모도로 타이머 애플리케이션입니다.
작업, 짧은 휴식, 긴 휴식 사이클을 자동으로 관리하여 집중력 향상을 돕습니다.
"""

from tkinter import Tk, Canvas, PhotoImage, Label, Button
import math

# ---------------------------- 상수 (CONSTANTS) ------------------------------- #
# 상수는 프로그램 전체에서 변하지 않는 값을 저장하며, 대문자로 작성하는 것이 관례입니다.
PINK = "#e2979c"
RED = "#e7305b"
GREEN = "#9bdeac"
YELLOW = "#f7f5dd"
FONT_NAME = "Courier"
WORK_MIN = 25
SHORT_BREAK_MIN = 5
LONG_BREAK_MIN = 20
reps = 0  # 현재 사이클(작업/휴식) 횟수를 저장하는 변수
timer = None  # window.after()의 ID를 저장할 변수. 타이머 취소에 사용됩니다.


# ---------------------------- 타이머 리셋 (TIMER RESET) ------------------------------- #
def reset_timer():
    """
    reset + 초기화하다: 타이머를 중지하고 모든 상태를 초기 값으로 되돌립니다.
    """
    global timer, reps  # 전역(global) 변수 timer와 reps의 값을 변경하기 위해 선언합니다.

    # window.after_cancel: 이전에 예약된 타이머 작업을 취소합니다.
    # timer 변수에 저장된 ID를 사용하여 실행 중인 count_down 함수를 멈춥니다.
    if timer:  # timer에 유효한 ID가 있을 때만 (타이머가 작동 중일 때만) 실행합니다.
        window.after_cancel(timer)
        timer = None  # 타이머를 취소했으므로 변수를 다시 None으로 설정합니다.

    # UI를 초기 상태로 설정합니다.
    canvas.itemconfig(timer_text, text="00:00")  # 타이머 텍스트를 "00:00"으로 변경
    title_label.config(text="Timer", fg=GREEN)  # 제목을 "Timer"로, 색상은 녹색으로 변경
    check_marks.config(text="")  # 체크마크를 모두 제거
    reps = 0  # 사이클 횟수를 0으로 초기화


# ---------------------------- 타이머 메커니즘 (TIMER MECHANISM) ------------------------------- #
def start_timer():
    """
    start + 시작하다: 'Start' 버튼을 누르면 호출됩니다.
    현재 사이클(reps)에 따라 작업 또는 휴식 타이머를 시작합니다.
    """
    global reps  # 전역 변수 reps의 값을 변경하기 위해 선언합니다.
    reps += 1  # 사이클 횟수를 1 증가시킵니다.

    work_sec = WORK_MIN * 60
    short_break_sec = SHORT_BREAK_MIN * 60
    long_break_sec = LONG_BREAK_MIN * 60

    # reps 값에 따라 어떤 세션을 시작할지 결정합니다.
    if reps % 8 == 0:  # 8번째 사이클 (4번째 휴식) -> 긴 휴식
        title_label.config(text="Break", fg=RED)
        count_down(long_break_sec)
    elif reps % 2 == 0:  # 2, 4, 6번째 사이클 -> 짧은 휴식
        title_label.config(text="Break", fg=PINK)
        count_down(short_break_sec)
    else:  # 1, 3, 5, 7번째 사이클 -> 작업
        # 작업 세션이 끝난 직후 (즉, 휴식이 시작될 때) 체크마크를 추가합니다.
        if reps > 1:
            work_sessions = math.floor((reps - 1) / 2)
            check_marks.config(text="✔" * work_sessions)
        title_label.config(text="Work", fg=GREEN)
        count_down(work_sec)


# ---------------------------- 카운트다운 메커니즘 (COUNTDOWN MECHANISM) ------------------------------- #
def count_down(count):
    """
    count down + 숫자를 거꾸로 세다: 1초마다 화면의 시간을 업데이트합니다.
    count가 0이 되면 다음 사이클을 시작합니다.
    """
    count_min = math.floor(count / 60)  # 남은 시간을 '분'으로 변환
    count_sec = count % 60  # '분'으로 변환하고 남은 '초'

    # 캔버스 위 텍스트를 "분:초" 형식으로 업데이트합니다. (예: 05:09)
    # :02d는 정수를 항상 두 자리로 표시하고, 한 자리 수일 경우 앞에 0을 붙여줍니다.
    canvas.itemconfig(timer_text, text=f"{count_min}:{count_sec:02d}")

    if count > 0:
        # 0보다 크면, 1초(1000ms) 후에 자기 자신을 다시 호출하여 카운트를 1 줄입니다.
        global timer
        timer = window.after(1000, count_down, count - 1)
    else:
        # 카운트가 0이 되면, 다음 세션을 시작합니다.
        start_timer()


# ---------------------------- UI 설정 (UI SETUP) ------------------------------- #
window = Tk()
window.title("Pomodoro")
# padx, pady는 창의 내부 여백을, bg는 배경색을 설정합니다.
window.config(padx=100, pady=50, bg=YELLOW)

# 제목 레이블(Label)
title_label = Label(text="Timer", fg=GREEN, bg=YELLOW, font=(FONT_NAME, 50, "bold"))
title_label.grid(column=1, row=0)  # grid는 위젯을 격자 형태로 배치합니다.

# 캔버스(Canvas) 위젯은 이미지나 도형, 텍스트를 그릴 때 사용합니다.
canvas = Canvas(width=200, height=224, bg=YELLOW, highlightthickness=0)
# PhotoImage로 이미지 파일을 불러옵니다. 스크립트와 같은 폴더에 tomato.png가 있어야 합니다.
tomato_img = PhotoImage(
    file="self_study\\Day_27_257_the_pomodoro_technique\\tomato.png"
)
canvas.create_image(100, 112, image=tomato_img)  # 캔버스 중앙에 이미지 생성
# 캔버스 위에 텍스트 생성
timer_text = canvas.create_text(
    100, 130, text="00:00", fill="white", font=(FONT_NAME, 35, "bold")
)
canvas.grid(column=1, row=1)

# 시작(Start) 버튼
# command에 함수를 연결하면 버튼을 누를 때 해당 함수가 실행됩니다.
start_button = Button(text="Start", highlightthickness=0, command=start_timer)
start_button.grid(column=0, row=3)

# 리셋(Reset) 버튼
reset_button = Button(text="Reset", highlightthickness=0, command=reset_timer)
reset_button.grid(column=2, row=3)

# 체크마크(✔) 레이블
check_marks = Label(fg=GREEN, bg=YELLOW, font=(FONT_NAME, 15, "bold"))
check_marks.grid(column=1, row=4)

window.mainloop()  # 프로그램 창이 닫히기 전까지 계속 실행되도록 합니다.
