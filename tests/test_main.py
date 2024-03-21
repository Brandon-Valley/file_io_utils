from pprint import pprint
from typing import Tuple
from file_io_utils import (
    delete_last_n_lines_from_txt,
    read_txt_as_line_generator,
    read_txt_as_line_list,
    write_csv_from_concatenated_csvs,
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


def test_delete_last_n_lines_from_txt(tmp_path: Path):
    # Create a test file with some lines
    test_file = tmp_path / "test.txt"
    test_file.write_text("line 1\nline 2\nline 3\nline 4\nline 5")

    # Call the function to delete the last 2 lines
    delete_last_n_lines_from_txt(test_file, 2)

    # Verify that the lines were deleted
    expected_lines = ["line 1", "line 2", "line 3"]
    actual_lines = test_file.read_text().splitlines()
    assert actual_lines == expected_lines


@pytest.fixture
def create_temp_csv_files(tmp_path: Path) -> Tuple[Path, Path]:
    """
    Creates temporary CSV files for testing and returns their paths.
    """
    row_dicts_1 = [
        {
            "header1": "file_1_row1_1",
            "header2": "file_1_row1_2",
        },
        {
            "header1": "file_1_row2_1",
            "header2": "file_1_row2_2",
        },
    ]
    row_dicts_2 = [
        {
            "header1": "file_2_row1_1",
            "header2": "file_2_row1_2",
        },
        {
            "header1": "file_2_row2_1",
            "header2": "file_2_row2_2",
        },
    ]

    # Create first CSV file
    csv_file_path_1 = tmp_path / "file1.csv"
    print(f"Writing {csv_file_path_1=}...")
    write_csv_from_row_dicts(row_dicts_1, csv_file_path_1)

    # Create second CSV file
    csv_file_path_2 = tmp_path / "file2.csv"
    print(f"Writing {csv_file_path_2=}...")
    write_csv_from_row_dicts(row_dicts_2, csv_file_path_2)

    return [csv_file_path_1, csv_file_path_2]


def test_write_csv_from_concatenated_csvs(create_temp_csv_files, tmp_path):
    """
    Tests that the write_csv_from_concatenated_csvs function correctly concatenates CSV files.
    """
    out_csv_path = tmp_path / "concatenated.csv"
    print(f"Writing {out_csv_path=}...")
    write_csv_from_concatenated_csvs(create_temp_csv_files, out_csv_path)

    # Verify that the concatenated CSV file was written correctly
    final_row_dicts = read_csv_as_row_dicts(out_csv_path)
    print("final_row_dicts:")
    pprint(final_row_dicts)

    expected_content = [
        {"header1": "file_1_row1_1", "header2": "file_1_row1_2"},
        {"header1": "file_1_row2_1", "header2": "file_1_row2_2"},
        {"header1": "file_2_row1_1", "header2": "file_2_row1_2"},
        {"header1": "file_2_row2_1", "header2": "file_2_row2_2"},
    ]

    actual_content = read_csv_as_row_dicts(out_csv_path)
    assert actual_content == expected_content, f"Expected:\n{expected_content}\n\nGot:\n{actual_content}"
