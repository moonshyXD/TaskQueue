from typing import Any


class TaskHandlerError(Exception):
    pass


class InputValidationError(TaskHandlerError):
    def __init__(self, field: str, value: Any, reason: str):
        """
        Инициализировать ошибку валидации ввода
        :param field: Имя поля, не прошедшего валидацию
        :param value: Переданное некорректное значение
        :param reason: Текстовая причина ошибки валидации
        """
        self.field = field
        self.value = value
        self.reason = reason
        message = (
            f"Некорректное значение в поле '{self.field}': {self.reason} "
            f"Передано: {self.value}"
        )

        super().__init__(message)


class TaskNotFoundError(TaskHandlerError):
    """
    Инициализировать ошибку ненайденной задачи
    :param id: ID задачи, которая не была найдена
    """

    def __init__(self, id: int):
        self.id = id
        message = f"Задача с id: {self.id} не найдена"

        super().__init__(message)


class ContractViolationError(TaskHandlerError):
    def __init__(self, source_obj: Any):
        """
        Инициализировать ошибку нарушения контракта
        :param source_obj: Объект, не соответствующий ожидаемому контракту
        """
        self.source_type = type(source_obj).__name__
        message = (
            f"Объект типа '{self.source_type}' "
            "не поддерживает требуемый поведенческий контракт"
        )

        super().__init__(message)
