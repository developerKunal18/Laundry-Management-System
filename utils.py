from datetime import date, datetime
from config import CURRENCY


def money(amount):
    """Format an amount as Indian rupees."""
    return f"{CURRENCY}{float(amount):,.2f}"


def input_non_empty(prompt):
    """Request a non-empty string."""
    while True:
        value = input(prompt).strip()

        if value:
            return value

        print("This field cannot be empty.")


def input_phone(prompt="Enter phone number: "):
    """Validate a phone number containing 10 to 15 digits."""
    while True:
        phone = input(prompt).strip()
        digits = "".join(character for character in phone if character.isdigit())

        if 10 <= len(digits) <= 15:
            return phone

        print("Enter a valid phone number containing 10 to 15 digits.")


def input_positive_number(prompt):
    """Accept a positive decimal number."""
    while True:
        try:
            value = float(input(prompt).strip())

            if value <= 0:
                print("Enter a number greater than zero.")
                continue

            if value != value or value in (float("inf"), float("-inf")):
                print("Enter a valid finite number.")
                continue

            return round(value, 2)

        except ValueError:
            print("Enter a valid number, for example 2 or 2.5.")


def input_money(prompt):
    """Accept a positive monetary amount."""
    while True:
        amount = input_positive_number(prompt)

        if round(amount, 2) == amount:
            return amount


def input_integer(prompt, minimum=1):
    """Accept an integer at least equal to minimum."""
    while True:
        try:
            value = int(input(prompt).strip())

            if value < minimum:
                print(f"Enter a number greater than or equal to {minimum}.")
                continue

            return value

        except ValueError:
            print("Enter a valid whole number.")


def today_string():
    return date.today().isoformat()


def current_datetime_string():
    return datetime.now().isoformat(timespec="seconds")


def parse_date(value):
    """Convert an ISO date string to a date object."""
    return date.fromisoformat(value)


def pause():
    input("\nPress Enter to continue...")
