from typing import Iterator

from src.domain.errors import TaskCreationError, TaskNotFoundError
from src.domain.task import Task
from src.usecases.interfaces import TaskQueue


class QueueService:
    def __init__(self, repository: TaskQueue):
        """
        Инициализировать сервис очереди
        :param repository: Репозиторий задач
        """
        self.repository = repository

    def add_task(self, task: Task) -> Task:
        """
        Добавить задачу в очередь
        :param task: Объект задачи
        :raises TaskCreationError: Если не удалось добавить задачу
        :return: Добавленная задача
        """
        request = self.repository.add_task(task)
        if request is None:
            raise TaskCreationError(
                reason="Не удалось сохранить задачу в репозитории"
            )

        return request

    def delete_task(self, task_id: int) -> Task:
        """
        Удалить задачу из очереди по ID
        :param task_id: Идентификатор задачи
        :raises TaskNotFoundError: Если задача не найдена
        :return: Удаленная задача
        """
        request = self.repository.delete_task_by_id(task_id)
        if request is None:
            raise TaskNotFoundError(task_id)

        return request

    def update_task(self, task_id: int, new_task: Task) -> Task:
        """
        Обновить данные задачи
        :param task_id: Идентификатор задачи
        :param new_task: Объект с новыми данными
        :raises TaskNotFoundError: Если задача не найдена
        :return: Обновленная задача
        """
        request = self.repository.update_task_by_id(task_id, new_task)
        if request is None:
            raise TaskNotFoundError(task_id)

        return request

    def get_task(self, task_id: int) -> Task:
        """
        Получить задачу по ID
        :param task_id: Идентификатор задачи
        :raises TaskNotFoundError: Если задача не найдена
        :return: Найденная задача
        """
        request = self.repository.get_task_by_id(task_id)
        if request is None:
            raise TaskNotFoundError(task_id)

        return request

    def get_all_tasks(self) -> Iterator[Task]:
        """
        Получить итератор всех задач в очереди
        :return: Итератор задач
        """
        return iter(self.repository)

    def filter_tasks_by_status(self, status: int) -> Iterator[Task]:
        """
        Отфильтровать задачи по статусу
        :param status: Код статуса
        :return: Итератор отфильтрованных задач
        """
        return self.repository.filter_by_status(status)

    def filter_tasks_by_priority(self, priority: int) -> Iterator[Task]:
        """
        Отфильтровать задачи по приоритету
        :param priority: Значение приоритета
        :return: Итератор отфильтрованных задач
        """
        return self.repository.filter_by_priority(priority)

    def get_ready_tasks(self) -> Iterator[Task]:
        """
        Получить задачи, готовые к выполнению
        :return: Итератор готовых задач
        """
        return self.repository.get_ready_for_execution_tasks()

    def get_highest_priority_task(self) -> Task | None:
        """
        Получить задачу с наивысшим приоритетом
        :return: Объект задачи или None
        """
        return self.repository.get_highest_priority_task()
