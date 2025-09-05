"""Fixtures used by multiple tests."""

# pylint: skip-file

import subprocess
import shlex
import pytest
import os
from postcode_functions import CACHE_FILE


@pytest.fixture()
def run_shell_command():
    """Runs a command in the shell, returning any standard output and error messages."""

    def func(command):
        command = command.strip()

        if command.startswith("python3"):
            command = command.replace("python3", 'python3 -W "ignore"', 1)
        elif command.startswith("python"):
            command = command.replace("python", 'python -W "ignore"', 1)

        
        result = subprocess.run(shlex.split(command), capture_output=True)
        return result.stdout.decode("UTF-8"), result.stderr.decode("UTF-8")

    return func


@pytest.fixture(autouse=True)
def clear_cache_file():
    # Remove cache file before each test
    if os.path.exists(CACHE_FILE):
        os.remove(CACHE_FILE)
    yield
    if os.path.exists(CACHE_FILE):
        os.remove(CACHE_FILE)