from pathlib import Path
from typing import Any

from src.domain.errors import InputValidationError
from src.domain.status import TaskStatus


class TaskCountValidator:
    REASON_INT = "Должно вводиться целое число"
    REASON_NOT_NEGATIVE = "Число должно быть неотрицательным"

    def __set_name__(self, owner: Any, name: str) -> None:
        """
        Установить имя атрибута для дескриптора
        :param owner: Класс-владелец дескриптора
        :param name: Имя атрибута
        """
        self.name = name

    def __set__(self, instance: Any, value: Any) -> None:
        """
        Провалидировать и установить количество задач
        :param instance: Экземпляр класса-владельца
        :param value: Значение для проверки
        :raise InputValidationError: Если значение не целое или отрицательное
        """
        try:
            val_int = int(value)
        except ValueError:
            raise InputValidationError(
                field=self.name, reason=self.REASON_INT, value=value
            ) from None

        if val_int < 0:
            raise InputValidationError(
                field=self.name, reason=self.REASON_NOT_NEGATIVE, value=value
            )

        instance.__dict__[self.name] = val_int


class FilePathValidator:
    REASON_NOT_STRING = "Путь должен быть строкой"
    REASON_NOT_EXISTS = "Файл по указанному пути не найден"
    REASON_NOT_FILE = "Указанный путь ведет к папке, а надо к файлу"

    def __set_name__(self, owner: Any, name: str) -> None:
        """
        Установить имя атрибута для дескриптора
        :param owner: Класс-владелец дескриптора
        :param name: Имя атрибута
        """
        self.name = name

    def __get__(self, instance: Any, owner: Any) -> Any:
        """
        Получить путь к файлу
        :param instance: Экземпляр класса
        :param owner: Класс-владелец
        :return: Значение
        """
        if instance is None:
            return self
        return instance.__dict__.get(self.name)

    def __set__(self, instance: Any, value: Any) -> None:
        """
        Провалидировать и установить путь к файлу
        :param instance: Экземпляр класса-владельца
        :param value: Путь для проверки
        :raise InputValidationError: Если пути нет, он не строка и не файл
        """
        if not isinstance(value, str):
            raise InputValidationError(
                field=self.name, reason=self.REASON_NOT_STRING, value=value
            )

        path = Path(value).resolve()
        if not path.exists():
            raise InputValidationError(
                field=self.name, reason=self.REASON_NOT_EXISTS, value=str(path)
            )

        if not path.is_file():
            raise InputValidationError(
                field=self.name, reason=self.REASON_NOT_FILE, value=str(path)
            )

        instance.__dict__[self.name] = path


class PriorityValidator:
    REASON_NOT_INT = "Приоритет должен быть целым числом"
    REASON_OUT_OF_BOUNDS = "Приоритет должен быть от 1 до 5"

    def __set_name__(self, owner: Any, name: str) -> None:
        """
        Установить имя атрибута
        :param owner: Класс-владелец
        :param name: Имя атрибута
        """
        self.name = name

    def __get__(self, instance: Any, owner: Any) -> Any:
        """
        Получить значение приоритета
        :param instance: Экземпляр класса
        :param owner: Класс-владелец
        :return: Значение приоритета
        """
        if instance is None:
            return self
        return instance.__dict__.get(self.name)

    def __set__(self, instance: Any, value: Any) -> None:
        """
        Установить значение приоритета
        :param instance: Экземпляр класса
        :param value: Новое значение
        :raise InputValidationError: Если значение не целое или не от 1 до 5
        """
        try:
            val_int = int(value)
        except ValueError:
            raise InputValidationError(
                field=self.name, reason=self.REASON_NOT_INT, value=value
            ) from None

        if not (1 <= val_int <= 5):
            raise InputValidationError(
                field=self.name, reason=self.REASON_OUT_OF_BOUNDS, value=value
            )

        instance.__dict__[self.name] = val_int


class DescriptionValidator:
    REASON_NOT_STRING = "Описание должно быть строкой"
    REASON_EMPTY = "Описание не может быть пустым"

    def __set_name__(self, owner: Any, name: str) -> None:
        """
        Установить имя атрибута
        :param owner: Класс-владелец
        :param name: Имя атрибута
        """
        self.name = name

    def __get__(self, instance: Any, owner: Any) -> Any:
        """
        Получить описание
        :param instance: Экземпляр класса
        :param owner: Класс-владелец
        :return: Описание
        """
        if instance is None:
            return self
        return instance.__dict__.get(self.name, "")

    def __set__(self, instance: Any, value: Any) -> None:
        """
        Установить описание
        :param instance: Экземпляр класса
        :param value: Новое значение
        :raise InputValidationError: Если описание не строка или пустая строка
        """
        if not isinstance(value, str):
            raise InputValidationError(
                field=self.name, reason=self.REASON_NOT_STRING, value=value
            )
        if not value.strip():
            raise InputValidationError(
                field=self.name, reason=self.REASON_EMPTY, value=value
            )
        instance.__dict__[self.name] = value


class StatusInfoDescriptor:
    def __get__(self, instance: Any, owner: Any) -> Any:
        """
        Получить справочную информацию о статусе
        :param instance: Экземпляр класса
        :param owner: Класс-владелец
        :return: Справочная информация
        """
        if instance is None:
            return self

        status_map = TaskStatus.to_dict()
        return status_map.get(instance.status, "Неизвестно")
