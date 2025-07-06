from tkinter import Tk, Canvas, PhotoImage, Label, Entry, Button, END, messagebox
import random
import json

# ---------------------------- 상수 ------------------------------- #
# 함수 밖으로 빼서 상수로 만들어 메모리 효율성 증대
LETTERS = [
    "a",
    "b",
    "c",
    "d",
    "e",
    "f",
    "g",
    "h",
    "i",
    "j",
    "k",
    "l",
    "m",
    "n",
    "o",
    "p",
    "q",
    "r",
    "s",
    "t",
    "u",
    "v",
    "w",
    "x",
    "y",
    "z",
    "A",
    "B",
    "C",
    "D",
    "E",
    "F",
    "G",
    "H",
    "I",
    "J",
    "K",
    "L",
    "M",
    "N",
    "O",
    "P",
    "Q",
    "R",
    "S",
    "T",
    "U",
    "V",
    "W",
    "X",
    "Y",
    "Z",
]
NUMBERS = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
SYMBOLS = ["!", "#", "$", "%", "&", "(", ")", "*", "+"]


# ---------------------------- 비밀번호 생성기 ------------------------------- #
def generate_password():
    """랜덤 비밀번호를 생성하고 입력 필드에 삽입하며 클립보드에 복사합니다."""
    password_letters = [random.choice(LETTERS) for _ in range(random.randint(8, 10))]
    password_symbols = [random.choice(SYMBOLS) for _ in range(random.randint(2, 4))]
    password_numbers = [random.choice(NUMBERS) for _ in range(random.randint(2, 4))]

    password_list = password_letters + password_symbols + password_numbers
    random.shuffle(password_list)

    password = "".join(password_list)
    password_entry.delete(0, END)
    password_entry.insert(0, password)
    window.clipboard_clear()
    window.clipboard_append(password)
    messagebox.showinfo(title="알림", message="비밀번호가 클립보드에 복사되었습니다!")


# ---------------------------- 비밀번호 검색 ------------------------------- #
def find_password():
    """JSON 파일에서 웹사이트를 검색하여 정보를 보여줍니다."""
    website = website_entry.get()
    try:
        with open("self_study/Day_28_264_password_manager/data.json", "r") as data_file:
            data = json.load(data_file)
    except FileNotFoundError:
        messagebox.showinfo(title="오류", message="저장된 데이터 파일이 없습니다.")
    else:
        if website in data:
            email = data[website]["email"]
            password = data[website]["password"]
            messagebox.showinfo(
                title=website, message=f"이메일: {email}\n비밀번호: {password}"
            )
        else:
            messagebox.showinfo(
                title="오류", message=f"'{website}'에 대한 정보를 찾을 수 없습니다."
            )


# ---------------------------- 비밀번호 저장 ------------------------------- #
def save():
    """입력된 데이터를 JSON 파일에 저장합니다."""
    website = website_entry.get()
    email = email_entry.get()
    password = password_entry.get()
    new_data = {
        website: {
            "email": email,
            "password": password,
        }
    }

    # 더 간결하고 파이썬다운 방식의 유효성 검사
    if not website or not password:
        messagebox.showinfo(
            title="Oops", message="비어있는 칸이 있습니다. 확인해주세요."
        )
        return

    is_ok = messagebox.askokcancel(
        website,
        f"입력하신 정보는 다음과 같습니다:\n이메일: {email}\n비밀번호: {password}\n저장하시겠습니까?",
    )

    if is_ok:
        try:
            with open("data.json", "r") as data_file:
                # 1. 기존 데이터 읽기
                data = json.load(data_file)
        except FileNotFoundError:
            # 2. 파일이 없으면, 쓰기 모드로 파일 생성
            with open("data.json", "w") as data_file:
                json.dump(new_data, data_file, indent=4)
        else:
            # 3. 기존 데이터에 새로운 정보 추가
            data.update(new_data)
            with open("data.json", "w") as data_file:
                # 4. 업데이트된 전체 데이터 저장
                json.dump(data, data_file, indent=4)
        finally:
            website_entry.delete(0, END)
            password_entry.delete(0, END)


# ---------------------------- UI 설정 ------------------------------- #
window = Tk()
window.title("비밀번호 관리자")
window.config(padx=50, pady=50)

canvas = Canvas(height=200, width=200, highlightthickness=0)
try:
    logo_img = PhotoImage(file="self_study/Day_28_264_password_manager/logo.png")
    canvas.create_image(100, 100, image=logo_img)
except Exception:
    canvas.create_text(100, 100, text="LOGO", font=("Arial", 50))
canvas.grid(row=0, column=1)

# --- 위젯 ---
website_label = Label(text="웹사이트:")
website_label.grid(row=1, column=0, sticky="w")
email_label = Label(text="이메일/사용자명:")
email_label.grid(row=2, column=0, sticky="w")
password_label = Label(text="비밀번호:")
password_label.grid(row=3, column=0, sticky="w")

website_entry = Entry()
website_entry.grid(row=1, column=1, sticky="ew")
website_entry.focus()
email_entry = Entry()
email_entry.grid(row=2, column=1, columnspan=2, sticky="ew")
email_entry.insert(0, "asdf@gmail.com")
password_entry = Entry()
password_entry.grid(row=3, column=1, sticky="ew")

search_button = Button(text="검색", command=find_password)
search_button.grid(row=1, column=2, sticky="ew")
generate_password_button = Button(text="비밀번호 생성", command=generate_password)
generate_password_button.grid(row=3, column=2, sticky="ew")
add_button = Button(text="추가", command=save)
add_button.grid(row=4, column=1, columnspan=2, sticky="ew")

window.mainloop()
