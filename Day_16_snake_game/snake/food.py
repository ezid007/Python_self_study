from turtle import Turtle
import random

class Food(Turtle):
    def __init__(self, shape = "circle"):
        super().__init__(shape)
        self.penup()
        self.shapesize(stretch_len=0.5, stretch_wid=0.5)
        self.color("#00D9FF")
        self.speed(0)
        self.refresh()
        
    def refresh(self):
        random_x = random.randint(-260, 260)
        random_y = random.randint(-260, 260)
        self.goto(random_x, random_y)