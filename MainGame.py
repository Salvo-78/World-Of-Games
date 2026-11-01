
from Live import welcome, load_game


def main():
    name = input("Please enter your name: ").strip()

    if not name:
        name = "Player"

    print(welcome(name))
    load_game()


if __name__ == "__main__":
    main()
