import random
import os

def ace_card(deck):
    """Adjust Ace value if total exceeds 21."""
    while 11 in deck and sum(deck) > 21:
        deck[deck.index(11)] = 1

def deal_card(cards, num, deck):
    """Deal a specified number of cards to a deck."""
    for _ in range(num):
        card = random.choice(cards)
        cards.remove(card)
        deck.append(card)

def blackjack(deck):
    """Check if a deck has a Blackjack."""
    if 10 in deck and 11 in deck:
        return True
    return False

def game_over(user_deck, com_deck, result):
    """Handle the game-over logic."""
    print(f'{result}\nGame Over')
    print(f'Your Cards: {user_deck}, Total: {sum(user_deck)}')
    print(f'Computer Cards: {com_deck}, Total: {sum(com_deck)}')
    return False

def compare_decks(user_deck, com_deck):
    """Compare user and computer decks to decide the winner."""
    user_total = sum(user_deck)
    com_total = sum(com_deck)

    if user_total > com_total or com_total > 21:
        return game_over(user_deck, com_deck, 'You win!')
    elif user_total < com_total:
        return game_over(user_deck, com_deck, 'You lose!')
    else:
        return game_over(user_deck, com_deck, 'It\'s a draw!')

# Initialize variables
cards = [11, 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10]
user_deck = []
com_deck = []

deal_card(cards, 2, user_deck)
deal_card(cards, 2, com_deck)

# Check for Blackjack
if blackjack(user_deck):
    game_continue = game_over(user_deck, com_deck, 'Blackjack! You win!')
elif blackjack(com_deck):
    game_continue = game_over(user_deck, com_deck, 'Blackjack! Computer wins!')
else:
    game_continue = True

# Main game loop
while game_continue:
    os.system('cls')
    print(f'Your Cards: {user_deck}, Total: {sum(user_deck)}')
    print(f'Computer Cards: [{com_deck[0]}, ?]')

    action = input('Do you want another card? [y/n]: ').lower()

    if action == 'y':
        deal_card(cards, 1, user_deck)
        ace_card(user_deck)

        if sum(user_deck) > 21:
            game_continue = game_over(user_deck, com_deck, 'You busted! You lose!')
    else:
        while sum(com_deck) < 17:
            deal_card(cards, 1, com_deck)
            ace_card(com_deck)

        game_continue = compare_decks(user_deck, com_deck)
