import random
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP

import requests


API_URL = "https://open.er-api.com/v6/latest/USD"
CENT = Decimal("0.01")


def get_exchange_rate():
    try:
        response = requests.get(API_URL, timeout=5)
        response.raise_for_status()
        data = response.json()

        if data.get("result") != "success":
            raise ValueError("The currency API returned an unsuccessful result.")

        rates = data.get("rates")
        if not isinstance(rates, dict) or "ILS" not in rates:
            raise ValueError("The API response does not contain the ILS rate.")

        rate = Decimal(str(rates["ILS"]))

        if not rate.is_finite() or rate <= 0:
            raise ValueError("The ILS exchange rate is invalid.")

        return rate

    except (
        requests.RequestException,
        ValueError,
        InvalidOperation,
        TypeError,
        KeyError,
    ) as error:
        print(f"Currency service error: {error}")
        return None


def get_money_interval(difficulty, usd_amount, exchange_rate):
    correct_value = (
        Decimal(usd_amount) * exchange_rate
    ).quantize(CENT, rounding=ROUND_HALF_UP)

    tolerance = Decimal(5 - difficulty)

    lower = correct_value - tolerance
    upper = correct_value + tolerance

    return lower, upper


def get_guess_from_user(usd_amount):
    while True:
        value = input(
            f"Estimate the ILS value of {usd_amount} USD: "
        ).strip()

        try:
            guess = Decimal(value)
        except InvalidOperation:
            print("Invalid input. Enter a non-negative decimal number.")
            continue

        if not guess.is_finite() or guess < 0:
            print("Your estimate must be a finite, non-negative number.")
            continue

        return guess


def play(difficulty):
    usd_amount = random.randint(1, 100)

    exchange_rate = get_exchange_rate()
    if exchange_rate is None:
        return None

    lower, upper = get_money_interval(
        difficulty, usd_amount, exchange_rate
    )

    guess = get_guess_from_user(usd_amount)

    return lower <= guess <= upper
