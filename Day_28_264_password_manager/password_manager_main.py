from tkinter import Tk, Canvas, PhotoImage, Label, Entry, Button, END, messagebox
import random

# ---------------------------- PASSWORD GENERATOR ------------------------------- #


# ---------------------------- SAVE PASSWORD ------------------------------- #


def save():
    website = website_entry.get()
    email = email_entry.get()
    password = password_entry.get()

    is_ok = messagebox.askokcancel(
        website,
        f"These are the details entered:\nEmail: {email}\nPassword: {password}\nIs it ok to save?",
    )

    if is_ok:
        with open(
            "self_study/Day_28_264_password_manager/data.txt", "a", encoding="utf-8"
        ) as data_file:
            data_file.write(f"{website} | {email} | {password}\n")
            website_entry.delete(0, END)
            password_entry.delete(0, END)


# ---------------------------- UI SETUP ------------------------------- #


window = Tk()
window.title("Password Manager")
# 창 전체에 좌우 50, 상하 20의 여백을 줍니다.
window.config(padx=50, pady=50)


canvas = Canvas(height=200, width=200, highlightthickness=0)
logo_img = PhotoImage(file="self_study/Day_28_264_password_manager/logo.png")
canvas.create_image(100, 100, image=logo_img)
# 로고 이미지를 0행 1열에 배치합니다.
canvas.grid(
    row=0, column=1, pady=(0, 20)
)  # 이미지와 라벨 글씨 사이의 여백을 추가합니다.

# --- Labels ---
# 레이블들을 모두 0열에 배치하고, 오른쪽 정렬(sticky="e")하여 깔끔하게 맞춥니다.
website_label = Label(text="Website:")
website_label.grid(row=1, column=0, sticky="e")

email_label = Label(text="Email/Username:")
email_label.grid(row=2, column=0, sticky="e")

password_label = Label(text="Password:")
password_label.grid(row=3, column=0, sticky="e")

# --- Entries ---
# 입력 필드들을 1열에 배치하고, 가로로 꽉 채우도록(sticky="ew") 설정합니다.
website_entry = Entry()
# 1열과 2열을 병합(columnspan=2)하고, 가로로 꽉 채웁니다(sticky="ew").
website_entry.grid(row=1, column=1, columnspan=2, sticky="ew", padx=5)
website_entry.focus()  # 프로그램 시작 시 커서를 여기에 둡니다.

email_entry = Entry()
email_entry.grid(row=2, column=1, columnspan=2, sticky="ew", padx=5, pady=5)
email_entry.insert(0, "asdf@gmail.com")

password_entry = Entry()
# 1열에만 배치하고 가로로 채웁니다.
password_entry.grid(row=3, column=1, sticky="ew", padx=5)

# --- Buttons ---
# 버튼들도 가로로 꽉 채워(sticky="ew") 균형을 맞춥니다.
generate_password_button = Button(text="Generate Password")
# 2열에 배치하고 가로로 채웁니다.
generate_password_button.grid(row=3, column=2, sticky="ew", padx=(5, 0))

add_button = Button(text="Add", width=36, command=save)
# 1열과 2열을 병합하고 가로로 채웁니다.
add_button.grid(row=4, column=1, columnspan=2, sticky="ew", padx=5, pady=5)


window.mainloop()
