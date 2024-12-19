from typing import Dict, List, Optional
from src.models import Transaction
from rapidfuzz import fuzz

CategoryMapping = Dict[str, List[str]]


class CategorizationService:
    def __init__(self, categories_mapping: CategoryMapping) -> Optional[str]:
        self.categories_mapping = categories_mapping

    def categorize_transaction(self, transaction: Transaction, source_category: Optional[str] = None) -> Optional[str]:
        # 1. User-defined rules

        # 2A. Predefined rules: by category
        return fuzzy_categorize(source_category or transaction.description, self.categories_mapping)
        # 2A. Predefined rules: by merchant
        # 2B. Predefined rules: by details
        # 3. Embeddings and Vectors
        # 4. LLM model


def fuzzy_categorize(description: str, categories_mapping: CategoryMapping, threshold=80):
    """
    Example:
    categories_mapping = {"Groceries": ["Tesco", "Supermarket"], "Transport": ["Uber", "Rail Services"]}
    description = "TESCO Superstore Purchase"
    result = fuzzy_categorize(description, categories_mapping)
    print(result)  # Output: "Groceries"
    """
    for category, keywords in categories_mapping.items():
        for keyword in keywords:
            score = fuzz.partial_ratio(keyword.lower(), description.lower())
            if score >= threshold:  # Accept if similarity exceeds threshold
                return category
    return None
