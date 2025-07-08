import tkinter as tk
import pandas as ps
import random

BACKGROUND_COLOR = "#B1DDC6"

data = ps.read_csv("self_study\\Day_31_flash_card\\data\\eng_words.csv")
to_learn = data.to_dict(orient="records")


def next_card():
    current_card = random.choice(to_learn)
    canvas.itemconfig(card_title, text="English")
    canvas.itemconfig(card_word, text=current_card["English"])


window = tk.Tk()
window.title("Flashy")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

canvas = tk.Canvas(width=800, height=526)
card_front_img = tk.PhotoImage(
    file="self_study\\Day_31_flash_card\\images\\card_front.png"
)
canvas.create_image(400, 263, image=card_front_img)
canvas.config(bg=BACKGROUND_COLOR, highlightthickness=0)
card_title = canvas.create_text(400, 150, text="Title", font=("Ariel", 40, "italic"))
card_word = canvas.create_text(400, 263, text="word", font=("Ariel", 60, "bold"))
canvas.grid(row=0, column=0, columnspan=2)

right_img = tk.PhotoImage(file="self_study\\Day_31_flash_card\\images\\right.png")
right_button = tk.Button(image=right_img, highlightthickness=0, command=next_card)
right_button.grid(column=0, row=1)

wrong_img = tk.PhotoImage(file="self_study\\Day_31_flash_card\\images\\wrong.png")
wrong_button = tk.Button(image=wrong_img, highlightthickness=0, command=next_card)
wrong_button.grid(column=1, row=1)


window.mainloop()
