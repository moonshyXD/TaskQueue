from typing import Iterator
from unittest.mock import mock_open, patch

import pytest

from src.domain.errors import ContractViolationError, TaskNotFoundError
from src.domain.task import Task
from src.repository.queue import TaskQueueInMemory
from src.repository.task_api import TaskAPI
from src.repository.task_file import TaskFile
from src.repository.task_random import TaskRandom
from src.usecases.import_tasks import ImportTasks
from src.usecases.queue import QueueService


class MockQueue:
    def __init__(self) -> None:
        self.tasks: list[Task] = []

    def add_task(self, task: Task) -> Task | None:
        self.tasks.append(task)
        return task

    def get_task_by_id(self, task_id: int) -> Task | None:
        return next((t for t in self.tasks if t.id == task_id), None)

    def delete_task_by_id(self, task_id: int) -> Task | None:
        for i, t in enumerate(self.tasks):
            if t.id == task_id:
                return self.tasks.pop(i)
        return None

    def update_task_by_id(self, task_id: int, new_task: Task) -> Task | None:
        task = self.get_task_by_id(task_id)
        if task:
            task.description = new_task.description
            task.priority = new_task.priority
            task.status = new_task.status
            return task
        return None

    def filter_by_status(self, status: int) -> Iterator[Task]:
        return (t for t in self.tasks if t.status == status)

    def filter_by_priority(self, priority: int) -> Iterator[Task]:
        return (t for t in self.tasks if t.priority == priority)

    def filter_by_id(self, task_id: int) -> Iterator[Task]:
        task = self.get_task_by_id(task_id)
        if task:
            yield task

    def get_highest_priority_task(self) -> Task | None:
        if not self.tasks:
            return None
        return max(self.tasks, key=lambda t: t.priority)

    def get_ready_for_execution_tasks(self) -> Iterator[Task]:
        return (t for t in self.tasks if t.is_ready_for_execution)

    def __iter__(self) -> Iterator[Task]:
        return iter(self.tasks)


class TestTaskSources:
    def test_task_api(self) -> None:
        assert len(TaskAPI().get_tasks()) == 2

    def test_task_random(self) -> None:
        random_source = TaskRandom(tasks_count=3)
        tasks = random_source.get_tasks()
        assert len(tasks) == 3
        assert 1 <= tasks[0].priority <= 5
        assert tasks[0].description in TaskRandom.DESCRIPTIONS
        assert tasks[0].status in TaskRandom.STATUSES
        assert tasks[0].id is None

    def test_task_file(self) -> None:
        file_content = (
            '1 {"description": "Test", "priority": 1, "status": 0, "id": 1}\n'
        )
        with patch("builtins.open", mock_open(read_data=file_content)):
            tasks = TaskFile("dummy_path.txt").get_tasks()
            assert len(tasks) == 1
            assert tasks[0].id == 1
            assert tasks[0].description == "Test"
            assert tasks[0].priority == 1
            assert tasks[0].status == 0


class TestImportTasks:
    def test_import_success(self) -> None:
        queue = MockQueue()
        importer = ImportTasks(queue)  # type: ignore[arg-type]
        count = importer.execute(TaskAPI())
        assert count == 2
        assert len(queue.tasks) == 2

    def test_import_fail_contract_violation(self) -> None:
        with pytest.raises(ContractViolationError):
            ImportTasks(MockQueue()).execute(123)  # type: ignore[arg-type]


@pytest.fixture
def queue_service() -> QueueService:
    return QueueService(repository=TaskQueueInMemory())


class TestQueueService:
    def test_add_task(self, queue_service: QueueService) -> None:
        task = Task(description="T1", priority=1, status=0)
        added_task = queue_service.add_task(task)
        assert added_task.id is not None
        assert added_task == task

    def test_get_task(self, queue_service: QueueService) -> None:
        task = Task(description="T1", priority=1, status=0)
        added_task = queue_service.add_task(task)
        assert added_task.id is not None
        found_task = queue_service.get_task(added_task.id)
        assert found_task == added_task

    def test_update_task(self, queue_service: QueueService) -> None:
        task = Task(description="T1", priority=1, status=0)
        added_task = queue_service.add_task(task)
        assert added_task.id is not None
        new_data = Task(description="Updated", priority=2, status=1)
        updated_task = queue_service.update_task(added_task.id, new_data)
        assert updated_task.description == "Updated"

    def test_delete_task(self, queue_service: QueueService) -> None:
        task = Task(description="T1", priority=1, status=0)
        added_task = queue_service.add_task(task)
        assert added_task.id is not None
        deleted_task = queue_service.delete_task(added_task.id)
        assert deleted_task == added_task
        with pytest.raises(TaskNotFoundError):
            queue_service.get_task(added_task.id)

    def test_get_all_tasks(self, queue_service: QueueService) -> None:
        task1 = Task(description="T1", priority=1, status=0)
        task2 = Task(description="T2", priority=1, status=0)
        queue_service.add_task(task1)
        queue_service.add_task(task2)
        tasks = list(queue_service.get_all_tasks())
        assert len(tasks) == 2

    def test_filter_tasks_by_status(self, queue_service: QueueService) -> None:
        task1 = Task(description="T1", priority=1, status=0)
        task2 = Task(description="T2", priority=1, status=1)
        queue_service.add_task(task1)
        queue_service.add_task(task2)
        filtered = list(queue_service.filter_tasks_by_status(1))
        assert len(filtered) == 1
        assert filtered[0].status == 1

    def test_filter_tasks_by_priority(
        self, queue_service: QueueService
    ) -> None:
        task1 = Task(description="T1", priority=1, status=0)
        task2 = Task(description="T2", priority=5, status=0)
        queue_service.add_task(task1)
        queue_service.add_task(task2)
        filtered = list(queue_service.filter_tasks_by_priority(5))
        assert len(filtered) == 1
        assert filtered[0].priority == 5


class TestQueueServiceErrors:
    def test_get_nonexistent_task(self, queue_service: QueueService) -> None:
        with pytest.raises(TaskNotFoundError):
            queue_service.get_task(999)

    def test_delete_nonexistent_task(
        self, queue_service: QueueService
    ) -> None:
        with pytest.raises(TaskNotFoundError):
            queue_service.delete_task(999)

    def test_update_nonexistent_task(
        self, queue_service: QueueService
    ) -> None:
        with pytest.raises(TaskNotFoundError):
            queue_service.update_task(
                999, Task(description="T1", priority=1, status=0)
            )

    def test_add_task_fail(self) -> None:
        class FailingMockQueue(MockQueue):
            def add_task(self, task: Task) -> Task | None:
                return None

        service = QueueService(repository=FailingMockQueue())  # type: ignore[arg-type]
        with pytest.raises(ValueError, match="Не получилось добавить задачу"):
            service.add_task(Task(description="T1", priority=1, status=0))
