import GuessGame
import MemoryGame
import CurrencyRouletteGame


def welcome(name):
    return (
        f"Hello {name} and welcome to the World of Games (WoG).\n"
        "Here you can find many cool games to play."
    )


def get_integer_input(prompt, minimum, maximum):
    while True:
        value = input(prompt).strip()

        try:
            number = int(value)
        except ValueError:
            print(
                f"Invalid input. Please enter a whole number "
                f"from {minimum} to {maximum}."
            )
            continue

        if not minimum <= number <= maximum:
            print(
                f"Out of range. Choose a number from "
                f"{minimum} to {maximum}."
            )
            continue

        return number


def load_game():
    games = {
        1: (
            "Memory Game",
            "Remember the displayed sequence of numbers.",
            MemoryGame.play,
        ),
        2: (
            "Guess Game",
            "Guess the computer's secret number.",
            GuessGame.play,
        ),
        3: (
            "Currency Roulette",
            "Estimate the ILS value of a USD amount.",
            CurrencyRouletteGame.play,
        ),
    }

    print("\nPlease choose a game to play:")
    for number, (name, description, _) in games.items():
        print(f"{number}. {name} - {description}")

    choice = get_integer_input("Game choice (1-3): ", 1, 3)
    difficulty = get_integer_input(
        "Please choose game difficulty from 1 to 5: ", 1, 5
    )

    try:
        won = games[choice][2](difficulty)
    except (KeyboardInterrupt, EOFError):
        print("\nGame cancelled.")
        return

    if won is True:
        print("Congratulations! You won!")
    elif won is False:
        print("Game over. You lost!")
    else:
        print("Round cancelled. No win or loss was recorded.")
