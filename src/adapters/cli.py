from typing import Iterable

import questionary

from src.domain.descriptors import FilePathValidator, TaskCountValidator
from src.domain.status import TaskStatus
from src.domain.task import Task


class GenerateTasksRequest:
    count = TaskCountValidator()


class GenerateFilePathRequest:
    file_path = FilePathValidator()


class CLI:
    GREET_MESSAGE = "Приветствуем вас в интекративном обработчике задач!"
    GOODBYE_MESSAGE = "Спасибо, что работали с нами. До свидания!"

    TASKS_FROM_FILE = "Задачи из файла"
    TASKS_RANDOM = "Рандомные задачи"
    TASKS_API = "Задачи из API-заглушки"
    CHECK_TASKS = "Просмотреть список задач"
    GET_TASK_BY_ID = "Найти задачу по ID"
    FILTER_TASKS = "Отфильтровать задачи"
    SHOW_READY = "Задачи, готовые к выполнению"
    SHOW_HIGHEST_PRIORITY = "Задача с наивысшим приоритетом"
    EXIT = "Выход из программы"

    ACTION_ASK = "Выберите режим приёмки задач"
    TASKS_COUNT_ASK = "Какое количество заданий вы хотите сгенерировать?"
    FILE_PATH_ASK = "Укажите путь к файлу относительно папки TaskHandler"
    FILTER_ASK = "Выберите критерий фильтрации"
    TASK_ID_ASK = "Введите ID задачи"
    STATUS_ASK = "Выберите статус для фильтрации"
    PRIORITY_ASK = "Выберите приоритет для фильтрации"

    BY_PRIORITY = "По приоритету"
    BY_STATUS = "По статусу"

    @staticmethod
    def get_tasks_count() -> int:
        """
        Запросить у пользователя количество задач для генерации
        :return: Количество задач
        """
        raw_input = questionary.text(CLI.TASKS_COUNT_ASK).ask()
        request = GenerateTasksRequest()
        request.count = raw_input
        return int(request.count)

    @staticmethod
    def get_file_path() -> str:
        """
        Запросить у пользователя путь к файлу с задачами
        :return: Путь к файлу
        """
        raw_input = questionary.text(CLI.FILE_PATH_ASK).ask()
        request = GenerateFilePathRequest()
        request.file_path = raw_input
        return str(request.file_path)

    @staticmethod
    def greet() -> None:
        """
        Вывести приветственное сообщение
        """
        print(CLI.GREET_MESSAGE)

    @staticmethod
    def action_select() -> str:
        """
        Запросить у пользователя выбор действия из меню
        :return: Выбранное пользователем действие
        """
        action = questionary.select(
            CLI.ACTION_ASK,
            choices=[
                CLI.TASKS_FROM_FILE,
                CLI.TASKS_RANDOM,
                CLI.TASKS_API,
                CLI.CHECK_TASKS,
                CLI.GET_TASK_BY_ID,
                CLI.FILTER_TASKS,
                CLI.SHOW_READY,
                CLI.SHOW_HIGHEST_PRIORITY,
                CLI.EXIT,
            ],
        ).ask()

        return action

    @staticmethod
    def get_filter_criteria() -> str:
        """
        Запросить критерий фильтрации
        :return: Критерий фильтрации
        """
        return questionary.select(
            CLI.FILTER_ASK,
            choices=[CLI.BY_PRIORITY, CLI.BY_STATUS],
        ).ask()

    @staticmethod
    def get_status_value() -> int:
        """
        Запросить статус для фильтрации
        :return: Выбранный статус
        """
        status_map = TaskStatus.to_dict()
        display_map = {v: k for k, v in status_map.items()}
        choice = questionary.select(
            CLI.STATUS_ASK,
            choices=list(display_map.keys()),
        ).ask()
        return display_map[choice]

    @staticmethod
    def get_priority_value() -> int:
        """
        Запросить приоритет для фильтрации
        :return: Выбранный приоритет
        """
        choice = questionary.select(
            CLI.PRIORITY_ASK,
            choices=["1", "2", "3", "4", "5"],
        ).ask()
        return int(choice)

    @staticmethod
    def get_task_id() -> int:
        """
        Запросить ID задачи
        :return: ID задачи
        """
        raw_input = questionary.text(CLI.TASK_ID_ASK).ask()
        return int(raw_input)

    @staticmethod
    def goodbye() -> None:
        """
        Вывести прощальное сообщение
        """
        print(CLI.GOODBYE_MESSAGE)

    @staticmethod
    def print_tasks(
        tasks: Iterable[Task], full_description: bool = False
    ) -> None:
        """
        Вывести список задач в консоль
        :param tasks: Список задач
        :param full_description: Если True, выводить полное описание
        """
        desc_width = 40 if full_description else 20
        header = (
            f"{'ID':<5} | {'Описание':<{desc_width}} | "
            f"{'Приор.':<8} | {'Статус':<15} | {'Готов'}"
        )
        print(header)
        print("-" * (65 + (20 if full_description else 0)))
        for task in tasks:
            description = (
                task.description
                if full_description
                else task.short_description
            )
            print(
                f"{str(task.id):<5} | "
                f"{description:<{desc_width}} | "
                f"{str(task.priority):<8} | "
                f"{task.status_info:<15} | "
                f"{'Да' if task.is_ready_for_execution else 'Нет'}"
            )
