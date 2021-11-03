"""Common test setup classes."""
import tempfile
import shutil
from typing import Any


class TempDirTestSetup:
    """Setup class to initialize the test environment with a temporary directory."""

    def __init__(self) -> None:
        """Initializes all variables."""
        self.test_dir = tempfile.mkdtemp()

    def __enter__(self) -> "TempDirTestSetup":
        """Executes when the class is entered through a context manager."""
        return self

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        """Executes when the class is exited through a context manager."""
        # Remove the temporary directory after the test
        if self.test_dir is not None:
            shutil.rmtree(self.test_dir)
