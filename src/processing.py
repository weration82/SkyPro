from datetime import datetime
from typing import Any, Dict, List


def filter_by_state(data: List[Dict[str, Any]], state: str = "EXECUTED") -> List[Dict[str, Any]]:
    """
    Возвращает список словарей, у которых значение ключа 'state' совпадает с указанным.

    :param data: список словарей
    :param state: значение состояния для фильтрации (по умолчанию 'EXECUTED')
    :return: новый список словарей
    """
    return [item for item in data if item.get("state") == state]


# Код для проверки
# print(filter_by_state([
#     {'id': 41428829, 'state': 'EXECUTED', 'date': '2019-07-03T18:35:29.512364'},
#     {'id': 939719570, 'state': 'EXECUTED', 'date': '2018-06-30T02:08:58.425572'},
#     {'id': 594226727, 'state': 'CANCELED', 'date': '2018-09-12T21:27:25.241689'},
#     {'id': 615064591, 'state': 'CANCELED', 'date': '2018-10-14T08:21:33.419441'}
# ], "CANCELED"))


def sort_by_date(data: List[Dict[str, Any]], descending: bool = True) -> List[Dict[str, Any]]:
    """
    Возвращает новый список словарей, отсортированный по дате (ключ 'date').

    :param data: список словарей, содержащих ключ 'date'
    :param descending: порядок сортировки (по умолчанию True — убывание)
    :return: отсортированный список словарей
    """
    return sorted(data, key=lambda x: datetime.fromisoformat(x["date"]), reverse=descending)


# Код для проверки
# print(sort_by_date([
#     {'id': 41428829, 'state': 'EXECUTED', 'date': '2019-07-03T18:35:29.512364'},
#     {'id': 939719570, 'state': 'EXECUTED', 'date': '2018-06-30T02:08:58.425572'},
#     {'id': 594226727, 'state': 'CANCELED', 'date': '2018-09-12T21:27:25.241689'},
#     {'id': 615064591, 'state': 'CANCELED', 'date': '2018-10-14T08:21:33.419441'}
# ]))
