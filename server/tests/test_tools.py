from unittest.mock import patch
from src.models import Account
from src.tools import load_csv
from click.testing import CliRunner


def test_load_csv(account: Account, engine, db_session):
    runner = CliRunner()

    with (
        patch("src.tools.database.get_session", return_value=db_session),
        patch("src.tools.database.get_engine", return_value=engine),
    ):
        result = runner.invoke(
            load_csv,
            [
                "tests/assets/test-transactions.csv",
                "--account_id", account.id,
                "--date", "date",
                "--description", "description",
                "--amount", "amount",
                "--date_format", "%Y-%m-%d",
            ],  
        )  # fmt: off

    assert result.exit_code == 0, result.stdout
