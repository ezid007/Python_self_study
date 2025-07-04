from tkinter import Tk, Canvas, PhotoImage, Label, Button
import math

# ---------------------------- CONSTANTS ------------------------------- #
PINK = "#e2979c"
RED = "#e7305b"
GREEN = "#9bdeac"
YELLOW = "#f7f5dd"
FONT_NAME = "Courier"
WORK_MIN = 25
SHORT_BREAK_MIN = 5
LONG_BREAK_MIN = 20
reps = 0
timer = None


# ---------------------------- TIMER RESET ------------------------------- #
def reset_timer():
    """
    reset + 초기화하다 + timer + 타이머
    이 함수는 'Reset' 버튼을 눌렀을 때 호출됩니다.
    """

    """
    global + 전역의
    함수 바깥에 있는 전역 변수 timer와 reps를
    이 함수 안에서 값을 바꾸겠다고 선언합니다.
    """
    global timer
    global reps

    """
    if + 만약 ~라면
    timer 변수의 값이 None + 없음(값이 할당되지 않음)이 아닐 때,
    즉, 타이머가 한 번이라도 시작해서 작동 중일 때만 아래 코드를 실행합니다.
    프로그램 시작 직후 'Reset'을 눌러도 오류가 나지 않도록 막아주는 안전장치입니다.
    """
    if timer is not None:
        """
        window.after_cancel(timer)
        tkinter의 기능으로, 이전에 window.after로 예약해 둔 타이머 작업을 취소합니다.
        'timer' 변수에는 "after#1"과 같은 타이머의 고유 ID가 저장되어 있습니다.
        이 코드를 통해 1초마다 반복되던 count_down 함수의 실행이 즉시 멈춥니다.
        """
        window.after_cancel(timer)
        """
        timer = None
        타이머를 취소했으니, 이제 활성화된 타이머가 없다는 의미로
        timer 변수를 다시 None 상태로 만들어 줍니다.
        """
        timer = None

    """
    canvas.itemconfig(timer_text, text="00:00")
    토마토 이미지 위에 있는 타이머 텍스트(timer_text)의 설정을 변경합니다.
    text 속성을 "00:00"으로 바꿔서 화면의 숫자를 초기화합니다.
    """
    canvas.itemconfig(timer_text, text="00:00")

    """
    title_label.config(text="Timer")
    화면 상단의 제목 레이블(title_label)의 설정을 변경합니다.
    "Work"나 "Break"로 바뀌었던 텍스트를 다시 기본값인 "Timer"로 되돌립니다.
    """
    title_label.config(text="Timer")

    """
    check_marks.config(text="")
    화면 하단의 체크마크(check_marks) 레이블의 설정을 변경합니다.
    text를 빈 문자열("")로 만들어서 쌓여있던 "✔" 표시를 모두 지웁니다.
    """
    check_marks.config(text="")

    """
    reps = 0
    (작업+휴식) 사이클 횟수를 기록하던 reps 변수를 0으로 초기화합니다.
    다음에 'Start' 버튼을 누르면 첫 번째 작업 세션부터 다시 시작하게 됩니다.
    """
    reps = 0


# ---------------------------- TIMER MECHANISM ------------------------------- #
def start_timer():
    """타이머를 시작하고, 현재 사이클에 따라 작업/휴식을 결정하는 함수"""
    global reps  # 1. 전역 변수 reps 사용 선언
    reps += 1  # 2. 사이클 카운터 증가

    # 3. 각 세션의 시간을 초 단위로 계산
    work_sec = WORK_MIN * 60
    short_break_sec = SHORT_BREAK_MIN * 60
    long_break_sec = LONG_BREAK_MIN * 60

    # 4. reps 값에 따라 어떤 세션을 시작할지 결정 (조건문)
    if reps % 8 == 0:  # 8번째 사이클(4번째 작업 + 4번째 휴식)인가?
        count_down(long_break_sec)
        title_label.config(text="Break", fg=RED)
    elif reps % 2 == 0:  # 짝수 번째 사이클인가? (휴식)
        count_down(short_break_sec)
        title_label.config(text="Break", fg=PINK)
    else:  # 홀수 번째 사이클인가? (작업)
        count_down(work_sec)
        title_label.config(text="Work", fg=GREEN)


# ---------------------------- COUNTDOWN MECHANISM ------------------------------- #
def count_down(count):
    """(재귀적으로) 1초마다 카운트를 줄여나가며 화면에 표시하고, 0이 되면 다음 타이머를 시작하는 함수"""

    # 1. '초'를 '분:초' 형식으로 변환
    count_min = math.floor(count / 60)
    count_sec = count % 60

    # 2. 캔버스 위 텍스트 업데이트
    canvas.itemconfig(timer_text, text=f"{count_min}:{count_sec:02d}")

    # 3. 카운트가 0보다 큰지 확인
    if count > 0:
        # 4. 1초 후에 자기 자신을 다시 호출 (재귀)
        global timer
        timer = window.after(1000, count_down, count - 1)
    else:
        # 5. 카운트가 0이 되었을 때의 동작
        marks = ""
        work_sessions = math.floor(reps / 2)
        for _ in range(work_sessions):
            marks += "✔"
        check_marks.config(text=marks)
        start_timer()  # 다음 세션 시작


# ---------------------------- UI SETUP ------------------------------- #

window = Tk()
window.title("Pomodoro")
window.config(padx=100, pady=50, bg=YELLOW)


title_label = Label(text="Timer", fg=GREEN, bg=YELLOW, font=(FONT_NAME, 50, "bold"))
title_label.grid(column=1, row=0)

canvas = Canvas(width=200, height=224, bg=YELLOW, highlightthickness=0)
tomato_img = PhotoImage(
    file="self_study\\Day_27_257_the_pomodoro_technique\\tomato.png"
)

canvas.create_image(100, 112, image=tomato_img)
timer_text = canvas.create_text(
    100, 130, text="00:00", fill="white", font=(FONT_NAME, 35, "bold")
)
canvas.grid(column=1, row=1)

start_button = Button(text="Start", command=start_timer)
start_button.grid(column=0, row=3)

reset_button = Button(text="Reset", command=reset_timer)
reset_button.grid(column=2, row=3)

check_marks = Label(text="", fg=GREEN, bg=YELLOW)
check_marks.grid(column=1, row=4)


window.mainloop()
