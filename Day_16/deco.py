class Player:
    def __init__(self, name, level):
        self.name = name
        self._level = level # 실제 값은 _(언더스코어)가 붙은 변수에 저장

    @property
    def level(self):
        print("레벨 값을 가져갑니다.")
        return self._level

    @level.setter
    def level(self, value):
        if value < 1:
            print("레벨은 1보다 낮을 수 없습니다. 레벨을 1로 설정합니다.")
            self._level = 1
        else:
            print(f"레벨을 {value}로 설정합니다.")
            self._level = value

player2 = Player("마법사", 5)

# .level 속성에 접근하면 @property 메소드가 호출됨
print(f"{player2.name}의 레벨은 {player2.level}입니다.")
# 출력:
# 레벨 값을 가져갑니다.
# 마법사의 레벨은 5입니다.

# .level 속성에 값을 할당하면 @level.setter 메소드가 호출됨
player2.level = -5
# 출력:
# 레벨은 1보다 낮을 수 없습니다. 레벨을 1로 설정합니다.

print(f"조정된 레벨은 {player2.level}입니다.")
# 출력:
# 레벨 값을 가져갑니다.
# 조정된 레벨은 1입니다.


class Player2:
    MAX_LEVEL = 99 # 클래스 속성 (모든 Player 객체가 공유)

    def __init__(self, name):
        self.name = name

    # 클래스 메소드: '만렙' 플레이어를 만드는 특별한 생성 방법
    @classmethod
    def create_max_level_player(cls, name):
        print(f"최대 레벨({cls.MAX_LEVEL}) 플레이어를 생성합니다.")
        return cls(name) # cls는 Player 클래스 자체를 의미함

    # 정적 메소드: 게임 규칙을 설명하는, 상태와 무관한 함수
    @staticmethod
    def get_game_rules():
        return "1. 즐겁게 플레이하세요. 2. 다른 유저를 존중하세요."



# 클래스 메소드 호출 (객체 생성 없이 클래스에서 바로 호출)
max_player = Player2.create_max_level_player("지존전사")

# 정적 메소드 호출
print("게임 규칙:", Player2.get_game_rules())
