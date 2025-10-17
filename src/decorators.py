import functools
from typing import Callable, Optional, ParamSpec, TypeVar

P = ParamSpec("P")
R = TypeVar("R")


def log(filename: Optional[str] = None) -> Callable[[Callable[P, R]], Callable[P, R]]:
    """
    Декоратор логирует начало/конец выполнения функции:
    - при успехе: "<funcname> ok"
    - при ошибке: "<funcname> error: <текст ошибки>. Inputs: (<args>), <kwargs>"
    Если filename задан — пишет в файл (append), иначе выводит в stdout.
    """

    def decorator(func: Callable[P, R]) -> Callable[P, R]:
        @functools.wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            try:
                result = func(*args, **kwargs)
                line = f"{func.__name__} ok\n"
                if filename:
                    with open(filename, "a", encoding="utf-8") as f:
                        f.write(line)
                else:
                    # print добавит перевод строки; чтобы совпасть с ожиданием без лишних пробелов:
                    print(line.strip())
                return result
            except Exception as e:
                line = f"{func.__name__} error: {e}. Inputs: {args}, {kwargs}\n"
                if filename:
                    with open(filename, "a", encoding="utf-8") as f:
                        f.write(line)
                else:
                    print(line.strip())
                raise  # пробрасываю исключение дальше

        return wrapper

    return decorator


# Проверка

# @log(filename="mylog.txt")
# def my_function(x, y):
#     return x + y
#
# my_function(1, 2)
