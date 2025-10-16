# tests/test_card_number_generator.py
import types
from typing import Any, Dict, List

import pytest

from src.generators import card_number_generator


def _is_card_format(s: str) -> bool:
    # "XXXX XXXX XXXX XXXX" - длина 19, пробелы в позициях 4, 9, 14
    return (
        len(s) == 19
        and s[4] == s[9] == s[14] == " "
        and all(ch.isdigit() for i, ch in enumerate(s) if i not in (4, 9, 14))
    )


def test_cardgen_ok(cardgen_case: Dict[str, Any]) -> None:
    """Проверяю корректную генерацию диапазона и формат номера."""
    start, end = cardgen_case["start"], cardgen_case["end"]
    expected: List[str] = cardgen_case["expected"]

    gen = card_number_generator(start, end)
    # это именно генератор-итератор
    assert isinstance(gen, types.GeneratorType)
    output = list(gen)

    assert output == expected, cardgen_case["name"]
    assert all(_is_card_format(s) for s in output)


def test_cardgen_next_iteration(cardgen_case: Dict[str, Any]) -> None:
    """Проверяю поэлементную выдачу через next()."""
    start, end = cardgen_case["start"], cardgen_case["end"]
    expected: List[str] = cardgen_case["expected"]

    gen = card_number_generator(start, end)
    acc: List[str] = []
    for _ in range(len(expected)):
        acc.append(next(gen))
    assert acc == expected
    with pytest.raises(StopIteration):
        next(gen)


def test_cardgen_errors(cardgen_error_case: Dict[str, Any]) -> None:
    """Негативные сценарии - ожидаемые исключения."""
    with pytest.raises(cardgen_error_case["exc"]):
        # type ignore[arg-type] - осознанно подаю неверный тип для негативного теста
        list(card_number_generator(cardgen_error_case["start"], cardgen_error_case["end"]))


@pytest.mark.parametrize(
    "start,end,first,last",
    [
        (1, 1, "0000 0000 0000 0001", "0000 0000 0000 0001"),
        (1, 2, "0000 0000 0000 0001", "0000 0000 0000 0002"),
        (9_999_999_999_999_999, 9_999_999_999_999_999, "9999 9999 9999 9999", "9999 9999 9999 9999"),
    ],
)
def test_cardgen_direct(start: int, end: int, first: str, last: str) -> None:
    """Прямая параметризация: проверяю первые/последние значения диапазона."""
    out = list(card_number_generator(start, end))
    assert out[0] == first and out[-1] == last
    assert all(_is_card_format(s) for s in out)
