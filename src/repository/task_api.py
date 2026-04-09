from src.domain.task import Task


class TaskAPI:
    def get_tasks(self) -> list[Task]:
        """
        Получить список задач из API-заглушки
        :return: Список сгенерированных задач
        """
        description1 = "Эта первая задача для гуся"
        priority1 = 1
        status1 = 1
        task1 = Task(
            description=description1, priority=priority1, status=status1
        )

        description2 = "Эта вторая задача для гуся"
        priority2 = 5
        status2 = 0
        task2 = Task(
            description=description2, priority=priority2, status=status2
        )

        tasks = [task1, task2]
        return tasks
