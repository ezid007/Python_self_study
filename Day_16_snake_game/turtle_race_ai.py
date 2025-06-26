from turtle import Turtle, Screen
import random
# tkinter의 messagebox를 사용하기 위해 import 합니다.
from tkinter import messagebox

# --- (이전 코드와 동일한 부분) ---
COLORS = ["red", "orange", "yellow", "green", "blue", "purple", "black"]
Y_POSITIONS = [-180, -120, -60, 0, 60, 120, 180]
START_LINE_X = -270
FINISH_LINE_X = 270

screen = Screen()
screen.setup(width=600, height=500)

user_bet = screen.textinput(title="Make your bet", prompt=f"어떤 거북이가 경주에서 이길까요? 색깔을 입력하세요:\n{COLORS}")

def draw_line(x_pos):
    line_drawer = Turtle()
    line_drawer.hideturtle()
    line_drawer.speed('fastest')
    line_drawer.penup()
    line_drawer.goto(x_pos, 220)
    line_drawer.setheading(270)
    line_drawer.pendown()
    line_drawer.forward(440)

draw_line(START_LINE_X)
draw_line(FINISH_LINE_X)

def create_turtle(color, y_pos):
    t = Turtle(shape="turtle")
    t.color(color)
    t.penup()
    t.goto(x=START_LINE_X - 20, y=y_pos)
    return t

all_turtles = [create_turtle(COLORS[i], Y_POSITIONS[i]) for i in range(len(COLORS))]

# 결과를 팝업창으로 보여주는 함수
def show_result_popup(winner_color, bet_color):
    """레이스 결과를 tkinter 메시지 박스(팝업창)로 표시합니다."""
    if winner_color == bet_color:
        title = "성공!"
        message = f"🎉 예측 성공! {winner_color} 거북이가 우승했습니다!"
    else:
        title = "실패!"
        message = f"😥 예측 실패! {winner_color} 거북이가 우승했습니다."
    
    # 정보 메시지 박스를 화면에 띄웁니다.
    messagebox.showinfo(title, message)

is_race_on = bool(user_bet)

while is_race_on:
    for turtle in all_turtles:
        if turtle.xcor() > FINISH_LINE_X - 20:
            is_race_on = False
            winning_color = turtle.pencolor()
            # 수정된 팝업 함수를 호출합니다.
            show_result_popup(winning_color, user_bet)
            break

        rand_distance = random.randint(0, 10)
        turtle.forward(rand_distance)

screen.exitonclick()