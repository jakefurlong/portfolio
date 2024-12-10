import tkinter as tk
from tkinter import StringVar, IntVar
import random

# Initialize the main window
win = tk.Tk()
win.geometry("750x750")
win.title("JF Apps - Number Guessing Game")

# Variables
hint = StringVar()
score = IntVar()
final_score= IntVar()
guess= IntVar()
max_num = 10
num=random.randint(1,max_num)

# Initialize game state
hint.set(f"Guess a number between 1 and {max_num}")
score.set(3)
final_score.set(score.get())

# Function to check the guess
def check_guess():
    x = guess.get()
    if score.get()>0:

        if x <1 or x > max_num:
            hint.set(f"Out of range. Choose a number between 1 and {max_num}.")
            score.set(score.get()-1)
            final_score.set(score.get())
        elif num == x:
            hint.set("Congratulations, YOU WON!!!")
        elif num > x:
            hint.set("Your guess was too low. Try a higher number.")
            score.set(score.get() - 1)
        elif num < x:
            hint.set("Your guess was too high. Try a lower number.")
            score.set(score.get() - 1)
    else:
        hint.set("Game Over. You Lost.")

    final_score.set(score.get())

# Function to reset the game
def reset_game():
    global num
    num = random.randint(1, max_num)
    score.set(3)
    final_score.set(score.get())
    hint.set(f"Guess a number between 1 to {max_num}")
    guess.set(0)

# UII Components
tk.Label(win, text='The Number Guessing Game',font=("Courier", 25)).place(relx=0.5, rely=0.09, anchor=tk.CENTER)
tk.Entry(win, textvariable=guess, width=3,font=('Ubuntu', 50), relief=tk.GROOVE, justify=tk.CENTER).place(relx=0.5, rely=0.3, anchor=tk.CENTER)
tk.Button(win, width=8, text='CHECK', font=('Courier', 25), command=check_guess, relief=tk.GROOVE,bg='light blue').place(relx=0.5, rely=0.5, anchor=tk.CENTER)
tk.Label(win, textvariable=hint, width=50,font=('Courier', 15), relief=tk.GROOVE,bg='orange').place(relx=0.5, rely=0.7, anchor=tk.CENTER)
tk.Entry(win, text=final_score, width=2,font=('Ubuntu', 24), relief=tk.GROOVE, justify=tk.CENTER).place(relx=0.61, rely=0.85, anchor=tk.CENTER)
tk.Label(win, text='Score out of 3',font=("Courier", 25)).place(relx=0.3, rely=0.85, anchor=tk.CENTER)
tk.Button(win, width=8, text='RESET', font=('Courier', 25), command=reset_game, relief=tk.GROOVE, bg='light green').place(relx=0.5, rely=0.6, anchor=tk.CENTER)

# Start the main event loop
win.mainloop()