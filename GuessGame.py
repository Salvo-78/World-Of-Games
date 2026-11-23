
import random


def generate_number(difficulty):
    """Generate a secret number between 1 and difficulty."""
    secret_number = random.randint(1, difficulty)
    return secret_number


def get_guess_from_user(difficulty):
    """Ask for a valid whole-number guess."""
    while True:
        raw = input(
            f"Guess a whole number from 1 to {difficulty}: "
        ).strip()

        try:
            guess = int(raw)
        except ValueError:
            print("Invalid input. Please enter a whole number.")
            continue

        if 1 <= guess <= difficulty:
            return guess

        print(
            f"Your guess must be between 1 and {difficulty}."
        )


def compare_results(guess, secret_number):
    """Return True if the guess matches the secret number."""
    return guess == secret_number


def play(difficulty):
    """Play one round and return True for a win, False for a loss."""
    secret_number = generate_number(difficulty)

    guess = get_guess_from_user(difficulty)

    return compare_results(guess, secret_number)
