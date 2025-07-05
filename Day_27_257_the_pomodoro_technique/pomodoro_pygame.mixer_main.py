# pomodoro_main.py

"""
Pomodoro Technique Timer (Main Logic)
이 프로그램은 Tkinter를 사용하여 만든 간단한 뽀모도로 타이머 애플리케이션입니다.
[수정] 타이머 업데이트 로직 오류를 수정하고 버튼 디자인을 복원했습니다.
"""

# --- 라이브러리 및 데이터 가져오기 (Import) ---
# 프로그램에 필요한 다양한 기능들을 불러옵니다.
import tkinter  # GUI(창, 버튼 등 그래픽 사용자 인터페이스)를 만들기 위한 기본 라이브러리
from tkinter import (
    messagebox,
)  # 사용자에게 메시지 박스(알림, 오류 창 등)를 보여주기 위한 기능
import math  # 수학 계산(내림, 올림 등)을 위한 라이브러리
import base64  # 바이너리(binary+2진법의) 데이터를 텍스트로 변환하거나(인코딩), 되돌릴 때(디코딩) 사용
import io  # 메모리 상의 데이터를 파일처럼 다루기 위한 라이브러리
import pygame  # 게임 개발용 라이브러리지만, 여기서는 사운드 재생을 위해 사용
import time  # 현재 시간을 가져오거나 시간 관련 기능을 사용하기 위한 라이브러리

# --- 외부 데이터 로드 ---
# 별도의 파일에 저장된 이미지와 사운드 데이터를 불러옵니다.
try:
    # code_data.py 파일에서 이미지(IMG_DATA)와 사운드(SOUND_DATA) 변수를 가져옵니다.
    from code_data import IMG_DATA, SOUND_DATA
except ImportError:
    # 만약 code_data.py 파일이 없어서 ImportError(가져오기+오류)가 발생하면,
    # 사용자에게 오류 메시지 창을 보여주고 프로그램을 종료합니다.
    messagebox.showerror(
        "파일 없음 오류",
        "'code_data.py' 파일을 찾을 수 없습니다. 두 파일이 같은 폴더에 있는지 확인하세요.",
    )
    exit()  # 프로그램 즉시 종료

# ---------------------------- 상수 (CONSTANTS) 및 전역 변수 (Global Variables) ------------------------------- #
# 프로그램 전체에서 사용될 변하지 않는 값(상수)과 여러 함수에서 공유할 변수(전역 변수)를 정의합니다.

# --- 색상 및 글꼴 상수 ---
PINK = "#e2979c"
RED = "#e7305b"
GREEN = "#9bdeac"
YELLOW = "#f7f5dd"
FONT_NAME = "Courier"

# --- 타이머 시간 상수 (단위: 분) ---
WORK_MIN = 25  # 작업 시간
SHORT_BREAK_MIN = 5  # 짧은 휴식 시간
LONG_BREAK_MIN = 20  # 긴 휴식 시간

# --- 상태 관리용 전역 변수 ---
reps = 0  # 현재 몇 번째 작업/휴식 세션인지 카운트하는 변수 (repetition+반복)
timer = (
    None  # window.after() 타이머의 ID를 저장할 변수. 타이머를 중지시킬 때 필요합니다.
)

# ---------------------------- 사운드 관리 (SOUND MANAGEMENT) ------------------------------- #
# pygame을 이용한 사운드 재생, 정지, 볼륨 조절 기능을 담당하는 부분입니다.

pygame.mixer.init()  # pygame의 사운드 시스템(mixer+믹서)을 초기화합니다. 소리 사용 전 필수입니다.
sound_loaded = False  # 사운드 파일이 메모리에 로드되었는지 확인하는 깃발(flag) 변수. False는 '아직'이라는 의미.


