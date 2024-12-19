import click
import csv
from datetime import datetime
from typing import Optional

from pydantic import BaseModel
from src import base_categories
from src.models import Transaction
from src.services.categorization import CategorizationService
from src.database import get_session


def get_file_data(file_path):
    with open(file_path, mode="r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        return [row for row in reader]


class ColumnMapper(BaseModel):
    date: str
    date_format: str  # eg: "%d/%m/%Y" or "%Y-%m-%d"
    description: str
    amount: str
    category: Optional[str] = None


def data_to_transaction(data, account_id: str, column_mapper: ColumnMapper):
    mapping_strategy = base_categories.category_mapping if column_mapper.category else base_categories.mapping
    cat_service = CategorizationService(mapping_strategy)

    transactions = []
    for row in data:
        # conver row["Date"] (eg: 07/09/2024) to a datetime object
        date = datetime.strptime(row[column_mapper.date], column_mapper.date_format)
        transaction = Transaction(
            date=date,
            description=row[column_mapper.description],
            amount=row[column_mapper.amount],
            account_id=account_id,
        )
        source_category = row.get(column_mapper.category)
        category_id = cat_service.categorize_transaction(transaction, source_category=source_category)
        transaction.category_id = category_id
        transactions.append(transaction)
    return transactions


@click.command()
@click.argument("file_path", type=click.Path(exists=True))
@click.argument("account_id", type=str)
@click.argument("date", type=str)
@click.argument("title", type=str)
@click.argument("amount", type=str)
@click.argument("date_format", type=str)
def load_csv(file_path: str, account_id: str, date: str, title: str, amount: str, date_format: str):
    """
    Load a CSV file from the given FILE_PATH and display its contents.
    """
    column_mapper = ColumnMapper(date=date, description=title, amount=amount, date_format=date_format)
    # print(column_mapper)
    import_data(file_path, account_id, column_mapper)


def import_data(file_path: str, account_id: str, column_mapper: ColumnMapper):
    """
    Load a CSV file from the given FILE_PATH and display its contents.
    """
    data = get_file_data(file_path)
    transactions = data_to_transaction(data, account_id, column_mapper)
    session = get_session()
    for transaction in transactions:
        session.add(transaction)
    session.commit()
    print("Data successfully imported!")


if __name__ == "__main__":
    load_csv()
