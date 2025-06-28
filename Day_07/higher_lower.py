import random
import data
import os
import msvcrt


def pt_item():
    compare_pt = random.sample(data.data, 2)
    for indx, i in enumerate(compare_pt):
        for key, value in i.items():
            if 'follower_count' not in key:
                print(f"{key}: {value}")
        if indx == 0:
            print(data.vs)
    return compare_pt

def win_item(items: list):
    if items[0]['follower_count'] > items[1]['follower_count']:
        return items[0]
    else:
        return items[1]

def compare_item(win, items, choice):
    global game_over
    if choice == 'up':
        if items[0] == win:
            print(f"name = {items[0]["name"]}")
            print(f"follower_count = {items[0]["follower_count"]}")
            print()
            print(f"name = {items[1]["name"]}")
            print(f"follower_count = {items[1]["follower_count"]}")
            print('You win')
        else:
            print(f"name = {items[0]["name"]}")
            print(f"follower_count = {items[0]["follower_count"]}")
            print()
            print(f"name = {items[1]["name"]}")
            print(f"follower_count = {items[1]["follower_count"]}")
            print('You lose')
            game_over = False

    elif choice == 'down':
        if items[1] == win:
            print(f"name = {items[0]["name"]}")
            print(f"follower_count = {items[0]["follower_count"]}")
            print()
            print(f"name = {items[1]["name"]}")
            print(f"follower_count = {items[1]["follower_count"]}")
            print('You win')
        else:
            print(f"name = {items[0]["name"]}")
            print(f"follower_count = {items[0]["follower_count"]}")
            print()
            print(f"name = {items[1]["name"]}")
            print(f"follower_count = {items[1]["follower_count"]}")
            print('You lose')
            game_over = False


os.system('cls')
print(data.logo)

print('Higher Lower 게임을 시작하겠습니다.\n아무키나 누르시오...')
msvcrt.getch()

game_over = True

while game_over:
    os.system('cls')
    items = pt_item()

    choice = input("당신의 초이스는? [up/down]: ").strip().lower()

    win = win_item(items)

    os.system('cls')
    compare_item(win, items, choice)