def get_mask_card_number(card_number: str) -> str:
    """Принимает на вход номер карты возвращает маску номера."""
    card_str = card_number
    if len(card_str) != 16 or not card_str.isdigit():
        raise ValueError("Номер карты должен состоять из 16 цифр")

    card_numbers_begin = card_str[:6]
    card_numbers_end = card_str[-4:]
    hidden_numbers = "** ****"

    result = f"{card_numbers_begin[:4]} {card_numbers_begin[4:6]}{hidden_numbers} {card_numbers_end}"

    return result


def get_mask_account(account_number: str) -> str:
    """Принимает на вход номер счета возвращает маску номера."""
    account_str = account_number

    if len(account_str) < 4 or not account_str.isdigit():
        raise ValueError("Номер счета должен иметь больше 4х цифр")

    last_four_digits = account_str[-4:]

    return f"**{last_four_digits}"
