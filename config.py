from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"

CUSTOMERS_FILE = DATA_DIR / "customers.json"
ORDERS_FILE = DATA_DIR / "orders.json"
PAYMENTS_FILE = DATA_DIR / "payments.json"

CURRENCY = "₹"

SERVICES = {
    "Washing": {"rate": 60.0, "unit": "kg"},
    "Ironing": {"rate": 15.0, "unit": "item"},
    "Dry Cleaning": {"rate": 120.0, "unit": "item"},
    "Folding": {"rate": 20.0, "unit": "kg"},
    "Wash and Iron": {"rate": 80.0, "unit": "kg"},
}

ORDER_STATUSES = [
    "Received",
    "Washing",
    "Ready",
    "Delivered",
]

STATUS_TRANSITIONS = {
    "Received": ["Washing"],
    "Washing": ["Ready"],
    "Ready": ["Delivered"],
    "Delivered": [],
}
