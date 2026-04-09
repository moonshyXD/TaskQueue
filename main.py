from src.adapters.cli import CLI
from src.adapters.logger import logging
from src.adapters.orchestrator import ActionOrchestrator
from src.domain.errors import ContractViolationError, InputValidationError
from src.repository.queue import TaskQueueInMemory


def run() -> None:
    """Запуск интерактивного обработчика задач"""
    logging.info("Начало работы программы")
    CLI.greet()

    queue = TaskQueueInMemory()
    orchestrator = ActionOrchestrator(repository=queue)

    while (action := CLI.action_select()) != CLI.EXIT:
        try:
            logging.info(f"Пользователь выбрал событие: {action}")
            logging.info(f"Начало выполнения события: {action}")

            orchestrator.handle(action)

            logging.info(f"Успешно выполнено событие: {action}")

        except InputValidationError as e:
            logging.error(f"Ошибка ввода: {e}")
            print(f"Ошибка ввода: \n{e}")

        except ContractViolationError as e:
            logging.error(f"Ошибка системы: {e}")
            print(f"Ошибка системы: \n{e}")

        except Exception as e:
            logging.error(
                f"Произошла непредвиденная ошибка: {e}", exc_info=True
            )
            print(f"Произошла непредвиденная ошибка: \n{e}")

    logging.info("Окончание работы программы")
    CLI.goodbye()


if __name__ == "__main__":
    run()
