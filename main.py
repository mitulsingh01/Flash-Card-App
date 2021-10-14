from tkinter import *
import pandas
import random

BACKGROUND_COLOR = "#B1DDC6"
currCard = {}
try:
    data = pandas.read_csv("wordToCheck.csv")
except FileNotFoundError:
    originaldata = pandas.read_csv("french_words.csv")
    toLearn = originaldata.to_dict(orient="records")
else:
    toLearn = data.to_dict(orient="records")

def nextCard():
    global currCard, flip
    window.after_cancel(flip)
    currCard = random.choice(toLearn)
    canvas.itemconfig(cardTitle, text="French", fill="black")
    canvas.itemconfig(cardWord, text=currCard["French"], fill="black")
    canvas.itemconfig(cardBackground, image=cardFront)
    flip = window.after(3000, func=flipCard)

def flipCard():
    canvas.itemconfig(cardTitle, text="English", fill="white")
    canvas.itemconfig(cardWord, text=currCard["English"], fill="white")
    canvas.itemconfig(cardBackground, image=cardBack)

def is_known():
    toLearn.remove(currCard)
    data = pandas.DataFrame(toLearn)
    data.to_csv("wordToCheck.csv", index=False)
    nextCard()

window = Tk()
window.title("Flash Cards")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)
flip = window.after(3000, func=flipCard)

canvas = Canvas(width=800, height=526)
cardFront =PhotoImage(file="card_front.png")
cardBack = PhotoImage(file="card_back.png")
cardBackground = canvas.create_image(400, 263, image=cardFront)
canvas.config(bg=BACKGROUND_COLOR, highlightthickness=0)
cardTitle = canvas.create_text(400, 150, text="Title", font=("Ariel", 50, "italic"))
cardWord = canvas.create_text(400, 263, text="Word", font=("Ariel", 75, "bold"))
canvas.grid(row=0, column=0, columnspan=2)

wrong = PhotoImage(file="wrong.png")
right = PhotoImage(file="right.png")

wrongButton = Button(image=wrong, highlightthickness=0, command=nextCard)
wrongButton.grid(row=1, column=0)

rightButton = Button(image=right, highlightthickness=0, command=is_known)
rightButton.grid(row=1, column=1)

nextCard()

window.mainloop()