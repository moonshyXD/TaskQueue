from src.adapters.cli import CLI
from src.adapters.logger import logging
from src.adapters.orchestrator import ActionOrchestrator
from src.domain.errors import InputValidationError, TaskHandlerError
from src.repository.queue import TaskQueueInMemory


class TaskSchedulerRunner:
    def __init__(self) -> None:
        """
        Инициализация очереди задач и оркестратора
        """
        self.queue = TaskQueueInMemory()
        self.orchestrator = ActionOrchestrator(repository=self.queue)

    def handle_action(self, action: str) -> None:
        """
        Обработка выбранного действия
        :param action: Выбранное пользователем действие
        """
        logging.info(f"Пользователь выбрал событие: {action}")
        logging.info(f"Начало выполнения события: {action}")

        self.orchestrator.handle(action)

        logging.info(f"Успешно выполнено событие: {action}")

    @classmethod
    def handle_input_validation_error(
        cls, exception: InputValidationError
    ) -> None:
        """
        Обработка ошибок валидации ввода
        :param exception: Ошибка валидации
        """
        logging.error(f"Ошибка ввода: {exception}")
        print(f"Ошибка ввода: \n{exception}")

    @classmethod
    def handle_task_handler_error(
        cls, exception: TaskHandlerError
    ) -> None:
        """
        Обработка системных ошибок обработки задач
        :param exception: Системная ошибка
        """
        logging.error(f"Ошибка системы: {exception}")
        print(f"Ошибка системы: \n{exception}")

    @classmethod
    def handle_another_error(cls, exception: Exception) -> None:
        """
        Обработка непредвиденных ошибок
        :param exception: Непредвиденная ошибка
        """
        logging.error(
            f"Произошла непредвиденная ошибка: {exception}", exc_info=True
        )
        print(f"Произошла непредвиденная ошибка: \n{exception}")

    def run(self) -> None:
        """
        Запуск интерактивного обработчика задач
        """
        logging.info("Начало работы программы")
        CLI.greet()
        while (action := CLI.action_select()) != CLI.EXIT:
            try:
                self.handle_action(action)
            except InputValidationError as e:
                self.handle_input_validation_error(e)
            except TaskHandlerError as e:
                self.handle_task_handler_error(e)
            except Exception as e:
                self.handle_another_error(e)

        logging.info("Окончание работы программы")
        CLI.goodbye()



if __name__ == "__main__":
    TaskSchedulerRunner().run()
