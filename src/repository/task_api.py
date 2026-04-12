from typing import Iterator

from src.domain.status import TaskStatus
from src.domain.task import Task


class TaskAPI:
    def get_tasks(self) -> Iterator[Task]:
        """
        Получить задачи из API-заглушки
        :yield: Сгенерированная задача
        """
        yield Task(
            description="Эта первая задача для гуся",
            priority=1,
            status=TaskStatus.IN_PROGRESS,
        )
        yield Task(
            description="Эта вторая задача для гуся",
            priority=5,
            status=TaskStatus.WAITING,
        )
