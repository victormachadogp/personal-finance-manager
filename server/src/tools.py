import click
import csv
from typing import BinaryIO, Optional

from src.dtos import ColumnMapper
from src import database
from src.services.finances import FinanceService


def get_file_data(file_path):
    with open(file_path, mode="r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        return [row for row in reader]


@click.command()
@click.argument("file_path", type=click.Path(exists=True), required=True)
@click.option("--account_id", type=str, required=True, help="The account ID to associate with the CSV.")
@click.option("--date", type=str, required=True, help="The column name for the date.")
@click.option("--description", type=str, required=True, help="The column name for the transaction description.")
@click.option("--amount", type=str, required=True, help="The column name for the transaction amount.")
@click.option("--date_format", type=str, required=True, help="The format of the date in the CSV (e.g., '%Y-%m-%d').")
@click.option("--category", type=str, required=False, help="Optional transaction category.")
def load_csv(
    file_path: str,
    account_id: str,
    date: str,
    description: str,
    amount: str,
    date_format: str,
    category: Optional[str] = None,
):
    """
    Load a CSV file from the given FILE_PATH and display its contents.
    """
    column_mapper = ColumnMapper(
        date=date, description=description, amount=amount, date_format=date_format, category=category
    )
    with open(file_path, mode="rb") as file:
        import_data(file, account_id, column_mapper)


def import_data(file: BinaryIO, account_id: str, column_mapper: ColumnMapper):
    """
    Load a CSV file from the given FILE_PATH and display its contents.
    """
    engine = database.get_engine()
    session = database.get_session(engine=engine)
    finance_service = FinanceService(session=session)
    finance_service.import_csv(file, account_id, column_mapper)
    print("Data successfully imported!")


if __name__ == "__main__":
    load_csv()
