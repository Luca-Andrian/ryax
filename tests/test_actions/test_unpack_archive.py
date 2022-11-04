import mock
import pytest

from actions.unpack_archive.ryax_handler import handle


@pytest.mark.parametrize(
    "files,is_dir,result",
    [
        pytest.param(["archive"], True, "/tmp/new_uuid/archive/archive"),
        pytest.param(["archive"], False, "/tmp/new_uuid/archive/archive"),
        pytest.param(["other_dir"], True, "/tmp/new_uuid/archive/archive"),
        pytest.param(["file1", "file2"], False, "/tmp/new_uuid/archive"),
    ],
)
@mock.patch("uuid.uuid4", mock.MagicMock(return_value="new_uuid"))
@mock.patch("os.rename")
@mock.patch("os.path.isdir")
@mock.patch("os.listdir")
@mock.patch("shutil.unpack_archive")
@mock.patch("shutil.move")
def test_handle(
    shutil_move,
    unpack_archive_mock,
    oslistdir_mock,
    osisdir_mock,
    osrename_mock,
    files,
    is_dir,
    result,
):
    osisdir_mock.return_value = is_dir
    oslistdir_mock.return_value = files
    req = {"archive": "archive.zip"}
    assert handle(req) == {"directory": result}
