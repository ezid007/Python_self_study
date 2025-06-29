from rich import print
import turtle
import pandas as pd
import os

os.system('cls')

IMAGE = "self_study/Day_22_231_us_states_game/blank_states_img.gif"
STATES_50 = "self_study/Day_22_231_us_states_game/50_states.csv"

screen = turtle.Screen()
screen.title("U.S. States Game")
screen.addshape(IMAGE)
turtle.shape(IMAGE)

# def get_mouse_click_coor(x, y):
#     print(x,y)

# turtle.onscreenclick(get_mouse_click_coor)
# turtle.mainloop()

data = pd.read_csv(STATES_50)
all_states = data.state.to_list()
guessed_states = []

while len(guessed_states) < 50:
    
    answer_state = screen.textinput(
        title="Guess the State", prompt="What's another state's name?"
    )

    if answer_state in all_states:
        guessed_states.append(answer_state)
        t = turtle.Turtle()
        t.hideturtle()
        t.penup()
        state_data = data[data.state == answer_state]
        t.goto(int(state_data.x.item()), int(state_data.y.item()))
        t.write(state_data.state.iloc[0])

screen.exitonclick()

