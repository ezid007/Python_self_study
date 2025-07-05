import tkinter
from tkinter import messagebox
import math
import base64
import io
import pygame
import time
import requests
from datetime import datetime, timedelta

# --- 외부 데이터 로드 ---
try:
    from code_data import IMG_DATA, SOUND_DATA, TOMATO_ICO
except ImportError:
    messagebox.showerror(
        "파일 없음 오류",
        "'code_data.py' 파일을 찾을 수 없습니다. 두 파일이 같은 폴더에 있는지 확인하세요.",
    )
    exit()

# ---------------------------- 상수 (CONSTANTS) 및 전역 변수 (Global Variables) ------------------------------- #

# --- 색상 및 글꼴 상수 ---
PINK = "#e2979c"
RED = "#e7305b"
GREEN = "#9bdeac"
YELLOW = "#f7f5dd"
FONT_NAME = "Courier"

# --- 타이머 시간 상수 (단위: 분) ---
WORK_MIN = 25
SHORT_BREAK_MIN = 5
LONG_BREAK_MIN = 20

# --- 기상청 API 관련 상수 ---
# 중요: 아래 'YOUR_KMA_API_KEY' 부분에 공공데이터포털에서 발급받은 본인의 인증키를 입력해야 합니다.
# URL 인코딩된 키가 아닌, 일반 인증키(Decoding)를 사용하세요.
KMA_API_KEY = "Qm%2BeM3tI2A%2FndGQSlFsYDJhFeHx7FfFLbfNGSRzxNzEtemy3O%2BK4pncX%2FbgykEhQEmr%2FLhQP7aLBXctq6vbznw%3D%3D"

# 주요 도시 이름(ipinfo.io 결과)과 기상청 격자 좌표(X, Y) 매핑
CITY_GRID_COORDS = {
    "Seoul": (60, 127),
    "Seongnam": (62, 123),
    "Incheon": (55, 124),
    "Suwon": (60, 121),
    "Busan": (98, 76),
    "Daegu": (89, 90),
    "Gwangju": (58, 74),
    "Daejeon": (67, 100),
    "Ulsan": (102, 84),
    "Jeju": (52, 38),
}

# --- 상태 관리용 전역 변수 ---
reps = 0
timer = None

# ---------------------------- 사운드 관리 (SOUND MANAGEMENT) ------------------------------- #
pygame.mixer.init()
sound_loaded = False


def start_sound_loop():
    """작업 시간 동안 배경음을 무한 반복 재생합니다."""
    global sound_loaded
    try:
        stop_sound_loop()
        if not sound_loaded:
            decoded_audio_data = base64.b64decode(SOUND_DATA)
            audio_stream = io.BytesIO(decoded_audio_data)
            pygame.mixer.music.load(audio_stream)
            sound_loaded = True
        pygame.mixer.music.play(loops=-1)
    except Exception as e:
        print(f"사운드 재생 오류: {e}")


def stop_sound_loop():
    """재생 중인 배경음을 정지시킵니다."""
    try:
        pygame.mixer.music.stop()
    except Exception as e:
        print(f"사운드 정지 오류: {e}")


def set_volume(volume_level):
    """슬라이더의 값으로 볼륨을 조절합니다."""
    try:
        volume = float(volume_level) / 100
        pygame.mixer.music.set_volume(volume)
    except Exception as e:
        print(f"볼륨 조절 오류: {e}")


# ---------------------------- 날씨 및 날짜 정보 (WEATHER & DATE) ------------------------------- #
def get_city_from_ip():
    """IP 주소 기반으로 현재 도시 이름을 가져옵니다."""
    try:
        response = requests.get("https://ipinfo.io/json")
        response.raise_for_status()
        data = response.json()
        city = data.get("city", "Seoul")
        return city
    except requests.exceptions.RequestException:
        print("IP 주소로 위치를 찾는 데 실패했습니다. 기본 위치(Seoul)를 사용합니다.")
        return "Seoul"


