# conftest.py
import pytest

# =============================
# get_mask_card_number
# =============================


# Правильный ввод: ожидаем правильную маску
@pytest.fixture(
    params=[
        {
            "name": "обычный_номер",
            "inp": "1234567890123456",
            "expected": "1234 56** **** 3456",
        },
        {
            "name": "ведущие_нули",
            "inp": "0000001234567890",
            "expected": "0000 00** **** 7890",
        },
        {
            "name": "разные_цифры",
            "inp": "9876543210987654",
            "expected": "9876 54** **** 7654",
        },
        {
            "name": "все_одинаковые",
            "inp": "1111111111111111",
            "expected": "1111 11** **** 1111",
        },
    ]
)
def card_ok_case(request):
    """Позитивные примеры: 16 цифр, корректный вывод маски."""
    return request.param


# Неправильный ввод: ожидаем исключения
@pytest.fixture(
    params=[
        # Длина не 16
        {"name": "короче_15", "inp": "123456789012345", "exc": ValueError},
        {"name": "длиннее_17", "inp": "12345678901234567", "exc": ValueError},
        {"name": "пустая_строка", "inp": "", "exc": ValueError},
        # Недопустимые символы / форматы
        {"name": "с_пробелами", "inp": "1234 5678 9012 3456", "exc": ValueError},
        {"name": "с_дефисами", "inp": "1234-5678-9012-3456", "exc": ValueError},
        {"name": "буква_внутри", "inp": "12345678901234a6", "exc": ValueError},
        {"name": "только_буквы", "inp": "abcdabcdabcdabcd", "exc": ValueError},
        # Тип не str
        {"name": "None", "inp": None, "exc": TypeError},
        {"name": "int", "inp": 1234567890123456, "exc": TypeError},
    ]
)
def card_bad_case(request):
    """
    Негативные примеры:
    - длина != 16
    - нецифровые/разделители
    - неверный тип (не str)
    """
    return request.param


# =============================
# get_mask_account
# =============================


# Правильный ввод: только цифры, длина >= 4
@pytest.fixture(
    params=[
        {"name": "минимум_проходит_5", "inp": "12345", "expected": "**2345"},
        {"name": "обычный_длинный", "inp": "987654321", "expected": "**4321"},
        {"name": "ведущие_нули", "inp": "000012345", "expected": "**2345"},
        {"name": "все_одинаковые", "inp": "111111", "expected": "**1111"},
        {"name": "оканчивается_нулями", "inp": "55550000", "expected": "**0000"},
        {"name": "очень_длинный", "inp": "12345678901234567890", "expected": "**7890"},
    ]
)
def account_ok_case(request):
    """Правильные входные данные для get_mask_account."""
    return request.param


# Неправильный ввод: длина <= 4, нецифровые, неверный тип
@pytest.fixture(
    params=[
        {"name": "короче_3", "inp": "123", "exc": ValueError},
        {"name": "ровно_4", "inp": "1234", "exc": ValueError},
        {"name": "пустая", "inp": "", "exc": ValueError},
        {"name": "с_пробелами", "inp": "12 345", "exc": ValueError},
        {"name": "с_дефисами", "inp": "12-345", "exc": ValueError},
        {"name": "буква", "inp": "12a45", "exc": ValueError},
        {"name": "None", "inp": None, "exc": TypeError},
        {"name": "int", "inp": 12345, "exc": TypeError},
    ]
)
def account_bad_case(request):
    """Неправильные входные данные для get_mask_account."""
    return request.param


# =============================
# mask_account_card
# =============================


