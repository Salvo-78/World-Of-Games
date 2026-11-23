
import os
import tempfile

from Utils import SCORES_FILE_NAME, BAD_RETURN_CODE


def _read_score():
    """Read the score from the shared score file."""

    if not os.path.exists(SCORES_FILE_NAME):
        return 0

    try:
        with open(SCORES_FILE_NAME, "r", encoding="utf-8") as file:
            content = file.read().strip()

        if not content:
            print("Score error: score file is empty.")
            return BAD_RETURN_CODE

        score = int(content)

        if score < 0:
            print("Score error: score cannot be negative.")
            return BAD_RETURN_CODE

        return score

    except (ValueError, OSError):
        print("Score error: unable to read a valid score.")
        return BAD_RETURN_CODE


def _write_score(score):
    """Safely write the updated score."""

    directory = os.path.dirname(
        os.path.abspath(SCORES_FILE_NAME)
    )

    temporary_path = None

    try:
        with tempfile.NamedTemporaryFile(
            mode="w",
            encoding="utf-8",
            dir=directory,
            delete=False
        ) as temp_file:

            temporary_path = temp_file.name
            temp_file.write(str(score))
            temp_file.flush()
            os.fsync(temp_file.fileno())

        os.replace(temporary_path, SCORES_FILE_NAME)

        return True

    except OSError:
        print("Score error: unable to save the score.")

        if temporary_path and os.path.exists(temporary_path):
            try:
                os.remove(temporary_path)
            except OSError:
                pass

        return False


def add_score(difficulty):
    """Calculate and save points after a win."""

    points = (difficulty * 3) + 5

    current_score = _read_score()

    if current_score == BAD_RETURN_CODE:
        return BAD_RETURN_CODE

    new_score = current_score + points

    if not _write_score(new_score):
        return BAD_RETURN_CODE

    return new_score
