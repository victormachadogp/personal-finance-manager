from src.models import Account
from src.tools import ColumnMapper, import_data


def test_load_csv(account: Account):
    file_path = "/Users/jonathan/Downloads/Nubank_2024-03-28.csv"
    column_mapper = ColumnMapper(date="date", description="title", amount="amount", date_format="%Y-%m-%d")
    import_data(file_path=file_path, account_id=account.id, column_mapper=column_mapper)
