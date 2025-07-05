"""
Pomodoro Technique Timer (Main Logic)
이 프로그램은 Tkinter를 사용하여 만든 간단한 뽀모도로 타이머 애플리케이션입니다.
데이터는 code_data.py에서 가져오고, 여기서는 프로그램의 핵심 로직만 처리합니다.
[수정] 이미지 핸들링 안정성을 개선하고, 오류 처리 방식을 개선했습니다.
"""

import tkinter
import tkinter.messagebox
import math
import base64
import simpleaudio as sa
import io

# [수정] code_data 파일에서 이미지 및 사운드 데이터를 가져옵니다.
try:
    from code_data import IMG_DATA, SOUND_DATA
except ImportError:
    # [수정] 파일이 없을 경우, 사용자에게 오류 메시지 창을 띄우고 프로그램을 종료합니다.
    tkinter.messagebox.showerror(
        "파일 없음 오류",
        "'code_data.py' 파일을 찾을 수 없습니다. 두 파일이 같은 폴더에 있는지 확인하세요.",
    )
    exit()  # 프로그램 종료

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
play_obj = None
sound_check_id = None
wave_obj = None


def _load_wave_obj():
    global wave_obj
    if wave_obj is None:
        try:
            decoded_audio_data = base64.b64decode(SOUND_DATA)
            wave_obj = sa.WaveObject.from_wave_file(io.BytesIO(decoded_audio_data))
        except Exception as e:
            print(f"오디오 데이터 로딩 오류: {e}")
            wave_obj = "failed"
    return wave_obj if wave_obj != "failed" else None


def start_sound_loop():
    global play_obj, sound_check_id
    stop_sound_loop()

    if _load_wave_obj() is None:
        return

    def loop_check():
        global play_obj, sound_check_id
        if not play_obj or not play_obj.is_playing():
            play_obj = wave_obj.play()
        # [수정] window 객체를 명시적으로 사용하여 after 메소드를 호출합니다.
        sound_check_id = window.after(500, loop_check)

    loop_check()


def stop_sound_loop():
    global play_obj, sound_check_id
    if sound_check_id:
        # [수정] window 객체를 명시적으로 사용하여 after_cancel을 호출합니다.
        window.after_cancel(sound_check_id)
        sound_check_id = None
    if play_obj and play_obj.is_playing():
        play_obj.stop()
        play_obj = None


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

# [핵심 수정] 생성된 이미지 객체(photo)가 사라지지 않도록 canvas 위젯에 대한 참조로 저장합니다.
# 이렇게 하면 파이썬의 가비지 컬렉터가 이미지를 임의로 삭제하는 것을 방지하여 프로그램 충돌을 막습니다.
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
