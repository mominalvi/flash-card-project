from tkinter import *
import pandas
import random

BACKGROUND_COLOR = "#B1DDC6"
random_choice = {}
sorted_df = []

import pandas.errors

try:
    df = pandas.read_csv("words_to_learn.csv")
    if df.empty:
        df = pandas.read_csv("data/french_words.csv")
except (FileNotFoundError, pandas.errors.EmptyDataError):
    df = pandas.read_csv("data/french_words.csv")

sorted_df = df.to_dict(orient="records")

def next_card():
    global random_choice, flip_timer, sorted_df
    window.after_cancel(flip_timer)

    # Use the in-memory list for the random choice
    random_choice = random.choice(sorted_df)

    canvas.itemconfig(card_title, text="French", fill="black")
    canvas.itemconfig(card_word, text=random_choice['French'], fill="black")
    canvas.itemconfig(front, image=front_img)
    flip_timer = window.after(3000, func=flip_card)

def right_button():
    global sorted_df
    if random_choice in sorted_df:
        sorted_df.remove(random_choice)
    # Write the updated list back to the CSV
    if sorted_df:
        df = pandas.DataFrame(sorted_df)
        df.to_csv("words_to_learn.csv", index=False)


def flip_card():
    canvas.itemconfig(card_title, text="English", fill="white")
    canvas.itemconfig(card_word, text=random_choice["English"], fill="white")
    canvas.itemconfig(front, image=back_img)

# create the window
window = Tk()
window.title("Flashcards")
window.config(padx=50, pady=50, background=BACKGROUND_COLOR)
flip_timer = window.after(3000, func=flip_card)

# create the big white background and text boxes
canvas = Canvas(height=526, width=800, background=BACKGROUND_COLOR, highlightthickness=0)
front_img = PhotoImage(file="images/card_front.png")
back_img = PhotoImage(file="images/card_back.png")
front = canvas.create_image(400, 263, image=front_img)
canvas.grid(column=0, row=0, columnspan=2)
card_title = canvas.create_text(400, 150, font=("Ariel", 40, "italic"))
card_word = canvas.create_text(400, 263, font=("Ariel", 60, "bold"))

# creating the buttons
my_image = PhotoImage(file="images/right.png")
right = Button(image=my_image, highlightthickness=0, command=lambda:[next_card(),right_button()])
right.grid(column=1, row=1)
my_image2 = PhotoImage(file="images/wrong.png")
wrong = Button(image=my_image2, highlightthickness=0, command=next_card)
wrong.grid(column=0, row=1)

next_card()


window.mainloop()