# import click
import csv
from datetime import datetime

import click
from src.database import get_session
from src import base_categories
from src.models import Transaction
from src.services.categorization import CategorizationService


def get_file_data(file_path):
    with open(file_path, mode="r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        return [row for row in reader]


def data_to_transaction(data, account_id: str):
    cat_service = CategorizationService(base_categories.category_mapping)

    transactions = []
    for row in data:
        # conver row["Date"] (eg: 07/09/2024) to a datetime object
        date = datetime.strptime(row["Date"], "%d/%m/%Y")
        transaction = Transaction(
            date=date, description=row["Description"], amount=row["Amount"], account_id=account_id
        )
        category_id = cat_service.categorize_transaction(transaction, source_category=row["Category"])
        transaction.category_id = category_id
        transactions.append(transaction)
    return transactions


@click.command()
@click.argument("file_path", type=click.Path(exists=True))
@click.argument("account_id", type=str)
def load_csv(file_path: str, account_id: str):
    """
    Load a CSV file from the given FILE_PATH and display its contents.
    """
    data = get_file_data(file_path)
    transactions = data_to_transaction(data, account_id)
    session = get_session()
    for transaction in transactions:
        session.add(transaction)
    session.commit()
    print("Data loaded successfully")


if __name__ == "__main__":
    load_csv()
