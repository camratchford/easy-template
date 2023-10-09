
import os
import pytest
from click.testing import CliRunner
from ez_temp.cli import run


@pytest.fixture
def runner():
    return CliRunner()


def test_run_with_no_arguments(runner):
    result = runner.invoke(run)
    assert result.exit_code != 0
    assert "Error: Missing option '-o' / '--output-file'." in result.output


def test_run_with_missing_config_file(runner):
    result = runner.invoke(run, ["-c", "nonexistent.yaml", "-o", "output.txt", "-t", "template.txt"])
    assert result.exit_code != 0
    assert "nonexistent.yaml not found" in result.output


def test_run_with_valid_arguments(runner):
    with runner.isolated_filesystem():
        with open("template.txt", "w") as f:
            f.write("Hello, {{ name }}!")

        result = runner.invoke(run, ["-o", "output.txt", "-t", "template.txt", "-v", "name=World"])

        assert result.exit_code == 0
        assert os.path.exists("output.txt")


def test_run_with_var_file(runner):
    with runner.isolated_filesystem():
        with open("vars.yaml", "w") as f:
            f.write("name: World")

        result = runner.invoke(run, ["--var-file", "vars.yaml", "-o", "output.txt", "-t", "template.txt"])

        assert result.exit_code == 0
        assert os.path.exists("output.txt")


def test_run_with_external_function_dir(runner):
    with runner.isolated_filesystem():
        os.mkdir("functions")

        result = runner.invoke(run, ["--external-function-dir", "functions", "-o", "output.txt", "-t", "template.txt"])

        assert result.exit_code == 0


def test_run_with_force_flag(runner):
    with runner.isolated_filesystem():
        with open("output.txt", "w") as f:
            f.write("Existing content.")

        result = runner.invoke(run, ["-f", "-o", "output.txt", "-t", "template.txt"])

        assert result.exit_code == 0
        assert os.path.exists("output.txt")


def test_run_with_silent_flag(runner):
    result = runner.invoke(run, ["--silent", "-o", "output.txt", "-t", "template.txt"])
    assert result.exit_code == 0
    assert "Logging suppressed" not in result.output  # Assuming your main function handles this

