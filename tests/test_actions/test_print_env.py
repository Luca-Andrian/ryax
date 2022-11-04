import os
import random

import mock
import pytest

from actions.print_env.ryax_handler import (
    check_dir,
    get_dir_stat_string,
    get_dirs_files_privileges,
    get_environment_vars,
)
from actions.print_env.ryax_handler import handle as print_env_handler
from actions.print_env.ryax_handler import permissions_to_unix_name, treat_dir


@mock.patch(
    "actions.print_env.ryax_handler.get_environment_vars",
    mock.MagicMock(return_value=""),
)
@mock.patch(
    "actions.print_env.ryax_handler.check_dir",
    mock.MagicMock(return_value=""),
)
@mock.patch(
    "actions.print_env.ryax_handler.permissions_to_unix_name",
    mock.MagicMock(return_value=""),
)
@mock.patch(
    "actions.print_env.ryax_handler.treat_dir",
    mock.MagicMock(return_value=""),
)
@mock.patch(
    "actions.print_env.ryax_handler.get_dirs_files_privileges",
    mock.MagicMock(return_value=""),
)
@mock.patch(
    "actions.print_env.ryax_handler.get_dir_stat_string",
    mock.MagicMock(return_value=""),
)
@mock.patch("getpass.getuser", mock.MagicMock(return_value=""))
@mock.patch("os.getcwd", mock.MagicMock(return_value=""))
def test_print_env(capfd):
    print_env_handler()
    out, err = capfd.readouterr()
    assert (
        out
        == "User: \nWorking Directory: \nEnvironment Variables:\n\nUser Directories and Files:\n\n"
    )


@mock.patch("os.walk", mock.MagicMock(return_value=(("", "", ""),)))
@mock.patch(
    "actions.print_env.ryax_handler.treat_dir",
    mock.MagicMock(return_value=""),
)
def test_get_dirs_files_privileges():
    expected_value = ""
    assert get_dirs_files_privileges() == expected_value


@mock.patch("os.stat", mock.MagicMock(return_value=""))
@mock.patch(
    "actions.print_env.ryax_handler.permissions_to_unix_name",
    mock.MagicMock(return_value=""),
)
@pytest.mark.parametrize("in_content", [[], ["./"]])
def test_treat_dir(in_content):
    s = ""
    for item in in_content:
        s += "\t\t{}  {}\n".format("", item)
    expected_value = "\t{}\n".format("") + s
    assert treat_dir("", in_content, "") == expected_value


@pytest.mark.parametrize("st_in", [["7", "6", "5", "4", "3", "2", "1"], []])
@mock.patch(
    "actions.print_env.ryax_handler.check_dir",
    mock.MagicMock(return_value=""),
)
@mock.patch(
    "actions.print_env.ryax_handler.get_dir_stat_string",
    mock.MagicMock(return_value=""),
)
def test_permissions_to_unix_name(st_in):
    assert permissions_to_unix_name(st_in) == ""


@pytest.mark.parametrize(
    "st_in",
    [
        random.choice(os.listdir("./")),
        random.choice(os.listdir("./")),
        random.choice(os.listdir("./")),
        random.choice(os.listdir("./")),
    ],
)
def test_get_dir_stat_string(st_in):
    st_in_stat = os.stat(st_in)
    assert get_dir_stat_string(st_in_stat) in str(oct(st_in_stat.st_mode))


@pytest.mark.parametrize("st_in", [os.stat(random.choice(os.listdir("./")))])
@mock.patch("stat.S_ISDIR", mock.MagicMock(return_value=True))
def test_check_dir_isdir(st_in):
    assert check_dir(st_in) == "d"


@pytest.mark.parametrize("st_in", [os.stat(random.choice(os.listdir("./")))])
@mock.patch("stat.S_ISDIR", mock.MagicMock(return_value=False))
def test_check_dir_is_not_dir(st_in):
    assert check_dir(st_in) == "-"


@mock.patch("os.environ.items", mock.MagicMock(return_value=(("k", "v"),)))
def test_get_environment_vars():
    assert get_environment_vars() == "\tk: v\n"
