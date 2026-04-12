import json
import logging
from typing import Iterator

from src.domain.errors import TaskParsingError
from src.domain.task import Task


class TaskFile:
    def __init__(self, file_path: str):
        """
        Инициализировать источник задач из файла
        :param file_path: Путь к файлу с задачами
        """
        self.file_path = file_path

    def get_tasks(self) -> Iterator[Task]:
        """
        Прочитать и распарсить задачи из файла построчно
        :yield: Объект Task
        """
        file_path = self.file_path
        with open(file_path, "r", encoding="utf-8") as file:
            for line_num, line in enumerate(file, 1):
                try:
                    line = line.strip()
                    if not line:
                        continue

                    _, payload_str = line.split(" ", 1)
                    payload = json.loads(payload_str)

                    yield Task(
                        description=payload["description"],
                        priority=payload["priority"],
                        status=payload["status"],
                        task_id=payload.get("id"),
                    )
                except (ValueError, KeyError, json.JSONDecodeError) as e:
                    error = TaskParsingError(line_num=line_num, reason=str(e))
                    logging.warning(f"Ошибка в файле {file_path}: {error}")
                    continue
