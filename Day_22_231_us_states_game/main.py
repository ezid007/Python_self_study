from rich import print
import turtle
import pandas as pd

IMAGE = "self_study/Day_22_231_us_states_game/blank_states_img.gif"

screen = turtle.Screen()
screen.title("U.S. States Game")
screen.addshape(IMAGE)
turtle.shape(IMAGE)

t = turtle.Turtle()
t.hideturtle()
t.penup()

# def get_mouse_click_coor(x, y):
#     print(x,y)

# turtle.onscreenclick(get_mouse_click_coor)
# turtle.mainloop()

data = pd.read_csv("self_study/Day_22_231_us_states_game/50_states.csv")
all_states = data.state.to_list()
guessed_states = []

while len(guessed_states) < 50:
    answer_state = screen.textinput(
        title=f"{len(guessed_states)}/50 States Correct", prompt="What's another state's name?"
    )
    
    if answer_state is None:
        continue
    
    answer_state = answer_state.title()
    
    if answer_state == 'Exit':
        missing_states = [state for state in all_states if state not in guessed_states]
        pd.DataFrame(missing_states).to_csv("self_study/Day_22_231_us_states_game/states_to_learn.csv")
        break
    
    if answer_state in all_states and answer_state not in guessed_states:
        guessed_states.append(answer_state)
        state_data = data[data.state == answer_state]
        
        x_cor = state_data.x.item()
        y_cor = state_data.y.item()
        t.goto(x_cor, y_cor)
        
        t.write(state_data.state.item())
        
