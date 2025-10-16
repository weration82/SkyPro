# test_get_mask_card_number.py
import pytest

from src.masks import get_mask_card_number


def test_mask_happy_path(card_ok_case):
    inp = card_ok_case["inp"]
    expected = card_ok_case["expected"]
    got = get_mask_card_number(inp)
    assert got == expected, card_ok_case["name"]


@pytest.mark.parametrize("stripper", [str.strip, lambda s: s])  # лишние пробелы вокруг
def test_mask_rejects_nonpure_formats(card_bad_case, stripper):
    inp = card_bad_case["inp"]
    exc = card_bad_case["exc"]

    # Если это строка, применяю обрамляющие пробелы для проверки,
    # что функция не принимает такие форматы.
    if isinstance(inp, str):
        inp = stripper(inp) if stripper is str.strip else f" {inp} "

    with pytest.raises(exc):
        get_mask_card_number(inp)


def test_do_not_mutate_input(card_ok_case):
    # Проверка, что входная строка не меняется.
    inp = card_ok_case["inp"]
    before = inp
    _ = get_mask_card_number(inp)
    assert inp is before and inp == before
