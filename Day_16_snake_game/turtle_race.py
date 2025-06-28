from turtle import Turtle, Screen
import random


is_race_on = False
screen = Screen()
screen.setup(width=600, height=500)
user_bet = screen.textinput(
    title="Make your bet", prompt="Which turtle will win the race? Enter a color:"
)
colors = ["red", "orange", "yellow", "green", "blue", "purple", "black"]
y_positions = [-180, -120, -60, 0, 60, 120, 180]
all_turtles = []

for turtle_index in range(7):
    tt = Turtle("turtle")
    tt.color(colors[turtle_index])
    tt.penup()
    tt.goto(x=-230, y=y_positions[turtle_index])
    all_turtles.append(tt)

if user_bet:
    is_race_on = True

while is_race_on:
    for turtle in all_turtles:
        if turtle.xcor() > 230:
            is_race_on = False
            winning_color = turtle.pencolor()
            if winning_color == user_bet:
                print(f"You've won! The {winning_color} turtle is the winner!")
            else:
                print(f"You've lost! The {winning_color} turtle is the winner!")
        rand_distance = random.randint(0, 10)
        turtle.forward(rand_distance)

screen.exitonclick()
