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
final_score = IntVar()
guess = StringVar()
max_num = 10
num = random.randint(1, max_num)

# Initialize game state
hint.set(f"Guess a number between 1 and {max_num}")
score.set(3)
final_score.set(score.get())

# Function to check the guess
def check_guess():
    if score.get() <= 0:
        hint.set("Game Over. You Lost.")
        disable_check_button()
        return  # Stop further processing if score is 0

    try:
        x = int(guess.get())
        if x < 1 or x > max_num:
            hint.set(f"Out of range. Choose a number between 1 and {max_num}.")
        elif num == x:
            hint.set("Congratulations, YOU WON!!!")
            disable_check_button()
            return
        elif num > x:
            hint.set("Your guess was too low. Try a higher number.")
        elif num < x:
            hint.set("Your guess was too high. Try a lower number.")

        # Decrement the score after each guess
        score.set(score.get() - 1)

        # If score reaches 0 after decrementing
        if score.get() <= 0:
            hint.set("Game Over. You Lost.")
            disable_check_button()
    except ValueError:
        hint.set("Invalid input. Enter a number.")

    final_score.set(score.get())

# Function to disable the CHECK button
def disable_check_button():
    check_btn.config(state=tk.DISABLED)

# Function to reset the game
def reset_game():
    global num
    num = random.randint(1, max_num)
    score.set(3)
    final_score.set(score.get())
    hint.set(f"Guess a number between 1 to {max_num}")
    guess.set("")
    check_btn.config(state=tk.NORMAL)

# UI Components
tk.Label(win, text='The Number Guessing Game', font=("Courier", 25)).place(relx=0.5, rely=0.09, anchor=tk.CENTER)
tk.Entry(win, textvariable=guess, width=3, font=('Ubuntu', 50), relief=tk.GROOVE, justify=tk.CENTER).place(relx=0.5, rely=0.3, anchor=tk.CENTER)
check_btn = tk.Button(win, width=8, text='CHECK', font=('Courier', 25), command=check_guess, relief=tk.GROOVE, bg='light blue')
check_btn.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
tk.Label(win, textvariable=hint, width=50, font=('Courier', 15), relief=tk.GROOVE, bg='orange').place(relx=0.5, rely=0.7, anchor=tk.CENTER)
tk.Label(win, textvariable=final_score, width=2, font=('Ubuntu', 24), relief=tk.GROOVE, justify=tk.CENTER, bg='white').place(relx=0.61, rely=0.85, anchor=tk.CENTER)
tk.Label(win, text='Score out of 3', font=("Courier", 25)).place(relx=0.3, rely=0.85, anchor=tk.CENTER)
tk.Button(win, width=8, text='RESET', font=('Courier', 25), command=reset_game, relief=tk.GROOVE, bg='light green').place(relx=0.5, rely=0.6, anchor=tk.CENTER)

# Start the main event loop
win.mainloop()
