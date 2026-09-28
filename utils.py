from datetime import date, datetime


def input_int(prompt: str) -> int:
    """Запрашивать целое число, пока ввод не станет корректным."""
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print("Ошибка: введите целое число.")


def input_float(prompt: str) -> float:
    """Запрашивать число, пока ввод не станет корректным."""
    while True:
        try:
            return float(input(prompt))
        except ValueError:
            print("Ошибка: введите число.")


def input_date(prompt: str) -> date:
    """Запрашивать дату в формате ДД.ММ.ГГГГ до корректного ввода."""
    while True:
        try:
            return datetime.strptime(input(prompt), "%d.%m.%Y").date()
        except ValueError:
            print("Ошибка: неверный формат даты. Используйте ДД.ММ.ГГГГ.")


def input_text(prompt: str) -> str:
    """Запрашивать непустую строку, пока ввод не станет корректным."""
    while True:
        text = input(prompt).strip()
        if text:
            return text
        print("Ошибка: значение не может быть пустым.")
