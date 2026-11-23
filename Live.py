
import GuessGame
import MemoryGame
import CurrencyRouletteGame

from Score import add_score
from Utils import BAD_RETURN_CODE


def welcome(name):
    return (
        f"Hello {name} and welcome to the World of Games (WoG).\n"
        "Here you can find many cool games to play."
    )


def _read_integer(prompt, minimum, maximum):
    """
    Read a whole number within an inclusive range.

    Invalid input is rejected and does not start a game.
    """
    while True:
        raw = input(prompt).strip()

        try:
            value = int(raw)
        except ValueError:
            print(
                f"Invalid input. Please enter a whole number "
                f"from {minimum} to {maximum}."
            )
            continue

        if minimum <= value <= maximum:
            return value

        print(
            f"Out of range. Please enter a number "
            f"from {minimum} to {maximum}."
        )


def load_game():
    print("\nPlease choose a game to play:")

    print(
        "1. Memory Game - Memorize a sequence displayed briefly "
        "and recall it in order."
    )

    print(
        "2. Guess Game - Guess the computer's secret number."
    )

    print(
        "3. Currency Roulette - Estimate the ILS value "
        "of a random USD amount."
    )

    game_choice = _read_integer(
        "Game choice (1-3): ",
        1,
        3
    )

    difficulty = _read_integer(
        "Please choose game difficulty from 1 to 5: ",
        1,
        5
    )

    games = {
        1: MemoryGame,
        2: GuessGame,
        3: CurrencyRouletteGame
    }

    selected_game = games[game_choice]

    try:
        result = selected_game.play(difficulty)

    except (EOFError, KeyboardInterrupt):
        print("\nGame cancelled.")
        return

    # A cancelled Currency Roulette round is not a loss
    # and must not be reported as a win.
    if (
        game_choice == 3
        and CurrencyRouletteGame.round_cancelled
    ):
        print("The round was cancelled. No points were awarded.")
        return

    if result is True:
        print("\nCongratulations! You won!")

        score_result = add_score(difficulty)

        if score_result == BAD_RETURN_CODE:
            print(
                "Your win was recorded, but the score "
                "could not be saved."
            )
        else:
            print(f"Your updated score is: {score_result}")

    elif result is False:
        print("\nYou lost. Better luck next time!")

    else:
        print("\nThe game ended without a valid result.")
