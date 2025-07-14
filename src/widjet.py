from masks import get_mask_card_number, get_mask_account
from datetime import datetime


def mask_account_card(info: str) -> str:
    """Принимает строку с типом и номером, возвращает строку с замаскированным номером."""
    parts = info.strip().split()
    if len(parts) < 2:
        raise ValueError("Строка должна содержать тип (карта или счет) и номер")

    number = parts[-1]
    name = ' '.join(parts[:-1])

    if name.lower() in ('счет', 'счёт'):
        masked_number = get_mask_account(number)
    else:
        masked_number = get_mask_card_number(number)

    return f"{name} {masked_number}"


def get_date(date_str: str) -> str:
    """Принимает строку с датой в формате 'YYYY-MM-DDTHH:MM:SS.microseconds'
    и возвращает строку с датой в формате 'ДД.MM.ГГГГ'."""
    try:
        # Парсим строку в datetime-объект
        dt = datetime.fromisoformat(date_str)
        # Форматируем в нужный вид
        return dt.strftime("%d.%m.%Y")
    except ValueError:
        raise ValueError("Некорректный формат даты. Ожидается 'YYYY-MM-DDTHH:MM:SS.microseconds'")
