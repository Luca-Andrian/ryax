import mock
import pytest

from actions.catfile.ryax_handler import handle as catfile_handler


@pytest.mark.parametrize("mod_in", [{"file": "file1"}])
def test_catfile(mod_in):
    with mock.patch("builtins.open", mock.mock_open(read_data="test")):
        assert catfile_handler(mod_in) == {"stdout": "test"}


@pytest.mark.parametrize("mod_in", [{"file": "this file does not exist"}])
def test_catfile_when_nofile(mod_in):
    with pytest.raises(FileNotFoundError):
        catfile_handler(mod_in)
