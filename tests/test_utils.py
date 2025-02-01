import os
import tempfile

from src.utils import list_files


def test_list_files():
    with tempfile.TemporaryDirectory() as temp_dir:
        test_files = ["test1.txt", "test2.txt", "test3.txt"]
        for filename in test_files:
            with open(os.path.join(temp_dir, filename), "w") as f:
                f.write("test content")

        result = list_files(temp_dir)
        assert sorted(result) == sorted(test_files)

        result = list_files("/nonexistent/directory")
        assert result == []

        os.mkdir(os.path.join(temp_dir, "subdir"))
        result = list_files(temp_dir)
        assert sorted(result) == sorted(test_files)
