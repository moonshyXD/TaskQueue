from src.domain.errors import ContractViolationError
from src.domain.task_source import TaskSource
from src.usecases.interfaces import TaskQueue


class ImportTasks:
    def __init__(self, repository: TaskQueue):
        """
        Инициализировать импорт задач
        :param repository: Интерфейс хранилища задач
        """
        self.repository = repository

    def execute(self, source: TaskSource) -> int:
        """
        Выполнить импорт задач из указанного источника
        :param source: Объект источника задач
        :raises ContractViolationError: Если источник не поддерживает контракт
        :return: Количество успешно загруженных задач
        """
        if not isinstance(source, TaskSource):
            raise ContractViolationError(source_obj=source)

        count = 0
        for task in source.get_tasks():
            self.repository.add_task(task)
            count += 1

        return count
