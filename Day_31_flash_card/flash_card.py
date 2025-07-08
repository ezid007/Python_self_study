import tkinter as tk
import pandas as ps
import random

BACKGROUND_COLOR = "#B1DDC6"

try:
    data = ps.read_csv("self_study/Day_31_flash_card/data/words_to_learn.csv")
except FileNotFoundError:
    data = ps.read_csv("self_study/Day_31_flash_card/data/eng_words.csv")

to_learn = data.to_dict(orient="records")
current_card = {}
flip_timer = None


def next_card():
    global current_card, flip_timer

    if flip_timer:
        window.after_cancel(flip_timer)
    current_card = random.choice(to_learn)
    canvas.itemconfig(card_title, text="English", fill="black")
    canvas.itemconfig(card_word, text=current_card["English"], fill="black")
    canvas.itemconfig(card_background, image=card_front_img)
    flip_timer = window.after(3000, func=flip_card)


def flip_card():
    global current_card
    canvas.itemconfig(card_title, text="Korean", fill="white")
    canvas.itemconfig(card_word, text=current_card["Korean"], fill="white")
    canvas.itemconfig(card_background, image=card_back_img)


def is_known():
    to_learn.remove(current_card)
    next_card()


def on_closing():
    data = ps.DataFrame(to_learn)
    data.to_csv("self_study/Day_31_flash_card/data/words_to_learn.csv", index=False)
    window.destroy()


window = tk.Tk()
window.title("Flashy")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

canvas = tk.Canvas(width=800, height=526)
card_front_img = tk.PhotoImage(
    file="self_study/Day_31_flash_card/images/card_front.png"
)
card_back_img = tk.PhotoImage(file="self_study/Day_31_flash_card/images/card_back.png")
card_background = canvas.create_image(400, 263, image=card_front_img)
canvas.config(bg=BACKGROUND_COLOR, highlightthickness=0)
card_title = canvas.create_text(400, 150, text="", font=("Ariel", 40, "italic"))
card_word = canvas.create_text(400, 263, text="", font=("Ariel", 60, "bold"))
canvas.grid(row=0, column=0, columnspan=2)

right_img = tk.PhotoImage(file="self_study/Day_31_flash_card/images/right.png")
right_button = tk.Button(image=right_img, highlightthickness=0, command=is_known)
right_button.grid(column=0, row=1)

wrong_img = tk.PhotoImage(file="self_study/Day_31_flash_card/images/wrong.png")
wrong_button = tk.Button(image=wrong_img, highlightthickness=0, command=next_card)
wrong_button.grid(column=1, row=1)

next_card()
window.protocol("WM_DELETE_WINDOW", on_closing)
window.mainloop()
