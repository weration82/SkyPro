# tests/test_sort_by_date.py
import pytest

from src.processing import sort_by_date


def _ids(lst):
    return [x["id"] for x in lst]


def test_sort_by_date_desc_and_asc(sort_date_case):
    """
    Проверка сортировку по убыванию и возрастанию на валидных наборах.
    """
    data = sort_date_case["data"]

    desc_sorted = sort_by_date(data, descending=True)
    asc_sorted = sort_by_date(data, descending=False)

    assert _ids(desc_sorted) == sort_date_case["expected_desc_ids"], sort_date_case["name"]
    assert _ids(asc_sorted) == sort_date_case["expected_asc_ids"], sort_date_case["name"]

    # Возвращается НОВЫЙ список (а не та же ссылка)
    assert desc_sorted is not data
    assert asc_sorted is not data


def test_sort_by_date_stability_on_equal_dates():
    """
    Доп. проверка стабильности сортировки при одинаковых датах.
    """
    data = [
        {"id": 1, "date": "2024-02-29T10:00:00"},
        {"id": 2, "date": "2024-02-29T10:00:00"},
        {"id": 3, "date": "2024-02-29T10:00:01"},
    ]
    # По убыванию сначала 3, затем 1 и 2 в исходном порядке
    out_desc = sort_by_date(data, True)
    assert _ids(out_desc) == [3, 1, 2]

    # По возрастанию сначала 1 и 2 в исходном порядке, потом 3
    out_asc = sort_by_date(data, False)
    assert _ids(out_asc) == [1, 2, 3]


def test_sort_by_date_error_cases(sort_date_error_case):
    """
    Сценарии, где функция должна выбросить исключение (см. фикстуры).
    """
    with pytest.raises(sort_date_error_case["expected_exception"]):
        sort_by_date(sort_date_error_case["data"], True)


@pytest.mark.parametrize(
    "data,descending,expected_ids",
    [
        (
            [{"id": 1, "date": "2000-01-01"}, {"id": 2, "date": "1999-12-31"}],
            True,
            [1, 2],
        ),
        (
            [{"id": 1, "date": "2000-01-01"}, {"id": 2, "date": "1999-12-31"}],
            False,
            [2, 1],
        ),
    ],
)
def test_sort_by_date_direct_parametrize(data, descending, expected_ids):
    """
    Простая параметризация без фикстур: проверяю базовый порядок.
    """
    out = sort_by_date(data, descending)
    assert _ids(out) == expected_ids
