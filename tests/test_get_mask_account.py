# test_get_mask_account.py
import pytest

from src.masks import get_mask_account


def test_account_mask_happy_path(account_ok_case):
    # Проверка корректной маски для валидных номеров счёта.
    got = get_mask_account(account_ok_case["inp"])
    assert got == account_ok_case["expected"], account_ok_case["name"]


@pytest.mark.parametrize("wrap", [lambda s: s, lambda s: f" {s} "])
def test_account_rejects_bad_inputs(account_bad_case, wrap):
    # Неправильный ввод
    inp = account_bad_case["inp"]
    if isinstance(inp, str):
        inp = wrap(inp)
    with pytest.raises(account_bad_case["exc"]):
        get_mask_account(inp)


def test_account_input_not_mutated(account_ok_case):
    # Проверка, что входная строка не меняется.
    inp = account_ok_case["inp"]
    before = inp
    _ = get_mask_account(inp)
    assert inp is before and inp == before
