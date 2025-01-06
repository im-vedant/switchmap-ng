#!/usr/bin/env python3
"""Test the general module."""

import os
import sys
import json
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
from switchmap.core import graphene as testimport

@pytest.fixture(scope="module")
def config():
    """Create and return configuration for tests."""
    test_config = setup.config()
    test_config.save()
    yield test_config
    test_config.cleanup()

def test_normalize(config):
    """Testing function normalize."""
    # Initialize key variables
    expected = {
        "roots": [
            {
                "event": {
                    "zones": [
                        {
                            "devices": [
                                {
                                    "hostname": "device01.example.org",
                                    "idxDevice": 27,
                                },
                                {
                                    "hostname": "device02.example.org",
                                    "idxDevice": 28,
                                },
                            ],
                            "name": "TEST",
                        }
                    ]
                }
            }
        ]
    }

    data_string = """
{
  "data": {
    "roots": {
      "edges": [
        {
          "node": {
            "event": {
              "zones": {
                "edges": [
                  {
                    "node": {
                      "name": "TEST",
                      "devices": {
                        "edges": [
                          {
                            "node": {
                              "hostname": "device01.example.org",
                              "idxDevice": 27
                            }
                          },
                          {
                            "node": {
                              "hostname": "device02.example.org",
                              "idxDevice": 28
                            }
                          }
                        ]
                      }
                    }
                  }
                ]
              }
            }
          }
        }
      ]
    }
  }
}
"""
    # Convert data to dict
    data = json.loads(data_string).get("data")

    # Test
    result = testimport.normalize(data)
    assert result == expected

def test_nodes(config):
    """Testing function nodes."""
    # Initialize key variables
    expected = [
        {
            "name": "TEST",
            "devices": [
                {"hostname": "device01.example.org", "idxDevice": 27},
                {"hostname": "device02.example.org", "idxDevice": 28},
            ],
        }
    ]

    data_string = """
{
                "edges": [
                  {
                    "node": {
                      "name": "TEST",
                      "devices": {
                        "edges": [
                          {
                            "node": {
                              "hostname": "device01.example.org",
                              "idxDevice": 27
                            }
                          },
                          {
                            "node": {
                              "hostname": "device02.example.org",
                              "idxDevice": 28
                            }
                          }
                        ]
                      }
                    }
                  }
                ]
}
"""
    # Convert data to dict
    data = json.loads(data_string).get("edges")

    # Test
    result = testimport.nodes(data)
    assert result == expected