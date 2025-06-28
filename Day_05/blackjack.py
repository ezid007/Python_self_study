import random

def ace_card(deck: list):
    if 11 in deck and 21 < sum(deck):
        deck.remove(11)
        deck.append(1)
    
def deal_card(cards: list, num: int, who: int):
    for _ in range(num):
        deck = random.choice(cards)
        cards.remove(deck)
        if who == 0:
            my_deck.append(deck)
        else:
            com_deck.append(deck)
        
def blackjack(r_card: list, who: int):
    global game_continue
    if 10 in r_card and 11 in r_card:
        game_continue = False
        return "Blackjack!!"
    elif who == 0:
        return r_card
    else:
        return [r_card[0]]

def game_over(deck: list, who: int):
    global game_continue
    if sum(deck) > 21 and who == 0:
        game_continue = False
        print('you lose\n game over')
        print(f'나의카드: {my_deck} 합: {sum(my_deck)}')
        print(f'컴의카드: {com_deck} 합: {sum(com_deck)}')

    elif sum(deck) > 21 and who == 1:
        game_continue = False
        print('you win\n game over')
        print(f'나의카드: {my_deck} 합: {sum(my_deck)}')
        print(f'컴의카드: {com_deck} 합: {sum(com_deck)}')

def compare(user_card: list, com_card: list):
    global game_continue
    if sum(user_card) > sum(com_card):
        deal_card(cards, 1, 1)
        ace_card(com_deck)
        if sum(user_card) == sum(com_card):
            game_continue = False
            print('you lose\n game over')
            print(f'나의카드: {my_deck} 합: {sum(my_deck)}')
            print(f'컴의카드: {com_deck} 합: {sum(com_deck)}')

        game_over(cards, 1)
    if sum(user_card) < sum(com_card) and sum(com_card) <=21:
        print('you lose\n game over')
        print(f'나의카드: {my_deck} 합: {sum(my_deck)}')
        print(f'컴의카드: {com_deck} 합: {sum(com_deck)}')

        game_continue = False

cards = [11, 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10]
my_deck = []
com_deck = []

deal_card(cards, 2, 0)
deal_card(cards, 2, 1)

print(f'나의 카드: {blackjack(my_deck, 0)}')
print(f'컴의 카드: {blackjack(com_deck, 1)}')

game_continue = True

while game_continue:
    new_question = input(f'새로운 카드를 받겠습니까? [y/n]')

    if new_question == 'y':
        deal_card(cards, 1, 0)
        ace_card(my_deck)
        game_over(my_deck,0)
        print(f'나의카드: {my_deck} 합: {sum(my_deck)}')

    else:
        compare(my_deck, com_deck)
