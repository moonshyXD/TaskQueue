from typing import Callable, Dict

from src.adapters.cli import CLI
from src.repository.task_api import TaskAPI
from src.repository.task_file import TaskFile
from src.repository.task_random import TaskRandom
from src.usecases.import_tasks import ImportTasks
from src.usecases.interfaces import TaskQueue
from src.usecases.queue import QueueService


class ActionOrchestrator:
    def __init__(self, repository: TaskQueue):
        """
        Инициализировать оркестратор
        :param repository: Репозиторий задач
        """
        self.repository = repository
        self.service = QueueService(repository)
        self.importer = ImportTasks(repository)
        self._handlers: Dict[str, Callable[[], None]] = {
            CLI.TASKS_FROM_FILE: self._handle_import_file,
            CLI.TASKS_RANDOM: self._handle_import_random,
            CLI.TASKS_API: self._handle_import_api,
            CLI.CHECK_TASKS: self._handle_check_tasks,
            CLI.GET_TASK_BY_ID: self._handle_get_task_by_id,
            CLI.FILTER_TASKS: self._handle_filter_tasks,
            CLI.SHOW_READY: self._handle_show_ready,
            CLI.SHOW_HIGHEST_PRIORITY: self._handle_show_highest,
        }

    def handle(self, action: str) -> None:
        """
        Обработать выбранное действие
        :param action: Название действия из CLI
        """
        handler = self._handlers.get(action)
        if handler:
            handler()

    def _handle_import_file(self) -> None:
        """
        Оркестрация импорта из файла
        """
        file_path = CLI.get_file_path()
        self.importer.execute(TaskFile(file_path=file_path))

    def _handle_import_random(self) -> None:
        """
        Оркестрация генерации случайных задач
        """
        count = CLI.get_tasks_count()
        self.importer.execute(TaskRandom(tasks_count=count))

    def _handle_import_api(self) -> None:
        """
        Оркестрация импорта из API
        """
        self.importer.execute(TaskAPI())

    def _handle_check_tasks(self) -> None:
        """
        Оркестрация просмотра всех задач
        """
        tasks = self.service.get_all_tasks()
        CLI.print_tasks(tasks=tasks)

    def _handle_get_task_by_id(self) -> None:
        """
        Оркестрация поиска задачи по ID
        """
        task_id = CLI.get_task_id()
        task = self.service.get_task(task_id)
        CLI.print_tasks(tasks=[task], full_description=True)

    def _handle_filter_tasks(self) -> None:
        """
        Оркестрация фильтрации задач
        """
        criteria = CLI.get_filter_criteria()
        if criteria == CLI.BY_PRIORITY:
            value = CLI.get_priority_value()
            tasks = self.service.filter_tasks_by_priority(value)
        else:
            value = CLI.get_status_value()
            tasks = self.service.filter_tasks_by_status(value)

        CLI.print_tasks(tasks=tasks)

    def _handle_show_ready(self) -> None:
        """
        Оркестрация показа готовых задач
        """
        tasks = self.service.get_ready_tasks()
        CLI.print_tasks(tasks=tasks)

    def _handle_show_highest(self) -> None:
        """
        Оркестрация показа задачи с высшим приоритетом
        """
        highest = self.service.get_highest_priority_task()
        if highest:
            CLI.print_tasks(tasks=[highest])
        else:
            print("Очередь пуста")
