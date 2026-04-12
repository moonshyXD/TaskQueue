from typing import Iterator

from src.domain.task import Task


class TaskQueueInMemory:
    def __init__(self) -> None:
        """
        Инициализировать очередь задач
        """
        self._tasks: list[Task] = []
        self._id_counter = 1

    @property
    def total_tasks(self) -> int:
        """
        Получить общее количество задач в очереди
        :return: Количество задач
        """
        return len(self._tasks)

    @property
    def total_priority(self) -> int:
        """
        Вычислить суммарный приоритет всех задач
        :return: Сумма приоритетов
        """
        return sum(task.priority for task in self)

    @property
    def ready_tasks_count(self) -> int:
        """
        Вычислить количество задач, готовых к выполнению
        :return: Количество готовых задач
        """
        return sum(1 for task in self if task.is_ready_for_execution)

    def get_ready_for_execution_tasks(self) -> Iterator[Task]:
        """
        Генератор задач, готовых к выполнению
        :yield: Следующая готовая задача
        """
        for task in self:
            if task.is_ready_for_execution:
                yield task

    def get_highest_priority_task(self) -> Task | None:
        """
        Найти задачу с наивысшим приоритетом
        :return: Задача или None
        """
        if not self._tasks:
            return None

        return max(self, key=lambda t: t.priority)

    def filter_by_status(self, status: int) -> Iterator[Task]:
        """
        Фильтр задач по статусу
        :param status: Код статуса
        :yield: Задача с указанным статусом
        """
        for task in self:
            if task.status == status:
                yield task

    def filter_by_priority(self, priority: int) -> Iterator[Task]:
        """
        Фильтр задач по приоритету
        :param priority: Значение приоритета
        :yield: Задача с указанным приоритетом
        """
        for task in self:
            if task.priority == priority:
                yield task

    def filter_by_id(self, task_id: int) -> Iterator[Task]:
        """
        Найти задачу по ID
        :param task_id: ID задачи
        :yield: Найденная задача
        """
        for task in self:
            if task.id == task_id:
                yield task
                return

    def __iter__(self) -> Iterator[Task]:
        """
        Реализация протокола итерации
        :return: Итератор по задачам
        """
        return iter(self._tasks)

    def __len__(self) -> int:
        """
        Поддержка функции len
        :return: Количество задач
        """
        return self.total_tasks

    def add_task(self, task: Task) -> Task | None:
        """
        Добавить задачу в очередь и присвоить ID
        :param task: Объект задачи
        :return: Добавленная задача
        """
        if task.id is None:
            task.id = self._id_counter
            self._id_counter += 1

        self._tasks.append(task)
        return task

    def delete_task_by_id(self, task_id: int) -> Task | None:
        """
        Удалить задачу из очереди по ID
        :param task_id: ID задачи
        :return: Удаленная задача или None
        """
        for index, task in enumerate(self._tasks):
            if task.id == task_id:
                return self._tasks.pop(index)

        return None

    def get_task_by_id(self, task_id: int) -> Task | None:
        """
        Получить задачу по ID
        :param task_id: ID задачи
        :return: Задача или None
        """
        for task in self:
            if task.id == task_id:
                return task

        return None

    def update_task_by_id(self, task_id: int, new_task: Task) -> Task | None:
        """
        Обновить данные существующей задачи
        :param task_id: ID задачи
        :param new_task: Объект с новыми данными
        :return: Обновленная задача или None
        """
        task_to_update = self.get_task_by_id(task_id)
        if task_to_update:
            task_to_update.description = new_task.description
            task_to_update.priority = new_task.priority
            task_to_update.status = new_task.status
            return task_to_update

        return None
