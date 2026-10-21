from config import PAYMENTS_FILE
from storage import read_data, write_data, get_next_id
from order_manager import list_orders
from utils import (
    input_integer,
    input_positive_number,
    money,
    today_string,
    current_datetime_string,
)


def list_payments():
    return read_data(PAYMENTS_FILE)


def get_order_payments(order_id):
    return [
        payment
        for payment in list_payments()
        if payment["order_id"] == order_id
    ]


def get_paid_amount(order_id):
    payments = get_order_payments(order_id)
    return round(sum(payment["amount"] for payment in payments), 2)


def get_balance(order):
    paid = get_paid_amount(order["id"])
    return round(max(0, order["total_amount"] - paid), 2)


def record_payment():
    orders = list_orders()

    print("\n--- Record Payment ---")

    if not orders:
        print("No orders are available.")
        return

    order_id = input_integer("Enter order ID: ")

    order = next(
        (item for item in orders if item["id"] == order_id),
        None,
    )

    if not order:
        print("Order not found.")
        return

    paid = get_paid_amount(order_id)
    balance = round(order["total_amount"] - paid, 2)

    print(f"Order total : {money(order['total_amount'])}")
    print(f"Already paid: {money(paid)}")
    print(f"Balance     : {money(balance)}")

    if balance <= 0:
        print("This order is already fully paid.")
        return

    amount = input_positive_number("Enter payment amount: ")
    amount = round(amount, 2)

    if amount > balance:
        print(f"Payment cannot exceed the balance of {money(balance)}.")
        return

    payment_methods = ["Cash", "UPI", "Card", "Bank Transfer"]

    print("\nPayment methods:")

    for index, method in enumerate(payment_methods, start=1):
        print(f"{index}. {method}")

    method_choice = input_integer("Choose payment method: ")

    if method_choice > len(payment_methods):
        print("Invalid payment method.")
        return

    payments = list_payments()

    payment = {
        "id": get_next_id(payments, "id"),
        "order_id": order["id"],
        "customer_id": order["customer_id"],
        "customer_name": order["customer_name"],
        "amount": amount,
        "method": payment_methods[method_choice - 1],
        "payment_date": today_string(),
        "created_at": current_datetime_string(),
    }

    payments.append(payment)
    write_data(PAYMENTS_FILE, payments)

    new_balance = round(balance - amount, 2)

    print("\nPayment recorded successfully.")
    print(f"Payment ID : {payment['id']}")
    print(f"Amount     : {money(amount)}")
    print(f"Method     : {payment['method']}")
    print(f"Remaining  : {money(new_balance)}")


def show_payment_history():
    payments = list_payments()

    print("\n--- Payment History ---")

    if not payments:
        print("No payments recorded.")
        return

    for payment in sorted(payments, key=lambda item: item["id"]):
        print("-" * 45)
        print(f"Payment ID : {payment['id']}")
        print(f"Order ID   : {payment['order_id']}")
        print(f"Customer   : {payment['customer_name']}")
        print(f"Amount     : {money(payment['amount'])}")
        print(f"Method     : {payment['method']}")
        print(f"Date       : {payment['payment_date']}")


def show_order_balance():
    orders = list_orders()

    print("\n--- Outstanding Balances ---")

    unpaid_orders = [
        order for order in orders if get_balance(order) > 0
    ]

    if not unpaid_orders:
        print("There are no outstanding balances.")
        return

    for order in unpaid_orders:
        print("-" * 45)
        print(f"Order ID : {order['id']}")
        print(f"Customer : {order['customer_name']}")
        print(f"Total    : {money(order['total_amount'])}")
        print(f"Paid     : {money(get_paid_amount(order['id']))}")
        print(f"Balance  : {money(get_balance(order))}")