def start_sound_loop():
    """작업 시간 동안 배경음을 무한 반복 재생합니다."""
    global sound_loaded  # 함수 바깥의 sound_loaded 변수 값을 변경하기 위해 global 선언

    try:  # 사운드 관련 오류가 발생해도 프로그램이 멈추지 않도록 try-except 구문 사용
        stop_sound_loop()  # 혹시 다른 소리가 재생 중이라면 먼저 정지시킵니다.

        # 사운드가 아직 로드되지 않았을 때만 로드 작업을 수행합니다. (효율성 증가)
        if not sound_loaded:
            # 1. Base64로 인코딩된 텍스트 데이터를 원래의 오디오 바이너리 데이터로 디코딩합니다.
            decoded_audio_data = base64.b64decode(SOUND_DATA)
            # 2. 디코딩된 데이터를 파일이 아닌 메모리 상의 스트림(stream+흐름)으로 만듭니다.
            audio_stream = io.BytesIO(decoded_audio_data)
            # 3. 메모리 스트림에서 오디오 파일을 로드합니다.
            pygame.mixer.music.load(audio_stream)
            # 4. 로드가 완료되었으므로, 깃발을 True로 바꿔 다음부터는 이 작업을 생략하도록 합니다.
            sound_loaded = True

        # 로드된 음악을 재생합니다. loops=-1은 무한 반복을 의미합니다.
        pygame.mixer.music.play(loops=-1)
    except Exception as e:
        # 오류 발생 시 콘솔에 오류 메시지를 출력합니다.
        print(f"사운드 재생 오류: {e}")


def stop_sound_loop():
    """재생 중인 배경음을 정지시킵니다."""
    try:
        pygame.mixer.music.stop()  # 현재 재생 중인 음악을 즉시 중지합니다.
    except Exception as e:
        print(f"사운드 정지 오류: {e}")


def set_volume(volume_level):
    """슬라이더의 값(0-100)을 받아와 pygame의 볼륨(0.0-1.0)으로 변환하여 설정합니다."""
    try:
        # Scale 위젯에서 넘어오는 값은 문자열일 수 있으므로, 숫자로 변환(float)합니다.
        # 0~100 범위를 0.0~1.0 범위로 변환하기 위해 100으로 나눕니다.
        volume = float(volume_level) / 100
        pygame.mixer.music.set_volume(volume)  # 변환된 값으로 볼륨을 설정합니다.
    except Exception as e:
        print(f"볼륨 조절 오류: {e}")


# ---------------------------- 타이머 리셋 (TIMER RESET) ------------------------------- #
def reset_timer():
    """'Reset' 버튼 클릭 시 호출. 모든 상태를 초기 값으로 되돌립니다."""
    global timer, reps  # 전역 변수 timer와 reps의 값을 변경하기 위해 선언

    # 만약 타이머가 작동 중이라면(timer 변수에 ID가 저장되어 있다면)
    if timer:
        window.after_cancel(timer)  # 예약된 카운트다운을 취소합니다.
        timer = None  # 타이머 ID를 다시 None으로 초기화합니다.

    stop_sound_loop()  # 배경음을 정지합니다.
    # [수정] 타이머 텍스트 업데이트 헬퍼 함수를 호출하여 모든 텍스트 레이어를 초기화합니다.
    _update_timer_text("00:00")
    canvas.itemconfig(
        title_text, text="Timer", fill=GREEN
    )  # 캔버스 위의 제목 텍스트와 색상을 초기 상태로 변경
    canvas.itemconfig(check_marks_text, text="")
    reps = 0  # 세션 카운트를 0으로 초기화
    start_button.config(
        state="normal"
    )  # 'Start' 버튼을 다시 클릭 가능한 '정상(normal)' 상태로 변경


