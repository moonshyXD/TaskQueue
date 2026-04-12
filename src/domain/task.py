import datetime

from src.domain.descriptors import (
    DescriptionValidator,
    PriorityValidator,
    StatusInfoDescriptor,
)
from src.domain.errors import InvalidStatusError
from src.domain.status import TaskStatus


class Task:
    priority = PriorityValidator()
    description = DescriptionValidator()
    status_info = StatusInfoDescriptor()

    def __init__(
        self,
        description: str,
        priority: int,
        status: TaskStatus | int,
        task_id: int | None = None,
    ) -> None:
        """
        Инициализировать задачу
        :param description: Описание задачи
        :param priority: Приоритет задачи
        :param status: Статус задачи
        :param task_id: Идентификатор задачи
        """
        self._id = task_id
        self.description = description
        self.priority = priority
        self.status = status
        self._created_at = datetime.datetime.now()

    @property
    def id(self) -> int | None:
        """
        Получить идентификатор задачи
        :return: Идентификатор задачи
        """
        return self._id

    @id.setter
    def id(self, value: int) -> None:
        """
        Установить id задачи
        :param value: Новое значение id
        """
        self._id = value

    @property
    def status(self) -> TaskStatus:
        """
        Получить статус задачи
        :return: Статус задачи
        """
        return self._status

    @status.setter
    def status(self, value: TaskStatus | int) -> None:
        """
        Установить статус задачи
        :param value: Новое значение статуса
        :raise InvalidStatusError: Если статус некорректен
        """
        try:
            self._status = TaskStatus(value)
        except ValueError:
            raise InvalidStatusError(value=value) from None

    @property
    def created_at(self) -> datetime.datetime:
        """
        Получить время создания задачи
        :return: Время создания
        """
        return self._created_at

    @property
    def task_duration(self) -> datetime.timedelta:
        """
        Получить длительность существования задачи
        :return: Длительность существования
        """
        return datetime.datetime.now() - self.created_at

    @property
    def is_ready_for_execution(self) -> bool:
        """
        Проверить готовность задачи к выполнению
        :return: Истина, если задача готова
        """
        return self.status == TaskStatus.WAITING and self.priority >= 3

    @property
    def short_description(self) -> str:
        """
        Получить краткое описание задачи
        :return: Первые 10 символов описания
        """
        desc = self.description
        return f"{desc[:10]}..." if len(desc) > 10 else desc

    def __add__(self, other: "Task | int") -> int:
        """
        Поддержка функции sum для приоритетов задач
        :param other: Другая задача или число
        :return: Сумма приоритетов
        """
        if isinstance(other, Task):
            return self.priority + other.priority
        elif isinstance(other, (int, float)):
            return self.priority + int(other)
        return NotImplemented

    def __radd__(self, other: "Task | int") -> int:
        return self.__add__(other)
