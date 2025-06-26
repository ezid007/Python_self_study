import turtle

# --- 1. 기본 설정 ---
screen = turtle.Screen()
screen.title("키보드로 이모티콘을 움직여보세요!")
screen.bgcolor("white")
screen.tracer(0)  # 화면 업데이트를 수동으로 제어하여 깜빡임을 없앰

# --- 2. 플레이어(이모티콘) 거북이 설정 ---
player = turtle.Turtle()
player.hideturtle()  # 거북이 모양은 항상 숨깁니다.
player.penup()       # 선이 그려지면 안 되므로 펜을 듭니다.
player.speed(0)      # 거북이의 이동 속도는 최대로 (어차피 안 보임)

# 플레이어의 현재 모양(이모티콘)과 위치를 화면에 그리는 함수
def draw_player():
    player.clear()  # 이전에 그렸던 이모티콘 지우기
    player.write("👻", align="center", font=("Segoe UI Emoji", 30, "normal"))
    screen.update() # 변경된 내용을 화면에 최종 반영

# --- 3. 이동 함수 정의 ---
# 각 함수는 '이동'과 '다시 그리기'를 담당합니다.
def move_up():
    player.setheading(90)  # 위쪽 방향 설정
    player.forward(10)     # 10만큼 이동
    draw_player()          # 이동한 위치에 다시 그리기

def move_down():
    player.setheading(270) # 아래쪽 방향 설정
    player.forward(10)
    draw_player()

def move_left():
    player.setheading(180) # 왼쪽 방향 설정
    player.forward(10)
    draw_player()

def move_right():
    player.setheading(0)   # 오른쪽 방향 설정
    player.forward(10)
    draw_player()

# --- 4. 키보드 입력과 함수 연결 ---
screen.listen()  # 키보드 입력을 받을 수 있도록 설정
screen.onkey(move_up, "Up")        # ↑ 방향키를 누르면 move_up 함수 실행
screen.onkey(move_down, "Down")    # ↓ 방향키를 누르면 move_down 함수 실행
screen.onkey(move_left, "Left")    # ← 방향키를 누르면 move_left 함수 실행
screen.onkey(move_right, "Right")  # → 방향키를 누르면 move_right 함수 실행


# --- 5. 게임 시작 ---
draw_player()  # 맨 처음에 플레이어(유령)를 화면에 한번 그려줍니다.

screen.exitonclick()