# ---------------------------- 타이머 메커니즘 (TIMER MECHANISM) ------------------------------- #
def start_timer():
    """'Start' 버튼 클릭 또는 한 세션 종료 시 호출. 다음 세션을 시작합니다."""
    global reps  # 전역 변수 reps의 값을 변경하기 위해 선언
    reps += 1  # 세션 카운트를 1 증가시킵니다.

    # 타이머 시간을 분에서 초 단위로 변환합니다.
    work_sec = WORK_MIN * 60
    short_break_sec = SHORT_BREAK_MIN * 60
    long_break_sec = LONG_BREAK_MIN * 60

    # 타이머가 시작되면 'Start' 버튼을 '비활성(disabled)' 상태로 만들어 중복 클릭을 방지합니다.
    start_button.config(state="disabled")

    # reps 값에 따라 어떤 세션을 시작할지 결정합니다.
    if reps % 8 == 0:  # 8번째 세션 -> 긴 휴식
        canvas.itemconfig(title_text, text="Break", fill=RED)
        stop_sound_loop()
        count_down(long_break_sec)
    elif reps % 2 == 0:  # 2, 4, 6번째 세션 -> 짧은 휴식
        canvas.itemconfig(title_text, text="Break", fill=PINK)
        stop_sound_loop()
        work_sessions = math.floor(reps / 2)  # 완료된 작업 세션 수 계산
        canvas.itemconfig(check_marks_text, text="✔" * work_sessions)
        count_down(short_break_sec)
    else:  # 1, 3, 5, 7번째 세션 -> 작업
        canvas.itemconfig(title_text, text="Work", fill=GREEN)
        start_sound_loop()
        count_down(work_sec)


# ---------------------------- 카운트다운 메커니즘 (COUNTDOWN MECHANISM) ------------------------------- #
def _update_timer_text(text):
    """[헬퍼 함수] 타이머 텍스트와 외곽선을 모두 업데이트합니다."""
    canvas.itemconfig(timer_text_outline_n, text=text)
    canvas.itemconfig(timer_text_outline_s, text=text)
    canvas.itemconfig(timer_text_outline_e, text=text)
    canvas.itemconfig(timer_text_outline_w, text=text)
    canvas.itemconfig(timer_text_main, text=text)


def count_down(count):
    """1초마다 화면의 시간을 업데이트하고, 0이 되면 다음 세션을 시작합니다."""
    count_min = math.floor(count / 60)  # 남은 총 초를 60으로 나눈 몫 = '분'
    count_sec = count % 60  # 남은 총 초를 60으로 나눈 나머지 = '초'

    # "분:초" 형식의 문자열을 만듭니다.
    time_string = f"{count_min:02d}:{count_sec:02d}"
    # [수정] 헬퍼 함수를 사용하여 텍스트 레이어들을 한 번에 업데이트합니다.
    _update_timer_text(time_string)

    if count > 0:  # 남은 시간이 0보다 크면
        global timer
        # 1000ms(1초) 후에 count_down 함수를 'count - 1' 값으로 다시 호출하도록 예약합니다.
        timer = window.after(1000, count_down, count - 1)
    else:  # 남은 시간이 0이 되면
        start_timer()  # 다음 세션을 시작합니다.


def update_current_time():
    """1초마다 현재 시간을 가져와 상단 라벨을 업데이트합니다."""
    time_string_ampm = time.strftime("%p %I:%M")
    if "AM" in time_string_ampm:
        korean_time_string = time_string_ampm.replace("AM", "오전")
    else:
        korean_time_string = time_string_ampm.replace("PM", "오후")

    current_time_label.config(text=korean_time_string)
    window.after(1000, update_current_time)


# ---------------------------- UI 설정 (UI SETUP) ------------------------------- #
# 프로그램의 화면을 구성하는 부분입니다.

window = tkinter.Tk()  # 메인 윈도우(창) 객체를 생성합니다.
window.title("Pomodoro")  # 창의 제목을 설정합니다.
window.iconbitmap(
    "C:\\Users\\ye\\Documents\\study\\python\\self_study\\Day_27_257_the_pomodoro_technique\\tomato.ico"
)
window.config(padx=10, pady=10, bg=YELLOW)  # 창의 속성(내부 여백, 배경색)을 설정합니다.

