
import random
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP

import requests


API_URL = "https://open.er-api.com/v6/latest/USD"
REQUEST_TIMEOUT_SECONDS = 5
CENT = Decimal("0.01")

# True means the round was cancelled because a technical
# problem prevented it from being completed.
round_cancelled = False


def generate_usd_amount():
    """Generate a random USD amount between 1 and 100."""
    return random.randint(1, 100)


def get_exchange_rate():
    """
    Retrieve the current USD-to-ILS exchange rate.

    Raises an exception if the API is unavailable or invalid.
    """
    response = requests.get(
        API_URL,
        timeout=REQUEST_TIMEOUT_SECONDS
    )

    response.raise_for_status()

    data = response.json()

    if not isinstance(data, dict):
        raise ValueError("Invalid API response.")

    if data.get("result") != "success":
        raise ValueError("The currency API returned an error.")

    rates = data.get("rates")

    if not isinstance(rates, dict):
        raise ValueError("The API response does not contain rates.")

    if "ILS" not in rates:
        raise ValueError("The API response does not contain ILS.")

    try:
        rate = Decimal(str(rates["ILS"]))

    except (InvalidOperation, TypeError, ValueError) as error:
        raise ValueError("The ILS exchange rate is invalid.") from error

    if not rate.is_finite() or rate <= 0:
        raise ValueError("The ILS exchange rate is unusable.")

    return rate


def get_money_interval(difficulty, total):
    """
    Calculate the inclusive accepted interval.

    total is the correct ILS value, rounded to two decimals.
    """
    correct_value = Decimal(str(total)).quantize(
        CENT,
        rounding=ROUND_HALF_UP
    )

    tolerance = Decimal(5 - difficulty)

    lower = correct_value - tolerance
    upper = correct_value + tolerance

    return lower, upper


def get_guess_from_user(amount):
    """Collect a valid non-negative decimal ILS guess."""
    while True:
        raw = input(
            f"What is the ILS value of {amount} USD? "
        ).strip()

        try:
            guess = Decimal(raw)

        except (InvalidOperation, ValueError):
            print(
                "Invalid input. Enter a non-negative amount, "
                "for example 36.50."
            )
            continue

        if not guess.is_finite() or guess < 0:
            print("Please enter a non-negative amount.")
            continue

        return guess.quantize(
            CENT,
            rounding=ROUND_HALF_UP
        )


def play(difficulty):
    """
    Play one Currency Roulette round.

    Returns:
        True  - player wins
        False - player loses or the round is cancelled

    Check round_cancelled to distinguish technical cancellation
    from an ordinary loss.
    """
    global round_cancelled

    round_cancelled = False

    amount = generate_usd_amount()

    try:
        rate = get_exchange_rate()

    except (
        requests.RequestException,
        ValueError,
        TypeError,
        InvalidOperation
    ) as error:

        print(
            f"Currency Roulette could not retrieve "
            f"the exchange rate: {error}"
        )

        print("The round has been cancelled.")

        round_cancelled = True
        return False

    # Use the same exchange rate for the complete round.
    correct_value = (
        Decimal(amount) * rate
    ).quantize(
        CENT,
        rounding=ROUND_HALF_UP
    )

    lower, upper = get_money_interval(
        difficulty,
        correct_value
    )

    try:
        guess = get_guess_from_user(amount)

    except (EOFError, KeyboardInterrupt):
        print("\nThe round has been cancelled.")

        round_cancelled = True
        return False

    return lower <= guess <= upper
