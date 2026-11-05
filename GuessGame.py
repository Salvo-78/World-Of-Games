import random
# from live import difficulty imports the difficulty variable from live.py

def get_guess_from_user(difficulty):
# prompts the user for a guess between 1 and difficulty (inclusive), repeats the prompt with 'wrong selection' if the input is invalid.
    
    while True:
        try:
            guess_input = input(f"Enter your guess (1-{difficulty}): ").strip()
            if not guess_input:
                print("wrong selection")
                continue

            guess = int(guess_input)
            if guess < 1 or guess > difficulty:
                print("wrong selection")
                continue
            return guess
        except ValueError:
            print("wrong selection")


def compare_results(guess, secret_number):
# compares the user's guess with the secret number. returns True if they match, False otherwise.

    return guess == secret_number


def play(difficulty):
# generates a secret number, gets one valid guess, compares them, and returns True (win) or False (loss).
    
    secret_number = random.randint(1, difficulty)

    # collect exactly one valid guess (invalid attempts do not count)
    guess = get_guess_from_user(difficulty)

    # compare and return the result
    return compare_results(guess, secret_number)
