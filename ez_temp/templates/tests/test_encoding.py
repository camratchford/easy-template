import pytest
from pathlib import Path
from ez_temp.templates.encodings import check_encoding, change_encoding


@pytest.fixture
def test_file():
    file_path = "test_file.txt"
    with open(file_path, "w", encoding="utf-8") as f:
        f.write("Test content")
    yield file_path
    Path(file_path).unlink()


def test_check_encoding_utf8(test_file):
    encoding = check_encoding(test_file)
    assert encoding == "utf-8"


def test_check_encoding_non_utf8(test_file):
    with open(test_file, "w", encoding="latin1") as f:
        f.write("Test content")
    encoding = check_encoding(test_file)
    assert encoding == "iso-8859-1"


def test_change_encoding_to_utf8(test_file):
    with open(test_file, "w", encoding="latin1") as f:
        f.write("Test content")
    change_encoding(test_file, "latin1")
    encoding = check_encoding(test_file)
    assert encoding == "utf-8"


def test_change_encoding_content(test_file):
    with open(test_file, "w", encoding="latin1") as f:
        f.write("Test content")
    change_encoding(test_file, "latin1")
    with open(test_file, "r", encoding="utf-8") as f:
        content = f.read()
    assert content == "Test content"
