import io
import json
from fastapi.testclient import TestClient
from sqlmodel import Session

from src.models import Account
from src.services.finances import FinanceService


def test_upload_transactions_csv(client: TestClient, account: Account, db_session: Session):
    # Create a CSV file
    csv_data = [
        "date,description,amount",
        "2024-07-09,Test1,100.00",
        "2024-07-10,Test2,200.00",
        "2024-07-02,PAYMENT RECEIVED - THANK YOU,-500.00",
    ]

    # write to in memory file
    file = io.BytesIO("\n".join(csv_data).encode("utf-8"))

    # Upload the CSV file
    column_mapper = {"date": "date", "description": "description", "amount": "amount", "date_format": "%Y-%m-%d"}
    files_payload = {"file": ("test.csv", file, "text/csv")}
    response = client.post(
        f"/accounts/{account.id}/transactions/import",
        files=files_payload,
        data={"column_mapper": json.dumps(column_mapper)},
    )

    assert response.status_code == 200

    """THEN the transactions are imported"""
    finance_service = FinanceService(db_session)
    transactions = finance_service.get_transactions()
    assert len(transactions) == 3

    excluded_transaction = transactions[2]
    assert excluded_transaction.exclude_from_analytics is True
