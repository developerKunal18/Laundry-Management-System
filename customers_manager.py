from config import CUSTOMERS_FILE
from storage import read_data, write_data, get_next_id
from utils import input_non_empty, input_phone, current_datetime_string


def list_customers():
    return read_data(CUSTOMERS_FILE)


def find_customer(customer_id):
    customers = list_customers()

    for customer in customers:
        if customer["id"] == customer_id:
            return customer

    return None


def add_customer():
    customers = list_customers()

    print("\n--- Register Customer ---")
    name = input_non_empty("Customer name: ")
    phone = input_phone()

    if any(customer["phone"] == phone for customer in customers):
        print("A customer with this phone number already exists.")
        return

    email = input("Email address (optional): ").strip()
    address = input("Address (optional): ").strip()

    customer = {
        "id": get_next_id(customers, "id"),
        "name": name,
        "phone": phone,
        "email": email,
        "address": address,
        "created_at": current_datetime_string(),
    }

    customers.append(customer)
    write_data(CUSTOMERS_FILE, customers)

    print(f"\nCustomer registered successfully. Customer ID: {customer['id']}")


def display_customer(customer):
    print("-" * 45)
    print(f"Customer ID : {customer['id']}")
    print(f"Name        : {customer['name']}")
    print(f"Phone       : {customer['phone']}")
    print(f"Email       : {customer.get('email') or '-'}")
    print(f"Address     : {customer.get('address') or '-'}")


def show_customers():
    customers = list_customers()

    print("\n--- Customer List ---")

    if not customers:
        print("No customers registered yet.")
        return

    for customer in customers:
        display_customer(customer)


def search_customers():
    search_term = input_non_empty(
        "\nEnter customer name, phone number, or ID: "
    ).lower()

    customers = list_customers()
    matches = []

    for customer in customers:
        if (
            search_term in str(customer["id"]).lower()
            or search_term in customer["name"].lower()
            or search_term in customer["phone"].lower()
        ):
            matches.append(customer)

    if not matches:
        print("No matching customers found.")
        return

    print(f"\nFound {len(matches)} customer(s):")

    for customer in matches:
        display_customer(customer)
