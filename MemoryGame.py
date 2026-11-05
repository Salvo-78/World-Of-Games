import random
import time
import os
import sys


def generate_sequence(difficulty):
    return [
        random.randint(1, 101)
        for _ in range(difficulty)
    ]


def clear_screen():
   
    if os.name == "nt":
        os.system("cls")
    else:
        sys.stdout.write("\033[2J\033[H")
        sys.stdout.flush()


def get_list_from_user(difficulty):
    while True:
        value = input(
            f"Enter {difficulty} numbers separated by spaces: "
        ).strip()

        parts = value.split()

        if len(parts) != difficulty:
            print(f"Please enter exactly {difficulty} numbers.")
            continue

        try:
            numbers = [int(part) for part in parts]
        except ValueError:
            print("Invalid input. All entries must be whole numbers.")
            continue

        return numbers


def is_list_equal(list1, list2):
    return list1 == list2


def play(difficulty):
    sequence = generate_sequence(difficulty)

    print("Memorize this sequence:")
    print(sequence, flush=True)

    time.sleep(0.7)
    clear_screen()

    answer = get_list_from_user(difficulty)
    return is_list_equal(sequence, answer)
