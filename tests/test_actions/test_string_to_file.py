import mock

from actions.string_to_file.ryax_handler import handle, string_to_file


def test_string_to_file():
    test_string = "foo"
    test_save_path = "bar"
    with mock.patch(
        "builtins.open", new_callable=mock.mock_open, read_data=test_string
    ):
        assert string_to_file(test_string, save_path=test_save_path) == test_save_path
        assert open(test_save_path).read() == test_string


def test_string_to_file_handler():
    in_dict = {"instring": "foo"}
    mock_str_tofile_out = "test_out"
    with mock.patch(
        "actions.string_to_file.ryax_handler.string_to_file",
        mock.MagicMock(),
    ) as mock_str_tofile:
        mock_str_tofile.return_value = mock_str_tofile_out
        assert handle(in_dict) == {"outfile": mock_str_tofile_out}
        mock_str_tofile.assert_called_once_with("foo")
