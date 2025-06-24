from my_utils import print
import datetime

class Character:
    def __init__(self, name, level, hp, max_hp):
        self.name = name
        self.level = level
        self.hp = hp
        self.max_hp = max_hp
    
    # __repr__은 개발자를 위해 명확하게!
    def __repr__(self):
        return f"Character(name='{self.name}', level={self.level}, hp={self.hp}, max_hp={self.max_hp})"

    # __str__은 사용자를 위해 친절하게!
    def __str__(self):
        return f"<{self.name} | 레벨 {self.level} | HP {self.hp}/{self.max_hp}>"

today = datetime.datetime.now()
char = Character("용기사", 50, 2800, 3500)

# print()는 __str__을 호출합니다.
print(today) # 출력: 2025-06-23 10:35:15.123456 (사람이 보기 편한 형식)
print(char)  # 출력: <용기사 | 레벨 50 | HP 2800/3500>
print(f"{char}", style="warning")