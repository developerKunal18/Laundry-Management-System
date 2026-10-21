from datetime import date
from config import ORDERS_FILE, PAYMENTS_FILE
from storage import read_data
from payment_manager import get_paid_amount, get_balance
from utils import money


def daily_report():
    today = date.today().isoformat()

    orders = read_data(ORDERS_FILE)
    payments = read_data(PAYMENTS_FILE)

    todays_orders = [
        order for order in orders
        if order["order_date"] == today
    ]

    todays_payments = [
        payment for payment in payments
        if payment["payment_date"] == today
    ]

    total_billed = sum(
        order["total_amount"] for order in todays_orders
    )
    total_received = sum(
        payment["amount"] for payment in todays_payments
    )

    print(f"\n--- Daily Report: {today} ---")
    print(f"Orders created : {len(todays_orders)}")
    print(f"Amount billed  : {money(total_billed)}")
    print(f"Payments today : {money(total_received)}")

    if todays_orders:
        print("\nToday's orders:")

        for order in todays_orders:
            print(
                f"Order #{order['id']} | "
                f"{order['customer_name']} | "
                f"{order['service']} | "
                f"{money(order['total_amount'])} | "
                f"{order['status']}"
            )


def monthly_report():
    month = date.today().strftime("%Y-%m")

    orders = read_data(ORDERS_FILE)
    payments = read_data(PAYMENTS_FILE)

    monthly_orders = [
        order for order in orders
        if order["order_date"].startswith(month)
    ]

    monthly_payments = [
        payment for payment in payments
        if payment["payment_date"].startswith(month)
    ]

    total_billed = sum(
        order["total_amount"] for order in monthly_orders
    )
    total_received = sum(
        payment["amount"] for payment in monthly_payments
    )

    print(f"\n--- Monthly Report: {month} ---")
    print(f"Orders created  : {len(monthly_orders)}")
    print(f"Amount billed   : {money(total_billed)}")
    print(f"Payments received: {money(total_received)}")

    if monthly_orders:
        print("\nOrders this month:")

        for order in monthly_orders:
            print(
                f"Order #{order['id']} | "
                f"{order['customer_name']} | "
                f"{order['order_date']} | "
                f"{money(order['total_amount'])}"
            )


def overall_report():
    orders = read_data(ORDERS_FILE)
    payments = read_data(PAYMENTS_FILE)

    total_billed = sum(order["total_amount"] for order in orders)
    total_received = sum(payment["amount"] for payment in payments)
    total_outstanding = sum(get_balance(order) for order in orders)

    print("\n--- Overall Business Report ---")
    print(f"Total customers' orders : {len(orders)}")
    print(f"Total amount billed     : {money(total_billed)}")
    print(f"Total payments received : {money(total_received)}")
    print(f"Total outstanding       : {money(total_outstanding)}")

    print("\nOrders by status:")

    statuses = ["Received", "Washing", "Ready", "Delivered"]

    for status in statuses:
        count = sum(1 for order in orders if order["status"] == status)
        print(f"{status}: {count}")

    print("\nServices sold:")

    service_totals = {}

    for order in orders:
        service = order["service"]
        service_totals[service] = service_totals.get(service, 0) + 1

    if not service_totals:
        print("No services sold yet.")
    else:
        for service, count in sorted(service_totals.items()):
            print(f"{service}: {count} order(s)")
