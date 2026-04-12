from typing import Iterator, Protocol, runtime_checkable

from src.domain.task import Task


@runtime_checkable
class TaskSource(Protocol):
    def get_tasks(self) -> Iterator[Task]:
        """
        Получить итератор задач из источника
        :return: Итератор объектов Task
        """
        ...
