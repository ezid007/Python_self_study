from code_data import IMG_DATA, SOUND_DATA
import tkinter
import math
import base64
import io
import pygame

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
pygame.mixer.init()
sound_loaded = False


def start_sound_loop():
    global sound_loaded

    try:
        stop_sound_loop()  # 기존 사운드 중지

        if not sound_loaded:
            decoded_audio_data = base64.b64decode(SOUND_DATA)
            audio_stream = io.BytesIO(decoded_audio_data)
            pygame.mixer.music.load(audio_stream)
            sound_loaded = True

        pygame.mixer.music.play(-1)  # -1은 무한 반복
    except Exception as e:
        print(f"사운드 재생 오류: {e}")


def stop_sound_loop():
    try:
        pygame.mixer.music.stop()
    except Exception as e:
        print(f"사운드 정지 오류: {e}")


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
