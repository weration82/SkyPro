from typing import Any, Dict, Iterator, List


def filter_by_currency(transactions: List[Dict[str, Any]], currency: str) -> Iterator[Dict[str, Any]]:
    """
    Возвращает итератор, который поочерёдно выдаёт транзакции с заданной валютой.
    Строгая валидация входа: transactions должен быть списком словарей.
    """
    if not isinstance(transactions, list):
        raise TypeError("transactions должен быть списком словарей")

    for i, tx in enumerate(transactions):
        if not isinstance(tx, dict):
            # Под тест 'элемент_не_словарь' ожидаем AttributeError
            raise AttributeError(f"transactions[{i}] не является словарём")
        code = tx.get("operationAmount", {}).get("currency", {}).get("code")
        if code == currency:
            yield tx


# Проверка filter_by_currency
# transactions = [
#     {"id": 1, "operationAmount": {"amount": "100.00", "currency": {"code": "USD"}}},
#     {"id": 2, "operationAmount": {"amount": "200.00", "currency": {"code": "EUR"}}},
#     {"id": 3, "operationAmount": {"amount": "50.00", "currency": {"code": "USD"}}},
# ]
#
# for tx in filter_by_currency(transactions, "USD"):
#     print(tx["id"])


def transaction_descriptions(transactions: List[Dict[str, Any]]) -> Iterator[str]:
    """
    Генератор, который поочередно возвращает описания операций ('description')
    из списка транзакций.

    :param transactions: список словарей с ключом 'description'
    :return: итератор строк с описаниями операций
    """
    for tx in transactions:
        # Защита от битых записей: если нет ключа 'description' — пропускаем
        if isinstance(tx, dict) and "description" in tx:
            yield tx["description"]


# Проверка transaction_descriptions
# transactions = [
#     {"id": 1, "description": "Перевод организации"},
#     {"id": 2, "description": "Перевод со счета на счет"},
#     {"id": 3, "description": "Перевод со счета на счет"},
#     {"id": 4, "description": "Перевод с карты на карту"},
#     {"id": 5, "description": "Перевод организации"},
# ]
#
# descriptions = transaction_descriptions(transactions)
# for _ in range(5):
#     print(next(descriptions))


def card_number_generator(start: int, end: int) -> Iterator[str]:
    """
    Генератор, выдающий номера банковских карт в формате 'XXXX XXXX XXXX XXXX'
    от start до end включительно.

    :param start: начальное значение (например, 1)
    :param end: конечное значение (например, 9999_9999_9999_9999)
    :return: итератор строк с форматированными номерами карт
    """
    if not (isinstance(start, int) and isinstance(end, int)):
        raise TypeError("Аргументы start и end должны быть целыми числами")

    if start < 1 or end > 9999_9999_9999_9999:
        raise ValueError("Диапазон должен быть от 1 до 9999 9999 9999 9999 включительно")

    if start > end:
        raise ValueError("Начало диапазона не может быть больше конца")

    for number in range(start, end + 1):
        # Форматируем с ведущими нулями и разбиваем по 4 цифры
        num_str = f"{number:016d}"
        yield f"{num_str[:4]} {num_str[4:8]} {num_str[8:12]} {num_str[12:]}"


# Проверка card_number_generator
# for card_number in card_number_generator(1, 5):
#     print(card_number)
