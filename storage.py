import json
from config import DATA_DIR, CUSTOMERS_FILE, ORDERS_FILE, PAYMENTS_FILE


def initialize_storage():
    """Create the data directory and JSON files if missing."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    for file_path in (CUSTOMERS_FILE, ORDERS_FILE, PAYMENTS_FILE):
        if not file_path.exists():
            write_data(file_path, [])


def read_data(file_path):
    """Read a JSON file and return a list of records."""
    initialize_storage()

    try:
        with file_path.open("r", encoding="utf-8") as file:
            data = json.load(file)

        if not isinstance(data, list):
            raise ValueError(f"{file_path.name} must contain a JSON list.")

        return data

    except json.JSONDecodeError as error:
        raise ValueError(
            f"{file_path.name} contains invalid JSON. "
            "Restore a valid backup before continuing."
        ) from error


def write_data(file_path, data):
    """Write records to a JSON file."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    with file_path.open("w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)


def get_next_id(records, id_field):
    """Return the next numeric ID for a collection."""
    existing_ids = []

    for record in records:
        try:
            existing_ids.append(int(record[id_field]))
        except (KeyError, TypeError, ValueError):
            continue

    return max(existing_ids, default=0) + 1