def get_kma_weather(city):
    """기상청 API로 현재 날씨 정보를 가져옵니다."""
    if KMA_API_KEY == "YOUR_KMA_API_KEY":
        return "API 키 필요"

    nx, ny = CITY_GRID_COORDS.get(city, CITY_GRID_COORDS["Seoul"])

    now = datetime.now()
    base_dt = now - timedelta(hours=1)
    base_date = base_dt.strftime("%Y%m%d")
    base_time = base_dt.strftime("%H00")

    api_url = (
        "http://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getUltraSrtNcst"
        f"?serviceKey={KMA_API_KEY}&pageNo=1&numOfRows=10&dataType=JSON"
        f"&base_date={base_date}&base_time={base_time}&nx={nx}&ny={ny}"
    )

    try:
        response = requests.get(api_url, timeout=10)
        response.raise_for_status()
        items = response.json()["response"]["body"]["items"]["item"]

        weather_data = {item["category"]: item["obsrValue"] for item in items}

        temp = f"{weather_data.get('T1H')}°C"
        pty_code = weather_data.get("PTY", "0")
        sky_code = weather_data.get("SKY", "0")

        pty_map = {
            "0": "",
            "1": "비",
            "2": "비/눈",
            "3": "눈",
            "5": "빗방울",
            "6": "빗방울/눈날림",
            "7": "눈날림",
        }
        sky_map = {"1": "맑음", "3": "구름많음", "4": "흐림"}

        # --- [개선된 날씨 처리 로직] ---
        sky_description = None
        # 강수형태(PTY) 코드가 '0'(없음)이 아닌 경우, 강수 상태를 우선적으로 가져옵니다.
        if pty_code != "0":
            sky_description = pty_map.get(pty_code)
        # 강수가 없을 때만 하늘상태(SKY) 코드를 확인합니다.
        else:
            sky_description = sky_map.get(sky_code)

        # 최종 날씨 정보 문자열을 만듭니다. 정보가 없는 경우(None)는 제외합니다.
        if sky_description:
            return f"{sky_description} {temp}"
        else:
            # 하늘 정보가 없을 경우 온도만 표시합니다.
            return temp

    except requests.exceptions.RequestException as e:
        print(f"기상청 API 요청 오류: {e}")
        return "날씨 로드 실패"
    except (KeyError, TypeError):
        return "정보 파싱 오류"


def update_header_info():
    """창 상단의 날씨와 날짜 라벨을 업데이트하고 요일에 따라 색상을 변경합니다."""
    current_city = get_city_from_ip()
    weather_info = get_kma_weather(current_city)
    weather_label.config(text=weather_info)

    now = datetime.now()
    weekday_kr = ["월", "화", "수", "목", "금", "토", "일"]
    date_info = now.strftime(f"%m월 %d일 ({weekday_kr[now.weekday()]})")

    weekday = now.weekday()
    if weekday == 6:  # 일요일
        date_color = "red"
    elif weekday == 5:  # 토요일
        date_color = "blue"
    else:  # 평일
        date_color = "black"

    date_label.config(text=date_info, fg=date_color)


def update_current_time():
    """1초마다 현재 시간을 가져와 화면에 표시합니다."""
    time_string_ampm = time.strftime("%p %I:%M")
    korean_time_string = time_string_ampm.replace("AM", "오전").replace("PM", "오후")
    current_time_label.config(text=korean_time_string)
    window.after(1000, update_current_time)


# ---------------------------- 타이머 리셋 (TIMER RESET) ------------------------------- #
def reset_timer():
    """타이머를 초기 상태로 리셋합니다."""
    global timer, reps
    if timer:
        window.after_cancel(timer)
        timer = None
    stop_sound_loop()
    _update_timer_text("00:00")
    canvas.itemconfig(title_text, text="Timer", fill=GREEN)
    reps = 0
    start_button.config(state="normal")


