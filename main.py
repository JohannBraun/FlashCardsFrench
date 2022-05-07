from tkinter import *
import pandas
import random
from tkinter import messagebox

BACKGROUND_COLOR = "#B1DDC6"
COUNTDOWN = 3
random_entry = []


# ------------------- NEW ENTRY -------------------
def new_word(is_correct):
    global random_entry
    global data_list

    if is_correct:
        data_list.remove(random_entry)
        updated_df = pandas.DataFrame(data_list)
        updated_df.to_csv("./data/words_to_learn.csv", index=False)
    window.after_cancel(timer)

    try:
        random_entry = random.choice(data_list)
    except IndexError:
        messagebox.showinfo(title="No more words", message="There are no more unknown words. Starting from beginning!")
        new_data = pandas.read_csv("./data/french_words.csv")
        new_data.to_csv("./data/words_to_learn.csv", index=False)
        data_list = new_data.to_dict(orient="records")

    first_language = list(random_entry.keys())[0]
    canvas.itemconfig(canvas_image, image=canvas_card_front_img)
    canvas.itemconfig(canvas_language_text, text=first_language, fill="black")
    canvas.itemconfig(canvas_word_text, text=random_entry[first_language], fill="black")
    count_down(COUNTDOWN, random_entry)


# ------------------- COUNT DOWN --------------------
def count_down(count, random_entry):
    if count > 0:
        global timer
        timer = window.after(1000, count_down, count - 1, random_entry)
    elif count == 0:
        flip_card(random_entry)


# ------------------- FLIP CARD -------------------
def flip_card(random_entry):
    second_language = list(random_entry.keys())[1]
    print(second_language)
    print(random_entry[second_language])
    canvas.itemconfig(canvas_image, image=canvas_card_back_img)
    canvas.itemconfig(canvas_language_text, text=second_language, fill="white")
    canvas.itemconfig(canvas_word_text, text=random_entry[second_language], fill="white")


# ------------------- DATA -------------------
try:
    data = pandas.read_csv("./data/words_to_learn.csv")
except (FileNotFoundError, pandas.errors.EmptyDataError):
    data = pandas.read_csv("./data/french_words.csv")
    data.to_csv("./data/words_to_learn.csv", index=False)

data_list = data.to_dict(orient="records")

# ------------------- UI -------------------
window = Tk()
window.title("Flashy")
window.config(bg=BACKGROUND_COLOR, padx=50, pady=50)

canvas = Canvas(width=800, height=526, bg=BACKGROUND_COLOR, highlightthickness=0)
canvas_card_front_img = PhotoImage(file="./images/card_front.png")
canvas_card_back_img = PhotoImage(file="./images/card_back.png")
canvas_image = canvas.create_image(400, 268)
canvas_language_text = canvas.create_text(400, 150, font=("Ariel", 40, "italic"))
canvas_word_text = canvas.create_text(400, 263, font=("Ariel", 60, "bold"))

canvas.grid(row=0, column=0, columnspan=2)

wrong_image = PhotoImage(file="./images/wrong.png")
wrong_button = Button(image=wrong_image, highlightthickness=0, bg=BACKGROUND_COLOR, command=lambda: new_word(False))
wrong_button.grid(row=1, column=0)

right_image = PhotoImage(file="./images/right.png")
right_button = Button(image=right_image, highlightthickness=0, command=lambda: new_word(True))
right_button.grid(row=1, column=1)

timer = window.after(0, new_word, False)

window.mainloop()
