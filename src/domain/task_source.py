from typing import Protocol, runtime_checkable

from src.domain.task import Task


@runtime_checkable
class TaskSource(Protocol):
    def get_tasks(self) -> list[Task]:
        """
        Получить список задач из источника
        :return: Список объектов Task
        """
        ...