# --- 현재 시간 표시 라벨 ---
current_time_label = tkinter.Label(
    text="", fg=PINK, bg=YELLOW, font=(FONT_NAME, 16, "bold")
)
current_time_label.grid(
    column=1, row=0, pady=(0, 10)
)  # 격자(grid) 레이아웃에 배치. pady는 위아래 여백.

# --- 토마토 이미지와 타이머가 표시될 캔버스 ---
canvas = tkinter.Canvas(width=200, height=224, bg=YELLOW, highlightthickness=0)
photo = tkinter.PhotoImage(data=IMG_DATA)  # Base64 데이터로부터 이미지 객체 생성
canvas.photo = photo  # [중요] 생성된 이미지 객체가 사라지지 않도록 참조를 저장합니다.
canvas.create_image(100, 112, image=photo)  # 캔버스 중앙에 이미지 그리기

# --- 캔버스 내부 텍스트 생성 ---
title_text = canvas.create_text(
    100, 120, text="Timer", fill=GREEN, font=(FONT_NAME, 40, "bold")
)

# 타이머 텍스트에 외곽선 효과를 주기 위해 여러 개의 텍스트를 겹쳐서 생성합니다.
outline_offset = 2
# 외곽선 (검은색)
timer_text_outline_n = canvas.create_text(
    100, 170 - outline_offset, text="00:00", fill="black", font=(FONT_NAME, 35, "bold")
)
timer_text_outline_s = canvas.create_text(
    100, 170 + outline_offset, text="00:00", fill="black", font=(FONT_NAME, 35, "bold")
)
timer_text_outline_w = canvas.create_text(
    100 - outline_offset, 170, text="00:00", fill="black", font=(FONT_NAME, 35, "bold")
)
timer_text_outline_e = canvas.create_text(
    100 + outline_offset, 170, text="00:00", fill="black", font=(FONT_NAME, 35, "bold")
)
# 메인 텍스트 (흰색)
timer_text_main = canvas.create_text(
    100, 170, text="00:00", fill="white", font=(FONT_NAME, 35, "bold")
)

check_marks_text = canvas.create_text(
    100, 210, text="", fill=GREEN, font=(FONT_NAME, 20, "bold")
)
canvas.grid(column=1, row=1)

# --- 볼륨 컨트롤 슬라이더 ---
volume_scale = tkinter.Scale(
    from_=0,
    to=100,
    orient=tkinter.HORIZONTAL,
    bg=YELLOW,
    highlightthickness=0,
    troughcolor=GREEN,
    command=set_volume,
)
volume_scale.set(25)
volume_scale.grid(column=1, row=2, pady=10)

# --- 시작/리셋 버튼 ---
start_button = tkinter.Button(
    text="Start",
    font=(FONT_NAME, 12, "bold"),
    bg=GREEN,
    fg="white",
    activebackground="#78c48f",  # 클릭했을 때 배경색
    activeforeground="white",  # 클릭했을 때 글자색
    borderwidth=0,
    highlightthickness=0,
    command=start_timer,
    padx=20,  # 내부 좌우 여백
    pady=5,  # 내부 상하 여백
)
start_button.grid(column=0, row=2)

reset_button = tkinter.Button(
    text="Reset",
    font=(FONT_NAME, 12, "bold"),
    bg=PINK,
    fg="white",
    activebackground="#d48a90",
    activeforeground="white",
    borderwidth=0,
    highlightthickness=0,
    command=reset_timer,
    padx=20,
    pady=5,
)
reset_button.grid(column=2, row=2)

# --- 프로그램 실행 ---
update_current_time()  # 프로그램 시작과 동시에 현재 시간 업데이트를 시작합니다.
window.mainloop()  # 창이 닫히기 전까지 계속 실행되도록 이벤트 루프를 시작합니다.
