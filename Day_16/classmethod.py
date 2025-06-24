class GameCharacter:
    # 클래스 속성: 이 클래스로부터 생성된 모든 인스턴스가 공유합니다.
    species = "Human"

    def __init__(self, nickname):
        self.nickname = nickname

    def show_info(self):
        # 인스턴스 메소드는 클래스 속성에 접근할 수 있습니다.
        print(f"닉네임: {self.nickname}, 종족: {self.species}")

    # 클래스 속성을 제어하는 클래스 메소드
    @classmethod
    def change_species(cls, new_species):
        # cls는 GameCharacter 클래스 자체를 가리킵니다.
        print(f"모든 캐릭터의 종족을 '{cls.species}'에서 '{new_species}'(으)로 변경합니다.")
        cls.species = new_species

# 캐릭터 생성
char1 = GameCharacter("전사")
char2 = GameCharacter("마법사")

char1.show_info() # 출력: 닉네임: 전사, 종족: Human
char2.show_info() # 출력: 닉네임: 마법사, 종족: Human
print("-" * 20)

# 클래스 메소드를 호출하여 클래스 속성을 변경 (객체 없이 클래스 이름으로 바로 호출)
GameCharacter.change_species("Elf")
print("-" * 20)

# 기존에 생성된 객체들의 종족도 모두 변경됩니다.
char1.show_info() # 출력: 닉네임: 전사, 종족: Elf
char2.show_info() # 출력: 닉네임: 마법사, 종족: Elf

# 새로 생성하는 객체도 변경된 클래스 속성을 따릅니다.
char3 = GameCharacter("궁수")
char3.show_info() # 출력: 닉네임: 궁수, 종족: Elf



class Employee:
    # 1. 기본 생성자 (__init__)
    def __init__(self, name, age, department):
        self.name = name
        self.age = age
        self.department = department
        print(f"'{self.name}' 직원 객체가 성공적으로 생성되었습니다.")

    def __str__(self):
        return f"[{self.department}] {self.name} ({self.age}세)"

    # 2. 대안 생성자 1: 문자열로부터 객체를 만드는 팩토리
    @classmethod
    def from_string(cls, data_string):
        print(f"'{data_string}' 문자열로부터 객체를 생성합니다...")
        # 문자열을 파싱해서 이름, 나이, 부서를 분리
        name, age, department = data_string.split(',')
        # cls는 Employee 클래스이므로, cls()는 Employee()와 같음
        # 파싱한 데이터로 기본 생성자를 호출하여 객체를 생성하고 반환
        return cls(name, int(age), department)

    # 3. 대안 생성자 2: 딕셔너리로부터 객체를 만드는 팩토리
    @classmethod
    def from_dict(cls, data_dict):
        print(f"딕셔너리 데이터로부터 객체를 생성합니다...")
        return cls(data_dict['name'], data_dict['age'], data_dict['department'])


# --- 다양한 방법으로 직원 객체 생성하기 ---

# 방법 1: 기본 생성자 사용
e1 = Employee("이영희", 28, "개발팀")

# 방법 2: 문자열로부터 생성 (from_string 클래스 메소드 사용)
e2 = Employee.from_string("김철수,35,인사팀")

# 방법 3: 딕셔너리로부터 생성 (from_dict 클래스 메소드 사용)
api_data = {"name": "박지성", "age": 42, "department": "해외사업부"}
e3 = Employee.from_dict(api_data)

print("\n--- 생성된 직원 목록 ---")
print(e1)
print(e2)
print(e3)