import random

from src.domain.task import Task


class TaskRandom:
    DESCRIPTIONS = [
        "Сыграть в казино",
        "Задонатить гусю на пиво",
        "Купить пиво",
        "Поиграть с гусем",
        "Закоммитить в мастер",
        "Покормить гуся",
        "Дать кличку гусю",
        "Завести гуся",
        "Сходить в коворкинг",
        "Приготовить пиццу",
    ]
    PRIORITIIES = [1, 2, 3, 4, 5]
    STATUSES = [0, 1]

    def __init__(self, tasks_count: int):
        """
        Инициализировать генератор случайных задач
        :param tasks_count: Количество задач для генерации
        """
        self.tasks_count = tasks_count

    def get_tasks(self) -> list[Task]:
        """
        Сгенерировать случайные задачи
        :return: Список сгенерированных случайных задач
        """
        tasks = []
        tasks_count = self.tasks_count
        for _ in range(tasks_count):
            description = random.choice(self.DESCRIPTIONS)
            priority = random.choice(self.PRIORITIIES)
            status = random.choice(self.STATUSES)
            task = Task(
                description=description,
                priority=priority,
                status=status,
            )
            tasks.append(task)

        return tasks
