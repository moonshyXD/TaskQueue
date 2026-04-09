from datetime import timedelta

import pytest

from src.domain.errors import InputValidationError
from src.domain.task import Task


@pytest.fixture
def sample_task() -> Task:
    return Task(description="Valid task", priority=3, status=0, task_id=100)


class TestTaskCreation:
    def test_valid_creation(self, sample_task: Task) -> None:
        assert sample_task.id == 100
        assert sample_task.description == "Valid task"
        assert sample_task.priority == 3
        assert sample_task.status == 0
        assert isinstance(sample_task.task_duration, timedelta)

    def test_empty_description(self) -> None:
        with pytest.raises(InputValidationError):
            Task(description="", priority=3, status=0)

    def test_invalid_description_type(self) -> None:
        with pytest.raises(InputValidationError):
            Task(description=123, priority=3, status=0)  # type: ignore[arg-type]

    def test_long_description_shortening(self) -> None:
        long_desc = "GOOOOOOOSEEEEEEEEEE"
        task = Task(description=long_desc, priority=3, status=0)
        assert task.short_description == "GOOOOOOOSE..."
        assert len(task.short_description) == 13


class TestTaskPriority:
    def test_invalid_priority_type(self) -> None:
        with pytest.raises(InputValidationError):
            Task(description="Task", priority="high", status=0)  # type: ignore[arg-type]

    def test_priority_too_low(self) -> None:
        with pytest.raises(InputValidationError):
            Task(description="Task", priority=0, status=0)

    def test_priority_too_high(self) -> None:
        with pytest.raises(InputValidationError):
            Task(description="Task", priority=6, status=0)


class TestTaskStatus:
    def test_valid_status(self) -> None:
        task = Task(description="Task", priority=3, status=1)
        assert task.status == 1

    def test_status_too_high(self) -> None:
        with pytest.raises(ValueError):
            Task(description="Task", priority=3, status=2)

    def test_negative_status(self) -> None:
        with pytest.raises(ValueError):
            Task(description="Task", priority=3, status=-1)

    def test_set_valid_status(self, sample_task: Task) -> None:
        sample_task.status = 0
        assert sample_task.status == 0

    def test_set_invalid_status(self, sample_task: Task) -> None:
        with pytest.raises(ValueError):
            sample_task.status = 5


class TestTaskExecution:
    def test_is_ready_for_execution_true(self) -> None:
        task = Task(description="Task", priority=3, status=0)
        assert task.is_ready_for_execution is True

    def test_is_ready_for_execution_high_priority(self) -> None:
        task = Task(description="Task", priority=5, status=0)
        assert task.is_ready_for_execution is True

    def test_is_ready_for_execution_wrong_status(self) -> None:
        task = Task(description="Task", priority=3, status=1)
        assert task.is_ready_for_execution is False

    def test_is_ready_for_execution_low_priority(self) -> None:
        task = Task(description="Task", priority=2, status=0)
        assert task.is_ready_for_execution is False


class TestTaskMisc:
    def test_status_info_descriptor_returns_correct_info(
        self, sample_task: Task
    ) -> None:
        sample_task.status = 0
        assert sample_task.status_info == "В ожидании"
        sample_task.status = 1
        assert sample_task.status_info == "В работе"

    def test_task_id_setter(self, sample_task: Task) -> None:
        sample_task.id = 999
        assert sample_task.id == 999


class TestTaskMagicMethods:
    def test_add_with_task(self) -> None:
        task1 = Task(description="T1", priority=2, status=0)
        task2 = Task(description="T2", priority=3, status=0)
        assert task1 + task2 == 5

    def test_add_with_int(self) -> None:
        task1 = Task(description="T1", priority=2, status=0)
        assert task1 + 10 == 12

    def test_add_with_unsupported_type(self) -> None:
        task1 = Task(description="T1", priority=2, status=0)
        with pytest.raises(TypeError):
            task1 + "string"  # type: ignore[operator]

    def test_radd_with_sum(self) -> None:
        task1 = Task(description="T1", priority=2, status=0)
        task2 = Task(description="T2", priority=3, status=0)
        assert sum([task1, task2]) == 5
