import random
import os
import sys
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
    sys.path.insert(0, ROOT_DIR)
else:
    raise RuntimeError(
        f"This script is not installed in the '{_EXPECTED}' directory. Please fix."
    )

# Create the necessary configuration to load the module
from tests.testlib_ import setup
from switchmap.core import data
from switchmap import DeviceDetail

@pytest.fixture(scope="module")
def config():
    """Fixture for setup and cleanup of configuration."""
    config = setup.config()
    config.save()
    yield config
    config.cleanup()

random_string = "".join(
    [random.choice(string.ascii_letters + string.digits) for _ in range(9)]
)

def test_check_hashstring(config):
    """Test the hashstring function."""
    _string = "f5rAwrU@Rop=Op-1QE$?yOs&@phit-=swoP*lqo6T!iwlcUthE2PistA7Re-"
    shas = [1, 224, 384, 256, 512]
    expecteds = [
        "f53766caaf3a1f567c6013ecafb840818eee2901",
        "1ca8f5952d077dc378ae02deb6cec31587d3e6c064c51923e2ddde5c",
        "30b7c3d10960bfa47d304d3503bd247277aad3d145c135254e19f7b755806a7"
        "073af64e608a604595797d35136cb74fa",
        "4aeedc4229622c1724f7be54ad8f48ae748dc52b4bf14aadac50fc77a757fb01",
        "8bd7add2b47e3ad2e352d75a9392404e6b56bf2f91bddf092ceb0006a609732"
        "3b9dffd813f16aebc1c0f3b8f2e722d7ad5c2800c0930937bea62d7afb61bec95",
    ]

    for key, sha in enumerate(shas):
        result = data.hashstring(_string, sha=sha)
        assert result == expecteds[key]

        result_utf8 = data.hashstring(_string, sha=sha, utf8=True)
        assert result_utf8 == expecteds[key].encode()

def test_check_dictify(config):
    """Test the dictify function."""
    test_tuple = DeviceDetail(
        RDevice=1,
        InterfaceDetails=[
            DeviceDetail(RDevice=2, InterfaceDetails=[3, 4, 5, 6]),
            7,
            DeviceDetail(RDevice=8, InterfaceDetails=9),
        ],
    )
    expected = {
        "InterfaceDetails": [
            {"InterfaceDetails": [3, 4, 5, 6], "RDevice": 2},
            7,
            {"InterfaceDetails": 9, "RDevice": 8},
        ],
        "RDevice": 1,
    }

    result = data.dictify(test_tuple)
    assert result == expected
