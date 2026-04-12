from pathlib import Path

import pytest

from src.domain.status import TaskStatus
from src.domain.task import Task
from src.repository.queue import TaskQueueInMemory
from src.repository.task_api import TaskAPI
from src.repository.task_file import TaskFile
from src.repository.task_random import TaskRandom


class TestRepositories:
    def test_task_api(self) -> None:
        api_source = TaskAPI()
        tasks = list(api_source.get_tasks())

        assert len(tasks) == 2
        assert all(isinstance(t, Task) for t in tasks)
        assert tasks[0].description == "Эта первая задача для гуся"
        assert tasks[0].status == TaskStatus.IN_PROGRESS

    def test_task_random(self) -> None:
        count = 5
        random_source = TaskRandom(tasks_count=count)
        tasks = list(random_source.get_tasks())

        assert len(tasks) == count
        assert all(isinstance(t, Task) for t in tasks)

        for task in tasks:
            assert 1 <= task.priority <= 5
            assert task.status in list(TaskStatus)
            assert len(task.description) > 0

    def test_task_file(self) -> None:
        project_root = Path(__file__).parent.parent.resolve()
        file_path = project_root / "test.txt"

        if not file_path.exists():
            pytest.skip(f"Test file not found at {file_path}")

        file_source = TaskFile(file_path=str(file_path))
        tasks = list(file_source.get_tasks())

        assert len(tasks) == 3
        assert tasks[0].id == 1
        assert tasks[0].description == "Сделать лабу идеально"
        assert tasks[0].priority == 5
        assert tasks[0].status == TaskStatus.WAITING

        assert tasks[1].id == 2
        assert tasks[1].status == TaskStatus.IN_PROGRESS

    def test_task_file_invalid_line(self, tmp_path: Path) -> None:
        f = tmp_path / "invalid_tasks.txt"
        f.write_text(
            "invalid line without json\n"
            '1 {"description": "Test", "priority": 1, "status": 0, "id": 1}'
        )
        file_source = TaskFile(file_path=str(f))
        tasks = list(file_source.get_tasks())
        assert len(tasks) == 1
        assert tasks[0].id == 1

    def test_task_queue_operations(self) -> None:
        queue = TaskQueueInMemory()
        task1 = Task(description="T1", priority=1, status=0)
        task2 = Task(description="T2", priority=5, status=1)

        queue.add_task(task1)
        queue.add_task(task2)
        assert task1.id is not None
        assert task2.id is not None
        assert len(queue) == 2

        found = queue.get_task_by_id(task1.id)
        assert found == task1

        assert queue.get_task_by_id(999) is None

        new_data = Task(description="New Desc", priority=2, status=1)
        updated = queue.update_task_by_id(task1.id, new_data)
        assert updated is not None
        assert updated.description == "New Desc"
        assert updated.priority == 2

        not_updated = queue.update_task_by_id(999, new_data)
        assert not_updated is None

        deleted = queue.delete_task_by_id(task2.id)
        assert deleted == task2
        assert len(queue) == 1
        assert queue.get_task_by_id(task2.id) is None

        not_deleted = queue.delete_task_by_id(999)
        assert not_deleted is None

    def test_task_queue_filters_and_iteration(self) -> None:
        queue = TaskQueueInMemory()
        task1 = Task(description="T1", priority=1, status=0)
        task2 = Task(description="T2", priority=5, status=1)
        task3 = Task(description="T3", priority=5, status=0)
        queue.add_task(task1)
        queue.add_task(task2)
        queue.add_task(task3)

        all_tasks = list(queue)
        assert len(all_tasks) == 3

        status_0_tasks = list(queue.filter_by_status(0))
        assert len(status_0_tasks) == 2
        assert task1 in status_0_tasks
        assert task3 in status_0_tasks

        priority_5_tasks = list(queue.filter_by_priority(5))
        assert len(priority_5_tasks) == 2
        assert task2 in priority_5_tasks
        assert task3 in priority_5_tasks

        assert task1.id is not None
        id_task = list(queue.filter_by_id(task1.id))
        assert len(id_task) == 1
        assert task1 in id_task

        assert sum(queue) == 1 + 5 + 5

    def test_task_queue_extended_stats(self) -> None:
        queue = TaskQueueInMemory()
        task1 = Task(description="Low", priority=1, status=0)
        task2 = Task(description="High Ready", priority=5, status=0)
        task3 = Task(description="High Busy", priority=5, status=1)

        queue.add_task(task1)
        queue.add_task(task2)
        queue.add_task(task3)

        assert queue.total_tasks == 3
        assert queue.total_priority == 11
        assert queue.ready_tasks_count == 1

        highest = queue.get_highest_priority_task()
        assert highest is not None
        assert highest.priority == 5

        ready = list(queue.get_ready_for_execution_tasks())
        assert len(ready) == 1
        assert ready[0] == task2
