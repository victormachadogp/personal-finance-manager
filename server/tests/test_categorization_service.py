from datetime import datetime
from decimal import Decimal
import src.base_categories as base_categories
from src.models import Account, Transaction
from src.services.categorization import CategorizationService


def test_categorize_transaction(account: Account):
    """GIVEN a transaction and a categorization service"""
    cat_service = CategorizationService(base_categories.mapping)
    transaction = Transaction(
        date=datetime.now(),
        description="TESCO STORE 6785 WOOLWICH EXTRA",
        amount=Decimal("100.00"),
        account_id=account.id,
    )

    """WHEN the transaction is categorized"""
    category_id = cat_service.categorize_transaction(transaction)

    """THEN the transaction should be correctly categorized"""
    assert category_id == base_categories.GROCERIES.id


sample_batch = []


def test_categorize_transactions(account: Account):
    """GIVEN a list of transactions and a categorization service"""
    cat_service = CategorizationService(base_categories.mapping)

    """WHEN the transactions are categorized"""
    categories = cat_service.categor
