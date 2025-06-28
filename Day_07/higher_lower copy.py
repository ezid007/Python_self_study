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
    return max(items, key=lambda x: x['follower_count'])

def compare_item(win, items, choice):
    global game_over
    global win_count
    for item in items:
        print(f"{item['name']}")
        print(f"follower_count: {item['follower_count']}")
        print()
    if (choice == 'up' and items[0] == win) or (choice == 'down' and items[1] == win):
        win_count += 1
    else:
        print(f"correct: {win_count}\nGame Over")
        game_over = False
        
def main():
    os.system('cls')
    print(data.logo)

    print('Higher Lower 게임을 시작하겠습니다.\n아무키나 누르시오...')
    msvcrt.getch()
    
    global game_over
    global win_count
    
    game_over = True
    win_count = 0
    
    while game_over:
        os.system('cls')
        items = pt_item()

        choice = input(f"correct: {win_count} 당신의 초이스는? [up/down]: ").strip().lower()

        win = win_item(items)

        os.system('cls')
        compare_item(win, items, choice)
        
if __name__ == '__main__':
    main()