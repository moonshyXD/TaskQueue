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


class InvalidStatusError(TaskHandlerError):
    def __init__(self, value: Any):
        """
        Инициализировать ошибку некорректного статуса
        :param value: Переданное значение статуса
        """
        self.value = value
        message = f"Некорректный статус: {self.value}"
        super().__init__(message)


class TaskParsingError(TaskHandlerError):
    def __init__(self, line_num: int, reason: str):
        """
        Инициализировать ошибку парсинга задачи
        :param line_num: Номер строки с ошибкой
        :param reason: Причина ошибки
        """
        self.line_num = line_num
        self.reason = reason
        message = f"Ошибка парсинга на строке {self.line_num}: {self.reason}"
        super().__init__(message)


class TaskCreationError(TaskHandlerError):
    def __init__(self, reason: str):
        """
        Инициализировать ошибку создания задачи
        :param reason: Причина ошибки
        """
        self.reason = reason
        message = f"Ошибка создания задачи: {self.reason}"
        super().__init__(message)
