# tests/test_mask_account_card.py
import pytest

from src.widjet import mask_account_card


def test_mask_account_card_ok(mask_account_card_ok_case):
    """Позитив: функция корректно маскирует карты и счета."""
    result = mask_account_card(mask_account_card_ok_case["inp"])
    assert result == mask_account_card_ok_case["expected"], mask_account_card_ok_case["name"]


def test_mask_account_card_bad(mask_account_card_bad_case):
    """Негатив: некорректные входные данные вызывают ожидаемое исключение."""
    with pytest.raises(mask_account_card_bad_case["exc"]):
        mask_account_card(mask_account_card_bad_case["inp"])


@pytest.mark.parametrize("label", ["Счет", "Счёт", "счет", "сЧЁт"])
def test_account_case_insensitive(label):
    """Тип 'Счет/Счёт' должен распознаваться без учета регистра и варианта буквы 'ё'."""
    number = "1234567890"
    expected_tail = "**7890"
    result = mask_account_card(f"{label} {number}")
    assert result == f"{label} {expected_tail}"


@pytest.mark.parametrize(
    "title,number,expected_tail",
    [
        ("Visa Gold", "1234567890123456", "1234 56** **** 3456"),
        ("My Super Premium Card", "0000001234567890", "0000 00** **** 7890"),
    ],
)
def test_multiword_card_name(title, number, expected_tail):
    """Название может состоять из нескольких слов/частей, оно должно сохраняться целиком."""
    result = mask_account_card(f"{title} {number}")
    assert result == f"{title} {expected_tail}"
