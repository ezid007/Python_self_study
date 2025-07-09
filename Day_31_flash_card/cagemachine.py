# --- 1. 설계도(Class) 정의 ---
# "음료 제조기는 이런 부품과 기능을 가져야 한다"는 규칙을 정합니다.
class CafeMachine:
    # --- 2. 초기화 함수 (생성자) ---
    # 기계를 처음 만들 때, 필수 부품을 장착하는 부분입니다.
    def __init__(self, initial_coffee_beans, initial_milk):
        """
        CafeMachine 객체가 처음 생성될 때 실행됩니다.
        'self'는 만들어질 '기계 자기 자신'을 의미합니다.
        """
        print(f"새로운 음료 제조기를 설치합니다! (원두: {initial_coffee_beans}g, 우유: {initial_milk}ml)")
        # 기계의 부품(속성)을 설정합니다.
        self.coffee_beans = initial_coffee_beans  # '나의' 원두 재고
        self.milk = initial_milk                  # '나의' 우유 재고

    # --- 3. 기능(Method) 정의 ---
    # 이 기계가 할 수 있는 동작들을 정의합니다.
    def make_americano(self):
        """아메리카노를 만드는 기능"""
        print("\n[주문] 아메리카노 한 잔 부탁해요!")
        # '나의' 원두 재고를 확인합니다.
        if self.coffee_beans >= 20:
            print(">> 네, 아메리카노를 만듭니다. (원두 20g 사용)")
            self.coffee_beans -= 20  # 원두 재고 차감
        else:
            print(">> 죄송합니다. 원두가 부족합니다.")
        # 현재 재고 상태를 보여줍니다.
        self.check_stock()

    def make_latte(self):
        """라떼를 만드는 기능"""
        print("\n[주문] 라떼 한 잔 부탁해요!")
        # '나의' 원두와 우유 재고를 모두 확인합니다.
        if self.coffee_beans >= 20 and self.milk >= 150:
            print(">> 네, 라떼를 만듭니다. (원두 20g, 우유 150ml 사용)")
            self.coffee_beans -= 20  # 원두 재고 차감
            self.milk -= 150         # 우유 재고 차감
        else:
            print(">> 죄송합니다. 원두나 우유가 부족합니다.")
        # 현재 재고 상태를 보여줍니다.
        self.check_stock()

    def check_stock(self):
        """현재 재고를 확인하는 기능"""
        print(f"---- 현재 재고: 원두 {self.coffee_beans}g, 우유 {self.milk}ml ----")


# --- 4. 설계도로 실제 기계(Object) 만들기 ---
print("===== 1호점 기계 설치 =====")
machine_1 = CafeMachine(initial_coffee_beans=100, initial_milk=500)

print("\n===== 2호점 기계 설치 =====")
machine_2 = CafeMachine(initial_coffee_beans=50, initial_milk=200)


# --- 5. 만들어진 기계들 사용해보기 ---
# 각 기계는 자신만의 재고를 가지고 독립적으로 동작합니다.

print("\n\n===== 1호점 운영 시작! =====")
machine_1.make_latte()      # 1호점 기계로 라떼 만들기
machine_1.make_americano()  # 1호점 기계로 아메리카노 만들기

print("\n\n===== 2호점 운영 시작! =====")
machine_2.make_latte()      # 2호점 기계로 라떼 만들기 (재료 부족!)
machine_2.make_americano()  # 2호점 기계로 아메리카노 만들기

