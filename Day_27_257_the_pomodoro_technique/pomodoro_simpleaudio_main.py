from code_data import IMG_DATA, SOUND_DATA
import tkinter
import math
import base64
import simpleaudio as sa
import wave
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
play_obj = None
sound_check_id = None
wave_obj = None


def _load_wave_obj():
    try:
        decoded_audio_data = base64.b64decode(SOUND_DATA)
        byte_stream = io.BytesIO(decoded_audio_data)
        wave_read = wave.open(byte_stream, "rb")
        return sa.WaveObject.from_wave_read(wave_read)
    except Exception as e:
        print(f"오디오 데이터 로딩 오류: {e}")
        return None


def start_sound_loop():
    global play_obj, sound_check_id

    stop_sound_loop()

    wave_obj = _load_wave_obj()
    if wave_obj is None:
        return

    def loop_check():
        global play_obj, sound_check_id

        try:
            if not play_obj or not play_obj.is_playing():
                wave_obj = _load_wave_obj()
                if wave_obj:
                    play_obj = wave_obj.play()
            sound_check_id = window.after(500, loop_check)
        except Exception as e:
            print(f"사운드 루프 오류: {e}")
            stop_sound_loop()

    loop_check()


def stop_sound_loop():
    global play_obj, sound_check_id
    try:
        if sound_check_id:
            window.after_cancel(sound_check_id)
            sound_check_id = None
        if play_obj:
            try:
                if play_obj.is_playing():
                    play_obj.stop()
            except Exception as e:
                print(f"사운드 종료 시 play_obj 오류: {e}")
        play_obj = None
    except Exception as e:
        print(f"사운드 정지 중 오류: {e}")



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
