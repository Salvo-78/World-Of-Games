import os

if os.name == "nt":
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    SCORES_FILE_NAME = os.path.join(BASE_DIR, "Scores.txt")
else:
    SCORES_FILE_NAME = "/Scores.txt"

BAD_RETURN_CODE = -1

def Screen_cleaner():
    command = "cls" if os.name == "nt" else "clear"
    result = os.system(command)
    if result != 0:
        print("\033[2J\033[H", end="", flush=True)