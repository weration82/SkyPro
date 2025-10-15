# tests/test_get_date.py
import pytest

from src.widjet import get_date


def test_get_date_ok(date_ok_case):
    """
    Позитивные проверки:
    функция должна корректно конвертировать ISO-дату в формат 'ДД.ММ.ГГГГ'.
    """
    got = get_date(date_ok_case["inp"])
    assert got == date_ok_case["expected"], date_ok_case["name"]


def test_get_date_bad(date_bad_case):
    """
    Негативные проверки:
    некорректные входные строки и типы должны вызывать ожидаемое исключение.
    """
    with pytest.raises(date_bad_case["exc"]):
        get_date(date_bad_case["inp"])


@pytest.mark.parametrize(
    "iso_str,expected",
    [
        ("2020-01-01T00:00:00", "01.01.2020"),
        ("1999-12-31T23:59:59.999999", "31.12.1999"),
        ("2000-02-29", "29.02.2000"),  # високосный год
    ],
)
def test_get_date_direct_parametrize(iso_str, expected):
    """
    Дополнительная параметризация без фикстуры:
    проверяю прямые случаи преобразования.
    """
    assert get_date(iso_str) == expected


def test_get_date_no_mutation():
    """
    Проверка, что входная строка не меняется.
    """
    s = "2023-10-14T12:00:00"
    before = s
    _ = get_date(s)
    assert s is before and s == before
