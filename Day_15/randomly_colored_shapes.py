from rich import print
from turtle import Turtle, Screen
import random


# def get_random():
#     hex_digits = random.choices(string.hexdigits.lower(), k=6)
#     return f"#{''.join(hex_digits)}"

get_random = lambda : f"#{random.randint(1, 0xFFFFFF):06x}"

tim = Turtle()
tim.shape()
tim.speed(0)

for sides in range(3, 11):
        tim.color(get_random())

        for _ in range(sides):
            tim.right(360/sides)
            tim.forward(100)

screen = Screen()
screen.exitonclick()
