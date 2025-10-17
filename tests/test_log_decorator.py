# tests/test_log_decorator.py
from pathlib import Path
from typing import Any, Dict

import pytest

from src.decorators import log


def test_log_ok_console_and_file(
    log_ok_case: Dict[str, Any],
    capsys: pytest.CaptureFixture[str],
    tmp_path: Path,  # <-- ВАЖНО: это pathlib.Path
) -> None:
    """
    Успешное выполнение: проверяем, что возвращается результат,
    и лог попадает в консоль/файл в нужном формате.
    """
    if log_ok_case["to_file"]:
        logdir = tmp_path / "logs"
        logdir.mkdir()
        logfile = logdir / "mylog.txt"

        @log(filename=str(logfile))
        def add(x: int, y: int) -> int:
            return x + y

        res = add(*log_ok_case["args"], **log_ok_case["kwargs"])
        assert res == sum(log_ok_case["args"])
        text = logfile.read_text(encoding="utf-8").strip()
        assert text.endswith(log_ok_case["expected_line"])
    else:

        @log()
        def add(x: int, y: int) -> int:
            return x + y

        res = add(*log_ok_case["args"], **log_ok_case["kwargs"])
        assert res == sum(log_ok_case["args"])
        out = capsys.readouterr().out.strip()
        assert out.endswith(log_ok_case["expected_line"])


def test_log_error_console_and_file(
    log_err_case: Dict[str, Any],
    capsys: pytest.CaptureFixture[str],
    tmp_path: Path,  # <-- pathlib.Path
) -> None:
    """
    Ошибка выполнения: исключение пробрасывается,
    а лог содержит имя функции, текст ошибки и входные параметры.
    """
    if log_err_case["op"] == "div":

        def core(x: Any, y: Any) -> Any:
            return x / y

    else:

        def core(x: Any, y: Any) -> Any:
            return x + y

    if log_err_case["to_file"]:
        logdir = tmp_path / "logs"
        logdir.mkdir()
        logfile = logdir / "mylog.txt"

        @log(filename=str(logfile))
        def demo(x: Any, y: Any) -> Any:
            return core(x, y)

        with pytest.raises(log_err_case["exc"]):
            demo(*log_err_case["args"], **log_err_case["kwargs"])

        text = logfile.read_text(encoding="utf-8").strip()
        assert "demo error:" in text
        assert f"Inputs: {log_err_case['args']}, {log_err_case['kwargs']}" in text
        if log_err_case["exc_msg"]:
            assert log_err_case["exc_msg"] in text
    else:

        @log()
        def demo(x: Any, y: Any) -> Any:
            return core(x, y)

        with pytest.raises(log_err_case["exc"]):
            demo(*log_err_case["args"], **log_err_case["kwargs"])
        out = capsys.readouterr().out.strip()
        assert "demo error:" in out
        assert f"Inputs: {log_err_case['args']}, {log_err_case['kwargs']}" in out
        if log_err_case["exc_msg"]:
            assert log_err_case["exc_msg"] in out


def test_log_preserves_function_result_and_name(capsys: pytest.CaptureFixture[str]) -> None:
    @log()
    def multiply(a: int, b: int) -> int:
        """Докстринг должен сохраняться"""
        return a * b

    assert multiply.__name__ == "multiply"
    assert multiply.__doc__ == "Докстринг должен сохраняться"
    assert multiply(3, 4) == 12
    assert capsys.readouterr().out.strip().endswith("multiply ok")


def test_log_raises_same_exception_type(capsys: pytest.CaptureFixture[str]) -> None:
    class CustomError(RuntimeError):
        pass

    @log()
    def boom() -> None:
        raise CustomError("Бабах!")

    with pytest.raises(CustomError):
        boom()
    assert "boom error:" in capsys.readouterr().out
