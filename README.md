# Laundry Management System

A beginner-friendly Python project for managing a laundry shop.
It uses JSON files to store customers, laundry orders, and payments.

## Features

- Register new customers
- View and search customer records
- Create laundry orders
- Calculate charges automatically
- Support washing, ironing, dry cleaning, folding, and wash-and-iron services
- Track order progress
- Record partial and full payments
- View payment history
- Track outstanding balances
- Generate daily, monthly, and overall business reports
- Save data locally using JSON files

## Technologies Used

- Python
- JSON
- Python standard library

## Project Structure

```text
LaundryManagementSystem/
├── main.py
├── config.py
├── storage.py
├── utils.py
├── customer_manager.py
├── order_manager.py
├── payment_manager.py
├── report_manager.py
├── requirements.txt
├── .gitignore
└── data/
    ├── customers.json
    ├── orders.json
    └── payments.json
