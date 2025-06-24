import turtle
import random

random_color = lambda : (random.randint(0,255), random.randint(0,255), random.randint(0,255))

turtle.colormode(255)
tt = turtle.Turtle()
tt.speed(0)
gap = 5
radios = tt.heading()
for i in range(360//gap):
    tt.color(random_color())
    tt.circle(200)
    tt.setheading(radios + gap)
    gap += 5

screen = turtle.Screen()
screen.exitonclick()


