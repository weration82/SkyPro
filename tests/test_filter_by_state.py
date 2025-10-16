# tests/test_filter_by_state.py
import pytest

from src.processing import filter_by_state


def test_filter_by_state_ok(filter_state_case):
    """
    Проверка корректной фильтрации списка словарей по ключу 'state'.
    """
    data = filter_state_case["data"]
    state = filter_state_case["state"]
    expected_ids = filter_state_case["expected_ids"]

    result = filter_by_state(data, state)

    # проверяю, что возвращаются только нужные элементы и порядок сохраняется
    result_ids = [item["id"] for item in result]
    assert result_ids == expected_ids, filter_state_case["name"]

    # проверяю, что результат это новый список, а не ссылка на старый
    if isinstance(data, list):
        assert result is not data


def test_filter_by_state_default_state(filter_state_case):
    """
    Проверка, что по умолчанию фильтруется по 'EXECUTED', если параметр state не передан.
    """
    data = filter_state_case["data"]
    result = filter_by_state(data)  # state='EXECUTED' по умолчанию

    expected_ids = [item["id"] for item in data if item.get("state") == "EXECUTED"]
    result_ids = [item["id"] for item in result]
    assert result_ids == expected_ids, "Проверка значения по умолчанию EXECUTED"


def test_filter_by_state_empty_input():
    """
    Пустой список должен возвращать пустой результат.
    """
    assert filter_by_state([], "EXECUTED") == []


def test_filter_by_state_error_cases(filter_state_error_case):
    """
    Проверка сценариев, где функция должна вызвать исключение:
    - data=None
    - data не список словарей
    - внутри списка есть элементы, не являющиеся словарями
    """
    with pytest.raises(filter_state_error_case["expected_exception"]):
        filter_by_state(
            filter_state_error_case["data"],
            filter_state_error_case["state"],
        )


@pytest.mark.parametrize(
    "data,state,expected",
    [
        ([{"state": "EXECUTED"}], "EXECUTED", 1),
        ([{"state": "CANCELED"}], "EXECUTED", 0),
        ([{"state": "DONE"}, {"state": "DONE"}], "DONE", 2),
    ],
)
def test_filter_by_state_direct_parametrize(data, state, expected):
    """
    Простая параметризация без фикстур, проверка подсчёта результатов.
    """
    result = filter_by_state(data, state)
    assert len(result) == expected
