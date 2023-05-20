import pytest
from new_pandas_connector_1 import PandasConnector
from check import Check
import pandas as pd

data = [
    ["tom", 10, "jones"],
    ["nick", 15, "jones"],
    ["juli", 14, "jones"],
    ["sam", 14, "jones"],
    ["", 14.55, "jones"],
    ["nick", None, "jones"],
]
df = pd.DataFrame(data, columns=["Name", "Age", "LName"], dtype="object")

conn = PandasConnector(dataframe=df)
check = Check(connector=conn, checkpoint_id="test")


def test_auto_generate_checks():
    check._generate_checks()


def test_get_connector_check_methods():
    check._get_connector_checks()


def test_run_every_check_method():
    methods = check._get_connector_checks()
    for m in methods:
        method_run = getattr(conn, f"check__{m}")
        if m.startswith("table_"):
            method_run()
        elif m.startswith("col_"):
            method_run(col="Age")


def test_auto_generate_check_run_checks():
    check_list = check._generate_checks()
    check.run_local(checks=check_list)


def test_auto_generate_check_run_checks_exception():
    with pytest.raises(Exception) as e_info:
        check.run_local(checks=["bad list"])


def test_succeed_check__table_columns_count():
    checks = [{"check": "table_columns_count", "expected": [0, 5]}]
    assert check.run_local(checks=checks)["summary"]["success_rate"] == 100


def test_exception_check__table_columns_count():
    checks = [{"check": "table_columns_count", "expected": [0]}]
    with pytest.raises(Exception) as e_info:
        assert check.run_local(checks=checks)["summary"]["success_rate"] == 100


def test_fail_check__table_columns_count():
    checks = [{"check": "table_columns_count", "expected": [5, 10]}]
    assert check.run_local(checks=checks)["summary"]["success_rate"] == 0
