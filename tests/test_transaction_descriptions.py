# tests/test_transaction_descriptions.py
from typing import Any, Dict, List

import pytest

from src.generators import transaction_descriptions


def test_transaction_descriptions_ok(descriptions_case: Dict[str, Any]) -> None:
    """
    Проверка, что генератор корректно выдаёт описания транзакций.
    """
    transactions = descriptions_case["transactions"]
    expected = descriptions_case["expected"]

    generator = transaction_descriptions(transactions)
    result = list(generator)

    assert result == expected, descriptions_case["name"]
    assert hasattr(generator, "__iter__"), "Функция должна возвращать итератор"


def test_transaction_descriptions_error_cases(descriptions_error_case: Dict[str, Any]) -> None:
    """
    Проверка, что при некорректных данных выбрасывается ожидаемое исключение.
    """
    with pytest.raises(descriptions_error_case["expected_exception"]):
        list(transaction_descriptions(descriptions_error_case["transactions"]))


@pytest.mark.parametrize(
    "transactions,expected",
    [
        ([{"description": "A"}, {"description": "B"}], ["A", "B"]),
        ([{"description": "X"}], ["X"]),
        ([], []),
    ],
)
def test_transaction_descriptions_direct(transactions: List[Dict[str, Any]], expected: List[str]) -> None:
    """
    Прямая параметризация без фикстур, проверяю базовое поведение.
    """
    result = list(transaction_descriptions(transactions))
    assert result == expected
