from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
import src.base_categories as base_categories
from src.models import Account, Category, Transaction
from src.services.categorization import CategorizationService, fuzzy_categorize


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


@dataclass
class CategorizationTest:
    description: str
    expected_category: Category


def test_amex_categorize_transactions(account: Account):
    """GIVEN a list of transactions and a categorization service"""
    sample_batch = [
        CategorizationTest("General Purchases-Groceries", base_categories.GROCERIES),
        CategorizationTest("Travel-Rail Services", base_categories.TRANSPORT),
        CategorizationTest("Entertainment-Restaurants", base_categories.EATING_OUT),
        CategorizationTest("General Purchases-Department Stores", base_categories.SHOPPING),
        CategorizationTest("Entertainment-Other Entertainment", base_categories.ENTERTAINMENT),
        CategorizationTest("Business Services-Professional Services", None),
        CategorizationTest("General Purchases-Online Purchases", base_categories.GENERAL),
        CategorizationTest("Travel-Other Travel", base_categories.HOLIDAYS),
        CategorizationTest("Entertainment-Bars & Cafés", base_categories.ENTERTAINMENT),
        CategorizationTest("General Purchases-Clothing Stores", base_categories.SHOPPING),
        CategorizationTest("General Purchases-General Retail", base_categories.SHOPPING),
        CategorizationTest("General Purchases-Fuel", base_categories.TRANSPORT),
        CategorizationTest("Business Services-Other Services", base_categories.GENERAL),
        CategorizationTest("General Purchases-Computer Supplies", base_categories.GENERAL),
        CategorizationTest("General Purchases-Pharmacies", base_categories.PERSONAL_CARE),
        CategorizationTest("General Purchases-Parking Charges", base_categories.TRANSPORT),
        CategorizationTest("General Purchases-Government Services", base_categories.GENERAL),
        CategorizationTest("Entertainment-Theme Parks", base_categories.ENTERTAINMENT),
        CategorizationTest("Travel-Auto Services", base_categories.TRANSPORT),
        CategorizationTest("Business Services-Conferences & Training", base_categories.GENERAL),
        CategorizationTest("General Purchases-Mail Order", base_categories.GENERAL),
        CategorizationTest("Entertainment-General Attractions", base_categories.ENTERTAINMENT),
        CategorizationTest("Communications-Internet Communication", base_categories.GENERAL),
        CategorizationTest("General Purchases-Furnishing", base_categories.HOUSING),
        CategorizationTest("Travel-Travel Agencies", base_categories.HOLIDAYS),
        CategorizationTest("General Purchases-Hardware Supplies", base_categories.HOUSING),
        CategorizationTest("Miscellaneous-Education", base_categories.EDUCATION),
        CategorizationTest("Entertainment-Theatrical Events", base_categories.ENTERTAINMENT),
        CategorizationTest("General Purchases-Sporting Goods Stores", base_categories.GENERAL),
        CategorizationTest("Travel-Airline", base_categories.HOLIDAYS),
        CategorizationTest("Entertainment-General Events", base_categories.ENTERTAINMENT),
        CategorizationTest("Business Services-Insurance Services", base_categories.GENERAL),
        CategorizationTest("Business Services-Office Supplies", base_categories.GENERAL),
        CategorizationTest("Travel-Tolls & Fees", base_categories.HOLIDAYS),
        CategorizationTest("General Purchases-Wholesale Stores", base_categories.GENERAL),
        CategorizationTest("Travel-Lodging", base_categories.HOLIDAYS),
        CategorizationTest("Business Services-Mailing & Shipping", base_categories.GENERAL),
    ]

    """WHEN the transactions are categorized"""

    counter = 0
    for test in sample_batch:
        """THEN the transactions should be correctly categorized"""
        category_id = fuzzy_categorize(test.description, base_categories.category_mapping, threshold=85)

        expected = test.expected_category.id if test.expected_category else None
        if category_id != expected:
            print(f"\nProcessing: {test.description}")
            print(f"Expected: {test.expected_category.title}, id: {test.expected_category.id}")
            print(f"Got: {category_id}")
            counter += 1

    print(f"\n\n{counter}/{len(sample_batch)} mismatches found")

    assert counter <= 15