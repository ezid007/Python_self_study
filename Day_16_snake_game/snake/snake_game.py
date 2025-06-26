from turtle import Screen
from snake import Snake
from food import Food
from scoreboard import Scoreboard
import time


WALL = 290
COUNTDOWN_FONT = ("Courier", 80, "normal")
INITIAL_SPEED_DELAY = 150
SPEED_INCREMENT = 10
NIM_SPEED_DELAY = 10

current_speed_delay = INITIAL_SPEED_DELAY

screen = Screen()
screen.setup(width=600, height=600)
screen.bgcolor("black")
screen.title("My Snake Game")

player_name = screen.textinput(title="Player Name", prompt="Enter your name:")

if not player_name:
    player_name = "Player"

screen.tracer(0)

snake = Snake()
food = Food()
scoreboard = Scoreboard()

snake.hide()
food.hideturtle()

for i in range(5, 0 , -1):
    scoreboard.goto(0, 50)
    scoreboard.clear()
    scoreboard.write(i, align="center", font=COUNTDOWN_FONT)
    screen.update()
    time.sleep(1)

scoreboard.goto(0, 260)
scoreboard.update_scoreboard()

snake.show()
food.showturtle()
screen.update()

screen.listen()
screen.onkey(snake.up, "Up")
screen.onkey(snake.down, "Down")
screen.onkey(snake.left, "Left")
screen.onkey(snake.right, "Right")

game_is_on = True

def game_loop():
    global game_is_on
    global current_speed_delay
    if not game_is_on:
        return

    snake.move()
    screen.update()

    if snake.head.distance(food) < 15:
        scoreboard.increase_score()
        food.refresh()
        snake.extend()
        if current_speed_delay > NIM_SPEED_DELAY:
            current_speed_delay -= SPEED_INCREMENT

    if snake.head.xcor() > WALL or snake.head.xcor() < -WALL or snake.head.ycor() > WALL or snake.head.ycor() < -WALL:
        game_is_on = False
        snake.hide()
        food.hideturtle()
        screen.update()
        scoreboard.save_score(player_name)
        scoreboard.display_leaderboard()
    
    if len(snake.segments) > 4:
        for segment in snake.segments[1:]:
            if snake.head.distance(segment) < 10:
                game_is_on = False
                snake.hide()
                food.hideturtle()
                screen.update()
                scoreboard.save_score(player_name)
                scoreboard.display_leaderboard()

    screen.ontimer(game_loop, int(current_speed_delay))

game_loop()

screen.exitonclick()
