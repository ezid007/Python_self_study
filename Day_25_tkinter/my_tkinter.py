import tkinter

def button_clicked():
    print("I got clicked")

window = tkinter.Tk()
window.title("My first GUI program")
window.minsize(width=500, height=300)

my_label = tkinter.Label(text="I an a Label", font=("Arial", 24, "bold"))
my_label['text'] = "New text"

button = tkinter.Button(text="Click Me", command=button_clicked)
button.pack()



window.mainloop()