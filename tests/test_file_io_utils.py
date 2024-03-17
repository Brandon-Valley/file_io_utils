from file_io_utils import (
    read_txt_as_line_generator,
    read_txt_as_line_list,
    write_txt_from_lines,
    read_json,
    write_json,
    read_csv_as_row_dicts,
    write_csv_from_row_dicts,
)
import pytest
from pathlib import Path


# Example test for reading text files
def test_read_txt_as_line_generator(tmp_path: Path):
    test_file = tmp_path / "test.txt"
    test_file.write_text("line 1\nline 2\nline 3")

    lines = list(read_txt_as_line_generator(test_file))
    assert lines == ["line 1", "line 2", "line 3"]


def test_read_txt_as_line_list(tmp_path: Path):
    test_file = tmp_path / "test.txt"
    test_file.write_text("line 1\nline 2\nline 3")

    lines = read_txt_as_line_list(test_file)
    assert lines == ["line 1", "line 2", "line 3"]


def test_write_txt_from_lines(tmp_path: Path):
    lines = ["line 1", "line 2", "line 3"]
    test_file = tmp_path / "test.txt"
    write_txt_from_lines(lines, test_file, "overwrite")

    assert test_file.read_text() == "line 1\nline 2\nline 3"


# Example test for JSON utilities
def test_read_write_json(tmp_path: Path):
    test_file = tmp_path / "test.json"
    data = {"key": "value"}
    write_json(data, test_file)

    assert read_json(test_file) == data


# Example test for CSV utilities
def test_read_write_csv_as_row_dicts(tmp_path: Path):
    test_file = tmp_path / "test.csv"
    row_dicts = [{"Column1": "data1", "Column2": "data2"}]
    write_csv_from_row_dicts(row_dicts, test_file, ordered_headers=["Column1", "Column2"])

    read_data = read_csv_as_row_dicts(test_file)
    assert read_data == row_dicts


# Run pytest in the terminal where your test file is located with:
# pytest test_utilities.py
