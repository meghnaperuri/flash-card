import pandas as pd
import random
import tkinter as tk
from PIL import Image, ImageTk

BACKGROUND_COLOR = "#B1DDC6"


#------------- DATA FRAME, CSV FUNCTIONALITY-----------------

df=pd.read_csv("data/french_words.csv")
original_list = df.to_dict(orient='records')
to_learn = original_list.copy()

print(original_list)
english_word=""
french_word=""
random_french_word=""
english_list=[]
french_list=[]
score=0

def generate_random():
    global english_word, french_word,random_french_word
    random_row = random.choice(df.index)
    english_word = df.loc[random_row, 'English']
    french_word = df.loc[random_row, 'French']
    random_french_word = random.choice(to_learn)['French']
    # random_row_french = random.choice(df.index)
    # random_french_word=df.loc[random_row_french, 'French']
    print(f"english word: {english_word}, corresponding french word: {french_word},\nrandom french word on card: {random_french_word}")


def switch_flashcard():
    global is_front
    if is_front:
        # Switch to back card (French)
        flash_card_canvas.itemconfig(canvas_image, image=flashcard_back_photo)
        flash_card_canvas.itemconfig(card_title, text="French", fill="Black")
        flash_card_canvas.itemconfig(card_word, text=random_french_word, fill="Black")
    else:
        # Switch to front card (English)
        flash_card_canvas.itemconfig(canvas_image, image=flashcard_front_photo)
        flash_card_canvas.itemconfig(card_title, text="English", fill="Black")
        flash_card_canvas.itemconfig(card_word, text=english_word, fill="Black")
    is_front = not is_front

#---------------BUTTON DEFINITIONS--------------

def right():
    global is_front, score
    print("right button is clicked")
    if random_french_word==french_word:
        score+=1
        to_learn.remove({'English': english_word, 'French': french_word})  # Remove the correct pair
    print(to_learn)
    generate_random()
    is_front = False
    switch_flashcard()
    print(score)

def wrong():
    global score
    print("wrong button is clicked")
    if random_french_word != french_word:
        score += 1
    print(score)
    generate_random()
    switch_flashcard()
    window.after(3000, switch_flashcard)


#---------------LAYOUT----------------
window=tk.Tk()
window.title("flashy")
window.geometry("800x600")
window.config(bg='#B1DDC6')

canvas=tk.Canvas(window, bg=BACKGROUND_COLOR, width=1000, height=700)
#------flashcard front and back--------------

flashcard_front_image = Image.open('images/card_front.png')
resized_front_image = flashcard_front_image.resize((500, 350))
flashcard_front_photo = ImageTk.PhotoImage(resized_front_image)

flashcard_back_image = Image.open('images/card_back.png')
resized_back_image = flashcard_back_image.resize((500, 350))
flashcard_back_photo = ImageTk.PhotoImage(resized_back_image)

# Create canvas for flashcard
flash_card_canvas = tk.Canvas(window, width=500, height=350, bg=BACKGROUND_COLOR, highlightthickness=0)
flash_card_canvas.place(x=100, y=100)

# Initialize canvas with front card
canvas_image = flash_card_canvas.create_image(250, 175, image=flashcard_front_photo)
card_title = flash_card_canvas.create_text(250, 90, text="English", fill="Black", font=('Arial', 12, 'italic'))
card_word = flash_card_canvas.create_text(250, 150, text="word", fill="Black", font=('Arial', 24, 'bold'))

#---------right wrong buttons----------------
image=Image.open('images/right.png')
photo=ImageTk.PhotoImage(image)
button_correct=tk.Button(image=photo, command=right, bg=BACKGROUND_COLOR, borderwidth=0, highlightthickness=0)
button_correct.place(x=150,y=470)

wrong_image=Image.open('images/wrong.png')
wrong_photo=ImageTk.PhotoImage(wrong_image)
button_wrong=tk.Button(image=wrong_photo, command=wrong, bg=BACKGROUND_COLOR, borderwidth=-2, highlightthickness=0)
button_wrong.place(x=450,y=470)

#-----------switch refresh after 3 seconds------------
generate_random()
is_front = False
switch_flashcard()


window.after(3000, switch_flashcard)

window.mainloop()