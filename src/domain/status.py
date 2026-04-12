from enum import IntEnum


class TaskStatus(IntEnum):
    WAITING = 0
    IN_PROGRESS = 1

    @classmethod
    def to_dict(cls) -> dict[int, str]:
        """
        Получить словарь соответствия статусов и их названий
        :return: Словарь {код: название}
        """
        return {cls.WAITING: "В ожидании", cls.IN_PROGRESS: "В работе"}
