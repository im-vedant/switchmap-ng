#!/usr/bin/env python3
"""Test the log module."""

import os
import sys
import random
import string
import pytest

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
    # We need to prepend the path in case the repo has been installed
    # elsewhere on the system using PIP. This could corrupt expected results
    sys.path.insert(0, ROOT_DIR)
else:
    print(
        """This script is not installed in the "{0}" directory. Please fix.\
""".format(
            _EXPECTED
        )
    )
    sys.exit(2)

# Create the necessary configuration to load the module
from tests.testlib_ import setup
from switchmap.core import log as testimport

@pytest.fixture(scope="module")
def config():
    """Create and return configuration for tests."""
    test_config = setup.config()
    test_config.save()
    yield test_config
    test_config.cleanup()

@pytest.fixture
def random_string():
    """Generate a random string for tests."""
    return "".join(
        [random.choice(string.ascii_letters + string.digits) for n in range(9)]
    )

# ExceptionWrapper tests
def test_exception_wrapper_init():
    """Testing function __init__."""
    pass

def test_exception_wrapper_re_raise():
    """Testing function re_raise."""
    pass

# GetLog tests
def test_get_log_init():
    """Testing function __init__."""
    pass

def test_get_log_logfile():
    """Testing function logfile."""
    pass

def test_get_log_stdout():
    """Testing function stdout."""
    pass

# Function tests
def test_log2console():
    """Testing function log2console."""
    pass

def test_log2die_safe():
    """Testing function log2die_safe."""
    pass

def test_log2warning():
    """Testing function log2warning."""
    pass

def test_log2debug():
    """Testing function log2debug."""
    pass

def test_log2info():
    """Testing function log2info."""
    pass

def test_log2see():
    """Testing function log2see."""
    pass

def test_log2die():
    """Testing function log2die."""
    pass

def test_log2exception_die():
    """Testing function log2exception_die."""
    pass

def test_log2exception():
    """Testing function log2exception."""
    pass

def test_logit():
    """Testing function _logit."""
    pass

def test_logger_file():
    """Testing function _logger_file."""
    pass

def test_logger_stdout():
    """Testing function _logger_stdout."""
    pass

def test_message():
    """Testing function _message."""
    pass

def test_check_environment():
    """Testing function check_environment."""
    pass

def test_root_directory():
    """Testing function root_directory."""
    # Initialize key variables
    this_directory = os.path.dirname(os.path.realpath(__file__))
    expected = os.path.dirname(
        os.path.dirname(os.path.dirname(this_directory))
    )

    # Test
    result = testimport.root_directory()
    assert result == expected