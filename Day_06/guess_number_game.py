import random

def set_difficulty():
    diff_choice = {'easy': 10, 'hard': 5}
    while True:
        diff = input(f"난이도를 입력 하시오. [easy/hard]: ").strip().lower()
        if diff in diff_choice:
            return diff_choice[diff]
        else:
            print(f"잘못 입력 하였습니다. 다시 입력 해주세요.")

def check_answer(guess, answer, now_life):
    if guess > answer:
        print(f'설정된 숫자보다 높습니다. 생명: {now_life} ')
    elif guess < answer:
        print(f'설정된 숫자보다 낮습니다. 생명: {now_life}')
    else:
        print(f'정답 입니다. 숫자는 :{answer}입니다.')

def main_game():
    random_number = random.randint(1,100)
    my_guess = 0
    life = set_difficulty()

    while random_number != my_guess:
        
        my_guess = int(input(f'예측되는 숫자를 입력 하시오: '))
        check_answer(my_guess, random_number, life)
        if life == 0:
            print(f'Game over\n숫자는 :{random_number}입니다.')
            break
        elif life == 2:
            print(random_number)
        life -= 1
        
main_game()