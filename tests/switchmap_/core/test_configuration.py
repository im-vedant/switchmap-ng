#!/usr/bin/env python3
"""Test the configuration module using pytest."""

import os
import sys
import pytest
from tests.testlib_ import data, setup
from switchmap.core import configuration as test_module

# Try to create a working PYTHONPATH
EXEC_DIR = os.path.dirname(os.path.realpath(__file__))
ROOT_DIR = os.path.abspath(
    os.path.join(
        os.path.abspath(
            os.path.join(
                os.path.abspath(os.path.join(EXEC_DIR, os.pardir)), os.pardir
            )
        ),
        os.pardir,
    )
)
_EXPECTED = "{0}switchmap-ng{0}tests{0}switchmap_{0}core".format(os.sep)
if EXEC_DIR.endswith(_EXPECTED) is True:
    sys.path.insert(0, ROOT_DIR)
else:
    print(
        """This script is not installed in the "{0}" directory. Please fix.\n""".format(
            _EXPECTED
        )
    )
    sys.exit(2)

@pytest.fixture(scope="module")
def setup_environment():
    """Set up the test environment and return configuration objects."""
    setup.setenv()
    _config = setup.Config(data.configtester(), randomizer=True)
    _config.save()
    yield _config
    _config.cleanup()

@pytest.fixture(scope="module")
def config(setup_environment):
    """Provide the ConfigCore instance."""
    return test_module.ConfigCore()

def test_agent_subprocesses():
    """Test agent_subprocesses function."""
    # This function appears to vary based on CPU cores.
    pass

def test_api_log_file(setup_environment, config):
    """Test api_log_file function."""
    daemon = 1234
    expected = "{1}{0}log{0}switchmap-{2}.log".format(
        os.sep, setup_environment.metadata.system_directory, daemon
    )
    result = config.api_log_file(daemon)
    assert result == expected

def test_daemon_directory(setup_environment, config):
    """Test daemon_directory function."""
    expected = "{1}{0}daemon".format(os.sep, setup_environment.metadata.system_directory)
    result = config.daemon_directory()
    assert result == expected

def test_log_directory(setup_environment, config):
    """Test log_directory function."""
    expected = "{1}{0}log".format(os.sep, setup_environment.metadata.system_directory)
    result = config.log_directory()
    assert result == expected

def test_log_file(setup_environment, config):
    """Test log_file function."""
    expected = "{1}{0}log{0}switchmap.log".format(os.sep, setup_environment.metadata.system_directory)
    result = config.log_file()
    assert result == expected

def test_log_level(config):
    """Test log_level function."""
    expected = "info"
    result = config.log_level()
    assert result == expected

def test_multiprocessing(config):
    """Test multiprocessing function."""
    expected = False
    result = config.multiprocessing()
    assert result == expected

def test_system_directory(setup_environment, config):
    """Test system_directory function."""
    expected = setup_environment.metadata.system_directory
    result = config.system_directory()
    assert result == expected