@pytest.fixture(
    params=[
        # Карты
        {
            "name": "карта_валидная",
            "inp": "Visa 1234567890123456",
            "expected": "Visa 1234 56** **** 3456",
        },
        {
            "name": "карта_mastercard",
            "inp": "MasterCard 9876543210987654",
            "expected": "MasterCard 9876 54** **** 7654",
        },
        {
            "name": "карта_ведущие_нули",
            "inp": "Card 0000001234567890",
            "expected": "Card 0000 00** **** 7890",
        },
        # Счета
        {
            "name": "счет_валидный",
            "inp": "Счет 1234567890",
            "expected": "Счет **7890",
        },
        {
            "name": "счёт_с_ё",
            "inp": "Счёт 987654321",
            "expected": "Счёт **4321",
        },
        {
            "name": "счет_ведущие_нули",
            "inp": "Счет 000012345",
            "expected": "Счет **2345",
        },
    ]
)
def mask_account_card_ok_case(request):
    """
    Правильные входные данные для mask_account_card:
    """
    return request.param


@pytest.fixture(
    params=[
        # Некорректные строки (нет типа или номера)
        {"name": "только_тип", "inp": "Счет", "exc": ValueError},
        {"name": "только_номер", "inp": "1234567890", "exc": ValueError},
        {"name": "пустая", "inp": "", "exc": ValueError},
        {"name": "только_пробел", "inp": "   ", "exc": ValueError},
        # Ошибки формата номера
        {"name": "счет_слишком_короткий", "inp": "Счет 1234", "exc": ValueError},
        {"name": "карта_слишком_короткая", "inp": "Visa 1234", "exc": ValueError},
        {"name": "карта_с_буквами", "inp": "Visa 1234abcd90123456", "exc": ValueError},
        {"name": "счет_с_буквами", "inp": "Счет 12a45", "exc": ValueError},
        # Тип не str
        {"name": "None", "inp": None, "exc": AttributeError},
        {"name": "int", "inp": 12345, "exc": AttributeError},
    ]
)
def mask_account_card_bad_case(request):
    """
    Неправильные входные данные для mask_account_card:
    """
    return request.param


# =============================
# get_date
# =============================


# Позитивные кейсы: разные варианты ISO-дат, которые корректно парсит datetime.fromisoformat
@pytest.fixture(
    params=[
        {
            "name": "точный_формат_с_микросекундами",
            "inp": "2019-07-03T18:35:29.512364",
            "expected": "03.07.2019",
        },
        {
            "name": "без_микросекунд",
            "inp": "2021-12-01T00:00:00",
            "expected": "01.12.2021",
        },
        {
            "name": "только_дата",
            "inp": "2020-01-15",
            "expected": "15.01.2020",
        },
        {
            "name": "с_зоной_смещение_плюс",
            "inp": "2022-03-10T23:59:59.000001+03:00",
            "expected": "10.03.2022",
        },
        {
            "name": "с_зоной_смещение_минус",
            "inp": "2022-03-10T23:59:59-05:00",
            "expected": "10.03.2022",
        },
        {
            "name": "высокосный_день",
            "inp": "2024-02-29T12:00:00.000000",
            "expected": "29.02.2024",
        },
        {
            "name": "эпоха_дата_только",
            "inp": "1970-01-01",
            "expected": "01.01.1970",
        },
    ]
)
def date_ok_case(request):
    """
    Валидные входы для get_date:
    - точный формат с микросекундами
    - допустимые вариации ISO (без микросекунд, только дата, с таймзоной)
    """
    return request.param


# Негативные кейсы: строки, которые fromisoformat не принимает или явно некорректны
@pytest.fixture(
    params=[
        {
            "name": "пустая_строка",
            "inp": "",
            "exc": ValueError,
        },
        {
            "name": "natural_language",
            "inp": "yesterday",
            "exc": ValueError,
        },
        {
            "name": "неверный_формат_со_слешами",
            "inp": "2021/12/01 00:00:00",
            "exc": ValueError,
        },
        {
            "name": "несуществующая_дата",
            "inp": "2021-02-29T10:00:00",
            "exc": ValueError,
        },
        {
            "name": "часов_больше_24",
            "inp": "2021-12-01T25:00:00",
            "exc": ValueError,
        },
        {
            "name": "буквы_вместо_цифр",
            "inp": "abcd-ef-ghTij:kl:mn",
            "exc": ValueError,
        },
        # Неверные типы, datetime.fromisoformat ожидает str и бросит TypeError ещё до перехвата ValueError
        {
            "name": "None",
            "inp": None,
            "exc": TypeError,
        },
        {
            "name": "int",
            "inp": 20211201,
            "exc": TypeError,
        },
        {
            "name": "list",
            "inp": ["2021-12-01T00:00:00"],
            "exc": TypeError,
        },
    ]
)
def date_bad_case(request):
    """
    Невалидные входы для get_date:
    - пустая строка, неверные форматы, невозможные даты
    - неверные типы (None, int, list)
    """
    return request.param


