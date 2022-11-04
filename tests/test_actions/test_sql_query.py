import mock
import pytest

from actions.sql_query.ryax_handler import handle, write_to_csv


class TestSQLModule:
    @pytest.fixture()
    def mysql_cursor(self):
        class MySQLPCursorMock:
            def __init__(self):
                pass

            def execute(self, query):
                return "UNUSED_VARIABLE"

            def fetchall(self):
                return

            @property
            def column_names(self):
                return ("foo", "bar")

        return MySQLPCursorMock

    @mock.patch(
        "actions.sql_query.ryax_handler.write_to_csv",
        mock.MagicMock(),
    )
    @pytest.mark.parametrize(
        "module_input",
        [
            (
                {
                    "name": "test_name",
                    "host": "test_host",
                    "username": "test_user",
                    "password": "test_pass",
                    "query": "test_query",
                }
            )
        ],
    )
    def test_handle(self, module_input, module_metadata, module_outputs, mysql_cursor):
        metadata = module_metadata(handle)
        expected_outputs = module_outputs(metadata)
        with mock.patch("mysql.connector.connect") as conn_mock:
            mock_sql_cursor = mysql_cursor()
            mock_sql_cursor.execute = mock.MagicMock()
            mock_sql_cursor.fetchall = mock.MagicMock()
            conn_mock.return_value.cursor = mock.MagicMock(return_value=mock_sql_cursor)
            assert handle(module_input) == expected_outputs
            mock_sql_cursor.execute.assert_called_once_with(module_input.get("query"))
            mock_sql_cursor.fetchall.assert_called_once()

    @mock.patch("csv.writer", mock.MagicMock())
    @pytest.mark.parametrize(
        "mock_file_rows, mock_final_file",
        [
            ([["foo1", "bar1"]], "foo,bar\nfoo1,bar1"),
            ([["1", "2"], ["3", "4"]], "foo,bar\n1,2\n3,4"),
        ],
    )
    def test_write_to_csv(self, mock_file_rows, mock_final_file, mysql_cursor):
        save_loc = "/tmp/foo.csv"
        mocked_cursor = mysql_cursor()
        with mock.patch("builtins.open", mock.mock_open(read_data=mock_final_file)):
            write_to_csv(save_loc, list(mocked_cursor.column_names), mock_file_rows)
            with open(save_loc, "r") as comp_file:
                rows = [line for line in comp_file]
                assert rows[0].replace("\n", "").split(",") == list(
                    mocked_cursor.column_names
                )
                for i in range(len(mock_file_rows)):
                    assert rows[i + 1].replace("\n", "").split(",") == mock_file_rows[i]
