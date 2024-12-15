# A program where the computer randomly selects a number within a range, and the user tries to guess it.
# Features to add:
# Count the number of guesses.
# Provide hints (e.g., "Too high" or "Too low").
# Set a maximum number of attempts.

import random
import sys

answer = random.randint(1,10)
guess = 0
counter = 3

print("##### Welcome to the number guessing game!  #####")
print("##### You have 3 tries to guess the number. #####\n")

while guess != answer and counter > 0:
    try:
        guess = int(input("Enter a number between 1 and 10. You have %i guesses: " % (counter)))
    except ValueError:
        print("Enter a valid integer...")
        counter += 1
    except KeyboardInterrupt:
        print("\n\nAwwww, leaving so soon!")
        sys.exit(0)

    counter -= 1

    if guess == answer:
        print("You got it!")
    elif guess > answer:
        print("Too high.")
    elif guess < answer:
        print("Too low.")

if guess != answer:
    print("\nGame Over! Out of guesses!")
else:
    print("\nYou guessed my number in %i tries. You win!!!" % (3 - counter))