# =============================
# filter_by_state
# =============================


@pytest.fixture(
    params=[
        {
            "name": "несколько_EXECUTED_смешанные_состояния",
            "data": [
                {"id": 1, "state": "EXECUTED"},
                {"id": 2, "state": "CANCELED"},
                {"id": 3, "state": "EXECUTED"},
                {"id": 4, "state": "PROCESSING"},
            ],
            "state": "EXECUTED",
            "expected_ids": [1, 3],
        },
        {
            "name": "нет_совпадений_по_CANCELED",
            "data": [
                {"id": 1, "state": "EXECUTED"},
                {"id": 2, "state": "EXECUTED"},
            ],
            "state": "CANCELED",
            "expected_ids": [],
        },
        {
            "name": "пустой_входной_список",
            "data": [],
            "state": "EXECUTED",
            "expected_ids": [],
        },
        {
            "name": "регистрозависимость_executed_не_совпадает",
            "data": [
                {"id": 1, "state": "EXECUTED"},
                {"id": 2, "state": "executed"},
                {"id": 3, "state": "Executed"},
            ],
            "state": "executed",
            "expected_ids": [2],  # строгая проверка == без нормализации регистра
        },
        {
            "name": "хвостовые_пробелы_в_значениях_state",
            "data": [
                {"id": 1, "state": "EXECUTED"},
                {"id": 2, "state": "EXECUTED "},  # пробел в конце
                {"id": 3, "state": "EXECUTED"},
            ],
            "state": "EXECUTED ",
            "expected_ids": [2],
        },
        {
            "name": "state_None_фильтруем_None",
            "data": [
                {"id": 1, "state": None},
                {"id": 2, "state": "EXECUTED"},
                {"id": 3, "state": None},
            ],
            "state": None,  # функция сравнивает через ==, это допустимо
            "expected_ids": [1, 3],
        },
        {
            "name": "элементы_без_ключа_state_пропускаются",
            "data": [
                {"id": 1, "state": "EXECUTED"},
                {"id": 2},  # нет 'state'
                {"id": 3, "state": "CANCELED"},
                {"id": 4},  # нет 'state'
                {"id": 5, "state": "EXECUTED"},
            ],
            "state": "EXECUTED",
            "expected_ids": [1, 5],
        },
    ]
)
def filter_state_case(request):
    """
    Параметризованный набор для корректной работы filter_by_state:
    - несколько совпадений/нет совпадений
    - пустой вход
    - чувствительность к регистру и пробелам
    - фильтрация по None
    - пропуск элементов без ключа 'state'
    """
    return request.param


@pytest.fixture(
    params=[
        {
            "name": "data_None",
            "data": None,  # неитерируемый -> TypeError при попытке for item in data
            "state": "EXECUTED",
            "expected_exception": TypeError,
        },
        {
            "name": "data_не_список_а_словарь",
            "data": {"id": 1, "state": "EXECUTED"},  # итерация по ключам-строкам -> у str нет .get
            "state": "EXECUTED",
            "expected_exception": AttributeError,
        },
        {
            "name": "data_содержит_не_словарь",
            "data": [
                {"id": 1, "state": "EXECUTED"},
                "not_a_dict",  # у строки нет .get -> AttributeError
                {"id": 3, "state": "EXECUTED"},
            ],
            "state": "EXECUTED",
            "expected_exception": AttributeError,
        },
    ]
)
def filter_state_error_case(request):
    """
    Наборы, которые должны приводить к исключениям:
    - data=None
    - data, не список словарей (словарь или примеси не-словарей)
    """
    return request.param


# =============================
# sort_by_date
# =============================


