from turtle import Turtle, Screen
from rich import print
import colorgram
import random
import os

os.system('cls')

rgb_colors = []
colors = colorgram.extract('self_study\\Day_15\\hirst_spot_painting.jpg', 30)

rgb_colors = [(color.rgb.r, color.rgb.g, color.rgb.b) for color in colors 
              if not (color.rgb.r > 235 and color.rgb.g > 235 and color.rgb.b > 235)]

tt = Turtle()
tt.hideturtle()
tt.speed(0)
screen = Screen()
screen.colormode(255)

tt.up()
tt.setheading(220)
tt.forward(400)
tt.setheading(0)
tt.down()

def dotdotdot(i):
    for _ in range(1, i):
        tt.dot(20, random.choice(rgb_colors))
        tt.up()
        tt.forward(50)
        tt.down()

def turn_left():
    tt.dot(20, random.choice(rgb_colors))
    tt.up()
    tt.right(270)
    tt.forward(50)
    tt.down()
    tt.dot(20, random.choice(rgb_colors))
    tt.up()
    tt.right(270)
    tt.forward(50)
    tt.down()
    tt.dot(20, random.choice(rgb_colors))
    
def turn_right():
    tt.dot(20, random.choice(rgb_colors))
    tt.up()
    tt.right(90)
    tt.forward(50)
    tt.down()
    tt.dot(20, random.choice(rgb_colors))
    tt.up()
    tt.right(90)
    tt.forward(50)
    tt.down()
    tt.dot(20, random.choice(rgb_colors))   

dotdotdot(10)

for _ in range(4):
    turn_left()
    dotdotdot(9)
    turn_right()
    dotdotdot(9)

turn_left()
dotdotdot(9)
tt.dot(20, random.choice(rgb_colors))   

screen.exitonclick()