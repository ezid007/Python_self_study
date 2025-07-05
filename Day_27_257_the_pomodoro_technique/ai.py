from code_data import IMG_DATA, SOUND_DATA
import tkinter
import math
import base64
import pygame  # [수정] pygame 라이브러리를 가져옵니다.
import io


# ---------------------------- 상수 (CONSTANTS) ------------------------------- #
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

# ---------------------------- 사운드 관리 (SOUND MANAGEMENT) ------------------------------- #
sound_obj = None


def _load_sound_obj():
    """
    [수정] .wav 오디오 데이터를 pygame.mixer.Sound 객체로 메모리에 한 번만 로드합니다.
    """
    global sound_obj
    if sound_obj is None:
        try:
            # Base64 데이터를 디코딩하여 메모리에서 직접 사운드 객체를 생성합니다.
            decoded_audio_data = base64.b64decode(SOUND_DATA)
            sound_obj = pygame.mixer.Sound(io.BytesIO(decoded_audio_data))
        except Exception as e:
            print(f"오디오 데이터 로딩 오류: {e}")
            sound_obj = "failed"
    return sound_obj if sound_obj != "failed" else None


def start_sound_loop():
    """
    [수정] pygame을 사용하여 사운드를 무한 반복 재생합니다.
    """
    if _load_sound_obj() is not None:
        # loops=-1은 무한 반복을 의미합니다.
        sound_obj.play(loops=-1)


def stop_sound_loop():
    """
    [수정] pygame.mixer를 사용하여 현재 재생 중인 모든 사운드를 중지합니다.
    """
    pygame.mixer.stop()


# ---------------------------- 타이머 리셋 (TIMER RESET) ------------------------------- #
def reset_timer():
    global timer, reps
    if timer:
        window.after_cancel(timer)
        timer = None

    stop_sound_loop()
    canvas.itemconfig(timer_text, text="00:00")
    title_label.config(text="Timer", fg=GREEN)
    check_marks.config(text="")
    reps = 0
    start_button.config(state="normal")


# ---------------------------- 타이머 메커니즘 (TIMER MECHANISM) ------------------------------- #
def start_timer():
    global reps
    reps += 1
    work_sec = WORK_MIN * 60
    short_break_sec = SHORT_BREAK_MIN * 60
    long_break_sec = LONG_BREAK_MIN * 60
    start_button.config(state="disabled")

    if reps % 8 == 0:
        title_label.config(text="Break", fg=RED)
        stop_sound_loop()
        count_down(long_break_sec)
    elif reps % 2 == 0:
        title_label.config(text="Break", fg=PINK)
        stop_sound_loop()
        work_sessions = math.floor(reps / 2)
        check_marks.config(text="✔" * work_sessions)
        count_down(short_break_sec)
    else:
        title_label.config(text="Work", fg=GREEN)
        start_sound_loop()
        count_down(work_sec)


# ---------------------------- 카운트다운 메커니즘 (COUNTDOWN MECHANISM) ------------------------------- #
def count_down(count):
    count_min = math.floor(count / 60)
    count_sec = count % 60
    canvas.itemconfig(timer_text, text=f"{count_min:02d}:{count_sec:02d}")
    if count > 0:
        global timer
        timer = window.after(1000, count_down, count - 1)
    else:
        start_timer()


# ---------------------------- UI 설정 (UI SETUP) ------------------------------- #
window = tkinter.Tk()
window.title("Pomodoro")
window.config(padx=100, pady=50, bg=YELLOW)

# [수정] pygame 믹서 초기화. 사운드를 사용하기 전에 반드시 한 번 호출해야 합니다.
pygame.mixer.init()

title_label = tkinter.Label(
    text="Timer", fg=GREEN, bg=YELLOW, font=(FONT_NAME, 50, "bold")
)
title_label.grid(column=1, row=0)

canvas = tkinter.Canvas(width=200, height=224, bg=YELLOW, highlightthickness=0)
photo = tkinter.PhotoImage(data=IMG_DATA)
canvas.photo = photo

canvas.create_image(100, 112, image=photo)
timer_text = canvas.create_text(
    100, 130, text="00:00", fill="white", font=(FONT_NAME, 35, "bold")
)
canvas.grid(column=1, row=1)

start_button = tkinter.Button(text="Start", highlightthickness=0, command=start_timer)
start_button.grid(column=0, row=3)

reset_button = tkinter.Button(text="Reset", highlightthickness=0, command=reset_timer)
reset_button.grid(column=2, row=3)

check_marks = tkinter.Label(fg=GREEN, bg=YELLOW, font=(FONT_NAME, 15, "bold"))
check_marks.grid(column=1, row=4)

window.mainloop()
