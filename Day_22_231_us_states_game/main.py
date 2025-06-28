import turtle

IMAGE = "self_study/231_us_states_game/blank_states_img.gif"


screen = turtle.Screen()
screen.title("U.S. States Game")
screen.addshape(IMAGE)
turtle.shape(IMAGE)

def get_mouse_click_coor(x, y):
    print(x,y)

turtle.onscreenclick(get_mouse_click_coor)
turtle.mainloop()

screen.exitonclick() 