import random

EASY_LEVEL_TURNS = 10
HARD_LEVEL_TURNS = 5
DEBUG_MODE = False

def set_difficulty():
    diff_choice = {'easy': EASY_LEVEL_TURNS, 'hard': HARD_LEVEL_TURNS}
    while True:
        diff = input("난이도를 입력 하시오. [easy/hard]: ").strip().lower()
        if diff in diff_choice:
            return diff_choice[diff]
        print("잘못 입력 하였습니다. 다시 입력 해주세요.")

def check_answer(guess, answer):
    if guess > answer:
        print("설정된 숫자보다 높습니다.")
    elif guess < answer:
        print("설정된 숫자보다 낮습니다.")
    else:
        print(f"정답 입니다! 숫자는: {answer}입니다.")
        return True
    return False

def number_guessing_game():
    random_number = random.randint(1, 100)
    if DEBUG_MODE:
        print(f"디버깅 모드: 정답은 {random_number}입니다.")  # 디버깅용 메시지
    life = set_difficulty()
    print("1부터 100 사이의 숫자를 맞춰보세요!")

    while life > 0:
        try:
            guess = int(input(f"예측되는 숫자를 입력 하시오 (생명: {life}): "))
            if guess < 1 or guess > 100:
                print("숫자는 1에서 100 사이여야 합니다. 다시 입력하세요.")
                continue
        except ValueError:
            print("숫자를 입력해야 합니다. 다시 시도하세요.")
            continue

        if check_answer(guess, random_number):
            break

        life -= 1
        if life == 0:
            print(f"Game over! 정답은 {random_number}였습니다.")

if __name__ == "__main__":
    number_guessing_game()
