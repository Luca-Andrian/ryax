import mock

from actions.dir_archive.ryax_handler import handle


@mock.patch("uuid.uuid4", mock.MagicMock(return_value="random-uuid"))
@mock.patch("shutil.make_archive")
def test_handle(make_archive_mock):
    make_archive_mock.return_value = "/tmp/random-uuid-archive.zip"
    req = {"directory": "/path/my_dir"}
    assert handle(req) == {"archive": "/tmp/random-uuid-archive.zip"}
    make_archive_mock.assert_called_once_with(
        "/tmp/random-uuid-archive", "zip", "/path", "my_dir"
    )
