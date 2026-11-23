
import random
import time

from Utils import Screen_cleaner


def generate_sequence(difficulty):
    """
    Generate exactly difficulty random numbers.

    Each number is between 1 and 101, inclusive.
    Repeated numbers are allowed.
    """
    sequence = []

    for _ in range(difficulty):
        sequence.append(random.randint(1, 101))

    return sequence


def get_list_from_user(difficulty):
    """
    Collect exactly difficulty whole numbers.

    The player enters numbers separated by spaces.
    """
    while True:
        raw = input(
            f"Enter {difficulty} numbers separated by spaces: "
        ).strip()

        parts = raw.split()

        if len(parts) != difficulty:
            print(
                f"Please enter exactly {difficulty} numbers."
            )
            continue

        try:
            answer = [int(part) for part in parts]

        except ValueError:
            print(
                "Invalid input. Please enter whole numbers "
                "separated by spaces."
            )
            continue

        return answer


def is_list_equal(list_a, list_b):
    """Return True only if both lists match in order."""
    return list_a == list_b


def play(difficulty):
    """Play one Memory Game round."""
    sequence = generate_sequence(difficulty)

    print("\nMemorize this sequence:")
    print(sequence, flush=True)

    time.sleep(0.7)

    Screen_cleaner()

    answer = get_list_from_user(difficulty)

    return is_list_equal(sequence, answer)
