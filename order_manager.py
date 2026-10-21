from config import (
    ORDERS_FILE,
    SERVICES,
    STATUS_TRANSITIONS,
)
from storage import read_data, write_data, get_next_id
from customer_manager import list_customers, find_customer
from utils import (
    input_integer,
    input_positive_number,
    money,
    today_string,
    current_datetime_string,
)


def list_orders():
    return read_data(ORDERS_FILE)


def find_order(order_id):
    for order in list_orders():
        if order["id"] == order_id:
            return order

    return None


def create_order():
    customers = list_customers()

    print("\n--- Create Laundry Order ---")

    if not customers:
        print("Register a customer before creating an order.")
        return

    print("\nRegistered customers:")

    for customer in customers:
        print(
            f"ID: {customer['id']} | "
            f"{customer['name']} | {customer['phone']}"
        )

    customer_id = input_integer("\nEnter customer ID: ")
    customer = find_customer(customer_id)

    if not customer:
        print("Customer not found.")
        return

    print("\nAvailable services:")

    service_names = list(SERVICES.keys())

    for index, service_name in enumerate(service_names, start=1):
        details = SERVICES[service_name]
        print(
            f"{index}. {service_name} - "
            f"{money(details['rate'])} per {details['unit']}"
        )

    service_choice = input_integer(
        "\nChoose a service number: "
    )

    if service_choice > len(service_names):
        print("Invalid service number.")
        return

    service_name = service_names[service_choice - 1]
    service_details = SERVICES[service_name]

    quantity = input_positive_number(
        f"Enter quantity in {service_details['unit']}: "
    )

    total_amount = round(quantity * service_details["rate"], 2)
    orders = list_orders()

    order = {
        "id": get_next_id(orders, "id"),
        "customer_id": customer["id"],
        "customer_name": customer["name"],
        "service": service_name,
        "quantity": quantity,
        "unit": service_details["unit"],
        "rate": service_details["rate"],
        "total_amount": total_amount,
        "status": "Received",
        "order_date": today_string(),
        "created_at": current_datetime_string(),
    }

    orders.append(order)
    write_data(ORDERS_FILE, orders)

    print("\nOrder created successfully.")
    print(f"Order ID    : {order['id']}")
    print(f"Customer    : {order['customer_name']}")
    print(f"Service     : {order['service']}")
    print(f"Quantity    : {order['quantity']} {order['unit']}")
    print(f"Rate        : {money(order['rate'])}")
    print(f"Total       : {money(order['total_amount'])}")
    print(f"Status      : {order['status']}")


def display_order(order):
    print("-" * 50)
    print(f"Order ID    : {order['id']}")
    print(f"Customer    : {order['customer_name']}")
    print(f"Customer ID : {order['customer_id']}")
    print(f"Service     : {order['service']}")
    print(f"Quantity    : {order['quantity']} {order['unit']}")
    print(f"Rate        : {money(order['rate'])}")
    print(f"Total       : {money(order['total_amount'])}")
    print(f"Status      : {order['status']}")
    print(f"Order Date  : {order['order_date']}")


def show_orders():
    orders = list_orders()

    print("\n--- All Laundry Orders ---")

    if not orders:
        print("No orders found.")
        return

    for order in sorted(orders, key=lambda item: item["id"]):
        display_order(order)


def search_order():
    order_id = input_integer("Enter order ID: ")
    order = find_order(order_id)

    if not order:
        print("Order not found.")
        return

    display_order(order)


def update_order_status():
    orders = list_orders()

    print("\n--- Update Order Status ---")
    order_id = input_integer("Enter order ID: ")

    order = next(
        (item for item in orders if item["id"] == order_id),
        None,
    )

    if not order:
        print("Order not found.")
        return

    current_status = order["status"]
    allowed_statuses = STATUS_TRANSITIONS.get(current_status, [])

    print(f"Current status: {current_status}")

    if not allowed_statuses:
        print("This order has already been delivered.")
        return

    print("\nAllowed next statuses:")

    for index, status in enumerate(allowed_statuses, start=1):
        print(f"{index}. {status}")

    choice = input_integer("Choose the next status: ")

    if choice > len(allowed_statuses):
        print("Invalid status choice.")
        return

    order["status"] = allowed_statuses[choice - 1]
    order["updated_at"] = current_datetime_string()

    write_data(ORDERS_FILE, orders)

    print(f"Order status updated to: {order['status']}")
