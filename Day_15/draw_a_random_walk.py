from rich import print
from turtle import Turtle, Screen
import random

random_color = lambda : f"#{random.randint(0, 0xFFFFFF):06x}"

directions = [0, 90, 180, 270]

tt = Turtle('turtle')
screen = Screen()
tt.pensize(15)
tt.shape()

for _ in range(100):
    tt.color(random_color())
    tt.setheading(random.choice(directions))
    tt.forward(20)

screen.exitonclick()