# ---------------------------- 타이머 메커니즘 (TIMER MECHANISM) ------------------------------- #
def start_timer():
    """타이머를 시작합니다."""
    global reps
    reps += 1
    work_sec = WORK_MIN * 60
    short_break_sec = SHORT_BREAK_MIN * 60
    long_break_sec = LONG_BREAK_MIN * 60
    start_button.config(state="disabled")

    if reps % 8 == 0:
        canvas.itemconfig(title_text, text="Break", fill=RED)
        stop_sound_loop()
        count_down(long_break_sec)
    elif reps % 2 == 0:
        canvas.itemconfig(title_text, text="Break", fill=PINK)
        stop_sound_loop()
        count_down(short_break_sec)
    else:
        canvas.itemconfig(title_text, text="Work", fill=GREEN)
        start_sound_loop()
        count_down(work_sec)


# ---------------------------- 카운트다운 메커니즘 (COUNTDOWN MECHANISM) ------------------------------- #
def _update_timer_text(text):
    """타이머 텍스트와 외곽선을 모두 업데이트합니다."""
    canvas.itemconfig(timer_text_outline_n, text=text)
    canvas.itemconfig(timer_text_outline_s, text=text)
    canvas.itemconfig(timer_text_outline_e, text=text)
    canvas.itemconfig(timer_text_outline_w, text=text)
    canvas.itemconfig(timer_text_main, text=text)


def count_down(count):
    """1초마다 카운트다운을 진행합니다."""
    count_min = math.floor(count / 60)
    count_sec = count % 60
    time_string = f"{count_min:02d}:{count_sec:02d}"
    _update_timer_text(time_string)

    if count > 0:
        global timer
        timer = window.after(1000, count_down, count - 1)
    else:
        start_timer()


# ---------------------------- UI 설정 (UI SETUP) ------------------------------- #
window = tkinter.Tk()
window.title("Pomodoro")
icon_data_decoded = base64.b64decode(TOMATO_ICO)
icon_photo = tkinter.PhotoImage(data=icon_data_decoded)
window.iconphoto(True, icon_photo)
window.config(padx=30, pady=20, bg=YELLOW)

# --- 상단 정보 (날씨, 날짜, 시간) ---
header_frame = tkinter.Frame(window, bg=YELLOW)
header_frame.grid(column=0, row=0, columnspan=3, sticky="ew")

weather_label = tkinter.Label(
    header_frame,
    text="날씨 로딩 중...",
    fg="black",
    bg=YELLOW,
    font=(FONT_NAME, 12, "bold"),
)
weather_label.pack(side="left", padx=10)

date_label = tkinter.Label(
    header_frame,
    text="날짜 로딩 중...",
    fg="black",
    bg=YELLOW,
    font=(FONT_NAME, 12, "bold"),
)
date_label.pack(side="right", padx=10)

current_time_label = tkinter.Label(
    text="", fg=PINK, bg=YELLOW, font=(FONT_NAME, 16, "bold")
)
current_time_label.grid(column=0, row=1, columnspan=3, pady=(5, 0))


# --- 토마토 이미지와 타이머가 표시될 캔버스 ---
canvas = tkinter.Canvas(width=200, height=224, bg=YELLOW, highlightthickness=0)
photo = tkinter.PhotoImage(data=IMG_DATA)
canvas.photo = photo
canvas.create_image(100, 112, image=photo)

title_text = canvas.create_text(
    100, 120, text="Timer", fill=GREEN, font=(FONT_NAME, 40, "bold")
)
outline_offset = 2
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
timer_text_main = canvas.create_text(
    100, 170, text="00:00", fill="white", font=(FONT_NAME, 35, "bold")
)
canvas.grid(column=0, row=2, columnspan=3, pady=15)

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
volume_scale.grid(column=0, row=3, columnspan=3, padx=12, pady=(0, 6), sticky="ew")

# --- 시작/리셋 버튼 ---
start_button = tkinter.Button(
    text="Start",
    font=(FONT_NAME, 12, "bold"),
    bg=GREEN,
    fg="white",
    activebackground="#78c48f",
    activeforeground="white",
    borderwidth=0,
    highlightthickness=0,
    command=start_timer,
    padx=20,
    pady=5,
)
start_button.grid(column=0, row=4, sticky="e", padx=5, pady=(5, 0))

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
reset_button.grid(column=2, row=4, sticky="w", padx=5, pady=(5, 0))

# --- 프로그램 시작 시 정보 업데이트 ---
update_header_info()
update_current_time()

window.mainloop()