# Валидные кейсы: отдаем список записей + ожидаемый порядок id для убывания и возрастания
@pytest.fixture(
    params=[
        {
            "name": "basic_various_naive",
            "data": [
                {"id": 1, "date": "2021-01-01T00:00:00"},
                {"id": 2, "date": "2022-06-01T12:30:00.500000"},
                {"id": 3, "date": "2019-07-03T18:35:29.512364"},
            ],
            "expected_desc_ids": [2, 1, 3],
            "expected_asc_ids": [3, 1, 2],
        },
        {
            "name": "equal_dates_stability",
            "data": [
                {"id": 1, "date": "2024-02-29T10:00:00"},
                {"id": 2, "date": "2024-02-29T10:00:00"},  # та же дата/время
                {"id": 3, "date": "2024-03-01T00:00:00"},
            ],
            # При равных ключах Python-сортировка стабильна: порядок 1 перед 2 сохранится
            "expected_desc_ids": [3, 1, 2],
            "expected_asc_ids": [1, 2, 3],
        },
        {
            "name": "aware_timezones_all_aware",
            "data": [
                {"id": 1, "date": "2022-03-10T23:00:00+03:00"},  # 20:00Z
                {"id": 2, "date": "2022-03-10T21:59:59+00:00"},  # 21:59:59Z -> позже, чем id=1
                {"id": 3, "date": "2022-03-09T23:00:00+03:00"},  # 20:00Z на сутки раньше
            ],
            "expected_desc_ids": [2, 1, 3],
            "expected_asc_ids": [3, 1, 2],
        },
        {
            "name": "date_only_strings",
            "data": [
                {"id": 10, "date": "1970-01-01"},
                {"id": 11, "date": "2020-01-01"},
                {"id": 12, "date": "2000-02-29"},
            ],
            "expected_desc_ids": [11, 12, 10],
            "expected_asc_ids": [10, 12, 11],
        },
    ]
)
def sort_date_case(request):
    """
    Валидные наборы для sort_by_date:
    - разные форматы ISO (с/без микросекунд, только дата)
    - все aware (с таймзонами) корректно сравнимы между собой
    - равные датыб, проверяю стабильность сортировки
    """
    return request.param


# Невалидные кейсы: ожидаем исключения от datetime.fromisoformat или индексации по ключу
@pytest.fixture(
    params=[
        {
            "name": "data_None",
            "data": None,  # sorted(None) -> TypeError (неитерируемо)
            "expected_exception": TypeError,
        },
        {
            "name": "element_has_no_date_key",
            "data": [
                {"id": 1, "date": "2021-01-01T00:00:00"},
                {"id": 2},  # нет ключа 'date' -> x['date'] вызовет KeyError
            ],
            "expected_exception": KeyError,
        },
        {
            "name": "bad_format_slashes",
            "data": [
                {"id": 1, "date": "2021/12/01 00:00:00"},  # не ISO -> ValueError
            ],
            "expected_exception": ValueError,
        },
        {
            "name": "mixed_naive_and_aware",
            "data": [
                {"id": 1, "date": "2021-12-01T00:00:00"},  # naive
                {"id": 2, "date": "2021-12-01T00:00:00+00:00"},  # aware
            ],
            # Ключи станут datetime(naive) и datetime(aware); при сравнении возникнет TypeError
            "expected_exception": TypeError,
        },
        {
            "name": "date_is_None",
            "data": [
                {"id": 1, "date": None},  # fromisoformat(None) -> TypeError
            ],
            "expected_exception": TypeError,
        },
        {
            "name": "element_is_not_dict",
            "data": [
                {"id": 1, "date": "2021-01-01T00:00:00"},
                "not_a_dict",  # '...'['date'] -> TypeError: string indices must be integers
            ],
            "expected_exception": TypeError,
        },
    ]
)
def sort_date_error_case(request):
    """
    Наборы, которые должны приводить к исключениям:
    - неитерируемый вход
    - отсутствует ключ 'date'
    - смешение naive/aware datetime
    - неверные типы полей/элементов
    """
    return request.param
