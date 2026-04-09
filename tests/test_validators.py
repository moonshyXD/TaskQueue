from pathlib import Path

import pytest

from src.domain.descriptors import FilePathValidator, TaskCountValidator
from src.domain.errors import InputValidationError


class TestDescriptorContainer:
    count = TaskCountValidator()
    path = FilePathValidator()


@pytest.fixture
def container() -> TestDescriptorContainer:
    return TestDescriptorContainer()


class TestCountValidator:
    def test_set_valid_string(
        self, container: TestDescriptorContainer
    ) -> None:
        container.count = "5"
        assert container.count == 5

    def test_set_valid_int(self, container: TestDescriptorContainer) -> None:
        container.count = 10
        assert container.count == 10

    def test_set_invalid_string(
        self, container: TestDescriptorContainer
    ) -> None:
        with pytest.raises(InputValidationError):
            container.count = "abc"

    def test_set_negative_string(
        self, container: TestDescriptorContainer
    ) -> None:
        with pytest.raises(InputValidationError):
            container.count = "-1"


class TestFilePathValidator:
    def test_set_valid_path(
        self, container: TestDescriptorContainer, tmp_path: Path
    ) -> None:
        f = tmp_path / "test_file.txt"
        f.touch()
        container.path = str(f)
        assert str(container.path) == str(f.resolve())

    def test_set_invalid_type(
        self, container: TestDescriptorContainer
    ) -> None:
        with pytest.raises(InputValidationError):
            container.path = 123

    def test_set_non_existent_file(
        self, container: TestDescriptorContainer
    ) -> None:
        with pytest.raises(InputValidationError):
            container.path = "non_existent_file.txt"

    def test_set_directory_path(
        self, container: TestDescriptorContainer, tmp_path: Path
    ) -> None:
        with pytest.raises(InputValidationError):
            container.path = str(tmp_path)
