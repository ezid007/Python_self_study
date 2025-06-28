import random
import data
import os
import msvcrt

def display_item(item):
    """Display details of a single item."""
    for key, value in item.items():
        if key != 'follower_count':
            print(f"{key}: {value}")

def display_comparison(items):
    """Display details of the comparison items."""
    for item in items:
        print(f"name: {item['name']}")
        print(f"follower_count: {item['follower_count']}")
        print()

def pt_item():
    """Pick two random items for comparison and display them."""
    compare_pt = random.sample(data.data, 2)
    display_item(compare_pt[0])
    print(data.vs)
    display_item(compare_pt[1])
    return compare_pt

def win_item(items):
    """Determine the item with the higher follower count."""
    return max(items, key=lambda x: x['follower_count'])

def compare_item(win, items, choice):
    """Check if the player's choice matches the winning item."""
    global game_over
    display_comparison(items)

    if (choice == 'up' and items[0] == win) or (choice == 'down' and items[1] == win):
        print('You win')
    else:
        print('You lose')
        game_over = False

def main():
    os.system('cls')
    print(data.logo)
    print('Higher Lower 게임을 시작하겠습니다.\n아무키나 누르시오...')
    msvcrt.getch()

    global game_over
    game_over = True

    while game_over:
        os.system('cls')
        items = pt_item()
        choice = input("당신의 초이스는? [up/down]: ").strip().lower()
        win = win_item(items)
        os.system('cls')
        compare_item(win, items, choice)

if __name__ == "__main__":
    main()
    
