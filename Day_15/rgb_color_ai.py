from turtle import Turtle, Screen
from rich import print
import colorgram
import random

# --- 1. 초기 설정 ---
# 색상 추출
colors = colorgram.extract('self_study\\Day_15\\hirst_spot_painting.jpg', 30)

rgb_colors = [
    (c.rgb.r, c.rgb.g, c.rgb.b) for c in colors
    if not (c.rgb.r > 235 and c.rgb.g > 235 and c.rgb.b > 235)
]

print(f"흰색 계열 제외 후 남은 색상 수: {len(rgb_colors)}")

# 터틀 및 스크린 설정
screen = Screen()
screen.colormode(255)
tt = Turtle()
# tt.hideturtle()
tt.speed("fastest")

# --- 2. 시작 위치 설정 ---
tt.penup()
tt.setheading(225)
tt.forward(350)
tt.setheading(0)
start_x = tt.xcor()
start_y = tt.ycor()

# --- 3. 10x10 격자 그리기 ---
GRID_SIZE = 10
DOT_SIZE = 20
DOT_GAP = 50

for row in range(GRID_SIZE):
    tt.setpos(start_x, start_y + row * DOT_GAP)
    
    for _ in range(GRID_SIZE):
        # 필터링된 색상 리스트에서 무작위로 선택하여 점 찍기
        if rgb_colors: # 리스트가 비어있지 않은 경우에만 실행
             tt.dot(DOT_SIZE, random.choice(rgb_colors))
        tt.forward(DOT_GAP)

screen.exitonclick()