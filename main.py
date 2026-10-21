from storage import initialize_storage
from customer_manager import (
    add_customer,
    show_customers,
    search_customers,
)
from order_manager import (
    create_order,
    show_orders,
    search_order,
    update_order_status,
)
from payment_manager import (
    record_payment,
    show_payment_history,
    show_order_balance,
)
from report_manager import (
    daily_report,
    monthly_report,
    overall_report,
)
from utils import pause


def display_menu():
    print("\n" + "=" * 48)
    print("       LAUNDRY MANAGEMENT SYSTEM")
    print("=" * 48)
    print("1.  Register Customer")
    print("2.  View All Customers")
    print("3.  Search Customers")
    print("4.  Create Laundry Order")
    print("5.  View All Orders")
    print("6.  Search Order")
    print("7.  Update Order Status")
    print("8.  Record Payment")
    print("9.  View Payment History")
    print("10. View Outstanding Balances")
    print("11. Daily Report")
    print("12. Monthly Report")
    print("13. Overall Business Report")
    print("0.  Exit")
    print("=" * 48)


def main():
    initialize_storage()

    actions = {
        "1": add_customer,
        "2": show_customers,
        "3": search_customers,
        "4": create_order,
        "5": show_orders,
        "6": search_order,
        "7": update_order_status,
        "8": record_payment,
        "9": show_payment_history,
        "10": show_order_balance,
        "11": daily_report,
        "12": monthly_report,
        "13": overall_report,
    }

    print("Welcome to the Laundry Management System!")

    while True:
        display_menu()
        choice = input("Enter your choice: ").strip()

        if choice == "0":
            print("\nThank you for using the Laundry Management System.")
            break

        action = actions.get(choice)

        if action is None:
            print("Invalid choice. Please select a menu option.")
            pause()
            continue

        try:
            action()
        except (ValueError, OSError, KeyError) as error:
            print(f"\nUnable to complete this operation: {error}")
            print("Check the data files and try again.")

        pause()


if __name__ == "__main__":
    main()
