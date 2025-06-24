class Player:
    def __init__(self, nickname):
        # 닉네임이 유효한지 정적 메소드로 검사
        if not Player.is_valid_nickname(nickname):
            raise ValueError(f"'{nickname}'은(는) 사용할 수 없는 닉네임입니다.")
        self.nickname = nickname

    def attack(self):
        print(f"{self.nickname}이(가) 공격합니다!")

    # 정적 메소드 1: 닉네임 유효성 검사
    @staticmethod
    def is_valid_nickname(name):
        # 닉네임 길이는 3 이상 8 이하여야 한다는 규칙
        # 이 규칙은 특정 플레이어의 상태(self)나 클래스 상태(cls)와 무관함
        return 3 <= len(name) <= 8

    # 정적 메소드 2: 욕설 필터링
    @staticmethod
    def contains_profanity(text):
        # 욕설이 포함되어 있는지 검사하는 로직 (예시)
        profane_words = ["바보", "멍청이"]
        for word in profane_words:
            if word in text:
                return True
        return False

# --- 사용하기 ---

# 정적 메소드는 클래스 이름으로 바로 호출
print(f"닉네임 '전사'는 유효한가? {Player.is_valid_nickname('전사')}")
print(f"닉네임 '최강용기사'는 유효한가? {Player.is_valid_nickname('최강용기사')}")
print(f"'안녕 바보야'에 욕설이 포함되어 있는가? {Player.contains_profanity('안녕 바보야')}")

# 클래스 내부에서도 사용됨
try:
    p1 = Player("용사")     # 유효함
    p2 = Player("용")       # 에러 발생!
except ValueError as e:
    print(e)