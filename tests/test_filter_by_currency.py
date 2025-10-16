# tests/test_filter_by_currency.py
from typing import Any, Dict

import pytest

from src.generators import filter_by_currency


def test_filter_by_currency_ok(currency_case: Dict[str, Any]) -> None:
    """
    Проверяю корректную фильтрацию транзакций по коду валюты.
    """
    transactions = currency_case["transactions"]
    currency = currency_case["currency"]
    expected_ids = currency_case["expected_ids"]

    result_iter = filter_by_currency(transactions, currency)
    result = list(result_iter)
    result_ids = [t["id"] for t in result]

    assert result_ids == expected_ids, currency_case["name"]
    # Проверим, что возвращается именно итератор
    assert hasattr(result_iter, "__iter__"), "Функция должна возвращать итератор"


def test_filter_by_currency_error_cases(currency_error_case: Dict[str, Any]) -> None:
    """
    Проверяю, что при некорректных данных выбрасывается ожидаемое исключение.
    """
    with pytest.raises(currency_error_case["expected_exception"]):
        list(
            filter_by_currency(
                currency_error_case["transactions"],
                currency_error_case["currency"],
            )
        )


@pytest.mark.parametrize(
    "currency,expected",
    [
        ("USD", [1, 3]),
        ("EUR", [2]),
        ("JPY", []),
    ],
)
def test_filter_by_currency_direct_parametrize(currency: str, expected: list[int]) -> None:
    """
    Прямая параметризация: проверяю фильтрацию на упрощённом наборе данных.
    """
    data = [
        {"id": 1, "operationAmount": {"currency": {"code": "USD"}}},
        {"id": 2, "operationAmount": {"currency": {"code": "EUR"}}},
        {"id": 3, "operationAmount": {"currency": {"code": "USD"}}},
    ]
    result_ids = [tx["id"] for tx in filter_by_currency(data, currency)]
    assert result_ids == expected
